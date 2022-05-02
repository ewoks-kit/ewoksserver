def test_single_task(serverside_client):
    identifier = "myproject.tasks.Dummy"

    response = serverside_client.get(f"/task/{identifier}")
    assert response.status_code == 404

    task1a = {"task_identifier": identifier, "task_type": "class", "input_names": ["a"]}
    response = serverside_client.put(f"/task/{identifier}", json=task1a)
    data = response.get_json()
    assert response.status_code == 200, data
    assert data == identifier

    response = serverside_client.get(f"/task/{identifier}")
    data = response.get_json()
    assert response.status_code == 200, data
    assert data == task1a

    task1b = {
        "task_identifier": identifier,
        "task_type": "class",
        "input_names": ["a", "b"],
    }
    response = serverside_client.put(f"/task/{identifier}", json=task1b)
    data = response.get_json()
    assert response.status_code == 200, data
    assert data == identifier

    response = serverside_client.get(f"/task/{identifier}")
    data = response.get_json()
    assert response.status_code == 200, data
    assert data == task1b

    response = serverside_client.delete(f"/task/{identifier}")
    data = response.get_json()
    assert response.status_code == 200
    assert data == identifier

    response = serverside_client.delete(f"/task/{identifier}")
    data = response.get_json()
    assert response.status_code == 200
    assert data == identifier

    response = serverside_client.get(f"/task/{identifier}")
    data = response.get_json()
    assert response.status_code == 404
    assert data == f"task '{identifier}' does not exist"


def test_multiple_tasks(serverside_client):
    response = serverside_client.get("/tasks")
    data = response.get_json()
    assert response.status_code == 200
    assert data == []

    task1a = {
        "task_identifier": "myproject.tasks.Dummy1",
        "task_type": "class",
        "input_names": ["a"],
    }
    task1b = {
        "task_identifier": "myproject.tasks.Dummy1",
        "task_type": "class",
        "input_names": ["a", "b"],
    }
    task2 = {
        "task_identifier": "myproject.tasks.Dummy2",
        "task_type": "class",
        "input_names": ["a", "b"],
    }

    response = serverside_client.post("/tasks", json=task1a)
    data = response.get_json()
    assert response.status_code == 200, data
    response = serverside_client.post("/tasks", json=task1b)
    data = response.get_json()
    assert response.status_code == 403, data
    assert (
        data
        == "Task 'myproject.tasks.Dummy1' exists. Please change identifier and retry."
    )
    response = serverside_client.post("/tasks", json=task2)
    data = response.get_json()
    assert response.status_code == 200, data

    response = serverside_client.get("/tasks")
    data = response.get_json()
    assert response.status_code == 200, data
    expected = {"myproject.tasks.Dummy1", "myproject.tasks.Dummy2"}
    assert set(data) == expected


def test_discover_tasks(serverside_client):
    response = serverside_client.get("/tasks")
    data = response.get_json()
    assert response.status_code == 200
    assert data == []

    module = "ewoksserver.tests.dummy_tasks"

    response = serverside_client.post("/tasks/discover", json={"module": module})
    data = response.get_json()
    assert response.status_code == 200, data

    response = serverside_client.get("/tasks")
    identifiers = response.get_json()
    assert response.status_code == 200
    assert identifiers
    assert all(identifier.startswith(module) for identifier in identifiers)

    response = serverside_client.post("/tasks/discover", json={"module": module})
    data = response.get_json()
    assert response.status_code == 403, data
    assert "Please change identifier and retry." in data


def test_task_descriptions(serverside_client):
    response = serverside_client.get("/tasks/descriptions")
    data = response.get_json()
    assert response.status_code == 200
    assert data == []

    module = "ewoksserver.tests.dummy_tasks"

    response = serverside_client.post("/tasks/discover", json={"module": module})
    data1 = response.get_json()
    assert response.status_code == 200, data1

    response = serverside_client.get("/tasks/descriptions")
    data2 = response.get_json()
    data2 = {
        r["task_identifier"] for r in data2 if r["task_identifier"].startswith(module)
    }
    assert response.status_code == 200
    assert set(data1) == data2
