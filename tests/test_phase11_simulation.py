import sys
import os
import pytest

sys.path.insert(0, os.path.dirname(r"d:\CivicPulse-Monsoon\backend"))
sys.path.insert(0, r"d:\CivicPulse-Monsoon\backend")

from app.services.simulation_service import (
    run_what_if_simulation,
    get_preset_scenarios,
    BASELINE_STATE
)

def test_simulation_execution_basic():
    res = run_what_if_simulation(rainfall_multiplier=1.5, available_budget=50000.0, available_hours=24.0, available_teams=3)
    assert res["simulation_mode"] == "ACTIVE"
    assert "scenario_id" in res
    assert res["parameters"]["rainfall_multiplier"] == 1.5
    assert "simulated_scenario_results" in res
    assert "comparison_delta" in res

def test_rainfall_multiplier_recalculation():
    # Normal rain vs Extreme rain
    res_normal = run_what_if_simulation(rainfall_multiplier=0.5)
    res_extreme = run_what_if_simulation(rainfall_multiplier=2.2)

    assert res_extreme["simulated_scenario_results"]["total_potential_exposure"] >= res_normal["simulated_scenario_results"]["total_potential_exposure"]
    assert res_extreme["simulated_scenario_results"]["high_risk_wards_count"] >= res_normal["simulated_scenario_results"]["high_risk_wards_count"]

def test_resource_reduction_recalculation():
    # Full resource vs Resource deficit
    res_full = run_what_if_simulation(rainfall_multiplier=1.0, available_budget=50000.0, available_teams=3)
    res_deficit = run_what_if_simulation(rainfall_multiplier=1.0, available_budget=10000.0, available_teams=1)

    assert res_deficit["simulated_scenario_results"]["selected_actions_count"] <= res_full["simulated_scenario_results"]["selected_actions_count"]
    assert res_deficit["simulated_scenario_results"]["used_budget_inr"] <= 10000.0

def test_baseline_preservation():
    # Running a simulation must not mutate the original baseline state metrics
    original_baseline_exposure = BASELINE_STATE["metrics"]["total_potential_exposure"]
    res = run_what_if_simulation(rainfall_multiplier=2.5, available_budget=100000.0, available_teams=5)
    
    assert BASELINE_STATE["metrics"]["total_potential_exposure"] == original_baseline_exposure
    assert res["baseline"]["metrics"]["total_potential_exposure"] == original_baseline_exposure

def test_preset_scenarios():
    presets = get_preset_scenarios()
    assert len(presets) == 6
    assert any(p["preset_id"] == "PRESET_EXTREME_RAIN" for p in presets)
    assert any(p["preset_id"] == "PRESET_WORST_CASE" for p in presets)

def test_simulation_reproducibility():
    res1 = run_what_if_simulation(rainfall_multiplier=1.5, available_budget=30000.0, available_teams=2)
    res2 = run_what_if_simulation(rainfall_multiplier=1.5, available_budget=30000.0, available_teams=2)
    
    assert res1["simulated_scenario_results"]["total_potential_exposure"] == res2["simulated_scenario_results"]["total_potential_exposure"]
    assert res1["simulated_scenario_results"]["selected_actions_count"] == res2["simulated_scenario_results"]["selected_actions_count"]
