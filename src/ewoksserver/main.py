"""Start ewoks server from the command line with the Uvicorn CLI

..code: bash

    uvicorn ewoksserver.main:app

or the FastAPI CLI

..code: bash

    fastapi dev src/ewoksserver/main.py
    fastapi run src/ewoksserver/main.py

Ewoks specific parameters are supported through environment variables with prefix "EWOKSAPP_".
"""

from typing import Optional
from pydantic_settings import BaseSettings
from pydantic_settings import SettingsConfigDict

from .app import create_app
from .config import configure_app


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="ewoksapp_")

    config: Optional[str] = None  # ewoks parameter
    dir: Optional[str] = None  # ewoks parameter
    without_events: bool = False  # ewoks parameter
    frontend_tests: bool = False  # ewoks parameter
    rediscover_tasks: bool = False  # ewoks parameter
    no_older_versions: bool = False  # app parameter
    log_level: Optional[str] = None  # uvicorn parameter


settings = Settings()
_ = configure_app(**settings.dict())

app = create_app()
