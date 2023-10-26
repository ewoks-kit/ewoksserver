def test_default_workflows(rest_client_old, default_workflow_identifiers):
    for identifier in default_workflow_identifiers:
        response = rest_client_old.get(f"/workflow/{identifier}")
        data = response.get_json()
        assert response.status_code == 200, data


def test_default_icons(rest_client_old, default_icon_identifiers):
    for identifier in default_icon_identifiers:
        response = rest_client_old.get(f"/icon/{identifier}")
        data = response.get_json()
        assert response.status_code == 200, data


def test_default_tasks(rest_client_old, default_task_identifiers):
    for identifier in default_task_identifiers:
        response = rest_client_old.get(f"/task/{identifier}")
        data = response.get_json()
        assert response.status_code == 200, data
