from typing import Optional, List
from typing_extensions import Annotated
from pydantic import BaseModel
from pydantic import Field


class EwoksTaskDescription(BaseModel):
    task_type: Annotated[str, Field(title="One of the Ewoks task types")]
    task_identifier: Annotated[str, Field(title="Task identifier unique to the server")]
    category: Annotated[
        Optional[str], Field(title="Task category unique to the server", default=None)
    ]
    icon: Annotated[
        Optional[str],
        Field(title="Task icon identifier unique to the server", default=None),
    ]
    required_input_names: Annotated[
        Optional[List[str]], Field(title="Required task input names", default=None)
    ]
    optional_input_names: Annotated[
        Optional[List[str]], Field(title="Optional task input names", default=None)
    ]
    output_names: Annotated[
        Optional[List[str]], Field(title="Task output names", default=None)
    ]


class EwoksTaskIdentifiers(BaseModel):
    identifiers: Annotated[List[str], Field(title="Task identifiers")]


class EwoksTaskDescriptions(BaseModel):
    items: Annotated[List[EwoksTaskDescription], Field(title="Task descriptions")]


class EwoksTaskDiscovery(BaseModel):
    modules: Annotated[
        Optional[List[str]], Field(title="Ewoks task description", default=None)
    ]
    worker_options: Annotated[
        Optional[dict], Field(title="Worker options", default=None)
    ]
