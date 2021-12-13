import pytest
from ewokscore.tests.examples.graphs import graph_names
from ewokscore.tests.examples.graphs import get_graph


@pytest.mark.parametrize("graph_name", graph_names())
def test_execute(graph_name, client):
    # TODO: verify result
    graph, _ = get_graph(graph_name)
    response = client.post("/workflow/execute", json=graph)
    assert response.status_code == 200
