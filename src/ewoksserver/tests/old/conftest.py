from collections import namedtuple

import pytest

from ... import oldserver


@pytest.fixture
def rest_client_old(tmpdir):
    """Client to the REST server (no execution)."""
    app, *_ = oldserver.create_app(resource_directory=str(tmpdir))
    with oldserver.run_context(app):
        with app.test_client() as client:
            yield client


@pytest.fixture
def local_exec_client_old(tmpdir, ewoks_handlers):
    """Client to the REST server and Socket.IO (execution with process pool)."""
    ewoks_config = {"handlers": ewoks_handlers}
    app, *_ = oldserver.create_app(resource_directory=str(tmpdir), ewoks=ewoks_config)
    socketio = oldserver.add_socket(app)
    with oldserver.run_context(app):
        with app.test_client() as client:
            sclient = socketio.test_client(app, flask_test_client=client)
            yield client, sclient
            sclient.disconnect()


@pytest.fixture
def celery_exec_client_old(tmpdir, celery_session_worker, ewoks_handlers):
    """Client to the REST server and Socket.IO (execution with celery)."""
    ewoks_config = {"handlers": ewoks_handlers}
    app, *_ = oldserver.create_app(
        resource_directory=str(tmpdir), celery=dict(), ewoks=ewoks_config
    )
    socketio = oldserver.add_socket(app)
    with oldserver.run_context(app):
        with app.test_client() as client:
            sclient = socketio.test_client(app, flask_test_client=client)
            yield client, sclient
            sclient.disconnect()


@pytest.fixture
def mocked_local_submit_old(mocker) -> str:
    submit_local_mock = mocker.patch(
        "ewoksserver.resources.json.workflows.submit_local"
    )

    MockFuture = namedtuple("Future", ["task_id"])

    arguments = dict()
    task_id = 0

    def mocked_submit(*args, **kwargs):
        nonlocal task_id
        arguments["args"] = args
        arguments["kwargs"] = kwargs
        task_id += 1
        return MockFuture(task_id=task_id)

    submit_local_mock.side_effect = mocked_submit
    return arguments
