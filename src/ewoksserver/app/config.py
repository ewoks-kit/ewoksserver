from functools import lru_cache
from pathlib import Path
from pydantic import Field
from pydantic_settings import BaseSettings
from typing_extensions import Annotated
from typing import Optional
from fastapi import Depends


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


@lru_cache()
def get_api_settings():
    return ApiSettings()


ApiSettingsType = Annotated[ApiSettings, Depends(get_api_settings)]
