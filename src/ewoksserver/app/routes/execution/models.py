from typing import Optional, List, Union
from typing_extensions import Annotated
from pydantic import BaseModel
from pydantic import Field


class EwoksExecuteOptions(BaseModel):
    execute_arguments: Annotated[
        Optional[dict], Field(title="Workflow execution options", default=None)
    ]
    worker_options: Annotated[
        Optional[dict], Field(title="Worker options", default=None)
    ]


class EwoksJobInfo(BaseModel):
    job_id: Annotated[Union[str, int], Field(title="Workflow execution job identifier")]


class EwoksEvent(BaseModel):
    host_name: Annotated[str, Field(title="Host where the job was executed")]
    process_id: Annotated[int, Field(title="Process ID where the job was executed")]
    user_name: Annotated[str, Field(title="User name under which the job was executed")]
    job_id: Annotated[str, Field(title="Workflow execution job identifier")]
    binding: Annotated[
        Optional[str], Field(title="Workflow execution engine", default=None)
    ]
    context: Annotated[str, Field(title="Event context (job, workflow, node)")]
    workflow_id: Annotated[
        Optional[str], Field(title="Workflow identifier", default=None)
    ]
    node_id: Annotated[
        Optional[str], Field(title="Workflow node identifier", default=None)
    ]
    task_id: Annotated[
        Optional[str], Field(title="Workflow task identifier", default=None)
    ]
    type: Annotated[str, Field(title="Event type (start, end, progress)")]
    time: Annotated[str, Field(title="Event context send time")]
    error: Annotated[
        Optional[bool], Field(title="Workflow execution failed", default=None)
    ]
    error_message: Annotated[
        Optional[str], Field(title="Workflow execution error message", default=None)
    ]
    error_traceback: Annotated[
        Optional[str], Field(title="Workflow execution error traceback", default=None)
    ]
    progress: Annotated[
        Optional[int], Field(title="Task progress in percentage", default=None)
    ]
    task_uri: Annotated[
        Optional[str], Field(title="Workflow task output URI", default=None)
    ]
    input_uris: Annotated[
        Optional[List[dict]], Field(title="Workflow task input URIs", default=None)
    ]
    output_uris: Annotated[
        Optional[List[dict]], Field(title="Workflow task output URIs", default=None)
    ]


class EwoksEventFilter(BaseModel):
    user_name: Annotated[
        Optional[str],
        Field(title="User name under which the job was executed", default=None),
    ]
    job_id: Annotated[
        Optional[str], Field(title="Workflow execution job identifier", default=None)
    ]
    context: Annotated[
        Optional[str], Field(title="Event context (job, workflow, node)", default=None)
    ]
    workflow_id: Annotated[
        Optional[str], Field(title="Workflow identifier", default=None)
    ]
    node_id: Annotated[
        Optional[str], Field(title="Workflow node identifier", default=None)
    ]
    task_id: Annotated[
        Optional[str], Field(title="Workflow task identifier", default=None)
    ]
    type: Annotated[
        Optional[str], Field(title="Event type (start, end, progress)", default=None)
    ]
    starttime: Annotated[
        Optional[str], Field(title="Only events after this time", default=None)
    ]
    endtime: Annotated[
        Optional[str], Field(title="Only events before this time", default=None)
    ]
    error: Annotated[
        Optional[bool], Field(title="Workflow execution failed", default=None)
    ]


class EwoksEventList(BaseModel):
    jobs: Annotated[
        List[List[EwoksEvent]],
        Field(title="Workflow execution jobs grouped per job ID"),
    ]
