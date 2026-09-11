# CivicPulse Monsoon - Phase 5 Technical Analysis & Pattern Specification

## 1. Overview & Objectives
**Phase 5** establishes the analytical foundation for rainfall accumulation, historical waterlogging incident patterns, ward-level recurrence rates, and chronological ML dataset splitting without data leakage.

> [!IMPORTANT]
> **Correlation vs. Causation Disclaimer**: High rainfall accumulation and low terrain elevation correlate with historical waterlogging events, but correlation alone does not imply direct causation. All analytics outputs are explicitly tagged `"HISTORICAL ANALYSIS"` and `"DEMO / SYNTHETIC DATA"`.

---

## 2. Feature Formulas & Window Specifications

### A. Rolling Rainfall Accumulations
Calculated from observed weather gauge readings at target observation time $t$:
- **`rainfall_1h`**: $\sum R_i$ where $t - 1\text{h} \le t_i \le t$
- **`rainfall_6h`**: $\sum R_i$ where $t - 6\text{h} \le t_i \le t$
- **`rainfall_12h`**: $\sum R_i$ where $t - 12\text{h} \le t_i \le t$
- **`rainfall_24h`**: $\sum R_i$ where $t - 24\text{h} \le t_i \le t$
- **`rainfall_48h`**: $\sum R_i$ where $t - 48\text{h} \le t_i \le t$
- **`rainfall_72h`**: $\sum R_i$ where $t - 72\text{h} \le t_i \le t$

### B. Rolling Incident Aggregations
- **`incident_count_7d`**: Count of incident logs in ward within $t - 7\text{d} \le t_i \le t$.
- **`incident_count_30d`**: Count of incident logs in ward within $t - 30\text{d} \le t_i \le t$.
- **`incident_count_90d`**: Count of incident logs in ward within $t - 90\text{d} \le t_i \le t$.
- **`days_since_last_incident`**: $(t - \max(t_{\text{prev}})) / 86400$ seconds.

---

## 3. Hotspot Classification Thresholds

Wards are classified into recurring hotspot tiers based on historical incident volume:

- **`HIGH Hotspot`**: $\ge 10$ documented historical incidents in ward.
- **`MEDIUM Hotspot`**: $4 \text{ to } 9$ documented historical incidents in ward.
- **`LOW Hotspot`**: $< 4$ documented historical incidents in ward.

---

## 4. Data Leakage Safeguards

To prevent lookahead bias (data leakage) in future ML model training:
1. **Temporal Filtering**: For any feature calculated at prediction timestamp $T_P$, only data with $t_i \le T_P$ is included. Future rainfall or future incident reports ($t_i > T_P$) are strictly excluded.
2. **Chronological Splitting**: Dataset is split chronologically into **Train (60%)**, **Validation (20%)**, and **Test (20%)** without random shuffling.
