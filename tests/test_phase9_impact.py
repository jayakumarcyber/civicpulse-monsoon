import sys
import os
import pytest

sys.path.insert(0, os.path.dirname(r"d:\CivicPulse-Monsoon\backend"))
sys.path.insert(0, r"d:\CivicPulse-Monsoon\backend")

from app.core.config import settings
from app.services.impact_service import (
    calculate_ward_impact,
    compute_priority_score,
    classify_priority_level,
    generate_priority_reasons,
    get_priority_assessment_for_ward,
    get_priority_rankings
)

def test_impact_exposure_calculation():
    impact = calculate_ward_impact(db=None, ward_id=1)
    assert impact["ward_id"] == 1
    assert impact["potential_population_exposure"] > 0
    assert impact["critical_facility_count"] >= 0
    assert "Potential population exposure" in impact["exposure_label"]

def test_priority_score_formula():
    impact = {
        "potential_population_exposure": 8500,
        "critical_facility_count": 7,
        "hospital_count": 1,
        "school_count": 3,
        "exposed_road_count": 14,
        "exposed_drain_count": 8,
        "historical_waterlogging_count": 10
    }
    ml_prediction = {
        "predicted_probability": 0.85,
        "risk_level": "CRITICAL",
        "horizon_hours": 24
    }

    score = compute_priority_score(impact, ml_prediction)
    assert 0.0 <= score <= 100.0
    assert score >= 50.0  # High risk + hospital + high exposure should yield high score

def test_priority_level_classification():
    assert classify_priority_level(85.0) == "P1 — CRITICAL"
    assert classify_priority_level(65.0) == "P2 — HIGH"
    assert classify_priority_level(35.0) == "P3 — MEDIUM"
    assert classify_priority_level(15.0) == "P4 — LOW"

def test_priority_reasons_generation():
    impact = {
        "potential_population_exposure": 8500,
        "critical_facility_count": 7,
        "hospital_count": 1,
        "school_count": 3,
        "exposed_road_count": 14,
        "exposed_drain_count": 8,
        "historical_waterlogging_count": 10
    }
    ml_prediction = {
        "predicted_probability": 0.85,
        "risk_level": "CRITICAL",
        "horizon_hours": 24
    }

    reasons = generate_priority_reasons(impact, ml_prediction)
    assert len(reasons) >= 4
    assert any("85%" in r for r in reasons)
    assert any("8,500" in r for r in reasons)
    assert any("hospital" in r for r in reasons)

def test_priority_rankings_sorting():
    rankings = get_priority_rankings(db=None)
    assert len(rankings) == 4
    
    # Check ranks are 1, 2, 3, 4 and scores are strictly sorted descending
    for i in range(len(rankings) - 1):
        assert rankings[i]["priority_score"] >= rankings[i+1]["priority_score"]
        assert rankings[i]["rank"] == i + 1

def test_weight_configuration_presence():
    assessment = get_priority_assessment_for_ward(db=None, ward_id=1)
    weights = assessment["weight_configuration"]
    assert weights["risk_weight"] == settings.PRIORITY_WEIGHT_RISK
    assert weights["population_weight"] == settings.PRIORITY_WEIGHT_POPULATION
    assert "DEMO / CONFIGURABLE" in weights["label"]
