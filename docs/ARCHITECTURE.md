# CivicPulse Monsoon - System Architecture & Blueprint

## 1. Executive Overview
**CivicPulse Monsoon** is an AI-based predictive waterlogging and drainage risk management platform designed for municipal authorities during monsoon seasons. The system leverages multi-source data (rainfall, topography/elevation, historical incidents, drainage connectivity graphs, population density) to deliver actionable 24, 48, and 72-hour risk predictions and crew dispatch optimizations.

---

## 2. High-Level System Architecture

```
                                  +---------------------------------------+
                                  |         Municipal Dashboard           |
                                  |    (Next.js + TypeScript + Tailwind)  |
                                  +-------------------+-------------------+
                                                      |
                                                      | REST API (HTTP/JSON)
                                                      v
                                  +---------------------------------------+
                                  |            FastAPI Backend            |
                                  |    (Python 3.12 + Pydantic + Uvicorn) |
                                  +---------+-----------------+-----------+
                                            |                 |
                   +------------------------+                 +------------------------+
                   |                                                                   |
                   v                                                                   v
+-------------------------------------+                              +----------------------------------+
|           ML Engine                 |                              |        PostgreSQL / PostGIS       |
| (Pandas, Scikit-Learn, XGBoost/SHAP)|                              | (Spatial Queries & Grid Layers)  |
+-------------------------------------+                              +----------------------------------+
                   |                                                                   ^
                   v                                                                   |
+-------------------------------------+                                                |
|       OR-Tools Optimizer            |------------------------------------------------+
|  (Crew & Budget Allocation Engine)  |
+-------------------------------------+
```

---

## 3. Directory Layout & Module Responsibilities

- **`frontend/`**: Next.js single-page municipal dashboard, interactive geospatial map (MapLibre/Leaflet), forecast timeline sliders, risk explainability cards, and optimization status views.
- **`backend/`**: FastAPI REST service providing authentication, spatial API endpoints, data ingestion handlers, ML model serving hooks, and OR-Tools optimization solvers.
- **`ml/`**: Machine learning model pipelines, feature engineering scripts, model persistence (`.joblib` / `.json`), and SHAP explainability calculation pipelines.
- **`data/`**: Storage for raw spatial datasets (GeoJSON/Shapefiles), processed grid features, and synthetic incident benchmarks.
- **`docs/`**: Architectural blueprints, API schemas, and deployment guides.
- **`docker-compose.yml`**: Production and development container orchestration setup.
