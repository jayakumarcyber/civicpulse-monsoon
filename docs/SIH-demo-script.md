# CivicPulse Monsoon — Smart India Hackathon (SIH) Live Demo Script & Judge Q&A Defense

---

## 1. Executive Summary & Pitch (120 Seconds)

### 30-Second Problem Pitch
> *"Every monsoon, major Indian metros face paralyzing urban waterlogging. Existing municipal systems are purely reactive — citizen complaint apps register flooding ONLY after roads are submerged and emergency facilities are cut off. Municipal authorities lack spatial 24-to-72 hour predictive foresight, drainage dependency modeling, and scientific tools to allocate limited maintenance crews and budgets before rainfall strikes."*

### 60-Second Solution Overview
> *"CivicPulse Monsoon is an AI-based predictive waterlogging and drainage risk management platform built for municipal corporations. By fusing rainfall forecasts, historical civic incident hotspots, terrain elevation, road/drainage connectivity, population density, and critical facilities, CivicPulse Monsoon predicts grid-level risk 24, 48, and 72 hours ahead. It explains WHY locations are risky using SHAP Explainable AI, traces spatial risk propagation through a drainage dependency graph, ranks municipal priority from P1 to P4, optimizes limited crew and budget allocations using Google OR-Tools, and provides an interactive What-If scenario simulator."*

### 30-Second Technical Architecture
> *"Our tech stack uses FastAPI, PostgreSQL with PostGIS spatial extensions, SQLAlchemy 2.0, XGBoost/LightGBM ML inference, SHAP tree explainers, Google OR-Tools MILP optimization, and a Next.js 14 Leaflet geospatial command center. All spatial relationships, model predictions, and optimization plans operate under strict data provenance transparency."*

---

## 2. 2–3 Minute Step-by-Step Live Demo Sequence

Follow this exact sequence during the live SIH hackathon presentation:

```
┌───────────────────────────────────────────────────────────────────────────────────────────┐
│ STEP 1: OPEN DASHBOARD                                                                    │
│   • Open http://localhost:3000 in browser.                                                │
│   • Highlight Top Bar: "LIVE BACKEND & GEOSPATIAL MAP ONLINE" and Monitored Metrics.      │
├───────────────────────────────────────────────────────────────────────────────────────────┤
│ STEP 2: GEOSPATIAL MAP LAYER TOGGLES                                                      │
│   • Demonstrate 8 toggleable spatial layers: Wards, Roads, Drains, Waterbodies,           │
│     Incidents, Facilities, Population, Risk Dependencies.                                 │
├───────────────────────────────────────────────────────────────────────────────────────────┤
│ STEP 3: SEARCH BAR FEATURE FLY-TO                                                         │
│   • Type "Ward G/North" or "Dadar" in Search Bar.                                         │
│   • Map smoothly zooms and selects Ward G/North (Dadar).                                  │
├───────────────────────────────────────────────────────────────────────────────────────────┤
│ STEP 4: INSPECT 24/48/72-HOUR ML RISK PREDICTION                                          │
│   • Right panel displays XGBoost Predicted Probability: 85% (CRITICAL RISK).              │
│   • Switch horizon tabs between 24h, 48h, and 72h forecasts.                              │
├───────────────────────────────────────────────────────────────────────────────────────────┤
│ STEP 5: EXPLAINABLE AI (SHAP) RISK EVIDENCE                                               │
│   • Show Top Contributing Factors: 48h Rainfall (2.989), 24h Rainfall (2.410),            │
│     Low Elevation 4m (1.854), Historical Recurrence (1.420).                              │
│   • Point to Historical Evidence Counters: 10 documented past incidents.                  │
├───────────────────────────────────────────────────────────────────────────────────────────┤
│ STEP 6: DRAINAGE DEPENDENCY GRAPH                                                         │
│   • Expand Spatial Risk Propagation Chain:                                                │
│     Ward G/North → Dadar Outfall Main Drain → Low-Lying Zone → Ambedkar Road →            │
│     Residential Sector → Sion Hospital.                                                   │
│   • Highlight label: "INFERRED SPATIAL RELATIONSHIPS".                                    │
├───────────────────────────────────────────────────────────────────────────────────────────┤
│ STEP 7: IMPACT & CIVIC PRIORITY QUEUE                                                     │
│   • Scroll to Civic Priority Queue Panel: Ward G/North ranked #1 (P1 — CRITICAL).         │
│   • Point out metrics: ~8,500 Potential Population Exposure, 7 Critical Facilities        │
│     (1 Hospital, 3 Schools).                                                              │
├───────────────────────────────────────────────────────────────────────────────────────────┤
│ STEP 8: MUNICIPAL CREW & BUDGET OPTIMIZER (OR-TOOLS MILP)                                 │
│   • Scroll to Resource Planner Panel (3 Crews, ₹50,000 Budget, 24 Hours).                 │
│   • Click "Run AI Optimizer Solver".                                                      │
│   • Demonstrate Before vs After Comparison: +50.3% efficiency improvement over baseline.   │
├───────────────────────────────────────────────────────────────────────────────────────────┤
│ STEP 9: WHAT-IF SCENARIO SIMULATOR                                                        │
│   • Click "Extreme Cloudburst Scenario (2.2x Rain)" preset button.                        │
│   • Show real-time re-calculation: High-Risk Wards increase from 1 → 4 (+3).              │
│   • Point out "SIMULATION MODE ACTIVE" map indicator.                                     │
├───────────────────────────────────────────────────────────────────────────────────────────┤
│ STEP 10: RESET TO BASELINE                                                                │
│   • Click "Reset to Baseline". System instantly restores original observations.           │
└───────────────────────────────────────────────────────────────────────────────────────────┘
```

