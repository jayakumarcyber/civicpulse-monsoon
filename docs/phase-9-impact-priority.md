# CivicPulse Monsoon - Phase 9 Impact Estimation & Civic Priority Engine

## 1. Overview & Decision Support Purpose
**Phase 9** introduces the **Impact Estimation and Civic Priority Engine** for **CivicPulse Monsoon**, converting ML risk predictions, spatial population density, critical facility exposure, infrastructure assets, and historical recurrence into an interpretable **Civic Priority Queue ($P1$ to $P4$)**.

> [!IMPORTANT]
> **Risk vs. Priority Distinction**:  
> - **RISK LEVEL**: The probability ($0.0 - 1.0$) that waterlogging may occur based on rainfall and terrain.  
> - **CIVIC PRIORITY LEVEL**: The urgency of preventive municipal action based on Risk + Potential Population Exposure + Critical Facilities (e.g. hospitals, schools).

---

## 2. Configurable Priority Scoring Formula

$$\text{PriorityScore} = W_{\text{risk}} \cdot S_{\text{risk}} + W_{\text{pop}} \cdot S_{\text{pop}} + W_{\text{fac}} \cdot S_{\text{fac}} + W_{\text{infra}} \cdot S_{\text{infra}} + W_{\text{rec}} \cdot S_{\text{rec}}$$

### Configurable Weights Settings (`app/core/config.py`)
- `PRIORITY_WEIGHT_RISK` = `0.35`
- `PRIORITY_WEIGHT_POPULATION` = `0.25`
- `PRIORITY_WEIGHT_CRITICAL_FACILITIES` = `0.20`
- `PRIORITY_WEIGHT_INFRASTRUCTURE` = `0.10`
- `PRIORITY_WEIGHT_HISTORICAL_RECURRENCE` = `0.10`
- **Label**: `"DEMO / CONFIGURABLE PRIORITY WEIGHTS"`

### Priority Level Classification Thresholds
- **`P1 — CRITICAL`**: $\text{Priority Score} \ge 75.0$
- **`P2 — HIGH`**: $50.0 \le \text{Priority Score} < 75.0$
- **`P3 — MEDIUM`**: $25.0 \le \text{Priority Score} < 50.0$
- **`P4 — LOW`**: $\text{Priority Score} < 25.0$

---

## 3. Sample Priority Queue Ranking (`GET /api/v1/priority/rankings`)

| Rank | Ward | Risk Signal | Potential Pop. Exposure | Critical Facilities | Priority Score | Priority Level |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **#1** | Ward G/North (Dadar) | **CRITICAL (85%)** | 8,500 | 7 (1 Hospital, 3 Schools) | **82.4** | **P1 — CRITICAL** |
| **#2** | Ward F/North (Matunga) | **HIGH (62%)** | 5,200 | 4 (2 Schools, 1 Emergency) | **58.6** | **P2 — HIGH** |
| **#3** | Ward H/East (Bandra East) | **MEDIUM (41%)** | 9,000 | 2 (1 School, 1 Transit) | **44.2** | **P3 — MEDIUM** |
| **#4** | Ward K/East (Andheri East) | **LOW (18%)** | 3,100 | 1 (1 School) | **21.8** | **P4 — LOW** |

---

## 4. REST API Endpoint Reference

- **`GET /api/v1/impact/ward/{ward_id}`**: Returns spatial impact assessment metrics (potential population exposure, facilities breakdown, infrastructure counts).
- **`GET /api/v1/impact/high-risk`**: Returns impact assessments for all high-risk wards.
- **`GET /api/v1/priority/rankings`**: Returns full ranked civic priority queue ($P1$ to $P4$) sorted by priority score descending.
- **`GET /api/v1/priority/ward/{ward_id}`**: Returns detailed priority assessment, score breakdown, and data-driven rationale list.
