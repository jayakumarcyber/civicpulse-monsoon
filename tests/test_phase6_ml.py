import sys
import os
import pytest

sys.path.insert(0, os.path.dirname(r"d:\CivicPulse-Monsoon\backend"))
sys.path.insert(0, r"d:\CivicPulse-Monsoon\backend")

from ml.training.target_builder import build_multi_horizon_targets
from ml.training.train_all_and_compare import run_model_comparison_pipeline
from ml.inference.predictor import RiskPredictor, map_probability_to_risk_level
from ml.inference.batch_predictor import run_batch_prediction

def test_target_generation():
    df_targets = build_multi_horizon_targets()
    assert "target_waterlogging_24h" in df_targets.columns
    assert "target_waterlogging_48h" in df_targets.columns
    assert "target_waterlogging_72h" in df_targets.columns
    assert set(df_targets["target_waterlogging_24h"].unique()).issubset({0, 1})

def test_model_training_and_comparison():
    comparison = run_model_comparison_pipeline()
    assert comparison["Selected_Model"] == "XGBoost_Classifier"
    assert "Baseline_LogisticRegression" in comparison
    assert "XGBoost_Classifier" in comparison
    assert "LightGBM_Classifier" in comparison

def test_risk_level_mapping():
    assert map_probability_to_risk_level(0.10) == "LOW"
    assert map_probability_to_risk_level(0.35) == "MEDIUM"
    assert map_probability_to_risk_level(0.60) == "HIGH"
    assert map_probability_to_risk_level(0.85) == "CRITICAL"

def test_risk_predictor_inference():
    predictor = RiskPredictor(horizon_hours=24)
    sample_feat = {
        "ward_id": 1,
        "rainfall_last_24h": 120.0,
        "elevation_m": 3.0,
        "drainage_quality_score": 0.3
    }
    result = predictor.predict_risk(sample_feat)
    assert result["horizon_hours"] == 24
    assert 0.0 <= result["predicted_probability"] <= 1.0
    assert result["risk_level"] in ["LOW", "MEDIUM", "HIGH", "CRITICAL"]
    assert "DEMO MODEL" in result["data_provenance"]

def test_batch_prediction():
    batch = run_batch_prediction()
    assert len(batch) > 0
    assert "horizon_hours" in batch[0]
    assert "predicted_probability" in batch[0]
    assert "risk_level" in batch[0]