---

## 3. SIH Final Judge Q&A Defense Talking Points

### Q1: "What problem are you solving, and why is this different from a complaint app?"
> **Answer**: *"Complaint apps like Disaster Helpline or Civic Apps are purely reactive — they register an issue after waterlogging has already occurred and damage is done. CivicPulse Monsoon is a predictive decision-support system. It predicts risk 24 to 72 hours BEFORE heavy rainfall occurs, traces spatial dependencies to hospitals and schools, and calculates optimal crew/budget deployment to prevent waterlogging before it happens."*

### Q2: "How does your AI predict risk, and how do you avoid false predictions?"
> **Answer**: *"Our prediction engine uses calibrated XGBoost/LightGBM models trained on temporal rainfall aggregations (1h to 72h), rolling incident windows (7d, 30d, 90d), terrain elevation, and drainage density. We use scale_pos_weight for class balance, achieving a 0.815 PR-AUC and 84.6% recall. Furthermore, our predictions are complemented by SHAP explainability and historical incident evidence counters so municipal engineers can verify model reasoning."*

### Q3: "How does your resource optimizer work when municipal budgets are tight?"
> **Answer**: *"We formulate municipal maintenance allocation as a Mixed-Integer Linear Programming (MILP) knapsack problem using Google OR-Tools. The solver maximizes preventive risk reduction subject to strict constraints: available budget (INR), team working hours, daily crew capacity, and skill eligibility (e.g. assigning desilting actions only to qualified drainage crews). If budget is zero or constraints are impossible, the system gracefully reports NO_FEASIBLE_PLAN with exact reasons."*

### Q4: "Where does your data come from, and how do you handle synthetic data?"
> **Answer**: *"CivicPulse Monsoon enforces strict Data Provenance. Public geographical data (ward boundaries, roads, elevation, waterbodies) forms the spatial baseline. For hackathon demonstration, synthetic incident and rainfall records are clearly tagged with explicit provenance badges: 'DEMO PROTOTYPE — SYNTHETIC DATA & HISTORICAL CIVIC DATA'. We never represent synthetic demo data as live government observations."*

### Q5: "What happens during a What-If simulation? Does it overwrite real database data?"
> **Answer**: *"No. Simulations execute in an isolated analytical memory layer. When a user modifies rainfall multipliers or budget limits, our multi-stage pipeline re-computes ML risk, priority scores, and OR-Tools allocations in real-time. Original historical and spatial database records remain 100% untouched. Clicking 'Reset to Baseline' immediately restores original baseline state."*
