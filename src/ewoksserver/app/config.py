from functools import lru_cache
from pathlib import Path
from pydantic import Field
from pydantic_settings import BaseSettings
from typing_extensions import Annotated
from typing import Optional
from fastapi import Depends


class ApiSettings(BaseSettings):
    resource_directory: Annotated[
        Path, Field(default=Path("."), title="Backend file resource directory")
    ]
    ewoks: Annotated[Optional[dict], Field(default=None, title="Ewoks configuration")]
    celery: Annotated[Optional[dict], Field(default=None, title="Celery configuration")]


@lru_cache()
def get_api_settings():
    return ApiSettings()


ApiSettingsType = Annotated[ApiSettings, Depends(get_api_settings)]
