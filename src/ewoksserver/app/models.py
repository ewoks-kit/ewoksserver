from pathlib import Path
from typing import Dict, Optional

from pydantic import Field
from pydantic import BaseModel


class EwoksSettings(BaseModel):
    configured: bool = Field(
        default=False, title="Config or resource directory have been defined"
    )
    resource_directory: Path = Field(
        default=Path("."), title="Backend file resource directory"
    )
    ewoks: Optional[Dict] = Field(default=None, title="Ewoks configuration")
    celery: Optional[Dict] = Field(default=None, title="Celery configuration")
    without_events: bool = Field(default=False, title="Enable ewoks events")
    discover_tasks: bool = Field(default=False, title="Discover ewoks tasks on startup")
    discover_timeout: Optional[float] = Field(
        default=None, title="Timeout for task discovery (in seconds)"
    )


class AppSettings(BaseModel):
    no_older_versions: bool = Field(
        default=False, title="Do not create end points for older API versions"
    )
