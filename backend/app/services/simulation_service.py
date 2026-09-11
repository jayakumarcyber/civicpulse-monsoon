from typing import List, Dict, Any, Optional
from datetime import datetime, timezone
import uuid
from sqlalchemy.orm import Session

from ml.inference.predictor import RiskPredictor
from app.services.impact_service import get_priority_rankings, compute_priority_score, classify_priority_level
from app.services.optimization_service import solve_municipal_resource_optimization

BASELINE_STATE = {
    "rainfall_multiplier": 1.0,
    "rainfall_24h_mm": 140.0,
    "available_teams": 3,
    "available_hours": 24.0,
    "available_budget_inr": 50000.0,
    "metrics": {
        "high_risk_wards_count": 1,
        "critical_p1_wards_count": 1,
        "total_potential_exposure": 8500,
        "selected_actions_count": 6,
        "used_budget_inr": 48500.0,
        "used_teams_count": 3
    }
}

PRESET_SCENARIOS = [
    {
        "preset_id": "PRESET_NORMAL_RAIN",
        "name": "Normal Rain Scenario (0.5x Rain)",
        "rainfall_multiplier": 0.5,
        "available_teams": 3,
        "available_hours": 24.0,
        "available_budget_inr": 50000.0,
        "description": "Moderate monsoon rainfall scenario (70mm 24h)."
    },
    {
        "preset_id": "PRESET_HEAVY_RAIN",
        "name": "Heavy Rain Scenario (1.5x Rain)",
        "rainfall_multiplier": 1.5,
        "available_teams": 3,
        "available_hours": 24.0,
        "available_budget_inr": 50000.0,
        "description": "Severe heavy downpour scenario (210mm 24h)."
    },
    {
        "preset_id": "PRESET_EXTREME_RAIN",
        "name": "Extreme Cloudburst Scenario (2.2x Rain)",
        "rainfall_multiplier": 2.2,
        "available_teams": 3,
        "available_hours": 24.0,
        "available_budget_inr": 50000.0,
        "description": "Extreme flash flood cloudburst scenario (308mm 24h)."
    },
    {
        "preset_id": "PRESET_LIMITED_WORKFORCE",
        "name": "Limited Workforce Scenario (1 Team)",
        "rainfall_multiplier": 1.0,
        "available_teams": 1,
        "available_hours": 8.0,
        "available_budget_inr": 50000.0,
        "description": "Shortage of available maintenance crews (1 crew available)."
    },
    {
        "preset_id": "PRESET_LIMITED_BUDGET",
        "name": "Limited Budget Scenario (₹15,000)",
        "rainfall_multiplier": 1.0,
        "available_teams": 3,
        "available_hours": 24.0,
        "available_budget_inr": 15000.0,
        "description": "Municipal emergency budget constraint (₹15,000 limit)."
    },
    {
        "preset_id": "PRESET_WORST_CASE",
        "name": "Combined Worst Case (2.0x Rain + 1 Team + ₹10,000)",
        "rainfall_multiplier": 2.0,
        "available_teams": 1,
        "available_hours": 8.0,
        "available_budget_inr": 10000.0,
        "description": "Extreme downpour combined with severe resource deficit."
    }
]

