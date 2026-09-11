# CivicPulse Monsoon - Phase 11 What-If Scenario Simulator

## 1. Overview & Multi-Stage Simulation Engine
**Phase 11** introduces the **What-If Scenario Simulator** for **CivicPulse Monsoon**, empowering municipal decision-makers to simulate hypothetical monsoon conditions (rainfall intensity, available maintenance crews, working hours, and budget) and immediately observe how **ML Risk**, **Civic Priority**, and **OR-Tools Optimization** dynamically adjust.

> [!IMPORTANT]
> **Baseline Preservation & Simulation Disclaimer**:  
> Running simulations re-calculates analytical models in real-time under assumed parameters. It **NEVER** mutates, overwrites, or deletes historical, real, or public database records. Clicking **"Reset to Baseline"** instantly restores original baseline observations.

---

## 2. Multi-Stage Recalculation Flow

```
[ User Scenario Inputs: Rainfall Multiplier, Budget, Hours, Teams ]
                         │
                         ▼
┌─────────────────────────────────────────────────────────────────┐
│ Stage 1: ML Risk Recalculation (Phase 6 XGBoost Engine)         │
│   • Re-computes 24h, 48h, 72h risk probabilities for all wards   │
└─────────────────────────────────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────────┐
│ Stage 2: Priority Engine Recalculation (Phase 9 Scorer)         │
│   • Re-computes Priority Scores (0-100) & Levels (P1 to P4)     │
└─────────────────────────────────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────────┐
│ Stage 3: OR-Tools Optimization Recalculation (Phase 10 Solver) │
│   • Solves MILP Knapsack for optimal crew & budget allocation   │
└─────────────────────────────────────────────────────────────────┘
                         │
                         ▼
[ Baseline vs. Scenario Comparison & Impact Delta Generation ]
```

---

## 3. Preset Simulation Scenarios

1. **Normal Rain Scenario (0.5x Rain)**: Moderate monsoon rainfall scenario ($70\text{mm}$ 24h).
2. **Heavy Rain Scenario (1.5x Rain)**: Severe heavy downpour scenario ($210\text{mm}$ 24h).
3. **Extreme Cloudburst Scenario (2.2x Rain)**: Extreme flash flood cloudburst scenario ($308\text{mm}$ 24h).
4. **Limited Workforce Scenario (1 Team)**: Shortage of maintenance crews (1 crew available).
5. **Limited Budget Scenario (₹15,000)**: Municipal emergency budget constraint (₹15,000 limit).
6. **Combined Worst Case (2.0x Rain + 1 Team + ₹10,000)**: Extreme downpour combined with severe resource deficit.

---

## 4. Sample Simulation Output (`POST /api/v1/simulation/run`)

```json
{
  "scenario_id": "SIM_9F2B48A1",
  "simulation_mode": "ACTIVE",
  "parameters": {
    "rainfall_multiplier": 1.5,
    "simulated_rainfall_24h_mm": 210.0,
    "available_budget_inr": 50000.0,
    "available_hours": 24.0,
    "available_teams": 3
  },
  "baseline": {
    "rainfall_multiplier": 1.0,
    "available_budget_inr": 50000.0,
    "metrics": {
      "high_risk_wards_count": 1,
      "critical_p1_wards_count": 1,
      "total_potential_exposure": 8500,
      "selected_actions_count": 6,
      "used_budget_inr": 48500.0
    }
  },
  "simulated_scenario_results": {
    "high_risk_wards_count": 3,
    "critical_priority_wards_count": 2,
    "total_potential_exposure": 10410,
    "optimization_status": "OPTIMAL",
    "selected_actions_count": 6,
    "used_budget_inr": 48500.0
  },
  "comparison_delta": {
    "high_risk_wards_delta": "+2",
    "critical_p1_wards_delta": "+1",
    "potential_exposure_delta": "+1,910",
    "selected_actions_delta": "+0",
    "used_budget_delta_inr": "+0.00"
  },
  "assumptions_disclaimer": "SIMULATED ASSUMPTION: What-if outputs represent hypothetical decision-support scenarios and do NOT mutate real database records."
}
```

---

## 5. REST API Endpoint Reference

- **`POST /api/v1/simulation/run`**: Solves multi-stage simulation with scenario parameters and returns baseline comparison.
- **`GET /api/v1/simulation/scenarios`**: Returns list of preset scenario triggers.
- **`GET /api/v1/simulation/{scenario_id}`**: Returns scenario simulation result by ID.
- **`POST /api/v1/simulation/reset`**: Resets simulator to original baseline state without modifying database observations.
