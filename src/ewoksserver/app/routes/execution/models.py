from typing import Union

from pydantic import BaseModel
from pydantic import Field


class EwoksExecuteOptions_v1(BaseModel):
    execute_arguments: dict | None = Field(
        title="Workflow execution options", default=None
    )
    worker_options: dict | None = Field(title="Worker options", default=None)


class EwoksExecuteOptions_v2(BaseModel):
    execute_arguments: dict | None = Field(
        title="Workflow execution options", default=None
    )
    submit_arguments: dict | None = Field(
        title="Workflow submission options", default=None
    )


class EwoksJobInfo(BaseModel):
    job_id: Union[str, int] = Field(title="Workflow execution job identifier")


class EwoksEvent_v1(BaseModel):
    host_name: str = Field(title="Host where the job was executed")
    process_id: int = Field(title="Process ID where the job was executed")
    user_name: str = Field(title="User name under which the job was executed")
    job_id: str = Field(title="Workflow execution job identifier")
    binding: str | None = Field(title="Workflow execution engine", default=None)
    context: str = Field(title="Event context (job, workflow, node)")
    workflow_id: str | None = Field(title="Workflow identifier", default=None)
    node_id: str | None = Field(title="Workflow node identifier", default=None)
    task_id: str | None = Field(title="Workflow task identifier", default=None)
    type: str = Field(title="Event type (start, end, progress)")
    time: str = Field(title="Event context send time")
    error: bool | None = Field(title="Workflow execution failed", default=None)
    error_message: str | None = Field(
        title="Workflow execution error message", default=None
    )
    error_traceback: str | None = Field(
        title="Workflow execution error traceback", default=None
    )
    progress: int | None = Field(title="Task progress in percentage", default=None)
    task_uri: str | None = Field(title="Workflow task output URI", default=None)
    input_uris: list[dict] | None = Field(
        title="Workflow task input URIs", default=None
    )
    output_uris: list[dict] | None = Field(
        title="Workflow task output URIs", default=None
    )


class EwoksEventFilter(BaseModel):
    user_name: str | None = Field(
        title="User name under which the job was executed", default=None
    )
    job_id: str | None = Field(title="Workflow execution job identifier", default=None)
    context: str | None = Field(
        title="Event context (job, workflow, node)", default=None
    )
    workflow_id: str | None = Field(title="Workflow identifier", default=None)
    node_id: str | None = Field(title="Workflow node identifier", default=None)
    task_id: str | None = Field(title="Workflow task identifier", default=None)
    type: str | None = Field(title="Event type (start, end, progress)", default=None)
    starttime: str | None = Field(title="Only events after this time", default=None)
    endtime: str | None = Field(title="Only events before this time", default=None)
    error: bool | None = Field(title="Workflow execution failed", default=None)


class EwoksEventList_v1(BaseModel):
    jobs: list[list[EwoksEvent_v1]] = Field(
        title="Workflow execution jobs grouped per job ID"
    )


class EwoksWorkerList(BaseModel):
    workers: list[str] | None = Field(title="Available workers for execution")


class EwoksQueueList(BaseModel):
    queues: list[str] | None = Field(title="Available queues for execution")


class EwoksEvent_v2(BaseModel):
    host_name: str = Field(title="Host where the job was executed")
    process_id: int = Field(title="Process ID where the job was executed")
    user_name: str = Field(title="User name under which the job was executed")
    job_id: str = Field(title="Workflow execution job identifier")
    engine: str | None = Field(title="Workflow execution engine", default=None)
    context: str = Field(title="Event context (job, workflow, node)")
    workflow_id: str | None = Field(title="Workflow identifier", default=None)
    node_id: str | None = Field(title="Workflow node identifier", default=None)
    task_id: str | None = Field(title="Workflow task identifier", default=None)
    type: str = Field(title="Event type (start, end, progress)")
    time: str = Field(title="Event context send time")
    error: bool | None = Field(title="Workflow execution failed", default=None)
    error_message: str | None = Field(
        title="Workflow execution error message", default=None
    )
    error_traceback: str | None = Field(
        title="Workflow execution error traceback", default=None
    )
    progress: int | None = Field(title="Task progress in percentage", default=None)
    task_uri: str | None = Field(title="Workflow task output URI", default=None)
    input_uris: list[dict] | None = Field(
        title="Workflow task input URIs", default=None
    )
    output_uris: list[dict] | None = Field(
        title="Workflow task output URIs", default=None
    )


class EwoksEventList_v2(BaseModel):
    jobs: list[list[EwoksEvent_v2]] = Field(
        title="Workflow execution jobs grouped per job ID"
    )
