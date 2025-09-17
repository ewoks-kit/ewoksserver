from importlib.metadata import version
from packaging.version import Version

from fastapi import status

HTTP_400_BAD_REQUEST = status.HTTP_400_BAD_REQUEST
HTTP_403_FORBIDDEN = status.HTTP_403_FORBIDDEN
HTTP_404_NOT_FOUND = status.HTTP_404_NOT_FOUND
HTTP_409_CONFLICT = status.HTTP_409_CONFLICT
HTTP_503_SERVICE_UNAVAILABLE = status.HTTP_503_SERVICE_UNAVAILABLE

if Version(version("starlette")) >= Version("0.48.0"):
    # HTTP/1.1 protocol semantics RFC 9110
    HTTP_422_UNPROCESSABLE_CONTENT = status.HTTP_422_UNPROCESSABLE_CONTENT
else:
    # HTTP/1.1 protocol semantics RFC 7231
    HTTP_422_UNPROCESSABLE_CONTENT = status.HTTP_422_UNPROCESSABLE_ENTITY
