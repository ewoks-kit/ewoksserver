import logging
from typing import Optional, Dict, Any

from .app.config import create_ewoks_settings
from .app.config import create_app_settings


def configure_app(
    config: Optional[str] = None,  # ewoks parameter
    dir: Optional[str] = None,  # ewoks parameter
    without_events: bool = False,  # ewoks parameter
    frontend_tests: bool = False,  # ewoks parameter
    rediscover_tasks: bool = False,  # ewoks parameter
    no_older_versions: bool = False,  # app parameter
    log_level: Optional[str] = None,  # uvicorn parameter
) -> Dict[str, Any]:
    if not log_level:
        log_level = "info"
    if log_level:
        level = logging.getLevelName(log_level.upper())
        logging.basicConfig(
            level=level, format="%(levelname)8s(BACKEND %(asctime)s): %(message)s"
        )
    create_app_settings(no_older_versions=no_older_versions)
    create_ewoks_settings(
        config=config,
        directory=dir,
        without_events=without_events,
        frontend_tests=frontend_tests,
        rediscover_tasks=rediscover_tasks,
    )
    return {"log_level": log_level}
