import logging
from datetime import datetime
from datetime import timedelta
from datetime import timezone
from typing import Annotated

import jwt
from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException
from fastapi import status
from fastapi.security import OAuth2PasswordBearer
from fastapi.security import OAuth2PasswordRequestForm
from pwdlib import PasswordHash
from pydantic import BaseModel

from .config import EwoksSettingsType
from .models import EwoksAuthSettings
from .routes import BACKEND_PREFIX

logger = logging.getLogger(__name__)

_password_hash = PasswordHash.recommended()

_DUMMY_HASH = _password_hash.hash("dummy")

ANONYMOUS = "anonymous"

# auto_error=False so that disabled authentication does not require a token
oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl=f"{BACKEND_PREFIX}/token", auto_error=False
)


class Token(BaseModel):
    access_token: str
    token_type: str


class User(BaseModel):
    username: str


class UnauthorizedHTTPException(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )


def _authenticate_user(auth: EwoksAuthSettings, username: str, password: str) -> bool:
    hashed = auth.users.get(username)
    if hashed is None:
        # Do a dummy check to protect against user enumeration through timing.
        _password_hash.verify(password, _DUMMY_HASH)
        return False
    return _password_hash.verify(password, hashed)


def _create_access_token(auth: EwoksAuthSettings, username: str) -> str:
    expire = datetime.now(timezone.utc) + timedelta(minutes=auth.token_expire_minutes)
    return jwt.encode(
        {"sub": username, "exp": expire}, auth.secret_key, algorithm=auth.algorithm
    )


def get_current_user(
    settings: EwoksSettingsType,
    token: Annotated[str | None, Depends(oauth2_scheme)],
) -> User:
    auth = settings.ewoks_auth
    if not auth.enabled:
        return User(username=ANONYMOUS)

    if token is None:
        raise UnauthorizedHTTPException()
    try:
        payload = jwt.decode(token, auth.secret_key, algorithms=[auth.algorithm])
    except jwt.InvalidTokenError:
        raise UnauthorizedHTTPException()
    username = payload.get("sub")
    if username not in auth.users:
        raise UnauthorizedHTTPException()
    return User(username=username)


auth_router = APIRouter(tags=["authentication"])


@auth_router.post("/token", summary="Get an access token", response_model=Token)
def login(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    settings: EwoksSettingsType,
) -> Token:
    auth = settings.ewoks_auth
    if not auth.enabled:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Authentication is not enabled",
        )
    if not _authenticate_user(auth, form_data.username, form_data.password):
        raise UnauthorizedHTTPException()
    return Token(
        access_token=_create_access_token(auth, form_data.username),
        token_type="bearer",  # noqa: S106 - Ruff thinks this is a password while it is not.
    )
