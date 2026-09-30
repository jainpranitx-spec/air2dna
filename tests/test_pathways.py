from science.pathways import build_trace


def test_trace_is_connected() -> None:
    nodes = build_trace()
    assert nodes[0]["id"] == "pm25"
    assert nodes[-1]["next_nodes"] == []
    identifiers = {node["id"] for node in nodes}
    for node in nodes:
        assert set(node["next_nodes"]).issubset(identifiers)
