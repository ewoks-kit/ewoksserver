from pathlib import Path
from typing import Dict, Optional, Iterator

from ...backends import json_backend

_WORKFLOW_KEYWORDS = (
    "id",
    "label",
    "category",
    "keywords",
    "input_schema",
    "ui_schema",
)

_ALLOWED_IN_GRAPH = ("id", "label", "schema_version", "input_nodes", "output_nodes")
_ALLOWED_IN_NODES = (
    "id",
    "label",
    "task_type",
    "task_identifier",
    "inputs_complete",
    "task_generator",
    "default_inputs",
    "default_error_node",
    "conditions_else_value",
    "default_error_attributes",
)
_ALLOWED_IN_LINKS = (
    "source",
    "sub_source",
    "target",
    "sub_target",
    "sub_target_attributes",
    "data_mapping",
    "on_error",
    "map_all_data",
    "conditions",
    "required",
)


def workflow_descriptions(
    root: json_backend.ResourceUrlType, keywords: Optional[Dict] = None
) -> Iterator[Dict]:
    root_path = Path(root)
    for res in json_backend.resources(root):
        if res["graph"].get("id", None):  # general validation issue to be abstacted
            workflow_props = get_not_ewoks_props(
                root_path, res["graph"].get("id", None)
            )
            if workflow_props:
                description = merge_workflow_props(res, workflow_props)["graph"]
            else:
                description = res["graph"]

            if not _include_resource(description.get("keywords", dict()), keywords):
                continue

            yield {
                key: value
                for key, value in description.items()
                if key in _WORKFLOW_KEYWORDS
            }


def get_not_ewoks_props(root_path: Path, workflow_id: str):
    exists = json_backend.resource_exists(root_path / "notewoksprops", workflow_id)
    if exists:
        workflow_props = json_backend.load_resource(
            root_path / "notewoksprops", workflow_id
        )
        return workflow_props
    return None


def _include_resource(res_keywords: dict, keywords: Optional[Dict] = None) -> bool:
    if keywords is None:
        return True
    return all(res_keywords.get(key) == value for key, value in keywords.items())


def split_ewoks_properties(workflow):
    ewoks_props = {"graph": {}, "nodes": [], "links": []}
    not_ewoks_props = {}

    for key, value in workflow.items():
        if key == "graph":
            ewoks_props["graph"] = {
                k: v for k, v in value.items() if k in _ALLOWED_IN_GRAPH
            }
            not_ewoks_props["graph"] = {
                k: v for k, v in value.items() if k not in _ALLOWED_IN_GRAPH
            }
        elif key == "nodes":
            for node in value:
                ewoks_node = {k: v for k, v in node.items() if k in _ALLOWED_IN_NODES}
                properties_node = {
                    k: v for k, v in node.items() if k not in _ALLOWED_IN_NODES
                }
                # Add 'id' to not_ewoks_props of nodes to merge them on get
                properties_node["id"] = node.get("id")
                ewoks_props["nodes"].append(ewoks_node)
                not_ewoks_props.setdefault("nodes", []).append(properties_node)
        elif key == "links":
            for link in value:
                ewoks_link = {k: v for k, v in link.items() if k in _ALLOWED_IN_LINKS}
                properties_link = {
                    k: v for k, v in link.items() if k not in _ALLOWED_IN_LINKS
                }
                # Add 'source' and 'target' to not_ewoks_props of links to merge them on get
                properties_link["source"] = link.get("source")
                properties_link["target"] = link.get("target")
                ewoks_props["links"].append(ewoks_link)
                not_ewoks_props.setdefault("links", []).append(properties_link)

    return ewoks_props, not_ewoks_props


def merge_workflow_props(ewoks_workflow, not_ewoks_props):
    graph = {**ewoks_workflow["graph"], **not_ewoks_props["graph"]}

    nodes_props_dict = {node["id"]: node for node in not_ewoks_props.get("nodes", [])}

    nodes = []
    for ewoks_node in ewoks_workflow.get("nodes", []):
        node_id = ewoks_node.get("id", "")
        merged_node = ewoks_node.copy()
        if node_id in nodes_props_dict:
            merged_node.update(nodes_props_dict[node_id])
        nodes.append(merged_node)

    links_props_dict = {
        link["source"] + "-" + link["target"]: link
        for link in not_ewoks_props.get("links", [])
    }

    links = []
    for ewoks_link in ewoks_workflow.get("links", []):
        link_id = ewoks_link.get("source", "") + "-" + ewoks_link.get("target", "")
        merged_link = ewoks_link.copy()
        if link_id in links_props_dict:
            merged_link.update(links_props_dict[link_id])
        links.append(merged_link)

    result = {"graph": graph}
    result["nodes"] = nodes
    result["links"] = links
    return result
