# CivicPulse Monsoon - Phase 8 Spatial Drainage Dependency Graph & Risk Propagation

## 1. Overview & Graph Architecture
**Phase 8** establishes the **Spatial Drainage Dependency Graph** for **CivicPulse Monsoon**, representing spatial/network associations between municipal assets:
- **Nodes**: Wards, stormwater drains, roads, low-lying areas, waterbodies, population zones, and critical facilities.
- **Edges**: Spatial proximity, containment, intersection, and directional dependencies.

> [!IMPORTANT]
> **Data Quality & Relationship Labeling**: Where actual hydrological flow direction is unmapped, edges are explicitly tagged:  
> `"relationship_label": "INFERRED_SPATIAL_RELATIONSHIP"`.  
> Relationships represent spatial proximity and potential risk propagation, not confirmed hydraulic flooding.

---

## 2. Node & Edge Schema

### Node Types
- `ward`: Administrative municipal ward polygon
- `drain`: Stormwater drain segment or outfall
- `road`: Transportation corridor (arterial / local)
- `low_lying_area`: Terrain elevation depression ($\text{elevation} < 5.0\text{m}$)
- `waterbody`: Lake, bay, or natural reservoir
- `population_zone`: Residential population density sector
- `critical_facility`: Hospital, school, emergency station, or transport hub

### Edge Types
- `located_in`: Spatial containment within ward
- `drains_to`: Proximity association from low-lying area to drain
- `near`: Spatial proximity between drain and road corridor ($\le 50\text{m}$)
- `affects`: Spatial association between road and population zone
- `serves`: Population dependency on critical facility
- `flows_toward`: Outfall path toward waterbody

---

## 3. Sample Risk Dependency Propagation Chain (`/api/v1/graph/risk-chain/1`)

```json
{
  "ward_id": 1,
  "ml_risk_prediction": {
    "predicted_probability": 0.825,
    "risk_level": "CRITICAL",
    "horizon_hours": 24,
    "model_version": "XGBoost_24h_v1_DEMO"
  },
  "dependency_chain_length": 7,
  "risk_propagation_chain": [
    {
      "step_index": 1,
      "node_id": "WARD_1",
      "node_type": "ward",
      "name": "Ward G/North (Dadar)",
      "status": "active",
      "relationship": "PRIMARY_RISK_ZONE"
    },
    {
      "step_index": 2,
      "node_id": "DRAIN_001",
      "node_type": "drain",
      "name": "Dadar Outfall Main Drain",
      "status": "blocked",
      "relationship": "INFERRED_SPATIAL_RELATIONSHIP"
    },
    {
      "step_index": 3,
      "node_id": "LOWLAND_001",
      "node_type": "low_lying_area",
      "name": "Dadar TT Circle Low-Lying Zone",
      "status": "vulnerable",
      "relationship": "INFERRED_SPATIAL_RELATIONSHIP"
    },
    {
      "step_index": 4,
      "node_id": "ROAD_001",
      "node_type": "road",
      "name": "Dr. Babasaheb Ambedkar Road",
      "status": "active",
      "relationship": "INFERRED_SPATIAL_RELATIONSHIP"
    },
    {
      "step_index": 5,
      "node_id": "POP_001",
      "node_type": "population_zone",
      "name": "Dadar Central Residential Sector",
      "status": "dense",
      "relationship": "INFERRED_SPATIAL_RELATIONSHIP"
    },
    {
      "step_index": 6,
      "node_id": "FACILITY_001",
      "node_type": "critical_facility",
      "name": "Sion Hospital / Emergency Care",
      "status": "operational",
      "relationship": "INFERRED_SPATIAL_RELATIONSHIP"
    }
  ],
  "dependency_score": 0.85,
  "dependency_score_label": "Dependency/Association Score (Not scientifically validated flow)",
  "data_provenance": "DEMO GRAPH — TRAINED ON SYNTHETIC BENCHMARK DATA"
}
```

---

## 4. Graph REST API Endpoint Reference

- **`GET /api/v1/graph/ward/{ward_id}`**: Retrieves all graph nodes and edges for a ward.
- **`GET /api/v1/graph/drain/{drain_id}`**: Retrieves nodes and edges connected to a drain.
- **`GET /api/v1/graph/node/{node_id}`**: Retrieves single node attributes and direct neighbors.
- **`GET /api/v1/graph/affected-assets/{node_id}`**: Identifies potentially affected downstream/nearby connected assets.
- **`GET /api/v1/graph/risk-chain/{ward_id}`**: Combines Phase 6 ML risk prediction with spatial dependency chain traversal.
