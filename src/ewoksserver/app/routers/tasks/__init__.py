from typing import Optional, List, Dict
from typing_extensions import Annotated

from fastapi import APIRouter
from fastapi import Path
from fastapi import Body
from fastapi.responses import JSONResponse
from fastapi import status


from ...backends import json_backend
from ...config import ApiSettingsType
from . import discovery
from . import models

_router = APIRouter()

routers = {(1, 0, 0): _router}


@_router.get(
    "/task/{identifier}",
    summary="Get ewoks task description",
    response_model=models.EwoksTaskDescription,
    response_model_exclude_none=True,
    response_description="Ewoks task description",
    status_code=200,
    responses={
        status.HTTP_403_FORBIDDEN: {
            "description": "No permission to read task",
            "model": models.ResourceIdentifierError,
        },
        status.HTTP_404_NOT_FOUND: {
            "description": "Task not found",
            "model": models.ResourceIdentifierError,
        },
    },
)
def get_task(
    identifier: Annotated[
        str,
        Path(
            title="Task identifier",
            description="Unique identifier in the task database",
        ),
    ],
    settings: ApiSettingsType,
) -> json_backend.ResourceContentType:
    try:
        return json_backend.load_resource(
            settings.resource_directory / "tasks", identifier
        )
    except PermissionError:
        return JSONResponse(
            {
                "message": f"No permission to read task '{identifier}'.",
                "type": "task",
                "identifier": identifier,
            },
            status_code=status.HTTP_403_FORBIDDEN,
        )
    except FileNotFoundError:
        return JSONResponse(
            {
                "message": f"Task '{identifier}' is not found.",
                "type": "task",
                "identifier": identifier,
            },
            status_code=status.HTTP_404_NOT_FOUND,
        )


@_router.get(
    "/tasks",
    summary="Get all ewoks task identifiers",
    response_model=models.EwoksTaskIdentifiers,
    response_description="Ewoks task identifiers",
    status_code=200,
)
def get_task_identifiers(settings: ApiSettingsType) -> Dict[str, List[str]]:
    return {
        "identifiers": list(
            json_backend.resource_identifiers(settings.resource_directory / "tasks")
        )
    }


@_router.get(
    "/tasks/descriptions",
    summary="Get all ewoks task descriptions",
    response_model=models.EwoksTaskDescriptions,
    response_description="Ewoks task descriptions",
    status_code=200,
)
def get_tasks(settings: ApiSettingsType) -> Dict[str, List[str]]:
    return {
        "items": list(json_backend.resources(settings.resource_directory / "tasks"))
    }


@_router.put(
    "/task/{identifier}",
    summary="Update ewoks task description",
    response_model=models.EwoksTaskDescription,
    response_model_exclude_none=True,
    response_description="Ewoks task description",
    status_code=200,
    responses={
        status.HTTP_400_BAD_REQUEST: {
            "description": "Wrong task identifier",
            "model": models.ResourceIdentifierError,
        },
        status.HTTP_404_NOT_FOUND: {
            "description": "Task not found",
            "model": models.ResourceIdentifierError,
        },
        status.HTTP_403_FORBIDDEN: {
            "description": "No permission to edit task",
            "model": models.ResourceIdentifierError,
        },
    },
)
def update_task(
    identifier: Annotated[
        str,
        Path(
            title="Task identifier",
            description="Unique identifier in the task database",
        ),
    ],
    task: Annotated[models.EwoksTaskDescription, Body(title="Ewoks task description")],
    settings: ApiSettingsType,
) -> models.EwoksTaskDescription:
    ridentifier = task.task_identifier
    if identifier != ridentifier:
        return JSONResponse(
            {
                "message": f"Resource identifier '{identifier}' is not equal to '{ridentifier}'.",
                "type": "task",
                "identifier": identifier,
            },
            status_code=status.HTTP_400_BAD_REQUEST,
        )

    exists = json_backend.resource_exists(
        settings.resource_directory / "tasks", identifier
    )
    if not exists:
        return JSONResponse(
            {
                "message": f"Task '{identifier}' is not found.",
                "type": "task",
                "identifier": identifier,
            },
            status_code=status.HTTP_404_NOT_FOUND,
        )

    try:
        json_backend.save_resource(
            settings.resource_directory / "tasks", identifier, task.dict()
        )
    except PermissionError:
        return JSONResponse(
            {
                "message": f"No permission to edit task '{identifier}'.",
                "type": "task",
                "identifier": identifier,
            },
            status_code=status.HTTP_403_FORBIDDEN,
        )

    return task


