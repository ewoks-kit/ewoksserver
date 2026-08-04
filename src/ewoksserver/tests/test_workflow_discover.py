import json

import pytest
from ewoksjob.client.futures import TimeoutError

from .api_versions import api_version_bounds


@api_version_bounds(min_version="2.1.0")
def test_discover_workflows_from_a_module(rest_client, api_root):
    module_pattern = "ewoksserver.tests._loadtest.*"

    response = rest_client.post(
        f"{api_root}/workflows/discover", json={"modules": [module_pattern]}
    )
    data = response.json()
    assert response.status_code == 200, data
    expected = [
        "ewoksserver.tests._loadtest.graph",
        "ewoksserver.tests._loadtest.subgraph",
    ]
    assert sorted(data["identifiers"]) == sorted(expected)


@api_version_bounds(min_version="2.1.0")
def test_discover_workflow_extension(rest_client, api_root):
    module_pattern = "ewoksserver.tests._loadtest.*"

    response = rest_client.post(
        f"{api_root}/workflows/discover",
        json={"modules": [module_pattern], "workflow_extension": "yaml"},
    )
    data = response.json()
    assert response.status_code == 200, data
    assert data["identifiers"] == []


@api_version_bounds(min_version="2.1.0")
def test_discover_all_workflows(local_patched_ewoks_worker, rest_client, api_root):
    response = rest_client.post(f"{api_root}/workflows/discover")
    data = response.json()
    assert response.status_code == 200, data
    expected = [
        "ewoksserver.tests._loadtest.graph",
        "ewoksserver.tests._loadtest.subgraph",
    ]
    assert set(expected) <= set(data["identifiers"])


@api_version_bounds(min_version="2.1.0")
def test_discover_workflows_in_a_non_existing_module(rest_client, api_root):
    response = rest_client.post(
        f"{api_root}/workflows/discover", json={"modules": ["not_a_module.foo"]}
    )
    data = response.json()
    assert response.status_code == 404, data
    assert "No module named" in data["message"]


@api_version_bounds(min_version="2.1.0")
def test_discover_timeout(celery_discover_timeout_client, api_root):
    rest_client, _ = celery_discover_timeout_client
    with pytest.raises(TimeoutError):
        rest_client.post(f"{api_root}/workflows/discover")


@api_version_bounds(min_version="2.1.0")
def test_cache_on_discovery(rest_client, api_root, tmp_path):
    module_pattern = "ewoksserver.tests._loadtest.*"

    response = rest_client.post(
        f"{api_root}/workflows/discover", json={"modules": [module_pattern]}
    )
    assert response.status_code == 200, response.json()

    # Discovered workflows are shadowed right away.
    assert _workflow_file(tmp_path, "ewoksserver.tests._loadtest.subgraph").exists()
    assert _workflow_file(tmp_path, "ewoksserver.tests._loadtest.graph").exists()

    with open(tmp_path / "remote_workflow_index.json") as f:
        index = json.load(f)
    assert index == {
        "ewoksserver.tests._loadtest.graph": None,
        "ewoksserver.tests._loadtest.subgraph": None,
    }

    response = rest_client.get(f"{api_root}/workflows")
    data = response.json()
    assert "ewoksserver.tests._loadtest.graph" in data["identifiers"]
    assert "ewoksserver.tests._loadtest.subgraph" in data["identifiers"]

    # Standalone workflow (no subgraph reference): content is preserved as-is.
    identifier = "ewoksserver.tests._loadtest.subgraph"
    response = rest_client.get(f"{api_root}/workflow/{identifier}")
    data = response.json()
    assert response.status_code == 200, data
    assert data["graph"]["id"] == identifier
    assert [node["id"] for node in data["nodes"]] == ["subnode1"]

    # Workflow referencing a subgraph: converting flattens it into one graph.
    identifier = "ewoksserver.tests._loadtest.graph"
    response = rest_client.get(f"{api_root}/workflow/{identifier}")
    data = response.json()
    assert response.status_code == 200, data
    assert data["graph"]["id"] == identifier


@api_version_bounds(min_version="2.1.0")
def test_no_cache_on_discovery(rest_client_no_discover_cache, api_root, tmp_path):
    module_pattern = "ewoksserver.tests._loadtest.*"

    response = rest_client_no_discover_cache.post(
        f"{api_root}/workflows/discover", json={"modules": [module_pattern]}
    )
    assert response.status_code == 200, response.json()

    # Discovered workflows are not shadowed right away.
    assert not _workflow_file(tmp_path, "ewoksserver.tests._loadtest.subgraph").exists()
    assert not _workflow_file(tmp_path, "ewoksserver.tests._loadtest.graph").exists()

    with open(tmp_path / "remote_workflow_index.json") as f:
        index = json.load(f)
    assert index == {
        "ewoksserver.tests._loadtest.graph": None,
        "ewoksserver.tests._loadtest.subgraph": None,
    }

    # They are still exposed through the REST API.
    response = rest_client_no_discover_cache.get(f"{api_root}/workflows")
    data = response.json()
    assert "ewoksserver.tests._loadtest.graph" in data["identifiers"]
    assert "ewoksserver.tests._loadtest.subgraph" in data["identifiers"]

    # Standalone workflow (no subgraph reference): content is preserved as-is.
    identifier = "ewoksserver.tests._loadtest.subgraph"
    response = rest_client_no_discover_cache.get(f"{api_root}/workflow/{identifier}")
    data = response.json()
    assert response.status_code == 200, data
    assert data["graph"]["id"] == identifier
    assert [node["id"] for node in data["nodes"]] == ["subnode1"]

    # Workflow referencing a subgraph: converting flattens it into one graph.
    identifier = "ewoksserver.tests._loadtest.graph"
    response = rest_client_no_discover_cache.get(f"{api_root}/workflow/{identifier}")
    data = response.json()
    assert response.status_code == 200, data
    assert data["graph"]["id"] == identifier

    # Loading a workflow converts it on the fly; it still does not persist it.
    assert not _workflow_file(tmp_path, "ewoksserver.tests._loadtest.subgraph").exists()
    assert not _workflow_file(tmp_path, "ewoksserver.tests._loadtest.graph").exists()


