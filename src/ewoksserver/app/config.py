import os
import sys
import importlib.util
from pathlib import Path
from typing import Optional
from typing_extensions import Annotated

from pydantic import Field
from pydantic_settings import BaseSettings
from fastapi import Depends

try:
    from ewoksweb.serverutils import get_test_config
except ImportError:
    get_test_config = None


class EwoksSettings(BaseSettings):
    configured: Annotated[
        bool, Field(default=False, title="Any of the settings has been defined")
    ]
    resource_directory: Annotated[
        Path, Field(default=Path("."), title="Backend file resource directory")
    ]
    ewoks: Annotated[Optional[dict], Field(default=None, title="Ewoks configuration")]
    celery: Annotated[Optional[dict], Field(default=None, title="Celery configuration")]
    without_events: Annotated[bool, Field(default=False, title="Enable ewoks events")]
    discover_tasks: Annotated[
        bool, Field(default=False, title="Descover ewoks tasks on startup")
    ]


class AppSettings(BaseSettings):
    skip_older_versions: Annotated[
        bool,
        Field(
            default=False, title="Do not create the end points for older API versions"
        ),
    ]


_APP_SETTINGS = None

_EWOKS_SETTINGS = None


def create_ewoks_settings(
    config: Optional[str] = None,
    dir: Optional[str] = None,
    without_events: bool = False,
    frontend_tests: bool = False,
    rediscover_tasks: bool = False,
) -> EwoksSettings:
    global _EWOKS_SETTINGS

    # Get configuration file
    filename = os.environ.get("EWOKSSERVER_SETTINGS")
    if config:
        filename = config
    if frontend_tests:
        if get_test_config is None:
            raise RuntimeError("ewoksweb is not installed")
        filename = get_test_config()

    # Extract settings from configurations file
    resource_directory = None
    ewoks = None
    celery = None
    if filename:
        spec = importlib.util.spec_from_file_location("ewoksserverconfig", filename)
        mod = importlib.util.module_from_spec(spec)
        sys.modules["ewoksserverconfig"] = mod
        spec.loader.exec_module(mod)
        resource_directory = getattr(mod, "RESOURCE_DIRECTORY", resource_directory)
        ewoks = getattr(mod, "EWOKS", ewoks)
        celery = getattr(mod, "CELERY", celery)

    # Overwrite resource directory
    if dir:
        resource_directory = dir
    elif not resource_directory:
        resource_directory = "."

    configured = bool(filename) or bool(dir)

    _EWOKS_SETTINGS = EwoksSettings(
        configured=configured,
        resource_directory=resource_directory,
        ewoks=ewoks,
        celery=celery,
        without_events=without_events,
        discover_tasks=rediscover_tasks,
    )
    return _EWOKS_SETTINGS


def create_app_settings(skip_older_versions: bool = False) -> None:
    global _APP_SETTINGS
    _APP_SETTINGS = AppSettings(skip_older_versions=skip_older_versions)
    return _APP_SETTINGS


def get_ewoks_settings():
    global _EWOKS_SETTINGS
    if _EWOKS_SETTINGS is not None:
        return _EWOKS_SETTINGS
    return create_ewoks_settings()


def get_app_settings():
    global _APP_SETTINGS
    if _APP_SETTINGS is not None:
        return _APP_SETTINGS
    return create_app_settings()


EwoksSettingsType = Annotated[EwoksSettings, Depends(get_ewoks_settings)]
