import logging
from typing import Any
from typing import Callable

from ewoksjob.client import discover_all_tasks
from ewoksjob.client import discover_all_workflows
from ewoksjob.client import discover_tasks_from_modules
from ewoksjob.client import discover_workflows_from_modules
from ewoksjob.client import get_queues
from ewoksjob.client.local import discover_all_tasks as discover_all_tasks_local
from ewoksjob.client.local import discover_all_workflows as discover_all_workflows_local
from ewoksjob.client.local import (
    discover_tasks_from_modules as discover_tasks_from_modules_local,
)
from ewoksjob.client.local import (
    discover_workflows_from_modules as discover_workflows_from_modules_local,
)

from ...config import EwoksSettings
from ...models import EwoksSchedulingType

logger = logging.getLogger(__name__)


def discover_tasks(
    settings: EwoksSettings,
    modules: list[str] | None = None,
    reload: bool | None = None,
    task_type: str | None = None,
    worker_options: dict | None = None,
) -> list[dict[str, str]]:
    """
    :raises ModuleNotFoundError: failed importing tasks.
    :raises TimeoutError: timeout when asking a remote worker for tasks.
    :raises Exception: any other import or remote error.
    """
    if settings.ewoks_scheduling.type == EwoksSchedulingType.Local:
        if modules:
            discover = discover_tasks_from_modules_local
        else:
            discover = discover_all_tasks_local
    else:
        if modules:
            discover = discover_tasks_from_modules
        else:
            discover = discover_all_tasks

    discover_kwargs = dict()
    if reload is not None:
        discover_kwargs["reload"] = reload
    if task_type is not None:
        discover_kwargs["task_type"] = task_type

    tasks, _identifier_to_queue = _discover(
        discover,
        settings,
        modules=modules,
        discover_kwargs=discover_kwargs,
        worker_options=worker_options,
        id_extractor=lambda task: task["task_identifier"],
    )

    for task in tasks:
        _set_default_task_properties(task)
    return tasks


def discover_workflows(
    settings: EwoksSettings,
    modules: list[str] | None = None,
    workflow_extension: str | None = None,
    worker_options: dict | None = None,
) -> tuple[list[str], dict[str, str | None]]:
    """
    :raises ModuleNotFoundError: failed importing workflows.
    :raises TimeoutError: timeout when asking a remote worker for workflows.
    :raises Exception: any other import or remote error.
    :returns: the discovered workflow identifiers, and a mapping of each
        identifier to the celery queue it was discovered on (`None` for
        local scheduling).
    """
    if settings.ewoks_scheduling.type == EwoksSchedulingType.Local:
        if modules:
            discover = discover_workflows_from_modules_local
        else:
            discover = discover_all_workflows_local
    else:
        if modules:
            discover = discover_workflows_from_modules
        else:
            discover = discover_all_workflows

    discover_kwargs = dict()
    if workflow_extension is not None:
        discover_kwargs["workflow_extension"] = workflow_extension

    return _discover(
        discover,
        settings,
        modules=modules,
        discover_kwargs=discover_kwargs,
        worker_options=worker_options,
        id_extractor=lambda graph_id: graph_id,
    )


def _discover(
    discover,
    settings: EwoksSettings,
    modules: list[str] | None,
    discover_kwargs: dict,
    worker_options: dict | None,
    id_extractor: Callable[[Any], str],
) -> tuple[list, dict[str, str | None]]:
    """
    :raises ModuleNotFoundError: failed importing tasks or workflows.
    :raises TimeoutError: timeout when asking a remote worker.
    :raises Exception: any other import or remote error.
    :returns: the discovered items, and a mapping of each item's identifier
        (return value of `id_extractor`) to the celery queue it was discovered on
        (`None` for local scheduling).
    """
    if worker_options is None:
        kwargs = dict()
    else:
        kwargs = dict(worker_options)

    # Discovery: position arguments
    if modules:
        kwargs["args"] = modules

    # Discovery: named arguments
    kwargs["kwargs"] = discover_kwargs

    timeout = settings.ewoks_discovery.timeout
    if settings.ewoks_scheduling.type == EwoksSchedulingType.Local:
        items = _discover_locally(discover, kwargs, timeout=timeout)
        return items, {id_extractor(item): None for item in items}
    else:
        return _discover_in_all_queues(discover, kwargs, id_extractor, timeout=timeout)


def _discover_locally(discover, kwargs: dict, timeout: float | None = None) -> list:
    return discover(**kwargs).result(timeout=timeout)


def _discover_in_all_queues(
    discover,
    kwargs: dict,
    id_extractor: Callable[[Any], str],
    timeout: float | None = None,
) -> tuple[list, dict[str, str | None]]:
    futures = [(queue, discover(**kwargs, queue=queue)) for queue in get_queues()]

    # Store items in a dict to avoid duplicates
    item_dict = {}
    identifier_to_queue: dict[str, str | None] = {}
    for queue, future in futures:
        # Ignore failures of a single queue to not prevent discovery on other queues
        new_items = future.result(timeout=timeout)
        exc = future.exception()
        if exc:
            logger.warning(f"Discovery failed on queue {future.queue!r}: {exc}")
            continue
        if new_items is None:
            continue
        for item in new_items:
            identifier = id_extractor(item)
            item_dict[identifier] = item
            identifier_to_queue[identifier] = queue
    return list(item_dict.values()), identifier_to_queue


def _set_default_task_properties(task: dict) -> None:
    if not task.get("icon"):
        task["icon"] = "default.png"
    if not task.get("label"):
        task_identifier = task.get("task_identifier")
        if task_identifier:
            task["label"] = task_identifier.split(".")[-1]
