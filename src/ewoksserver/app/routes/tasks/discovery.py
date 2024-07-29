from typing import Optional, Dict, List
from ewoksjob.client import discover_all_tasks
from ewoksjob.client.local import discover_all_tasks as discover_all_tasks_local
from ewoksjob.client import discover_tasks_from_modules, get_workers
from ewoksjob.client.local import (
    discover_tasks_from_modules as discover_tasks_from_modules_local,
)

from ...config import EwoksSettings


def discover_tasks(
    settings: EwoksSettings,
    modules: Optional[List[str]] = None,
    reload: Optional[bool] = None,
    worker_options: Optional[Dict] = None,
) -> List[Dict[str, str]]:
    if worker_options is None:
        kwargs = dict()
    else:
        kwargs = dict(worker_options)

    # Task discovery: position arguments
    if modules:
        kwargs["args"] = modules
    # Task discovery: named arguments
    kwargs["kwargs"] = dict()
    if reload is not None:
        kwargs["kwargs"]["reload"] = reload

    timeout = settings.discover_timeout
    if settings.celery is None:
        if modules:
            future = discover_tasks_from_modules_local(**kwargs)
        else:
            future = discover_all_tasks_local(**kwargs)
        tasks = future.result(timeout=timeout)
    else:
        tasks = _discover_tasks_in_all_queues(kwargs, timeout=timeout)

    for task in tasks:
        _set_default_task_properties(task)
    return tasks


def _discover_tasks_in_all_queues(
    kwargs: Dict, timeout: Optional[float] = None
) -> List[Dict[str, str]]:
    discover_from_modules = "args" in kwargs and bool(kwargs["args"])
    discover = (
        discover_tasks_from_modules if discover_from_modules else discover_all_tasks
    )
    futures = [discover(**kwargs, queue=queue) for queue in get_workers()]

    # Store tasks in a dict to avoid duplicates
    task_dict = {}
    for future in futures:
        new_tasks = future.get(timeout=timeout)
        if new_tasks is None:
            continue
        for task in new_tasks:
            task_dict[task["task_identifier"]] = task
    return list(task_dict.values())


def _set_default_task_properties(task: dict) -> None:
    if not task.get("icon"):
        task["icon"] = "default.png"
    if not task.get("label"):
        task_identifier = task.get("task_identifier")
        if task_identifier:
            task["label"] = task_identifier.split(".")[-1]
