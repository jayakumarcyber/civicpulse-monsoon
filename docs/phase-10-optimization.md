# CivicPulse Monsoon - Phase 10 Municipal Crew & Budget Optimization Engine

## 1. Overview & Google OR-Tools Mathematical Model
**Phase 10** introduces the **Municipal Resource and Budget Optimization Engine** for **CivicPulse Monsoon**, recommending how limited maintenance crews, working hours, and budget should be allocated across high-priority waterlogging-risk locations using **Google OR-Tools** (Mixed-Integer Linear Programming / MILP Solver).

> [!IMPORTANT]
> **Decision-Support Recommendation Disclaimer**:  
> System-generated intervention recommendations optimize resource efficiency under constraints. They do NOT claim guaranteed flood prevention or exact financial savings.

---

## 2. MILP Mathematical Formulation

### Objective Function
$$\max \sum_{a \in A} \sum_{t \in T} \text{ExpectedBenefit}(a) \cdot x_{a, t}$$

### Constraints
1. **Budget Constraint**:
   $$\sum_{a \in A} \sum_{t \in T} \text{Cost}(a) \cdot x_{a, t} \le \text{AvailableBudget}$$
2. **Team Working Hours**:
   $$\sum_{a \in A} \text{Duration}(a) \cdot x_{a, t} \le \text{WorkingHours}(t), \quad \forall t \in T$$
3. **Daily Team Capacity**:
   $$\sum_{a \in A} x_{a, t} \le \text{Capacity}(t), \quad \forall t \in T$$
4. **Skill Eligibility**:
   $$x_{a, t} = 0 \quad \text{if } \text{Skill}(t) \ne \text{RequiredSkill}(a)$$
5. **Single Assignment**:
   $$\sum_{t \in T} x_{a, t} \le 1, \quad \forall a \in A$$

---

## 3. Sample Benchmark Optimization Result (`POST /api/v1/optimization/run`)

```json
{
  "run_id": "OPT_8F3A29B1",
  "optimization_status": "OPTIMAL",
  "available_budget_inr": 50000.0,
  "used_budget_inr": 49000.0,
  "remaining_budget_inr": 1000.0,
  "available_hours": 24.0,
  "total_teams_count": 3,
  "used_teams_count": 3,
  "selected_actions_count": 5,
  "total_expected_benefit_score": 399.5,
  "selected_actions": [
    {
      "action_id": "ACT_001",
      "ward_name": "Ward G/North (Dadar)",
      "name": "Dadar TT Circle Outfall Desilting",
      "priority_level": "P1 — CRITICAL",
      "assigned_team_name": "Stormwater Drainage Crew A",
      "estimated_cost_inr": 12000.0,
      "estimated_duration_hours": 4.0,
      "expected_benefit": 92.5,
      "recommendation_reason": "Selected for Ward G/North (Dadar) (P1 — CRITICAL): Matches Stormwater Drainage Crew A (drainage skill)."
    },
    {
      "action_id": "ACT_006",
      "ward_name": "Ward H/East (Bandra East)",
      "name": "BKC Connector Emergency Pump Setup",
      "priority_level": "P2 — HIGH",
      "assigned_team_name": "Road & Culvert Repair Crew C",
      "estimated_cost_inr": 15000.0,
      "estimated_duration_hours": 5.0,
      "expected_benefit": 88.0,
      "recommendation_reason": "Selected for Ward H/East (Bandra East) (P2 — HIGH): Matches Road & Culvert Repair Crew C (road_maintenance skill)."
    }
  ],
  "comparison": {
    "unplanned_baseline_benefit": 319.5,
    "optimized_plan_benefit": 399.5,
    "estimated_potential_impact_reduction": "+25.0% improvement over baseline"
  },
  "disclaimer": "DECISION SUPPORT RECOMMENDATION: OR-Tools allocation optimizes resource efficiency, not guaranteed flood prevention."
}
```

---

## 4. REST API Endpoint Reference

- **`POST /api/v1/optimization/run`**: Solves MILP knapsack problem with input budget, hours, and team count.
- **`GET /api/v1/optimization/latest`**: Returns the latest optimization recommendation.
- **`GET /api/v1/optimization/scenarios`**: Returns predefined demo benchmark scenarios (`Full Budget`, `Constrained Budget`, `Severe Resource Deficit`).
