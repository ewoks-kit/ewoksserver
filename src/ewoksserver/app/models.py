from pathlib import Path
from typing import Dict, List, Optional
import warnings
import logging

from pydantic import Field, model_validator
from pydantic import BaseModel


logger = logging.getLogger(__name__)


class EwoksDiscoverySettings(BaseModel):
    on_start_up: bool = Field(default=False, title="Discover ewoks tasks on startup")
    timeout: Optional[float] = Field(
        default=None, title="Timeout for task discovery (in seconds)"
    )


class EwoksExecutionSettings(BaseModel):
    handlers: List[Dict] = Field(default=list(), title="Ewoks execution handlers")


class EwoksSettings(BaseModel):
    configured: bool = Field(
        default=False, title="Config or resource directory have been defined"
    )
    resource_directory: Path = Field(
        default=Path("."), title="Backend file resource directory"
    )
    celery: Optional[Dict] = Field(default=None, title="Celery configuration")
    without_events: bool = Field(default=False, title="Enable ewoks events")
    ewoks_discovery: Optional[EwoksDiscoverySettings] = Field(
        default=None, title="Ewoks discovery settings"
    )
    ewoks_execution: Optional[EwoksExecutionSettings] = Field(
        default=None, title="Ewoks execution settings"
    )
    # DEPRECATED
    ewoks: Optional[Dict] = Field(default=None, title="Ewoks configuration")
    discover_timeout: Optional[float] = Field(
        default=None, title="Timeout for task discovery (in seconds)"
    )

    @model_validator(mode="after")
    def resolve_ewoks_execution_settings(self):
        ewoks_execution = self.ewoks_execution
        ewoks = self.ewoks

        if ewoks is None:
            return self

        if ewoks_execution is None:
            warnings.warn(
                "EWOKS configuration field has been renamed EWOKS_EXECUTION",
                DeprecationWarning,
            )
            self.ewoks_execution = EwoksExecutionSettings(**ewoks)
        else:
            logger.warning(
                "Both EWOKS_EXECUTION and EWOKS fields were specified but EWOKS field is deprecated. EWOKS field will be ignored."
            )

        return self

    @model_validator(mode="after")
    def resolve_ewoks_discovery_timeout(self):
        ewoks_discovery = self.ewoks_discovery
        discover_timeout = self.discover_timeout

        if discover_timeout is None:
            return self

        if ewoks_discovery is not None:
            logger.warning(
                "Both EWOKS_DISCOVERY and DISCOVER_TIMEOUT fields were specified but DISCOVER_TIMEOUT field is deprecated. DISCOVER_TIMEOUT field will be ignored."
            )
            return self

        warnings.warn(
            "DISCOVER_TIMEOUT is deprecated. The timeout should be specified via the `timeout` field of EWOKS_DISCOVERY",
            DeprecationWarning,
        )
        self.ewoks_discovery = EwoksDiscoverySettings(timeout=discover_timeout)

        return self


class AppSettings(BaseModel):
    no_older_versions: bool = Field(
        default=False, title="Do not create end points for older API versions"
    )
