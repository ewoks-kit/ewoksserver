import pytest
from ewoksweback.app.server import create_app
from ewoksweback.app.server import test_app


@pytest.fixture
def client():
    app = create_app()
    with test_app(app) as client:
        yield client
