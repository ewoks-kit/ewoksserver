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


def _split_in_out_nodes(ewoks_nodes):
    new_ewoks_nodes = []
    not_ewoks_nodes = []
    for node in ewoks_nodes:
        ewoks_node = {k: v for k, v in node.items() if k not in ["uiProps"]}
        not_ewoks_node = {k: v for k, v in node.items() if k in ["uiProps"]}
        not_ewoks_node["id"] = node["id"]
        new_ewoks_nodes.append(ewoks_node)
        not_ewoks_nodes.append(not_ewoks_node)
    return new_ewoks_nodes, not_ewoks_nodes


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
            # Handle input_nodes
            in_nodes = ewoks_props["graph"].get("input_nodes", [])
            if in_nodes:
                new_ewoks_in_nodes, not_ewoks_out_nodes = _split_in_out_nodes(in_nodes)
                ewoks_props["graph"]["input_nodes"] = new_ewoks_in_nodes
                not_ewoks_props["graph"]["input_nodes"] = not_ewoks_out_nodes
            # Handle output_nodes
            out_nodes = ewoks_props["graph"].get("output_nodes", [])
            if out_nodes:
                new_ewoks_out_nodes, not_ewoks_out_nodes = _split_in_out_nodes(
                    out_nodes
                )
                ewoks_props["graph"]["output_nodes"] = new_ewoks_out_nodes
                not_ewoks_props["graph"]["output_nodes"] = not_ewoks_out_nodes

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


def _merge_in_out_nodes(ewoks_nodes, not_ewoks_nodes):
    nodes_dict = {node["id"]: node for node in not_ewoks_nodes}
    nodes = []
    for node in ewoks_nodes:
        node_id = node.get("id", "")
        merged_node = node.copy()
        if node_id in nodes_dict:
            merged_node.update(nodes_dict[node_id])
        nodes.append(merged_node)

    return nodes


def merge_workflow_props(ewoks_workflow, not_ewoks_props):
    # merge the input-nodes if there are any.
    input_nodes = ewoks_workflow["graph"].get("input_nodes", [])
    not_ewoks_input_nodes = not_ewoks_props["graph"].get("input_nodes", [])
    if input_nodes and not_ewoks_input_nodes:
        in_nodes = _merge_in_out_nodes(input_nodes, not_ewoks_input_nodes)
        ewoks_workflow["graph"]["input_nodes"] = in_nodes
    # merge the output-nodes if there are any.
    output_nodes = ewoks_workflow["graph"].get("output_nodes", [])
    not_ewoks_output_nodes = not_ewoks_props["graph"].get("output_nodes", [])
    if output_nodes and not_ewoks_output_nodes:
        out_nodes = _merge_in_out_nodes(output_nodes, not_ewoks_output_nodes)
        ewoks_workflow["graph"]["output_nodes"] = out_nodes
    # merge graph
    graph = {**not_ewoks_props["graph"], **ewoks_workflow["graph"]}
    # merge nodes
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
