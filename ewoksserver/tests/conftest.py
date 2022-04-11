import pytest
from ewoksserver.app.server import create_app
from ewoksserver.app.server import test_app


@pytest.fixture
def client():
    app = create_app()
    with test_app(app) as client:
        yield client
