import json
import logging
from pathlib import Path
from typing import Iterable, Union


ResourceIdentifierType = str
ResourceUrlType = Path
ResourceContentType = dict

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


def save_resource(
    root: ResourceUrlType,
    identifier: ResourceIdentifierType,
    resource: ResourceContentType,
):
    url = _identifier_to_url(root, identifier)
    _save_url(url, resource)


def load_resource(
    root: ResourceUrlType, identifier: ResourceIdentifierType
) -> ResourceContentType:
    url = _identifier_to_url(root, identifier)
    return _load_url(url)


def delete_resource(root: ResourceUrlType, identifier: ResourceIdentifierType) -> None:
    url = _identifier_to_url(root, identifier)
    _delete_url(url)


def _identifier_to_url(root: ResourceUrlType, identifier: ResourceIdentifierType):
    return root / (identifier + ".json")


def _url_to_identifier(url: ResourceUrlType) -> ResourceIdentifierType:
    return url.stem


def _save_url(url: ResourceUrlType, resource: ResourceContentType):
    _logger.debug("Save file '%s'", url)
    url.parent.mkdir(parents=True, exist_ok=True)
    with open(url, "w") as f:
        json.dump(resource, f, indent=2)


def _load_url(url: ResourceUrlType) -> ResourceContentType:
    try:
        with open(url, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        _logger.error(f"'{url}' not found")
        raise


def _delete_url(url: ResourceUrlType) -> ResourceContentType:
    if url.exists():
        _logger.debug("Delete file '%s'", url)
        url.unlink()
