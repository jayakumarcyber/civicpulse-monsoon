import sys
import os
import pytest

sys.path.insert(0, os.path.dirname(r"d:\CivicPulse-Monsoon\backend"))
sys.path.insert(0, r"d:\CivicPulse-Monsoon\backend")

from app.services.optimization_service import solve_municipal_resource_optimization

def test_ortools_optimization_budget_constraint():
    res = solve_municipal_resource_optimization(available_budget=50000.0, available_hours=24.0, team_count=3)
    assert res["optimization_status"] == "OPTIMAL"
    assert res["used_budget_inr"] <= 50000.0
    assert res["selected_actions_count"] > 0

def test_ortools_optimization_skill_matching():
    res = solve_municipal_resource_optimization(available_budget=50000.0, available_hours=24.0, team_count=3)
    for act in res["selected_actions"]:
        # Drainage actions must be assigned to drainage or general maintenance teams
        if act["action_type"] == "drain_cleaning":
            assert act["assigned_team_id"] in ["TEAM_01", "TEAM_02"]

def test_ortools_optimization_capacity_limits():
    res = solve_municipal_resource_optimization(available_budget=50000.0, available_hours=24.0, team_count=3)
    team_counts = {}
    for act in res["selected_actions"]:
        tid = act["assigned_team_id"]
        team_counts[tid] = team_counts.get(tid, 0) + 1
        assert team_counts[tid] <= 3  # Daily capacity limit is 3

def test_infeasible_budget_scenario():
    res = solve_municipal_resource_optimization(available_budget=1000.0, available_hours=24.0, team_count=3)
    assert res["optimization_status"] == "NO_FEASIBLE_PLAN"
    assert res["selected_actions_count"] == 0
    assert "Insufficient budget" in res["infeasibility_reason"]

def test_infeasible_zero_teams_scenario():
    res = solve_municipal_resource_optimization(available_budget=50000.0, available_hours=24.0, team_count=0)
    assert res["optimization_status"] == "NO_FEASIBLE_PLAN"
    assert res["selected_actions_count"] == 0

def test_optimization_reproducibility():
    res1 = solve_municipal_resource_optimization(available_budget=50000.0, available_hours=24.0, team_count=3)
    res2 = solve_municipal_resource_optimization(available_budget=50000.0, available_hours=24.0, team_count=3)
    assert res1["used_budget_inr"] == res2["used_budget_inr"]
    assert res1["selected_actions_count"] == res2["selected_actions_count"]

def test_before_vs_after_comparison():
    res = solve_municipal_resource_optimization(available_budget=50000.0, available_hours=24.0, team_count=3)
    comp = res["comparison"]
    assert "optimized_plan_benefit" in comp
    assert "unplanned_baseline_benefit" in comp
    assert comp["optimized_plan_benefit"] >= comp["unplanned_baseline_benefit"]
