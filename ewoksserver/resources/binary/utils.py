import io
import json
import logging
from pathlib import Path
from typing import Iterable, Union
from flask import Response, send_file, send_from_directory
import os
import io

ResourceIdentifierType = str
ResourceUrlType = Path
ResourceContentType = bin

_logger = logging.getLogger(__name__)


def root_url(root_url: Union[str, Path, None], category: str) -> ResourceUrlType:
    if not root_url:
        root_url = Path(".")
    elif isinstance(root_url, str):
        root_url = Path(root_url)
    return root_url / category


def resource_identifiers(root: ResourceUrlType) -> Iterable[ResourceIdentifierType]:
    if not root.exists():
        return
    for child in root.iterdir():
        if child.is_file() and not child.name.startswith("."):
            yield _url_to_identifier(child)


def resources(root: ResourceUrlType) -> Iterable[ResourceContentType]:
    if not root.exists():
        return
    for child in root.iterdir():
        if child.is_file() and not child.name.startswith("."):
            yield _load_url(child)


def resource_exists(root: ResourceUrlType, identifier: ResourceIdentifierType) -> bool:
    return _identifier_to_url(root, identifier).exists()


def load_resource(
    root: ResourceUrlType, identifier: ResourceIdentifierType
) -> ResourceContentType:
    url = _identifier_to_url(root, identifier)
    return _load_icon_url(url, identifier)


def delete_resource(root: ResourceUrlType, identifier: ResourceIdentifierType) -> None:
    url = _identifier_to_url(root, identifier)
    _delete_url(url)


def _identifier_to_url(root: ResourceUrlType, identifier: ResourceIdentifierType):
    path = root / identifier
    return path


def _url_to_identifier(url: ResourceUrlType) -> ResourceIdentifierType:
    return url.name
    # .stem


def _load_url(url: ResourceUrlType) -> ResourceContentType:
    try:
        with open(url, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        _logger.error(f"'{url}' not found")
        raise


def _load_icon_url(url: ResourceUrlType, resource: ResourceContentType):
    basedir = os.path.abspath(os.path.dirname(__file__))
    uploads_path = os.path.join(basedir, 'icons')
    
    UPLOAD_FOLDER =r"./icons"
    path=os.path.join(UPLOAD_FOLDER, resource)

    try:
        with open(path, "rb") as svg:
            data = io.BytesIO(svg.read())
            return data
    except FileNotFoundError:
        _logger.error(f"'{url}' not found")
        raise   


def _delete_url(url: ResourceUrlType) -> ResourceContentType:
    if url.exists():
        _logger.debug("Delete file '%s'", url)
        url.unlink()
