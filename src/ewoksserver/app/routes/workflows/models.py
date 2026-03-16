from pydantic import BaseModel
from pydantic import Field


class EwoksWorkflow(BaseModel):
    graph: dict | None = Field(title="Workflow attributes", default=None)
    nodes: list[dict] | None = Field(title="Node attributes", default=None)
    links: list[dict] | None = Field(title="Link attributes", default=None)


class EwoksWorkflowDescription(BaseModel):
    id: str | None = Field(
        title="Workflow identifier unique to the server", default=None
    )
    label: str | None = Field(
        title="Workflow label for human consumption", default=None
    )
    category: str | None = Field(title="Workflow category", default=None)
    keywords: dict | None = Field(title="Workflow search keywords", default=None)
    input_schema: dict | None = Field(
        title="Workflow execute input schema for the frontend", default=None
    )
    ui_schema: dict | None = Field(
        title="Workflow execute UI schema for the frontend", default=None
    )


class EwoksWorkflowIdentifiers(BaseModel):
    identifiers: list[str] = Field(title="Workflow identifiers")


class EwoksWorkflowDescriptions(BaseModel):
    items: list[EwoksWorkflowDescription] = Field(title="Workflow descriptions")
