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
