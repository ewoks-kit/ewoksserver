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
            non_ewoks_workflow_props = get_non_ewoks_props(
                root_path, res["graph"].get("id", None)
            )
            if non_ewoks_workflow_props:
                graph = merge_workflow_props(res, non_ewoks_workflow_props)["graph"]
            else:
                graph = res["graph"]

            if not _include_resource(graph.get("keywords", dict()), keywords):
                continue

            yield {
                key: value for key, value in graph.items() if key in _WORKFLOW_KEYWORDS
            }


def get_non_ewoks_props(root_path: Path, workflow_id: str) -> Optional[dict]:
    non_ewoks_props_exist = json_backend.resource_exists(
        root_path / "nonewoksprops", workflow_id
    )
    if non_ewoks_props_exist:
        non_ewoks_workflow_props = json_backend.load_resource(
            root_path / "nonewoksprops", workflow_id
        )
        return non_ewoks_workflow_props


def _include_resource(res_keywords: dict, keywords: Optional[Dict] = None) -> bool:
    if keywords is None:
        return True
    return all(res_keywords.get(key) == value for key, value in keywords.items())


# splits the props of input_nodes and the output_nodes that are in the graph
# these nodes have only a uiProps property that needs to be splitted out
def _split_input_output_nodes(ewoks_nodes):
    ewoks_props = [
        {k: v for k, v in node.items() if k != "uiProps"} for node in ewoks_nodes
    ]
    non_ewoks_props = [
        {k: v for k, v in node.items() if k in ["uiProps", "id"]}
        for node in ewoks_nodes
    ]
    return ewoks_props, non_ewoks_props


def split_ewoks_properties(workflow):
    ewoks_props = {"graph": {}, "nodes": [], "links": []}
    non_ewoks_props = {}

    for key, value in workflow.items():
        if key == "graph":
            ewoks_props["graph"] = {
                k: v for k, v in value.items() if k in _ALLOWED_IN_GRAPH
            }
            non_ewoks_props["graph"] = {
                k: v for k, v in value.items() if k not in _ALLOWED_IN_GRAPH
            }
            # Split {graph: input_nodes: [...]}
            input_nodes = ewoks_props["graph"].get("input_nodes", [])
            if input_nodes:
                (
                    ewoks_input_nodes_props,
                    non_ewoks_input_node_props,
                ) = _split_input_output_nodes(input_nodes)
                ewoks_props["graph"]["input_nodes"] = ewoks_input_nodes_props
                non_ewoks_props["graph"]["input_nodes"] = non_ewoks_input_node_props
            # Split {graph: output_nodes: [...]}
            output_nodes = ewoks_props["graph"].get("output_nodes", [])
            if output_nodes:
                (
                    ewoks_output_nodes_props,
                    non_ewoks_output_node_props,
                ) = _split_input_output_nodes(output_nodes)
                ewoks_props["graph"]["output_nodes"] = ewoks_output_nodes_props
                non_ewoks_props["graph"]["output_nodes"] = non_ewoks_output_node_props
        elif key == "nodes":
            for node in value:
                ewoks_node_props = {
                    k: v for k, v in node.items() if k in _ALLOWED_IN_NODES
                }
                non_ewoks_node_props = {
                    k: v for k, v in node.items() if k not in _ALLOWED_IN_NODES
                }
                # Add 'id' to non_ewoks_node_props of nodes to merge them on get
                non_ewoks_node_props["id"] = node.get("id")
                ewoks_props["nodes"].append(ewoks_node_props)
                non_ewoks_props.setdefault("nodes", []).append(non_ewoks_node_props)
        elif key == "links":
            for link in value:
                ewoks_link_props = {
                    k: v for k, v in link.items() if k in _ALLOWED_IN_LINKS
                }
                non_ewoks_link_props = {
                    k: v for k, v in link.items() if k not in _ALLOWED_IN_LINKS
                }
                # Add 'source' and 'target' to not_ewoks_props of links to merge them on get
                non_ewoks_link_props["source"] = link.get("source")
                non_ewoks_link_props["target"] = link.get("target")
                ewoks_props["links"].append(ewoks_link_props)
                non_ewoks_props.setdefault("links", []).append(non_ewoks_link_props)
    return ewoks_props, non_ewoks_props


def _merge_input_output_nodes(ewoks_nodes, not_ewoks_nodes):
    nodes_dict = {node["id"]: node for node in not_ewoks_nodes}
    merged_nodes = [
        {**node, **nodes_dict.get(node.get("id"), {})} for node in ewoks_nodes
    ]
    return merged_nodes


def merge_workflow_props(ewoks_workflow, not_ewoks_props):
    # merge the input-nodes if there are any.
    ewoks_input_nodes_props = ewoks_workflow["graph"].get("input_nodes", [])
    not_ewoks_input_nodes_props = not_ewoks_props["graph"].get("input_nodes", [])
    if ewoks_input_nodes_props and not_ewoks_input_nodes_props:
        input_nodes = _merge_input_output_nodes(
            ewoks_input_nodes_props, not_ewoks_input_nodes_props
        )
        ewoks_workflow["graph"]["input_nodes"] = input_nodes

    # merge the output-nodes if there are any.
    ewoks_output_nodes_props = ewoks_workflow["graph"].get("output_nodes", [])
    not_ewoks_output_nodes_props = not_ewoks_props["graph"].get("output_nodes", [])
    if ewoks_output_nodes_props and not_ewoks_output_nodes_props:
        output_nodes = _merge_input_output_nodes(
            ewoks_output_nodes_props, not_ewoks_output_nodes_props
        )
        ewoks_workflow["graph"]["output_nodes"] = output_nodes

    # merge all graph props in graph
    graph = {**not_ewoks_props["graph"], **ewoks_workflow["graph"]}

    # merge nodes props
    nodes_props_dict = {node["id"]: node for node in not_ewoks_props.get("nodes", [])}
    nodes = []
    for ewoks_node in ewoks_workflow.get("nodes", []):
        node_id = ewoks_node.get("id", "")
        merged_node = ewoks_node.copy()
        if node_id in nodes_props_dict:
            merged_node.update(nodes_props_dict[node_id])
        nodes.append(merged_node)

    #  merge links props
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

    result = {"graph": graph, "nodes": nodes}
    if links:
        result["links"] = links
    return result