@_router.post(
    "/tasks",
    summary="Create ewoks task description",
    response_model=models.EwoksTaskDescription,
    response_model_exclude_none=True,
    response_description="Ewoks task description",
    status_code=200,
    responses={
        status.HTTP_409_CONFLICT: {
            "description": "Task already exists",
            "model": models.ResourceIdentifierError,
        },
        status.HTTP_403_FORBIDDEN: {
            "description": "No permission to create task",
            "model": models.ResourceIdentifierError,
        },
    },
)
def create_task(
    task: Annotated[models.EwoksTaskDescription, Body(title="Ewoks task description")],
    settings: ApiSettingsType,
) -> models.EwoksTaskDescription:
    ridentifier = task.task_identifier

    exists = json_backend.resource_exists(
        settings.resource_directory / "tasks", ridentifier
    )
    if exists:
        return JSONResponse(
            {
                "message": f"Task '{ridentifier}' already exists.",
                "type": "task",
                "identifier": ridentifier,
            },
            status_code=status.HTTP_409_CONFLICT,
        )

    try:
        json_backend.save_resource(
            settings.resource_directory / "tasks", ridentifier, task.dict()
        )
    except PermissionError:
        return JSONResponse(
            {
                "message": f"No permission to create task '{ridentifier}'.",
                "type": "task",
                "identifier": ridentifier,
            },
            status_code=status.HTTP_403_FORBIDDEN,
        )

    return task


@_router.post(
    "/tasks/discover",
    summary="Create ewoks task descriptions from the worker environments",
    response_model=models.EwoksTaskIdentifiers,
    response_description="Discovered ewoks task identifiers",
    status_code=200,
    responses={
        status.HTTP_403_FORBIDDEN: {
            "description": "No permission to create or edit task",
            "model": models.ResourceIdentifierError,
        },
        status.HTTP_404_NOT_FOUND: {
            "description": "Module not found",
            "model": models.ResourceError,
        },
    },
)
def discover_tasks(
    settings: ApiSettingsType,
    modules: Annotated[
        Optional[List[str]], Body(title="Ewoks task description")
    ] = None,
    worker_options: Annotated[Optional[dict], Body(title="Worker options")] = None,
) -> Dict[str, List[str]]:
    try:
        tasks = discovery.discover_tasks(
            settings, modules=modules, reload=True, worker_options=worker_options
        )
    except ModuleNotFoundError as e:
        return JSONResponse(
            {
                "message": str(e),
                "type": "task",
            },
            status_code=status.HTTP_404_NOT_FOUND,
        )

    for task in tasks:
        ridentifier = task["task_identifier"]
        try:
            json_backend.save_resource(
                settings.resource_directory / "tasks", ridentifier, task
            )
        except PermissionError:
            return JSONResponse(
                {
                    "message": f"No permission to create task '{ridentifier}'.",
                    "type": "task",
                    "identifier": ridentifier,
                },
                status_code=status.HTTP_403_FORBIDDEN,
            )

    return {"identifiers": [task["task_identifier"] for task in tasks]}


@_router.delete(
    "/task/{identifier}",
    summary="Delete ewoks task",
    response_model=models.ResourceInfo,
    response_description="Deleted ewoks task",
    status_code=200,
    responses={
        status.HTTP_403_FORBIDDEN: {
            "description": "No permission to read task",
            "model": models.ResourceIdentifierError,
        },
        status.HTTP_404_NOT_FOUND: {
            "description": "Task not found",
            "model": models.ResourceIdentifierError,
        },
    },
)
def delete_task(
    identifier: Annotated[
        str,
        Path(
            title="Task identifier",
            description="Unique identifier in the task database",
        ),
    ],
    settings: ApiSettingsType,
) -> Dict[str, str]:
    try:
        json_backend.delete_resource(settings.resource_directory / "tasks", identifier)
    except PermissionError:
        return JSONResponse(
            {
                "message": f"No permission to delete task '{identifier}'.",
                "type": "task",
                "identifier": identifier,
            },
            status_code=status.HTTP_403_FORBIDDEN,
        )
    except FileNotFoundError:
        return JSONResponse(
            {
                "message": f"Task '{identifier}' is not found.",
                "type": "task",
                "identifier": identifier,
            },
            status_code=status.HTTP_404_NOT_FOUND,
        )
    return {"identifier": identifier, "type": "task"}
