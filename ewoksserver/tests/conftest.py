import pytest
from ewoksserver.server import create_app
from ewoksserver.server import run_context
from ewoksserver.server import add_socket
from ewoksjob.client.process import pool_context
from ewoksjob.tests.conftest import celery_config  # noqa F401
from ewoksjob.tests.conftest import celery_includes  # noqa F401
from ewoksjob.tests.conftest import sqlite3_ewoks_events  # noqa F401

from .data import resource_filenames
from ..resources.binary.utils import _load_url


@pytest.fixture
def serverside_client(tmpdir):
    """Client runs in the same process as the server."""
    app, *_ = create_app(resource_directory=str(tmpdir))
    with run_context(app):
        with pool_context():
            with app.test_client() as client:
                yield client


@pytest.fixture
def serverside_client_with_events(tmpdir, sqlite3_ewoks_events):  # noqa F811
    """Client runs in the same process as the server.
    Server is configured to handle ewoks events.
    """
    handlers, reader = sqlite3_ewoks_events
    ewoks_config = {"handlers": handlers}
    app, *_ = create_app(resource_directory=str(tmpdir), ewoks=ewoks_config)
    with run_context(app):
        with pool_context():
            with app.test_client() as client:
                yield client, reader


@pytest.fixture
def remote_client(tmpdir, celery_session_worker):
    """Client does not run in the same process as the server."""
    app, *_ = create_app(resource_directory=str(tmpdir), celery=dict())
    with run_context(app):
        with app.test_client() as client:
            yield client


@pytest.fixture
def remote_client_with_events(
    tmpdir, celery_session_worker, sqlite3_ewoks_events  # noqa F811
):
    """Client does not run in the same process as the server.
    Server is configured to handle ewoks events.
    """
    handlers, reader = sqlite3_ewoks_events
    ewoks_config = {"handlers": handlers}
    app, *_ = create_app(
        resource_directory=str(tmpdir), celery=dict(), ewoks=ewoks_config
    )
    with run_context(app):
        with app.test_client() as client:
            yield client, reader


@pytest.fixture
def remote_client_with_socket(
    tmpdir, celery_session_worker, sqlite3_ewoks_events  # noqa F811
):
    """Client does not run in the same process as the server.
    Server is configured to handle ewoks events.
    """
    handlers, _ = sqlite3_ewoks_events
    ewoks_config = {"handlers": handlers}
    app, *_ = create_app(
        resource_directory=str(tmpdir), celery=dict(), ewoks=ewoks_config
    )
    socketio = add_socket(app)
    with run_context(app):
        with app.test_client() as client:
            sclient = socketio.test_client(app, flask_test_client=client)
            yield client, sclient
            sclient.disconnect()


@pytest.fixture
def png_icons():
    filenames = resource_filenames()
    return [_load_url(filename) for filename in filenames if filename.endswith(".png")]


@pytest.fixture
def svg_icons():
    filenames = resource_filenames()
    return [_load_url(filename) for filename in filenames if filename.endswith(".svg")]
