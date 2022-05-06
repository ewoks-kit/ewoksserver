def test_single_workflow(serverside_client):
    identifier = "myworkflow"

    response = serverside_client.get(f"/workflow/{identifier}")
    assert response.status_code == 404

    workflow1a = {"graph": {"id": identifier}, "nodes": [{"id": "task1"}]}
    response = serverside_client.post("/workflows", json=workflow1a)
    data = response.get_json()
    assert response.status_code == 200, data
    assert data == workflow1a

    response = serverside_client.get(f"/workflow/{identifier}")
    data = response.get_json()
    assert response.status_code == 200, data
    assert data == workflow1a

    workflow1b = {"graph": {"id": identifier}, "nodes": [{"id": "task2"}]}
    response = serverside_client.put(f"/workflow/{identifier}", json=workflow1b)
    data = response.get_json()
    assert response.status_code == 200, data
    assert data == workflow1b

    response = serverside_client.get(f"/workflow/{identifier}")
    data = response.get_json()
    assert response.status_code == 200, data
    assert data == workflow1b

    response = serverside_client.delete(f"/workflow/{identifier}")
    data = response.get_json()
    assert response.status_code == 200
    assert data == {"identifier": identifier}

    response = serverside_client.delete(f"/workflow/{identifier}")
    data = response.get_json()
    assert response.status_code == 200
    assert data == {"identifier": identifier}

    response = serverside_client.get(f"/workflow/{identifier}")
    data = response.get_json()
    assert response.status_code == 404
    assert data["message"] == f"Workflow '{identifier}' is not found."


def test_multiple_workflows(serverside_client):
    response = serverside_client.get("/workflows")
    data = response.get_json()
    assert response.status_code == 200
    assert data == {"identifiers": []}

    workflow1a = {"graph": {"id": "myworkflow1"}, "nodes": [{"id": "task1"}]}
    workflow1b = {"graph": {"id": "myworkflow1"}, "nodes": [{"id": "task2"}]}
    workflow2 = {"graph": {"id": "myworkflow2"}, "nodes": [{"id": "task1"}]}

    response = serverside_client.post("/workflows", json=workflow1a)
    data = response.get_json()
    assert response.status_code == 200, data

    response = serverside_client.post("/workflows", json=workflow1b)
    data = response.get_json()
    assert response.status_code == 409, data
    assert data["message"] == "Workflow 'myworkflow1' already exists."
    response = serverside_client.post("/workflows", json=workflow2)
    data = response.get_json()
    assert response.status_code == 200, data

    response = serverside_client.get("/workflows")
    data = response.get_json()
    assert response.status_code == 200
    expected = {"myworkflow1", "myworkflow2"}
    assert set(data["identifiers"]) == expected
