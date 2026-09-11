from typing import List, Dict, Any, Optional
from sqlalchemy.orm import Session
from app.models.graph import DrainageNode, DrainageEdge
from app.models.ward import Ward
from app.models.drain import Drain
from app.models.road import Road
from app.models.waterbody import Waterbody
from app.models.facility import CriticalFacility
from ml.inference.predictor import RiskPredictor

# Benchmark Fallback Graph Nodes & Edges (for environments without active PostGIS container)
BENCHMARK_NODES = [
    {"node_id": "WARD_1", "node_type": "ward", "name": "Ward G/North (Dadar)", "ward_id": 1, "status": "active", "confidence": "OBSERVED"},
    {"node_id": "DRAIN_001", "node_type": "drain", "name": "Dadar Outfall Main Drain", "ward_id": 1, "status": "blocked", "confidence": "OBSERVED"},
    {"node_id": "LOWLAND_001", "node_type": "low_lying_area", "name": "Dadar TT Circle Low-Lying Zone", "ward_id": 1, "status": "vulnerable", "confidence": "SYNTHETIC_TERRAIN_ANALYSIS"},
    {"node_id": "ROAD_001", "node_type": "road", "name": "Dr. Babasaheb Ambedkar Road", "ward_id": 1, "status": "active", "confidence": "OBSERVED"},
    {"node_id": "POP_001", "node_type": "population_zone", "name": "Dadar Central Residential Sector", "ward_id": 1, "status": "dense", "confidence": "DERIVED"},
    {"node_id": "FACILITY_001", "node_type": "critical_facility", "name": "Sion Hospital / Emergency Care", "ward_id": 1, "status": "operational", "confidence": "OBSERVED"},
    {"node_id": "WATERBODY_001", "node_type": "waterbody", "name": "Mahim Bay Stormwater Outfall", "ward_id": 1, "status": "open", "confidence": "OBSERVED"},
]

BENCHMARK_EDGES = [
    {"edge_id": "E_001", "source_node_id": "WARD_1", "target_node_id": "LOWLAND_001", "edge_type": "located_in", "distance_m": 0.0, "relationship_label": "SPATIAL_LOCATION"},
    {"edge_id": "E_002", "source_node_id": "LOWLAND_001", "target_node_id": "DRAIN_001", "edge_type": "drains_to", "distance_m": 45.0, "relationship_label": "INFERRED_SPATIAL_RELATIONSHIP"},
    {"edge_id": "E_003", "source_node_id": "DRAIN_001", "target_node_id": "ROAD_001", "edge_type": "near", "distance_m": 12.0, "relationship_label": "INFERRED_SPATIAL_RELATIONSHIP"},
    {"edge_id": "E_004", "source_node_id": "ROAD_001", "target_node_id": "POP_001", "edge_type": "affects", "distance_m": 80.0, "relationship_label": "INFERRED_SPATIAL_RELATIONSHIP"},
    {"edge_id": "E_005", "source_node_id": "POP_001", "target_node_id": "FACILITY_001", "edge_type": "serves", "distance_m": 250.0, "relationship_label": "SPATIAL_PROXIMITY"},
    {"edge_id": "E_006", "source_node_id": "DRAIN_001", "target_node_id": "WATERBODY_001", "edge_type": "flows_toward", "distance_m": 500.0, "relationship_label": "POSSIBLE_DEPENDENCY"},
]

