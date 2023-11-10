from typing import List, Optional, Dict
from typing_extensions import Annotated
from pydantic import BaseModel
from pydantic import Field


class EwoksWorkflow(BaseModel):
    graph: Annotated[Optional[Dict], Field(title="Workflow attributes", default=None)]
    nodes: Annotated[Optional[List[Dict]], Field(title="Node attributes", default=None)]
    links: Annotated[Optional[List[Dict]], Field(title="Link attributes", default=None)]


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
        Field(title="Workflow category", default=None),
    ]
    keywords: Annotated[
        Optional[Dict], Field(title="Workflow search keywords", default=None)
    ]
    input_schema: Annotated[
        Optional[Dict],
        Field(title="Workflow execute input schema for the frontend", default=None),
    ]
    ui_schema: Annotated[
        Optional[Dict],
        Field(title="Workflow execute UI schema for the frontend", default=None),
    ]


class EwoksWorkflowIdentifiers(BaseModel):
    identifiers: Annotated[List[str], Field(title="Workflow identifiers")]


class EwoksWorkflowDescriptions(BaseModel):
    items: Annotated[
        List[EwoksWorkflowDescription], Field(title="Workflow descriptions")
    ]
