import sys
import os
import pytest

sys.path.insert(0, os.path.dirname(r"d:\CivicPulse-Monsoon\backend"))
sys.path.insert(0, r"d:\CivicPulse-Monsoon\backend")

from ml.explainability.explainer import ShapExplainerEngine, generate_deterministic_text_explanation

def test_shap_explainer_initialization_and_local_explanation():
    engine = ShapExplainerEngine(horizon_hours=24)
    sample_feat = {
        "ward_id": 1,
        "rainfall_last_24h": 140.0,
        "elevation_m": 3.0,
        "drainage_quality_score": 0.3
    }
    explanation = engine.explain_prediction(sample_feat)
    assert "prediction_summary" in explanation
    assert "top_contributing_factors" in explanation
    assert len(explanation["top_contributing_factors"]) > 0

def test_directional_consistency_and_non_hardcoded_values():
    engine = ShapExplainerEngine(horizon_hours=24)
    feat1 = {
        "ward_id": 1,
        "rainfall_last_24h": 200.0,
        "rainfall_last_48h": 250.0,
        "previous_waterlogging_count": 10.0,
        "incident_count_30d": 15.0,
        "elevation_m": 2.0,
        "historical_incident_density": 5.0
    }
    feat2 = {
        "ward_id": 1,
        "rainfall_last_24h": 0.0,
        "rainfall_last_48h": 0.0,
        "previous_waterlogging_count": 0.0,
        "incident_count_30d": 0.0,
        "elevation_m": 25.0,
        "historical_incident_density": 0.0
    }

    exp1 = engine.explain_prediction(feat1)
    exp2 = engine.explain_prediction(feat2)

    # Probabilities must change dynamically (not hardcoded)
    assert exp1["prediction_summary"]["predicted_probability"] != exp2["prediction_summary"]["predicted_probability"]

    # Verify directional consistency
    for factor in exp1["top_contributing_factors"]:
        s_val = factor["shap_value"]
        direction = factor["effect_direction"]
        if s_val > 0:
            assert direction == "increases risk"
        elif s_val < 0:
            assert direction == "decreases risk"

def test_deterministic_text_generation():
    txt_pos = generate_deterministic_text_explanation("rainfall_last_24h", 0.35, 140.0)
    assert "increasing predicted risk" in txt_pos or "increases" in txt_pos

    txt_neg = generate_deterministic_text_explanation("elevation_m", -0.20, 20.0)
    assert "mitigates" in txt_neg or "decreases" in txt_neg

def test_global_feature_importance():
    engine = ShapExplainerEngine(horizon_hours=24)
    global_imp = engine.get_global_feature_importance()
    assert len(global_imp) > 0
    assert "feature_name" in global_imp[0]
    assert "global_importance_score" in global_imp[0]
