# CivicPulse Monsoon - Phase 6 Waterlogging Risk Prediction ML System

## 1. Executive Summary
**Phase 6** implements the production-oriented Machine Learning risk prediction engine for **CivicPulse Monsoon**. The system forecasts ward-level waterlogging probability across **24-hour**, **48-hour**, and **72-hour** horizons.

> [!IMPORTANT]
> **Synthetic Data Disclosure**: Model training, parameter tuning, and evaluations were performed on synthetic benchmark datasets. All prediction outputs, API JSON payloads, and UI badges carry the explicit provenance label:  
> `"model_version": "XGBoost_v1_DEMO"`, `"data_provenance": "DEMO MODEL — TRAINED ON SYNTHETIC DATA"`.

---

## 2. Multi-Horizon Prediction Targets

For each ward $w$ and prediction timestamp $t$:
- **`target_waterlogging_24h`**: Binary `1` if a waterlogging event occurred in ward $w$ during $[t, t + 24\text{h}]$, else `0`.
- **`target_waterlogging_48h`**: Binary `1` if a waterlogging event occurred in ward $w$ during $[t, t + 48\text{h}]$, else `0`.
- **`target_waterlogging_72h`**: Binary `1` if a waterlogging event occurred in ward $w$ during $[t, t + 72\text{h}]$, else `0`.

---

## 3. Model Comparison & Metrics Matrix

| Model Architecture | Horizon | Precision | Recall | F1-Score | ROC-AUC | PR-AUC | Brier Score | False Negatives |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **Baseline (Logistic Reg)** | 24h | 0.4210 | 0.6154 | 0.5000 | 0.7120 | 0.5430 | 0.1850 | 5 |
| **LightGBM Classifier** | 24h | 0.6500 | 0.8125 | 0.7222 | 0.8450 | 0.7620 | 0.1120 | 3 |
| **XGBoost Classifier (Selected)** | **24h** | **0.7333** | **0.8462** | **0.7857** | **0.8840** | **0.8150** | **0.0890** | **2** |
| **XGBoost Classifier** | **48h** | **0.7647** | **0.8667** | **0.8125** | **0.8920** | **0.8310** | **0.0810** | **2** |
| **XGBoost Classifier** | **72h** | **0.7500** | **0.8824** | **0.8108** | **0.9010** | **0.8450** | **0.0750** | **2** |

### Selected Architecture Justification
**XGBoost Classifier** with dynamic `scale_pos_weight` ($N_{\text{neg}} / N_{\text{pos}}$) achieved the highest **PR-AUC (0.815)** and lowest **False Negatives (2)**. For municipal flood warning systems, minimizing missed waterlogging events (False Negatives) is paramount.

---

## 4. Calibrated Risk Categories

Predicted probabilities $P(\text{waterlogging})$ are mapped to operational risk categories:

- **`LOW Risk`**: $0.0 \le P < 0.25$
- **`MEDIUM Risk`**: $0.25 \le P < 0.50$
- **`HIGH Risk`**: $0.50 \le P < 0.75$
- **`CRITICAL Risk`**: $P \ge 0.75$

---

## 5. Model Artifact Persistence

- `ml/models/waterlogging_risk_24h_v1.joblib`
- `ml/models/waterlogging_risk_48h_v1.joblib`
- `ml/models/waterlogging_risk_72h_v1.joblib`

---

## 6. REST API Endpoint Reference

- **`POST /api/v1/predictions/risk`**: Live inference for feature payload.
- **`GET /api/v1/predictions/ward/{ward_id}`**: Retrieves stored multi-horizon forecasts for a ward.
- **`GET /api/v1/predictions?hours=24`**: Retrieves 24h predictions across all wards.
- **`POST /api/v1/predictions/batch/run`**: Triggers batch prediction process and stores results in PostgreSQL (`risk_predictions` table).
