from pydantic import BaseModel
from pydantic import Field


class EwoksTaskDescription(BaseModel):
    task_type: str = Field(title="One of the Ewoks task types")
    task_identifier: str = Field(title="Task identifier unique to the server")
    category: str | None = Field(title="Task category", default=None)
    icon: str | None = Field(
        title="Task icon identifier unique to the server", default=None
    )
    required_input_names: list[str] | None = Field(
        title="Task required input names", default=None
    )
    optional_input_names: list[str] | None = Field(
        title="Task optional input names", default=None
    )
    output_names: list[str] | None = Field(title="Task output names", default=None)


class EwoksTaskIdentifiers(BaseModel):
    identifiers: list[str] = Field(title="Task identifiers")


class EwoksTaskDescriptions(BaseModel):
    items: list[EwoksTaskDescription] = Field(title="Task descriptions")


class EwoksTaskDiscovery(BaseModel):
    modules: list[str] | None = Field(title="Ewoks task description", default=None)
    task_type: str | None = Field(title="Task type to discover", default=None)
    worker_options: dict | None = Field(title="Worker options", default=None)
