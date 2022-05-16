import json
import logging
from pathlib import Path
from typing import Iterable, Union
from flask import send_file, send_from_directory
import os


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
    print(url, root, identifier)
    if str(root) == 'icons':
        return _load_icon_url(url, identifier)
    else:
        return _load_url(url)
    


def delete_resource(root: ResourceUrlType, identifier: ResourceIdentifierType) -> None:
    url = _identifier_to_url(root, identifier)
    _delete_url(url)


def _identifier_to_url(root: ResourceUrlType, identifier: ResourceIdentifierType):
    # path = root / identifier  else root / (identifier + ".json")
    path = ''
    if str(root) == 'icons':
        path = root / identifier
    else:
        path = root / (identifier + ".json")
    print(root, path, type(root), type(path))
    
    return path

def _url_to_identifier(url: ResourceUrlType) -> ResourceIdentifierType:
    return url.stem


def _save_url(url: ResourceUrlType, resource: ResourceContentType):
    _logger.debug("Save file '%s'", url)
    url.parent.mkdir(parents=True, exist_ok=True)
    with open(url, "w") as f:
        json.dump(resource, f, indent=2)


def _load_url(url: ResourceUrlType) -> ResourceContentType:
    print(url)
    try:
        with open(url, "r") as f:
            print(url, f)
            return json.load(f)
    except FileNotFoundError:
        _logger.error(f"'{url}' not found")
        raise

def _load_icon_url(url: ResourceUrlType, resource: ResourceContentType) -> ResourceContentType:
    # if os.path.isfile(url):
    #     return send_file(url)
    # else:
    #     print('error in finding file')
    # from pathlib import Path
    # root = Path('.')
    # folder_path = root / 'icons'
    # print(root, folder_path, resource)
    # # return send_from_directory('~/code/ewoksserver/tasks', resource)
    # if os.path.exists(folder_path):
    #     print("exists", folder_path)
    #     return send_from_directory(folder_path, 'up.svg')
    try:
        with open(url, "rb") as f:
            print(url, resource, f)
            # send_from_directory('icons', 'up.svg')
            send_file(f, mimetype='image/svg')
            return send_file(f, mimetype='image/svg')
        # with open(url, "rb") as f:
        #     print("_load_icon_url", url, f, resource)
        #     return send_from_directory('icons', 'up.svg')
            # return send_file(f, mimetype='image')
    except FileNotFoundError:
        _logger.error(f"'{url}' not found")
        raise


def _delete_url(url: ResourceUrlType) -> ResourceContentType:
    if url.exists():
        _logger.debug("Delete file '%s'", url)
        url.unlink()
