def test_single_workflow(client):
    identifier = "myworkflow"

    response = client.get(f"/workflow/{identifier}")
    assert response.status_code == 404

    workflow1a = {"graph": {"id": identifier}, "nodes": {"id": "task1"}}
    response = client.put(f"/workflow/{identifier}", json=workflow1a)
    data = response.get_json()
    assert response.status_code == 200, data
    assert data == identifier

    response = client.get(f"/workflow/{identifier}")
    data = response.get_json()
    assert response.status_code == 200, data
    assert data == workflow1a

    workflow1b = {"graph": {"id": identifier}, "nodes": {"id": "task2"}}
    response = client.put(f"/workflow/{identifier}", json=workflow1b)
    data = response.get_json()
    assert response.status_code == 200, data
    assert data == identifier

    response = client.get(f"/workflow/{identifier}")
    data = response.get_json()
    assert response.status_code == 200, data
    assert data == workflow1b

    response = client.delete(f"/workflow/{identifier}")
    data = response.get_json()
    assert response.status_code == 200
    assert data == identifier

    response = client.delete(f"/workflow/{identifier}")
    data = response.get_json()
    assert response.status_code == 200
    assert data == identifier

    response = client.get(f"/workflow/{identifier}")
    data = response.get_json()
    assert response.status_code == 404
    assert data == f"workflow '{identifier}' does not exist"


def test_multiple_workflows(client):
    response = client.get("/workflows")
    data = response.get_json()
    assert response.status_code == 200
    assert data == []

    workflow1a = {"graph": {"id": "myworkflow1"}, "nodes": {"id": "task1"}}
    workflow1b = {"graph": {"id": "myworkflow1"}, "nodes": {"id": "task2"}}
    workflow2 = {"graph": {"id": "myworkflow2"}, "nodes": {"id": "task1"}}

    response = client.post("/workflows", json=workflow1a)
    data = response.get_json()
    assert response.status_code == 200, data
    response = client.post("/workflows", json=workflow1b)
    data = response.get_json()
    assert response.status_code == 400, data
    assert data == "Workflow 'myworkflow1' exists. Please change identifier and retry."
    response = client.post("/workflows", json=workflow2)
    data = response.get_json()
    assert response.status_code == 200, data

    response = client.get("/workflows")
    data = response.get_json()
    assert response.status_code == 200
    expected = {"myworkflow1", "myworkflow2"}
    assert set(data) == expected
