# CivicPulse Monsoon - Data Pipeline Specification & Reference Guide

## 1. Executive Summary
The **CivicPulse Monsoon Data Pipeline** processes, cleans, validates, spatially joins, and engineers ML-ready features from multi-source data (rainfall, civic incidents, ward boundaries, roads, drains, elevation, population density, critical facilities).

All generated features are saved into a versioned dataset (`data/processed/features.parquet` and `data/processed/features.csv`) where each row represents a **`[WARD_ID + TIMESTAMP]`** temporal-spatial observation window.

> [!IMPORTANT]
> **Data Integrity & Labeling Rule**: Synthetic demo records generated for development and testing are explicitly tagged with `"data_source_type": "SYNTHETIC_DEMO_DATA"`.

---

## 2. Directory Hierarchy

```
data/
├── raw/                          # Raw ingested CSV / GeoJSON datasets
│   ├── rainfall/
│   ├── incidents/
│   ├── roads/
│   ├── drains/
│   ├── waterbodies/
│   ├── wards/
│   ├── elevation/
│   ├── population/
│   └── facilities/
├── processed/                    # Cleaned & feature-engineered outputs (features.parquet, features.csv)
├── synthetic/                    # Generated synthetic benchmark datasets
└── schemas/                      # JSON validation schemas
```

---

## 3. Data Cleaning & Quality Control Rules

1. **CRS Normalization**: All spatial geometries are reprojected into a single project-wide reference system: **`EPSG:4326` (WGS84)**.
2. **Coordinate Boundaries**: Validates `-90.0 <= latitude <= 90.0` and `-180.0 <= longitude <= 180.0`. Rows with `(0.0, 0.0)` or missing coordinates are dropped.
3. **Rainfall Boundaries**: Enforces `rainfall_mm >= 0.0` and clips non-physical extreme sensor spikes (> 1000.0 mm/hr).
4. **Geometry Repair**: Invalid polygons are repaired using Shapely's `make_valid` utility; empty geometries are removed.
5. **Deduplication**: Drops duplicate records based on `[timestamp, latitude, longitude, forecast_hours]`.

---

## 4. Engineered Feature Matrix Schema

Output File: **`data/processed/features.parquet`** / **`data/processed/features.csv`**

| Column Name | Feature Type | Description |
| :--- | :--- | :--- |
| **`ward_id`** | Identifier | Unique municipal ward numeric ID |
| **`timestamp`** | Temporal Key | UTC ISO timestamp observation key |
| **`rainfall_last_1h`** | Temporal Feature | Accumulated rainfall over the preceding 1 hour (mm) |
| **`rainfall_last_6h`** | Temporal Feature | Accumulated rainfall over the preceding 6 hours (mm) |
| **`rainfall_last_24h`** | Temporal Feature | Accumulated rainfall over the preceding 24 hours (mm) |
| **`rainfall_last_48h`** | Temporal Feature | Accumulated rainfall over the preceding 48 hours (mm) |
| **`rainfall_last_72h`** | Temporal Feature | Accumulated rainfall over the preceding 72 hours (mm) |
| **`incident_count_7d`** | Temporal Feature | Count of reported incidents in the last 7 days |
| **`incident_count_30d`** | Temporal Feature | Count of reported incidents in the last 30 days |
| **`incident_count_90d`** | Temporal Feature | Count of reported incidents in the last 90 days |
| **`previous_waterlogging_count`** | Temporal Feature | Total historical waterlogging events prior to timestamp |
| **`days_since_last_incident`** | Temporal Feature | Elapsed days since the previous reported incident |
| **`elevation_m`** | Spatial Feature | Mean ground surface elevation (meters above sea level) |
| **`drainage_quality_score`** | Spatial Feature | Hydraulic capacity rating score (0.0 = poor, 1.0 = excellent) |
| **`distance_to_drain_m`** | Spatial Feature | Distance from ward centroid to nearest primary/secondary drain (m) |
| **`distance_to_waterbody_m`** | Spatial Feature | Distance to nearest lake/river outfall (m) |
| **`drainage_density_km_sqkm`** | Spatial Feature | Drainage network linear density (km of drains / sq km area) |
| **`road_density_km_sqkm`** | Spatial Feature | Road network linear density (km of roads / sq km area) |
| **`population_density_per_sqkm`** | Spatial Feature | Population density (people / sq km) |
| **`critical_facility_count`** | Spatial Feature | Count of schools, hospitals, transport hubs inside ward |
| **`historical_incident_density`** | Spatial Feature | Incidents per sq km density rating |
| **`data_source_type`** | Metadata | Provenance tag (`SYNTHETIC_DEMO_DATA`) |

---

## 5. Pipeline Commands & Execution

Execute the pipeline stages from the root directory:

```powershell
# Set PYTHONPATH to root directory
$env:PYTHONPATH="."

# 1. Generate Realistic Synthetic Benchmark Dataset
python -m pipeline.generate_synthetic

# 2. Run Data Ingestion & Quality Cleaning
python -m pipeline.ingest

# 3. Perform Spatial Joins (Incidents, Rainfall, Facilities -> Wards)
python -m pipeline.transform

# 4. Generate ML-Ready Feature Matrix (features.parquet & features.csv)
python -m pipeline.generate_features

# 5. Run Full Test Suite
.\backend\venv\Scripts\pytest.exe tests/
```