@api_version_bounds(min_version="2.1.0")
def test_discover_does_not_override_local_copy(rest_client, api_root, tmp_path):
    identifier = "ewoksserver.tests._loadtest.subgraph"
    custom_workflow = {
        "graph": {"id": identifier, "label": "custom"},
        "nodes": [],
    }
    response = rest_client.post(f"{api_root}/workflows", json=custom_workflow)
    assert response.status_code == 200, response.json()

    response = rest_client.post(
        f"{api_root}/workflows/discover",
        json={"modules": ["ewoksserver.tests._loadtest.*"]},
    )
    assert response.status_code == 200, response.json()

    response = rest_client.get(f"{api_root}/workflow/{identifier}")
    data = response.json()
    assert response.status_code == 200, data
    assert data == custom_workflow

    # The local identifier is not registered as a remote workflow,
    # so it stays a normal, deletable, locally owned workflow.
    with open(tmp_path / "remote_workflow_index.json") as f:
        index = json.load(f)
    assert identifier not in index


@api_version_bounds(min_version="2.1.0")
def test_delete_remote_workflow_is_not_allowed(rest_client, api_root):
    identifier = "ewoksserver.tests._loadtest.subgraph"
    response = rest_client.post(
        f"{api_root}/workflows/discover",
        json={"modules": ["ewoksserver.tests._loadtest.*"]},
    )
    assert response.status_code == 200, response.json()

    response = rest_client.delete(f"{api_root}/workflow/{identifier}")
    data = response.json()
    assert response.status_code == 403, data
    assert data["identifier"] == identifier

    response = rest_client.get(f"{api_root}/workflow/{identifier}")
    assert response.status_code == 200


@api_version_bounds(min_version="2.1.0")
def test_delete_remote_workflow_after_edit_is_allowed(
    rest_client_no_discover_cache, api_root, tmp_path
):
    identifier = "ewoksserver.tests._loadtest.subgraph"
    response = rest_client_no_discover_cache.post(
        f"{api_root}/workflows/discover",
        json={"modules": ["ewoksserver.tests._loadtest.*"]},
    )
    assert response.status_code == 200, response.json()
    assert not _workflow_file(tmp_path, identifier).exists()

    edited_workflow = {"graph": {"id": identifier, "label": "edited"}, "nodes": []}
    response = rest_client_no_discover_cache.put(
        f"{api_root}/workflow/{identifier}", json=edited_workflow
    )
    assert response.status_code == 200, response.json()

    # The first edit creates the local shadow.
    assert _workflow_file(tmp_path, identifier).exists()

    response = rest_client_no_discover_cache.delete(f"{api_root}/workflow/{identifier}")
    data = response.json()
    assert response.status_code == 200, data

    response = rest_client_no_discover_cache.get(f"{api_root}/workflow/{identifier}")
    assert response.status_code == 404


@api_version_bounds(min_version="2.1.0")
def test_edit_remote_workflow_creates_shadow(
    rest_client_no_discover_cache, api_root, tmp_path
):
    identifier = "ewoksserver.tests._loadtest.subgraph"
    response = rest_client_no_discover_cache.post(
        f"{api_root}/workflows/discover",
        json={"modules": ["ewoksserver.tests._loadtest.*"]},
    )
    assert response.status_code == 200, response.json()
    assert not _workflow_file(tmp_path, identifier).exists()

    # Editing creates a local shadow.
    edited_workflow = {"graph": {"id": identifier, "label": "edited"}, "nodes": []}
    response = rest_client_no_discover_cache.put(
        f"{api_root}/workflow/{identifier}", json=edited_workflow
    )
    assert response.status_code == 200, response.json()
    assert _workflow_file(tmp_path, identifier).exists()

    with open(tmp_path / "remote_workflow_index.json") as f:
        index = json.load(f)
    assert identifier not in index

    response = rest_client_no_discover_cache.get(f"{api_root}/workflow/{identifier}")
    assert response.status_code == 200
    assert response.json() == edited_workflow


@api_version_bounds(min_version="2.1.0")
def test_create_workflow_conflicts_with_remote_workflow(rest_client, api_root):
    identifier = "ewoksserver.tests._loadtest.subgraph"
    response = rest_client.post(
        f"{api_root}/workflows/discover",
        json={"modules": ["ewoksserver.tests._loadtest.*"]},
    )
    assert response.status_code == 200, response.json()

    new_workflow = {"graph": {"id": identifier, "label": "new"}, "nodes": []}
    response = rest_client.post(f"{api_root}/workflows", json=new_workflow)
    data = response.json()
    assert response.status_code == 409, data


def _workflow_file(tmp_path, identifier):
    return tmp_path / "workflows" / f"{identifier}.json"
