def test_single_workflow(rest_client):
    identifier = "myworkflow"

    response = rest_client.get(f"/workflow/{identifier}")
    assert response.status_code == 404

    workflow1a = {"graph": {"id": identifier}, "nodes": [{"id": "task1"}]}
    response = rest_client.post("/workflows", json=workflow1a)
    data = response.get_json()
    assert response.status_code == 200, data
    assert data == workflow1a

    response = rest_client.get(f"/workflow/{identifier}")
    data = response.get_json()
    assert response.status_code == 200, data
    assert data == workflow1a

    workflow1b = {"graph": {"id": identifier}, "nodes": [{"id": "task2"}]}
    response = rest_client.put(f"/workflow/{identifier}", json=workflow1b)
    data = response.get_json()
    assert response.status_code == 200, data
    assert data == workflow1b

    response = rest_client.get(f"/workflow/{identifier}")
    data = response.get_json()
    assert response.status_code == 200, data
    assert data == workflow1b

    response = rest_client.delete(f"/workflow/{identifier}")
    data = response.get_json()
    assert response.status_code == 200
    assert data == {"identifier": identifier}

    response = rest_client.delete(f"/workflow/{identifier}")
    data = response.get_json()
    assert response.status_code == 404
    assert data["message"] == f"Workflow '{identifier}' is not found."

    response = rest_client.get(f"/workflow/{identifier}")
    data = response.get_json()
    assert response.status_code == 404
    assert data["message"] == f"Workflow '{identifier}' is not found."


def test_multiple_workflows(rest_client, default_workflow_identifiers):
    response = rest_client.get("/workflows")
    data = response.get_json()
    assert response.status_code == 200
    assert data == {"identifiers": list(default_workflow_identifiers)}

    workflow1a = {"graph": {"id": "myworkflow1"}, "nodes": [{"id": "task1"}]}
    workflow1b = {"graph": {"id": "myworkflow1"}, "nodes": [{"id": "task2"}]}
    workflow2 = {"graph": {"id": "myworkflow2"}, "nodes": [{"id": "task1"}]}

    response = rest_client.post("/workflows", json=workflow1a)
    data = response.get_json()
    assert response.status_code == 200, data

    response = rest_client.post("/workflows", json=workflow1b)
    data = response.get_json()
    assert response.status_code == 409, data
    assert data["message"] == "Workflow 'myworkflow1' already exists."
    response = rest_client.post("/workflows", json=workflow2)
    data = response.get_json()
    assert response.status_code == 200, data

    response = rest_client.get("/workflows")
    data = response.get_json()
    assert response.status_code == 200
    expected = set(default_workflow_identifiers) | {"myworkflow1", "myworkflow2"}
    assert set(data["identifiers"]) == expected


def test_workflow_descriptions(rest_client, default_workflow_identifiers):
    response = rest_client.get("/workflows/descriptions")
    data = response.get_json()
    assert response.status_code == 200
    default_descriptions = [
        desc for desc in data["items"] if desc["id"] in default_workflow_identifiers
    ]
    assert data == {"items": default_descriptions}

    workflow1 = {
        "graph": {"id": "myworkflow1", "label": "label1", "category": "cat1"},
        "nodes": [{"id": "task1"}],
    }
    workflow2 = {"graph": {"id": "myworkflow2"}, "nodes": [{"id": "task1"}]}
    response = rest_client.post("/workflows", json=workflow1)
    data = response.get_json()
    assert response.status_code == 200, data
    response = rest_client.post("/workflows", json=workflow2)
    data = response.get_json()
    assert response.status_code == 200, data

    response = rest_client.get("/workflows/descriptions")
    data = response.get_json()["items"]
    assert response.status_code == 200
    expected = default_descriptions + [
        {"id": "myworkflow1", "label": "label1", "category": "cat1"},
        {"id": "myworkflow2"},
    ]
    data = sorted(data, key=lambda x: x["id"])
    assert data == expected


def test_workflow_description_keys(rest_client, default_workflow_identifiers):
    desc = {
        "id": "myworkflow1",
        "label": "label1",
        "category": "cat1",
        "keywords": {"key": "value"},
        "input_schema": {"dummy": "dummy"},
        "execute_arguments": {"dummy": "dummy"},
        "worker_options": {"dummy": "dummy"},
    }
    workflow1 = {
        "graph": {**desc, "custom1": 1, "custom2": {}},
        "nodes": [{"id": "task1"}],
    }
    response = rest_client.post("/workflows", json=workflow1)
    data = response.get_json()
    assert response.status_code == 200, data

    response = rest_client.get(
        "/workflows/descriptions", json={"keywords": {"key": "value"}}
    )
    data = response.get_json()["items"]
    assert data == [desc], data


def test_workflow_keywords(rest_client, default_workflow_identifiers):
    for key1 in ("A", "B"):
        for key2 in ("1", "2"):
            workflow1 = {
                "graph": {
                    "id": f"myworkflow{key1}{key2}",
                    "label": "label1",
                    "category": "cat1",
                    "keywords": {"key1": key1, "key2": key2},
                },
                "nodes": [{"id": "task1"}],
            }
            response = rest_client.post("/workflows", json=workflow1)
            data = response.get_json()
            assert response.status_code == 200, data

    response = rest_client.get("/workflows")
    data = response.get_json()["identifiers"]
    assert response.status_code == 200
    expected = set(default_workflow_identifiers) | {
        "myworkflowA1",
        "myworkflowA2",
        "myworkflowB1",
        "myworkflowB2",
    }
    assert set(data) == expected

    response = rest_client.get("/workflows", json={"keywords": {"key1": "A"}})
    data = response.get_json()["identifiers"]
    assert response.status_code == 200
    expected = {"myworkflowA1", "myworkflowA2"}
    assert set(data) == expected

    response = rest_client.get(
        "/workflows", json={"keywords": {"key1": "A", "key2": "1"}}
    )
    data = response.get_json()["identifiers"]
    assert response.status_code == 200
    expected = {"myworkflowA1"}
    assert set(data) == expected

    response = rest_client.get("/workflows/descriptions")
    data = [res["id"] for res in response.get_json()["items"]]
    expected = set(default_workflow_identifiers) | {
        "myworkflowA1",
        "myworkflowA2",
        "myworkflowB1",
        "myworkflowB2",
    }
    assert set(data) == expected

    response = rest_client.get(
        "/workflows/descriptions", json={"keywords": {"key1": "A"}}
    )
    data = [res["id"] for res in response.get_json()["items"]]
    expected = {"myworkflowA1", "myworkflowA2"}
    assert set(data) == expected

    response = rest_client.get(
        "/workflows/descriptions", json={"keywords": {"key1": "A", "key2": "1"}}
    )
    data = [res["id"] for res in response.get_json()["items"]]
    expected = {"myworkflowA1"}
    assert set(data) == expected
