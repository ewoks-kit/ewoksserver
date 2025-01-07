from typing import Any, Dict
from fastapi.responses import JSONResponse
from fastapi import status

from ewoksjob.client import submit
from ewoksjob.client.local import submit as submit_local

from ...models import EwoksSchedulingType
from ...config import EwoksSettingsType


class WorkflowNotReadableResponse(JSONResponse):
    def __init__(self, identifier: str):
        super().__init__(
            {
                "message": f"No permission to read workflow '{identifier}'.",
                "type": "workflow",
                "identifier": identifier,
            },
            status_code=status.HTTP_403_FORBIDDEN,
        )


class WorkflowNotFoundResponse(JSONResponse):
    def __init__(self, identifier: str):
        super().__init__(
            {
                "message": f"Workflow '{identifier}' is not found.",
                "type": "workflow",
                "identifier": identifier,
            },
            status_code=status.HTTP_404_NOT_FOUND,
        )


def submit_workflow(
    workflow,
    execute_arguments: Dict[str, Any],
    submit_arguments: Dict[str, Any],
    settings: EwoksSettingsType,
):
    submit_kwargs = {**submit_arguments}

    # Workflow execution: position arguments
    submit_kwargs["args"] = (workflow,)
    # Workflow execution: named arguments
    submit_kwargs["kwargs"] = execute_arguments

    execinfo = execute_arguments.setdefault("execinfo", dict())
    handlers = execinfo.setdefault("handlers", list())
    for handler in settings.ewoks_execution.handlers:
        if handler not in handlers:
            handlers.append(handler)

    if settings.ewoks_scheduling.type == EwoksSchedulingType.Local:
        return submit_local(**submit_kwargs)
    else:
        return submit(**submit_kwargs)
