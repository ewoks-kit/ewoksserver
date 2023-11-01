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


class ApiSettings(BaseSettings):
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


_SETTINGS = None


def create_api_settings(
    config: Optional[str] = None,
    dir: Optional[str] = None,
    without_events: bool = False,
    frontend_tests: bool = False,
    rediscover_tasks: bool = False,
) -> ApiSettings:
    global _SETTINGS

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

    _SETTINGS = ApiSettings(
        configured=configured,
        resource_directory=resource_directory,
        ewoks=ewoks,
        celery=celery,
        without_events=without_events,
        discover_tasks=rediscover_tasks,
    )


def get_api_settings():
    global _SETTINGS
    if _SETTINGS is not None:
        return _SETTINGS
    return create_api_settings()


ApiSettingsType = Annotated[ApiSettings, Depends(get_api_settings)]
