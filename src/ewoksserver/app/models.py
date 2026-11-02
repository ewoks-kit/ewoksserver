import logging
from enum import Enum
from pathlib import Path

from pydantic import BaseModel
from pydantic import Field
from pydantic import field_validator
from pydantic import model_validator

logger = logging.getLogger(__name__)


class EwoksSchedulingType(str, Enum):
    Local = "local"
    Celery = "celery"


class EwoksDiscoverySettings(BaseModel):
    on_start_up: bool = Field(
        default=True, title="Discover ewoks tasks/workflows on startup"
    )
    timeout: float | None = Field(
        default=None, title="Timeout for task/workflow discovery (in seconds)"
    )
    cache_workflows: bool = Field(
        default=True,
        title="Create a local copy of a workflow when it is discovered",
    )
    save_requirements: bool = Field(
        default=False,
        title="Save the python environment requirements in external workflows",
    )


class EwoksExecutionSettings(BaseModel):
    handlers: list[dict] = Field(default=list(), title="Ewoks execution handlers")


class EwoksJobSettings(BaseModel):
    type: EwoksSchedulingType = EwoksSchedulingType.Local
    configuration: dict = dict()


class EwoksAuthSettings(BaseModel):
    enabled: bool = Field(default=False, title="Require authentication")
    secret_key: str | None = Field(default=None, title="Secret used to sign tokens")
    algorithm: str = Field(default="HS256", title="Token signing algorithm")
    token_expire_minutes: int = Field(default=30, title="Token lifetime (in minutes)")
    users: dict[str, str] = Field(
        default=dict(), title="Mapping of user names to password hashes"
    )

    @model_validator(mode="after")
    def check_secret_key(self):
        if self.enabled and not self.secret_key:
            raise ValueError("`secret_key` is required when authentication is enabled")
        return self


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
    ewoks_auth: EwoksAuthSettings = Field(
        default=None, title="Ewoks authentication settings", validate_default=True
    )

    @field_validator(
        "ewoks_discovery",
        "ewoks_execution",
        "ewoks_scheduling",
        "ewoks_auth",
        mode="before",
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
