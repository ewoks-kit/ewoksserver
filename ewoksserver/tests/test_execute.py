import time
from ..events import is_running
from ewokscore.tests.examples.graphs import get_graph


def test_execute_serverside_client_handler(serverside_client, sqlite3_ewoks_events):
    """Execute in thread-pool and client-side event handler configuration."""
    graph_name, expected = _upload_graph(serverside_client)
    handlers, reader = sqlite3_ewoks_events
    execinfo = {"handlers": handlers}
    response = serverside_client.post(
        f"/execute/{graph_name}", json={"execinfo": execinfo}
    )
    _assert_response(response, reader, expected)


def test_execute_serverside_server_handler(serverside_client_with_events):
    """Execute in thread-pool and server-side event handler configuration."""
    serverside_client, reader = serverside_client_with_events
    graph_name, expected = _upload_graph(serverside_client)
    response = serverside_client.post(f"/execute/{graph_name}")
    _assert_response(response, reader, expected)


def test_execute_client_handler(remote_client, sqlite3_ewoks_events):
    """Execute with celery and client-side event handler configuration."""
    graph_name, expected = _upload_graph(remote_client)
    handlers, reader = sqlite3_ewoks_events
    execinfo = {"handlers": handlers}
    response = remote_client.post(f"/execute/{graph_name}", json={"execinfo": execinfo})
    _assert_response(response, reader, expected)


def test_execute_server_handler(remote_client_with_events):
    """Execute with celery and server-side event handler configuration."""
    remote_client, reader = remote_client_with_events
    graph_name, expected = _upload_graph(remote_client)
    response = remote_client.post(
        f"/execute/{graph_name}", json={"outputs": [{"all": False}]}
    )
    _assert_response(response, reader, expected)


def test_execute_server_socket_connection(remote_client_with_socket):
    _, remote_sclient = remote_client_with_socket

    assert remote_sclient.is_connected()
    _assert_eventloop_is_running(True)
    remote_sclient.disconnect()
    _assert_eventloop_is_running(False)
    remote_sclient.connect()
    _assert_eventloop_is_running(True)


def test_execute_server_socket(remote_client_with_socket):
    """Execute with celery and server-side event handler configuration.
    Events are returned to the client-side over a websocket.
    """
    remote_client, remote_sclient = remote_client_with_socket
    assert remote_sclient.is_connected()
    _assert_eventloop_is_running(True)

    graph_name, expected = _upload_graph(remote_client)
    response = remote_client.post(
        f"/execute/{graph_name}", json={"outputs": [{"all": False}]}
    )
    assert response.status_code == 200, response.get_json()

    n = 2 * (len(expected) + 2)
    events = _get_events(remote_sclient, n)
    _assert_events(response, events, expected)


def _assert_eventloop_is_running(running, timeout=3):
    t0 = time.time()
    while True:
        if is_running() == running:
            return
        time.sleep(0.1)
        if time.time() - t0 > timeout:
            raise TimeoutError


def _get_events(remote_sclient, nevents, timeout=3):
    t0 = time.time()
    events = list()
    while True:
        new_events = remote_sclient.get_received()
        events.extend(new_events)
        if len(events) == nevents:
            break
        time.sleep(0.1)
        if time.time() - t0 > timeout:
            break

    ewoks_events = list()
    for flask_event in events:
        ewoks_events.extend(flask_event["args"])
    return ewoks_events


def _upload_graph(client):
    graph_name = "acyclic1"
    graph, expected = get_graph(graph_name)
    response = client.put(f"/workflow/{graph_name}", json=graph)
    assert response.status_code == 200, response.get_json()
    return graph_name, expected


def _assert_response(response, reader, expected):
    assert response.status_code == 200, response.get_json()
    events = list(reader.wait_events(timeout=2))
    _assert_events(response, events, expected)


def _assert_events(response, events, expected):
    n = 2 * (len(expected) + 2)
    assert len(events) == n

    job_id = response.get_json()
    for event in events:
        assert event["job_id"] == job_id
        if event["node_id"]:
            assert event["node_id"] in expected
