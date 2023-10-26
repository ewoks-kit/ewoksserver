from typing import List
from typing_extensions import Annotated
from pydantic import BaseModel
from pydantic import Field


class EwoksIcon(BaseModel):
    data_url: Annotated[str, Field(title="Icon data url")]


class ResourceInfo(BaseModel):
    identifier: Annotated[str, Field(title="Resource identifier")]


class ResourceError(BaseModel):
    message: Annotated[str, Field(title="Error message")]
    type: Annotated[str, Field(title="Resource type")]


class ResourceIdentifierError(ResourceError):
    identifier: Annotated[str, Field(title="Resource identifier")]


class EwoksIconIdentifiers(BaseModel):
    identifiers: Annotated[List[str], Field(title="Icon identifiers")]
