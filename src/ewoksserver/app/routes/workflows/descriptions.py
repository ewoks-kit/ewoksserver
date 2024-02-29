from typing import Dict, Optional, Iterator

from ...backends import json_backend
import json

_WORKFLOW_KEYWORDS = (
    "id",
    "label",
    "category",
    "keywords",
    "input_schema",
    "ui_schema",
)


def workflow_descriptions(
    root: json_backend.ResourceUrlType, keywords: Optional[Dict] = None
) -> Iterator[Dict]:
    for res in json_backend.resources(root):
        description = res["graph"]
        if not _include_resource(description.get("keywords", dict()), keywords):
            continue
        yield {
            key: value
            for key, value in description.items()
            if key in _WORKFLOW_KEYWORDS
        }


def _include_resource(res_keywords: dict, keywords: Optional[Dict] = None) -> bool:
    if keywords is None:
        return True
    return all(res_keywords.get(key) == value for key, value in keywords.items())


def split_ewoks_properties(workflow):
    allowed_in_graph = ["id"]
    allowed_in_nodes = ["id", "label", "task_type", "task_identifier", "inputs_complete", "task_generator", "default_inputs", "default_error_node"]
    allowed_in_links = ["source", "target", "data_mapping", "on_error", "map_all_data"]

    ewoks_props = {"graph": {}, "nodes": [], "links": []}
    notEwoks_props = {}

    for key, value in workflow.items():
        if key == "graph":
            ewoks_props["graph"] = {k: v for k, v in value.items() if k in allowed_in_graph}
            notEwoks_props["graph"] = {k: v for k, v in value.items() if k not in allowed_in_graph}
        elif key == "nodes":
            for node in value:
                ewoks_node = {k: v for k, v in node.items() if k in allowed_in_nodes}
                properties_node = {k: v for k, v in node.items() if k not in allowed_in_nodes}
                # Add 'id' to notEwoks_props of nodes for mapping purposes
                properties_node["id"] = node.get("id")
                ewoks_props["nodes"].append(ewoks_node)
                if properties_node:
                    notEwoks_props.setdefault("nodes", []).append(properties_node)
        elif key == "links":
            for link in value:
                ewoks_link = {k: v for k, v in link.items() if k in allowed_in_links}
                properties_link = {k: v for k, v in link.items() if k not in allowed_in_links}
                # Add 'source' and 'target' to notEwoks_props of links for mapping purposes
                properties_link["source"] = link.get("source")
                properties_link["target"] = link.get("target")
                ewoks_props["links"].append(ewoks_link)
                if properties_link:
                    notEwoks_props.setdefault("links", []).append(properties_link)
        else:
            notEwoks_props[key] = value

    return ewoks_props, notEwoks_props

