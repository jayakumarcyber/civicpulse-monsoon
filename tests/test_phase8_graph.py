import sys
import os
import pytest

sys.path.insert(0, os.path.dirname(r"d:\CivicPulse-Monsoon\backend"))
sys.path.insert(0, r"d:\CivicPulse-Monsoon\backend")

from app.services.graph_service import (
    get_ward_graph,
    get_affected_assets,
    get_risk_dependency_chain,
    BENCHMARK_NODES,
    BENCHMARK_EDGES
)

def test_graph_node_and_edge_structure():
    assert len(BENCHMARK_NODES) > 0
    assert len(BENCHMARK_EDGES) > 0
    
    n0 = BENCHMARK_NODES[0]
    assert "node_id" in n0
    assert "node_type" in n0
    assert "name" in n0
    assert "ward_id" in n0

    e0 = BENCHMARK_EDGES[0]
    assert "edge_id" in e0
    assert "source_node_id" in e0
    assert "target_node_id" in e0
    assert "edge_type" in e0

def test_get_ward_graph():
    graph = get_ward_graph(db=None, ward_id=1)
    assert graph["ward_id"] == 1
    assert graph["total_nodes"] > 0
    assert graph["total_edges"] > 0
    assert "nodes" in graph
    assert "edges" in graph

def test_affected_asset_traversal():
    affected = get_affected_assets(db=None, node_id="DRAIN_001")
    assert affected["source_node_id"] == "DRAIN_001"
    assert affected["affected_assets_count"] > 0
    assert "INFERRED" in affected["relationship_disclaimer"]

def test_risk_dependency_chain():
    chain = get_risk_dependency_chain(db=None, ward_id=1)
    assert chain["ward_id"] == 1
    assert "ml_risk_prediction" in chain
    assert chain["dependency_chain_length"] > 0
    assert "risk_propagation_chain" in chain
    assert chain["dependency_score"] > 0.0
    assert "Dependency/Association Score" in chain["dependency_score_label"]

def test_inferred_relationship_label_enforcement():
    graph = get_ward_graph(db=None, ward_id=1)
    for edge in graph["edges"]:
        # Verify edge labels do not claim confirmed hydrological flow unless specified
        label = edge.get("relationship_label", "")
        assert "INFERRED" in label or "SPATIAL" in label or "POSSIBLE" in label or "LOCATION" in label