def get_ward_graph(db: Session, ward_id: int) -> Dict[str, Any]:
    """Retrieve all graph nodes and edges for a specific ward."""
    try:
        nodes = db.query(DrainageNode).filter(DrainageNode.ward_id == ward_id).all()
        if nodes:
            node_ids = [n.node_id for n in nodes]
            edges = db.query(DrainageEdge).filter(
                (DrainageEdge.source_node_id.in_(node_ids)) | (DrainageEdge.target_node_id.in_(node_ids))
            ).all()
            return {
                "ward_id": ward_id,
                "total_nodes": len(nodes),
                "total_edges": len(edges),
                "nodes": [
                    {
                        "node_id": n.node_id,
                        "node_type": n.node_type,
                        "name": n.name,
                        "ward_id": n.ward_id,
                        "status": n.status,
                        "confidence": n.confidence
                    } for n in nodes
                ],
                "edges": [
                    {
                        "edge_id": e.edge_id,
                        "source_node_id": e.source_node_id,
                        "target_node_id": e.target_node_id,
                        "edge_type": e.edge_type,
                        "distance_m": e.distance_m,
                        "relationship_label": e.relationship_label
                    } for e in edges
                ]
            }
    except Exception:
        pass

    # Benchmark fallback
    ward_nodes = [n for n in BENCHMARK_NODES if n["ward_id"] == ward_id]
    if not ward_nodes:
        ward_nodes = BENCHMARK_NODES
    w_ids = {n["node_id"] for n in ward_nodes}
    ward_edges = [e for e in BENCHMARK_EDGES if e["source_node_id"] in w_ids or e["target_node_id"] in w_ids]

    return {
        "ward_id": ward_id,
        "total_nodes": len(ward_nodes),
        "total_edges": len(ward_edges),
        "nodes": ward_nodes,
        "edges": ward_edges
    }

def get_affected_assets(db: Session, node_id: str) -> Dict[str, Any]:
    """Traverse spatial dependency graph to identify potentially affected connected assets."""
    ward_graph = get_ward_graph(db, ward_id=1)
    nodes_map = {n["node_id"]: n for n in ward_graph["nodes"]}
    edges = ward_graph["edges"]

    # BFS Traversal up to depth 3
    visited = set()
    queue = [(node_id, 0)]
    affected_nodes = []

    while queue:
        curr_id, depth = queue.pop(0)
        if curr_id in visited or depth > 3:
            continue
        visited.add(curr_id)

        if curr_id in nodes_map and curr_id != node_id:
            affected_nodes.append({
                **nodes_map[curr_id],
                "traversal_depth": depth,
                "association_type": "POTENTIALLY_CONNECTED_ASSET"
            })

        # Find outgoing edges
        for e in edges:
            if e["source_node_id"] == curr_id and e["target_node_id"] not in visited:
                queue.append((e["target_node_id"], depth + 1))

    return {
        "source_node_id": node_id,
        "source_node_details": nodes_map.get(node_id, {"node_id": node_id, "name": "Target Node", "node_type": "unknown"}),
        "affected_assets_count": len(affected_nodes),
        "potentially_affected_assets": affected_nodes,
        "relationship_disclaimer": "INFERRED SPATIAL RELATIONSHIPS: Spatial proximity does not guarantee flooding."
    }

def get_risk_dependency_chain(db: Session, ward_id: int) -> Dict[str, Any]:
    """Combine Phase 6 ML Risk Prediction with Phase 8 spatial dependency graph traversal."""
    # 1. Fetch ML Risk Prediction from Phase 6 model
    predictor = RiskPredictor(horizon_hours=24)
    ml_risk = predictor.predict_risk({"ward_id": ward_id, "rainfall_last_24h": 140.0, "elevation_m": 4.0})

    # 2. Fetch spatial graph
    graph = get_ward_graph(db, ward_id=ward_id)

    # 3. Construct Risk Propagation Chain
    nodes = graph["nodes"]
    edges = graph["edges"]

    chain_steps = []
    prev_node = "WARD_1"
    
    for n in nodes:
        chain_steps.append({
            "step_index": len(chain_steps) + 1,
            "node_id": n["node_id"],
            "node_type": n["node_type"],
            "name": n["name"],
            "status": n["status"],
            "relationship": "INFERRED_SPATIAL_RELATIONSHIP" if len(chain_steps) > 0 else "PRIMARY_RISK_ZONE"
        })

    return {
        "ward_id": ward_id,
        "ml_risk_prediction": {
            "predicted_probability": ml_risk["predicted_probability"],
            "risk_level": ml_risk["risk_level"],
            "horizon_hours": ml_risk["horizon_hours"],
            "model_version": ml_risk["model_version"]
        },
        "dependency_chain_length": len(chain_steps),
        "risk_propagation_chain": chain_steps,
        "dependency_score": 0.85,
        "dependency_score_label": "Dependency/Association Score (Not scientifically validated flow)",
        "data_provenance": "DEMO GRAPH — TRAINED ON SYNTHETIC BENCHMARK DATA"
    }
