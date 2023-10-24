import os
import shutil
from contextlib import asynccontextmanager
from contextlib import contextmanager, ExitStack

from fastapi import FastAPI
from ewoksjob.client.local import pool_context

from .backends import json_backend
from ..resources import data
from . import config


@asynccontextmanager
async def fastapi_lifespan(app: FastAPI):
    get_api_settings = app.dependency_overrides.get(
        config.get_api_settings, config.get_api_settings
    )
    api_settings = get_api_settings()
    _copy_default_resources(api_settings)
    with ExitStack() as stack:
        ctx = _enable_execution(api_settings)
        stack.enter_context(ctx)
        yield


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


@contextmanager
def _enable_execution(api_settings: config.ApiSettings):
    """Ensure workflows can be executed"""
    if api_settings.celery is not None:
        return
    with pool_context():
        yield
