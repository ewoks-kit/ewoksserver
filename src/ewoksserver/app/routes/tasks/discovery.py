from typing import Optional, Dict, List
from ewoksjob.client import discover_all_tasks
from ewoksjob.client.local import discover_all_tasks as discover_all_tasks_local
from ewoksjob.client import discover_tasks_from_modules
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

    discover_kwargs = dict()
    if modules:
        kwargs["args"] = modules
    if reload is not None:
        discover_kwargs["reload"] = reload
    kwargs["kwargs"] = discover_kwargs

    if settings.celery is None:
        if modules:
            future = discover_tasks_from_modules_local(**kwargs)
        else:
            future = discover_all_tasks_local(**kwargs)
        tasks = future.result()
    else:
        if modules:
            future = discover_tasks_from_modules(**kwargs)
        else:
            future = discover_all_tasks(**kwargs)
        tasks = future.get()

    for task in tasks:
        _default_task_properties(task)
    return tasks


def _default_task_properties(task: dict) -> None:
    if not task.get("icon"):
        task["icon"] = "default.png"
    if not task.get("label"):
        task_identifier = task.get("task_identifier")
        if task_identifier:
            task["label"] = task_identifier.split(".")[-1]
