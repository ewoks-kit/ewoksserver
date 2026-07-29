from pydantic import BaseModel
from pydantic import Field

from ...backends.binary_backend import DATA_URL_PREFIX


class EwoksIcon(BaseModel):
    data_url: str = Field(
        title="Icon data url",
        description="Base64-encoded data URL (e.g. 'data:image/png;base64,...')",
        pattern=DATA_URL_PREFIX.pattern,
    )


class EwoksIconIdentifiers(BaseModel):
    identifiers: list[str] = Field(title="Icon identifiers")
