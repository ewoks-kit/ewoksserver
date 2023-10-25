from typing import List, Optional
from typing_extensions import Annotated
from pydantic import BaseModel
from pydantic import Field


class EwoksWorkflow(BaseModel):
    graph: Annotated[Optional[dict], Field(title="Workflow attributes", default=None)]
    nodes: Annotated[Optional[List[dict]], Field(title="Node attributes", default=None)]
    links: Annotated[Optional[List[dict]], Field(title="Link attributes", default=None)]


class EwoksWorkflowDescription(BaseModel):
    id: Annotated[
        Optional[str],
        Field(title="Workflow identifier unique to the server", default=None),
    ]
    label: Annotated[
        Optional[str], Field(title="Workflow label for human consumption", default=None)
    ]
    category: Annotated[
        Optional[str],
        Field(title="Workflow category unique to the server", default=None),
    ]
    keywords: Annotated[
        Optional[dict], Field(title="Workflow search keywords", default=None)
    ]
    input_schema: Annotated[
        Optional[dict],
        Field(title="Workflow execute input schema for the frontend", default=None),
    ]
    ui_schema: Annotated[
        Optional[dict],
        Field(title="Workflow execute UI schema for the frontend", default=None),
    ]


class ResourceInfo(BaseModel):
    identifier: Annotated[str, Field(title="Resource identifier")]


class ResourceError(BaseModel):
    message: Annotated[str, Field(title="Error message")]
    type: Annotated[str, Field(title="Resource type")]


class ResourceIdentifierError(ResourceError):
    identifier: Annotated[str, Field(title="Resource identifier")]


class EwoksWorkflowIdentifiers(BaseModel):
    identifiers: Annotated[List[str], Field(title="Workflow identifiers")]


class EwoksWorkflowDescriptions(BaseModel):
    items: Annotated[
        List[EwoksWorkflowDescription], Field(title="Workflow descriptions")
    ]
