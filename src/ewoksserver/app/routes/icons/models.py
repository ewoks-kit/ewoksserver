from typing import List
from typing_extensions import Annotated
from pydantic import BaseModel
from pydantic import Field


class EwoksIcon(BaseModel):
    data_url: Annotated[str, Field(title="Icon data url")]


class EwoksIconIdentifiers(BaseModel):
    identifiers: Annotated[List[str], Field(title="Icon identifiers")]
