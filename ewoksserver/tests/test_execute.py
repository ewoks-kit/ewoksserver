import pytest
from ewokscore.tests.examples.graphs import graph_names
from ewokscore.tests.examples.graphs import get_graph


@pytest.mark.parametrize("graph_name", graph_names())
def test_execute(graph_name, client):
    # TODO: verify result
    graph, _ = get_graph(graph_name)
    data = {"graph": graph}
    response = client.post("/workflows/execute", json=data)
    assert response.status_code == 200, response.get_json()