def run_what_if_simulation(
    rainfall_multiplier: float = 1.0,
    available_budget: float = 50000.0,
    available_hours: float = 24.0,
    available_teams: int = 3,
    db: Optional[Session] = None
) -> Dict[str, Any]:
    """Execute multi-stage simulation pipeline: ML Risk -> Priority -> OR-Tools Optimization."""
    scenario_id = f"SIM_{uuid.uuid4().hex[:8].upper()}"

    # Stage 1: Recalculate ML Risk Predictions
    predictor = RiskPredictor(horizon_hours=24)
    simulated_rainfall_24h = round(140.0 * rainfall_multiplier, 1)

    high_risk_count = 0
    simulated_ward_risks = []
    
    for w_id, elev in [(1, 4.0), (2, 8.0), (3, 12.0), (4, 18.0)]:
        pred = predictor.predict_risk({"ward_id": w_id, "rainfall_last_24h": simulated_rainfall_24h, "elevation_m": elev})
        prob = pred["predicted_probability"]
        r_level = pred["risk_level"]
        if r_level in ["HIGH", "CRITICAL"]:
            high_risk_count += 1
        simulated_ward_risks.append({
            "ward_id": w_id,
            "predicted_probability": prob,
            "risk_level": r_level
        })

    # Stage 2: Recalculate Civic Priority Scores & Levels
    critical_p1_count = 0
    total_exposure = 0
    
    for wr in simulated_ward_risks:
        # Base impact
        pop_exp = int(8500 * (1.0 if wr["ward_id"] == 1 else (0.6 if wr["ward_id"] == 2 else 0.3)))
        total_exposure += int(pop_exp * (rainfall_multiplier ** 0.5))
        
        # Priority score
        score = min(100.0, wr["predicted_probability"] * 50.0 + (pop_exp / 8500.0) * 40.0)
        p_level = classify_priority_level(score)
        if p_level.startswith("P1"):
            critical_p1_count += 1

    # Stage 3: Recalculate OR-Tools Crew & Budget Optimization
    opt_res = solve_municipal_resource_optimization(
        available_budget=available_budget,
        available_hours=available_hours,
        team_count=available_teams,
        db=db
    )

    # Baseline vs Scenario Differences
    base_m = BASELINE_STATE["metrics"]
    diff_high_risk = high_risk_count - base_m["high_risk_wards_count"]
    diff_p1 = critical_p1_count - base_m["critical_p1_wards_count"]
    diff_exposure = total_exposure - base_m["total_potential_exposure"]
    diff_selected = opt_res.get("selected_actions_count", 0) - base_m["selected_actions_count"]
    diff_budget = opt_res.get("used_budget_inr", 0.0) - base_m["used_budget_inr"]

    return {
        "scenario_id": scenario_id,
        "simulation_mode": "ACTIVE",
        "parameters": {
            "rainfall_multiplier": rainfall_multiplier,
            "simulated_rainfall_24h_mm": simulated_rainfall_24h,
            "available_budget_inr": available_budget,
            "available_hours": available_hours,
            "available_teams": available_teams
        },
        "baseline": BASELINE_STATE,
        "simulated_scenario_results": {
            "high_risk_wards_count": high_risk_count,
            "critical_p1_wards_count": critical_p1_count,
            "total_potential_exposure": total_exposure,
            "optimization_status": opt_res.get("optimization_status", "FEASIBLE"),
            "selected_actions_count": opt_res.get("selected_actions_count", 0),
            "used_budget_inr": opt_res.get("used_budget_inr", 0.0),
            "used_teams_count": opt_res.get("used_teams_count", 0),
            "selected_actions": opt_res.get("selected_actions", []),
            "unselected_actions": opt_res.get("unselected_actions", [])
        },
        "comparison_delta": {
            "high_risk_wards_delta": f"{'+' if diff_high_risk >= 0 else ''}{diff_high_risk}",
            "critical_p1_wards_delta": f"{'+' if diff_p1 >= 0 else ''}{diff_p1}",
            "potential_exposure_delta": f"{'+' if diff_exposure >= 0 else ''}{diff_exposure:,}",
            "selected_actions_delta": f"{'+' if diff_selected >= 0 else ''}{diff_selected}",
            "used_budget_delta_inr": f"{'+' if diff_budget >= 0 else ''}{diff_budget:,.2f}"
        },
        "assumptions_disclaimer": "SIMULATED ASSUMPTION: What-if outputs represent hypothetical decision-support scenarios and do NOT mutate real database records."
    }

def get_preset_scenarios() -> List[Dict[str, Any]]:
    """Return list of predefined preset simulation scenarios."""
    return PRESET_SCENARIOS
