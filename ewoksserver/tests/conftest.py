import pytest
from ewoksserver.app.server import create_app
from ewoksserver.app.server import run_context


@pytest.fixture
def client(tmpdir):
    app = create_app(resource_directory=str(tmpdir))
    with run_context(app):
        with app.test_client() as client:
            yield client
