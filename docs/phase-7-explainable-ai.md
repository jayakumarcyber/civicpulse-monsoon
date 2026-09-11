# CivicPulse Monsoon - Phase 7 Explainable AI & Risk Evidence

## 1. Overview & XAI Methodology
**Phase 7** integrates **SHAP (SHapley Additive exPlanations)** with the Phase 6 XGBoost model. Every risk prediction ($P(\text{waterlogging})$) is decomposed into additive feature contributions:

$$\text{logit}(P_i) = \text{base\_value} + \sum_{j=1}^{M} \phi_{ij}$$

where $\phi_{ij}$ represents the exact SHAP marginal contribution of feature $j$ to observation $i$.

> [!IMPORTANT]
> **Deterministic Directionality**: UI text summaries are strictly derived from the sign of $\phi_{ij}$:
> - $\phi_{ij} > 0 \implies$ Feature $j$ **increases** predicted risk.
> - $\phi_{ij} < 0 \implies$ Feature $j$ **decreases** predicted risk.

---

## 2. Structured Evidence Categorization

Every feature metric and supporting evidence item is assigned a standardized category label:

- **`OBSERVED`**: Real-time gauge readings (e.g. `rainfall_last_1h`), ward terrain elevation (`elevation_m`).
- **`FORECAST`**: Forward 24h / 48h / 72h predicted rainfall accumulation.
- **`HISTORICAL`**: Recorded civic incident counters (`incident_count_30d`, `previous_waterlogging_count`).
- **`DERIVED`**: Computed spatial scores (`drainage_density_km_sqkm`, `historical_incident_density`).
- **`SYNTHETIC`**: Demo benchmark tags (`SYNTHETIC_DEMO_DATA`).

---

## 3. Sample SHAP Local Explanation Payload (`/api/v1/explanations/ward/1`)

```json
{
  "prediction_summary": {
    "ward_id": 1,
    "horizon_hours": 24,
    "predicted_probability": 0.825,
    "risk_level": "CRITICAL",
    "model_version": "XGBoost_24h_v1_DEMO",
    "data_provenance": "DEMO MODEL — TRAINED ON SYNTHETIC DATA"
  },
  "top_contributing_factors": [
    {
      "feature_name": "rainfall_last_24h",
      "display_name": "24-Hour Accumulated Rainfall",
      "raw_value": 140.0,
      "shap_value": 0.3842,
      "effect_direction": "increases risk",
      "category": "FORECAST",
      "text_summary": "High accumulated rainfall (140.0 mm) is a key driver increasing predicted risk."
    },
    {
      "feature_name": "previous_waterlogging_count",
      "display_name": "Historical Waterlogging Events",
      "raw_value": 8.0,
      "shap_value": 0.2115,
      "effect_direction": "increases risk",
      "category": "HISTORICAL",
      "text_summary": "Repeated historical incidents (8) increase the predicted risk."
    },
    {
      "feature_name": "elevation_m",
      "display_name": "Terrain Elevation",
      "raw_value": 4.0,
      "shap_value": 0.1542,
      "effect_direction": "increases risk",
      "category": "OBSERVED",
      "text_summary": "Lower terrain elevation (4.0 m) contributes to higher risk."
    }
  ],
  "data_quality_warnings": ["Data quality verified."],
  "prediction_limitations": [
    "Predictions indicate probabilistic risk, not confirmed flooding.",
    "Drainage blockage status requires field verification.",
    "Synthetic demo benchmark data used for prototype evaluation."
  ]
}
```

---

## 4. XAI REST API Endpoint Reference

- **`GET /api/v1/explanations/ward/{ward_id}`**: Local SHAP explanation & evidence breakdown for ward.
- **`GET /api/v1/explanations/prediction/{prediction_id}`**: Local SHAP explanation for specific prediction record.
- **`GET /api/v1/explanations/model/feature-importance`**: Global SHAP feature importances.
- **`GET /api/v1/explanations/model/metadata`**: Model training range, test range, metric benchmark, and calibration status.
