import logging
from enum import Enum
from pathlib import Path

from pydantic import BaseModel
from pydantic import Field
from pydantic import field_validator

logger = logging.getLogger(__name__)


class EwoksSchedulingType(str, Enum):
    Local = "local"
    Celery = "celery"


class EwoksDiscoverySettings(BaseModel):
    on_start_up: bool = Field(default=True, title="Discover ewoks tasks on startup")
    timeout: float | None = Field(
        default=None, title="Timeout for task discovery (in seconds)"
    )


class EwoksExecutionSettings(BaseModel):
    handlers: list[dict] = Field(default=list(), title="Ewoks execution handlers")


class EwoksJobSettings(BaseModel):
    type: EwoksSchedulingType = EwoksSchedulingType.Local
    configuration: dict = dict()


class EwoksSettings(BaseModel):
    configured: bool = Field(
        default=False, title="Config or resource directory have been defined"
    )
    resource_directory: Path = Field(
        default=Path("."), title="Backend file resource directory"
    )
    without_events: bool = Field(default=False, title="Enable ewoks events")
    ewoks_discovery: EwoksDiscoverySettings = Field(
        default=None, title="Ewoks discovery settings", validate_default=True
    )
    ewoks_execution: EwoksExecutionSettings = Field(
        default=None, title="Ewoks execution settings", validate_default=True
    )
    ewoks_scheduling: EwoksJobSettings = Field(
        default=None, title="Ewoks job scheduling settings", validate_default=True
    )

    @field_validator(
        "ewoks_discovery", "ewoks_execution", "ewoks_scheduling", mode="before"
    )
    @classmethod
    def set_default_value(cls, input_value):
        if input_value is None:
            return dict()

        return input_value


class AppSettings(BaseModel):
    no_older_versions: bool = Field(
        default=False, title="Do not create end points for older API versions"
    )
