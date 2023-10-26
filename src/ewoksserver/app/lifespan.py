import os
import shutil
from pprint import pformat
from typing import Generator
from contextlib import contextmanager
from contextlib import asynccontextmanager

from fastapi import FastAPI
from ewoksjob.client.local import pool_context
from celery import current_app as current_celery_app

from .backends import json_backend
from ..resources import data
from . import config
from .routes.execution import socketio


@asynccontextmanager
async def fastapi_lifespan(app: FastAPI) -> Generator[None, None, None]:
    get_api_settings = app.dependency_overrides.get(
        config.get_api_settings, config.get_api_settings
    )
    api_settings = get_api_settings()
    _configure_socketio(api_settings)
    _copy_default_resources(api_settings)
    _enable_execution_events(api_settings)
    with _enable_execution(api_settings):
        _print_api_settings(api_settings)
        yield


def _configure_socketio(app_settings: config.ApiSettings) -> None:
    socketio.configure_socketio(app_settings)


def _copy_default_resources(api_settings: config.ApiSettings) -> None:
    """Copy the default resources (tasks, workflows and icon) from the
    python package to the resource directory."""
    for resource, resource_ext in {
        "tasks": [".json"],
        "icons": [".png", ".svg"],
        "workflows": [".json"],
    }.items():
        root_url = json_backend.root_url(api_settings.resource_directory, resource)
        os.makedirs(root_url, exist_ok=True)
        for filename in os.listdir(data.DEFAULT_ROOT / resource):
            _, ext = os.path.splitext(filename)
            if ext not in resource_ext:
                continue

            src = data.DEFAULT_ROOT / resource / filename
            if not os.path.isfile(src):
                continue

            dest = root_url / filename
            if not os.path.exists(dest):
                shutil.copy(src, dest)


def _enable_execution_events(api_settings: config.ApiSettings) -> None:
    """Set default ewoks event handler when nothing has been configured"""
    if api_settings.configured:
        return
    if api_settings.ewoks is None:
        api_settings.ewoks = dict()
    if not api_settings.ewoks.get("handlers"):
        api_settings.ewoks["handlers"] = [
            {
                "class": "ewokscore.events.handlers.Sqlite3EwoksEventHandler",
                "arguments": [
                    {
                        "name": "uri",
                        "value": "file:ewoks_events.db",
                    }
                ],
            }
        ]


@contextmanager
def _enable_execution(api_settings: config.ApiSettings) -> Generator[None, None, None]:
    """Ensure workflows can be executed"""
    if api_settings.celery is None:
        with pool_context():
            yield
    else:
        current_celery_app.conf.update(api_settings.celery)
        yield


def _print_api_settings(api_settings: config.ApiSettings) -> None:
    """Print summary of all API settings"""
    resourcedir = api_settings.resource_directory
    if not resourcedir:
        resourcedir = "."
    print(f"\nRESOURCE DIRECTORY:\n {os.path.abspath(resourcedir)}\n")

    adict = api_settings.celery
    if adict is None:
        print("\nCELERY:\n Not configured (local workflow execution)\n")
    else:
        print(f"\nCELERY:\n {pformat(adict)}\n")

    adict = api_settings.ewoks
    if adict is None:
        print("\nEWOKS:\n Not configured\n")
    else:
        print(f"\nEWOKS:\n {pformat(adict)}\n")
