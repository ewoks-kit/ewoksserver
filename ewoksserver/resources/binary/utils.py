import io
import json
import logging
from pathlib import Path
from typing import Iterable, Union
from flask import Response, send_file, send_from_directory
import os
import io
from PIL import Image
from io import StringIO

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
    print('try to get all svgs at once in an Array?')
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
    print('utils-load resource', _load_icon_url(url, identifier), url, root, identifier)
    return _load_icon_url(url, identifier)


def delete_resource(root: ResourceUrlType, identifier: ResourceIdentifierType) -> None:
    url = _identifier_to_url(root, identifier)
    _delete_url(url)


def _identifier_to_url(root: ResourceUrlType, identifier: ResourceIdentifierType):
    path = root / identifier
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

def _load_icon_url(url: ResourceUrlType, resource: ResourceContentType):
    print('utils: _load_icon_url', url, resource)

    # import base64
    # img_stream = ''
    # with open('icons/up.svg', 'rb') as img_f:
    #     img_stream = img_f.read()
    #     img_stream = base64.b64encode(img_stream).decode()
    #     print(img_stream)
    # # return img_stream
    # return send_file(
    #     img_stream,
    #     mimetype='image/png',
    #     as_attachment=True,
    #     attachment_filename='%s.png' % 'ok')

    # img_path = './icons/up.svg'
    # img = get_encoded_icon(img_path)

    # response_data = {"name": 'value13', "image": img}

    # print(response_data)
    # return response_data
    basedir = os.path.abspath(os.path.dirname(__file__))
    uploads_path = os.path.join(basedir, 'icons')
    
    UPLOAD_FOLDER =r"./icons"
    path=os.path.join(UPLOAD_FOLDER, resource)
    print(path, uploads_path, Path(path).exists())
    try:
        with open(path, "rb") as svg:
            # b = io.BytesIO(f)
            print(svg, type(svg))
            data = io.BytesIO(svg.read())
            # resp = Response(
            #     response=data, mimetype=f"image/svg+xml", status=200
            # )
            # resp.headers.add("Content-Length", data.getbuffer().nbytes)

            # return resp

            return data
            # return send_file(f.read(), mimetype='image/svg+xml')
    except FileNotFoundError:
        _logger.error(f"'{url}' not found")
        raise

    # breakpoint()
    # return rv    

def _delete_url(url: ResourceUrlType) -> ResourceContentType:
    if url.exists():
        _logger.debug("Delete file '%s'", url)
        url.unlink()
