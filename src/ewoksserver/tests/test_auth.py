from datetime import datetime
from datetime import timedelta
from datetime import timezone

import jwt

from .conftest import AUTH_PASSWORD
from .conftest import AUTH_SECRET
from .conftest import AUTH_USER


def test_auth_disabled_by_default(rest_client):
    assert rest_client.get("/api/workflows").status_code == 200
    response = rest_client.post(
        "/api/token", data={"username": AUTH_USER, "password": AUTH_PASSWORD}
    )
    assert response.status_code == 404


def test_no_token(auth_rest_client):
    response = auth_rest_client.get("/api/workflows")
    assert response.status_code == 401
    assert response.headers["WWW-Authenticate"] == "Bearer"


def test_bad_credentials(auth_rest_client):
    response = auth_rest_client.post(
        "/api/token", data={"username": "bob", "password": "wrong"}
    )
    assert response.status_code == 401


def test_valid_token(auth_rest_client):
    response = auth_rest_client.post(
        "/api/token", data={"username": AUTH_USER, "password": AUTH_PASSWORD}
    )
    assert response.status_code == 200
    token = response.json()["access_token"]

    response = auth_rest_client.get(
        "/api/workflows", headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 200


def test_expired_token(auth_rest_client):
    expired = datetime.now(timezone.utc) - timedelta(minutes=1)
    token = jwt.encode(
        {"sub": AUTH_USER, "exp": expired}, AUTH_SECRET, algorithm="HS256"
    )
    response = auth_rest_client.get(
        "/api/workflows", headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 401


def test_token_wrong_signature(auth_rest_client):
    token = jwt.encode(
        {"sub": AUTH_USER}, "other-secret-with-at-least-32-bytes", algorithm="HS256"
    )
    response = auth_rest_client.get(
        "/api/workflows", headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 401
