import json
import logging
from pathlib import Path
from typing import Any
from typing import Iterator

from ewoksjob.client import convert_graph
from ewoksjob.client.local import convert_graph as convert_graph_local

from ...backends import json_backend
from ...config import EwoksSettings
from ...models import EwoksSchedulingType

logger = logging.getLogger(__name__)


def load_workflow(
    settings: EwoksSettings,
    root: json_backend.ResourceUrlType,
    identifier: str,
    worker_options: dict | None = None,
) -> json_backend.ResourceContentType:
    """Load a local or external workflow.

    :raises FileNotFoundError: no local and external workflow
        for this identifier.
    """
    if json_backend.resource_exists(root, identifier):
        return json_backend.load_resource(root, identifier)

    index = _load_external_workflow_index(settings)
    if identifier not in index:
        raise FileNotFoundError(identifier)

    graph = _load_external_workflow(
        settings, identifier, queue=index[identifier], worker_options=worker_options
    )
    if graph is None:
        raise FileNotFoundError(identifier)
    graph.setdefault("graph", {})["id"] = identifier
    return graph


def save_workflow(
    settings: EwoksSettings,
    root: json_backend.ResourceUrlType,
    identifier: str,
    content: json_backend.ResourceContentType,
) -> None:
    """Save a workflow, copying it locally when it is an
    external workflow. In that case it shadows the external
    workflow.

    :raises PermissionError: no permission to save the workflow.
    """
    index = _load_external_workflow_index(settings)
    if identifier in index:
        del index[identifier]
        _save_external_workflow_index(settings, index)

    json_backend.save_resource(root, identifier, content)


def delete_workflow(root: json_backend.ResourceUrlType, identifier: str) -> None:
    """Delete a local workflow. When it shadows an external workflow
    the external workflow needs to be re-discovered.

    :raises PermissionError: no permission to delete the workflow.
    :raises FileNotFoundError: no local workflow for this identifier.
    """
    json_backend.delete_resource(root, identifier)


def workflow_exists(
    settings: EwoksSettings, root: json_backend.ResourceUrlType, identifier: str
) -> bool:
    """Whether a local or external workflow exists for this identifier.

    :raises ValueError: invalid identifier.
    """
    return json_backend.resource_exists(root, identifier) or is_external_workflow(
        settings, identifier
    )


def workflow_identifiers(
    settings: EwoksSettings, root: json_backend.ResourceUrlType
) -> list[str]:
    """Identifiers of local and external workflows."""
    identifiers = set(json_backend.resource_identifiers(root))
    identifiers.update(_load_external_workflow_index(settings))
    return sorted(identifiers)


def iter_workflow_graphs(
    settings: EwoksSettings,
    root: json_backend.ResourceUrlType,
    worker_options: dict | None = None,
) -> Iterator[dict]:
    """Yield `graph` attributes of local or external workflows."""
    shadowed = set()
    for identifier in json_backend.resource_identifiers(root):
        shadowed.add(identifier)
        yield json_backend.load_resource(root, identifier).get("graph", {})

    index = _load_external_workflow_index(settings)
    for identifier, queue in index.items():
        if identifier in shadowed:
            continue
        graph = _load_external_workflow(
            settings, identifier, queue=queue, worker_options=worker_options
        )
        if graph is None:
            continue
        graph.setdefault("graph", {})["id"] = identifier
        yield graph["graph"]


def register_external_workflows(
    settings: EwoksSettings,
    root: json_backend.ResourceUrlType,
    identifier_to_queue: dict[str, str | None],
    worker_options: dict | None = None,
) -> None:
    """Register discovered external workflows, skipping ones already
    shadowed locally. Persists a shadow right away if `cache_workflows`
    is enabled.
    """
    create_shadow = settings.ewoks_discovery.cache_workflows
    index = _load_external_workflow_index(settings)
    index_changed = False
    for identifier, queue in identifier_to_queue.items():
        if json_backend.resource_exists(root, identifier):
            continue

        if create_shadow:
            graph = _load_external_workflow(
                settings, identifier, queue=queue, worker_options=worker_options
            )
            if graph is None:
                continue
            graph.setdefault("graph", {})["id"] = identifier
            json_backend.save_resource(root, identifier, graph)

        if identifier not in index or index[identifier] != queue:
            index[identifier] = queue
            index_changed = True

    if index_changed:
        _save_external_workflow_index(settings, index)


def is_external_workflow(settings: EwoksSettings, identifier: str) -> bool:
    """Whether a workflow is registered as a external workflow."""
    return identifier in _load_external_workflow_index(settings)


_EXTERNAL_WORKFLOW_INDEX = "external_workflow_index.json"


def _external_workflow_index_path(settings: EwoksSettings) -> Path:
    return settings.resource_directory / _EXTERNAL_WORKFLOW_INDEX


def _load_external_workflow_index(settings: EwoksSettings) -> dict[str, Any]:
    """The external workflow index: identifier -> discovery queue."""
    try:
        with open(_external_workflow_index_path(settings)) as f:
            return json.load(f)
    except FileNotFoundError:
        return {}


def _save_external_workflow_index(
    settings: EwoksSettings, index: dict[str, Any]
) -> None:
    """The external workflow index: identifier -> discovery queue."""
    path = _external_workflow_index_path(settings)
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w") as f:
        json.dump(index, f, indent=2)


def _load_external_workflow(
    settings: EwoksSettings,
    identifier: str,
    queue: str | None = None,
    worker_options: dict | None = None,
) -> dict | None:
    """Load a external workflow identified by its fully qualified
    module identifier, e.g.``"mypackage.subpackage.myworkflow"``.

    :returns: `None` when the workflow could not be loaded.
    """
    package, _, _ = identifier.rpartition(".")
    if not package:
        return None

    if worker_options is None:
        kwargs = dict()
    else:
        kwargs = dict(worker_options)
    kwargs["args"] = (identifier, None)
    kwargs["kwargs"] = {
        "load_options": {"representation": "json_module", "root_module": package}
    }

    timeout = settings.ewoks_discovery.timeout
    try:
        if settings.ewoks_scheduling.type == EwoksSchedulingType.Local:
            future = convert_graph_local(**kwargs)
        else:
            future = convert_graph(**kwargs, queue=queue)
        graph = future.result(timeout=timeout)
    except Exception as ex:
        logger.warning("Failed to load external workflow %r: %s", identifier, ex)
        return None

    if not isinstance(graph, dict):
        return None
    return graph
