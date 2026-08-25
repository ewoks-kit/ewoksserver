from typing import Iterator

from ...backends import json_backend
from ...config import EwoksSettings
from . import backend

_WORKFLOW_KEYWORDS = (
    "id",
    "label",
    "category",
    "keywords",
    "input_schema",
    "ui_schema",
)


def workflow_descriptions(
    settings: EwoksSettings,
    root: json_backend.ResourceUrlType,
    keywords: dict | None = None,
) -> Iterator[dict]:
    for description in backend.iter_workflow_graphs(settings, root):
        if not _include_resource(description.get("keywords", dict()), keywords):
            continue
        yield {
            key: value
            for key, value in description.items()
            if key in _WORKFLOW_KEYWORDS
        }


def _include_resource(res_keywords: dict, keywords: dict | None = None) -> bool:
    if keywords is None:
        return True
    return all(res_keywords.get(key) == value for key, value in keywords.items())
