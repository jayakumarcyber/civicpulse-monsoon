import sys
import os
import pytest

sys.path.insert(0, os.path.dirname(r"d:\CivicPulse-Monsoon\backend"))
sys.path.insert(0, r"d:\CivicPulse-Monsoon\backend")

from app.services.analytics_service import calculate_ward_recurrence
from ml.inference.predictor import RiskPredictor
from ml.explainability.explainer import ShapExplainerEngine
from app.services.graph_service import get_risk_dependency_chain
from app.services.impact_service import get_priority_assessment_for_ward, get_priority_rankings
from app.services.optimization_service import solve_municipal_resource_optimization
from app.services.simulation_service import run_what_if_simulation, BASELINE_STATE

def test_e2e_full_system_integration_pipeline():
    # 1. Historical Analytics Engine
    recurrence = calculate_ward_recurrence(db=None)
    assert len(recurrence) > 0

    # 2. Multi-Horizon ML Risk Prediction Engine
    predictor_24h = RiskPredictor(horizon_hours=24)
    pred_24h = predictor_24h.predict_risk({"ward_id": 1, "rainfall_last_24h": 140.0, "elevation_m": 4.0})
    assert 0.0 <= pred_24h["predicted_probability"] <= 1.0
    assert pred_24h["risk_level"] in ["LOW", "MEDIUM", "HIGH", "CRITICAL"]

    # 3. Explainable AI (SHAP) Engine
    xai = ShapExplainerEngine(horizon_hours=24)
    exp = xai.explain_prediction({"ward_id": 1, "rainfall_last_24h": 140.0, "elevation_m": 4.0})
    assert "top_contributing_factors" in exp
    assert len(exp["top_contributing_factors"]) > 0

    # 4. Drainage Dependency Graph Engine
    graph_chain = get_risk_dependency_chain(db=None, ward_id=1)
    assert graph_chain["ward_id"] == 1
    assert graph_chain["dependency_chain_length"] > 0

    # 5. Civic Priority Engine
    priority = get_priority_assessment_for_ward(db=None, ward_id=1)
    assert priority["priority_level"] in ["P1 — CRITICAL", "P2 — HIGH", "P3 — MEDIUM", "P4 — LOW"]
    assert len(priority["priority_reasons"]) > 0

    rankings = get_priority_rankings(db=None)
    assert len(rankings) == 4
    assert rankings[0]["rank"] == 1

    # 6. Municipal Crew & Budget Optimization Engine (Google OR-Tools MILP)
    opt = solve_municipal_resource_optimization(available_budget=50000.0, available_hours=24.0, team_count=3)
    assert opt["optimization_status"] == "OPTIMAL"
    assert opt["selected_actions_count"] > 0
    assert opt["used_budget_inr"] <= 50000.0

    # 7. What-If Scenario Simulator Engine
    sim = run_what_if_simulation(rainfall_multiplier=2.0, available_budget=30000.0, available_teams=2)
    assert sim["simulation_mode"] == "ACTIVE"
    assert "comparison_delta" in sim

    # 8. Baseline Preservation Verification
    assert BASELINE_STATE["metrics"]["high_risk_wards_count"] == 1
