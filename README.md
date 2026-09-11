# 🌧️ CivicPulse Monsoon

### AI-Based Urban Waterlogging Risk Prediction and Preventive Response System

[![Smart India Hackathon 2026](https://img.shields.io/badge/SIH-2026-blue.svg)](https://www.sih.gov.in/)
[![Problem Statement ID](https://img.shields.io/badge/Problem%20Statement-SIH26206-orange.svg)](https://www.sih.gov.in/)
[![Theme](https://img.shields.io/badge/Theme-Disaster%20Management-red.svg)](https://www.sih.gov.in/)
[![Category](https://img.shields.io/badge/Category-Software-green.svg)](https://www.sih.gov.in/)
[![Team](https://img.shields.io/badge/Team-DM07%20|%20INNOVEX-purple.svg)]()
[![FastAPI](https://img.shields.io/badge/Backend-FastAPI%200.110-009688.svg)](https://fastapi.tiangolo.com/)
[![Next.js](https://img.shields.io/badge/Frontend-Next.js%2014-000000.svg)](https://nextjs.org/)
[![PostgreSQL PostGIS](https://img.shields.io/badge/Database-PostgreSQL%2015%20%2B%20PostGIS-336791.svg)](https://postgis.net/)
[![Python](https://img.shields.io/badge/Python-3.12-3776AB.svg)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-Proprietary%20SIH%20Prototype-lightgrey.svg)]()

---

## 2. Project Description

**CivicPulse Monsoon** is an AI-powered predictive civic infrastructure intelligence and decision-support platform engineered for municipal corporations and disaster management authorities. 

The system shifts urban drainage and municipal flood response from **reactive emergency management** (responding only after streets are flooded and emergency routes are blocked) to **proactive preventive intervention**. It achieves this by synthesizing meteorological forecasts, historical incident archives, OpenStreetMap (OSM) infrastructure graphs, terrain elevation data, and official Census demographics to forecast potential waterlogging risks **24, 48, and 72 hours in advance**, explain the underlying risk drivers through **Explainable AI (SHAP)**, prioritize vulnerable locations, and optimize field crew and budget allocations using **Mixed-Integer Linear Programming (Google OR-Tools)**.

---

## 3. Smart India Hackathon 2026 Details

| Field | Submission Specification |
|:---|:---|
| **Competition** | Smart India Hackathon 2026 |
| **Problem Statement ID** | SIH26206 |
| **Problem Statement Title** | AI-Based Urban Waterlogging Risk Prediction and Preventive Response System |
| **Theme** | Disaster Management |
| **PS Category** | Software |
| **Team ID** | DM07 |
| **Team Name** | INNOVEX |

---

## 4. Problem Statement

Urban waterlogging is a chronic, recurring disaster across Indian cities and towns during monsoon events. Inadequate stormwater drainage, rapid urban concretization, silt accumulation, and extreme localized rainfall lead to rapid inundation of arterial roads, disruption of transit corridors, and severe exposure for vulnerable populations and emergency health facilities.

Municipal authorities face six core operational bottlenecks during heavy rainfall:
1. **Lack of Early Warning**: Identifying where waterlogging is likely to occur before water levels rise.
2. **Temporal Uncertainty**: Pinpointing *when* the peak inundation risk is expected (24h vs. 48h vs. 72h lead time).
3. **Black-Box Confusion**: Understanding *why* a particular ward or drainage catchment is at risk (rainfall intensity, topography, choked outfalls, or soil saturation).
4. **Exposure Blindness**: Quantifying how many residents, hospitals, schools, and emergency facilities will be endangered.
5. **Prioritization Paralysis**: Determining which specific roads, culverts, and low-lying zones require preventive action first when resources are constrained.
6. **Sub-optimal Crew Allocation**: Deploying limited municipal maintenance crews and equipment efficiently across competing high-risk zones without human bias.

---

## 5. Proposed Solution

CivicPulse Monsoon provides an end-to-end predictive decision-support system centered on a structured five-stage workflow:

```
Predict  ──▶  Explain  ──▶  Prioritize  ──▶  Optimize  ──▶  Simulate
```

- **Predict**: Estimates probabilistic waterlogging risk levels (`HIGH`, `MEDIUM`, `LOW`, `NO DATA`) across 24h, 48h, and 72h horizons based on rainfall, terrain, drainage proximity, and historical incident recurrence.
- **Explain**: Deconstructs every prediction into transparent evidence factors using SHAP (SHapley Additive exPlanations) and rule-based diagnostic narratives.
- **Prioritize**: Scores civic intervention urgency using a multi-factor weighting formula (Risk Probability + Population Exposure + Critical Facilities + Infrastructure Vulnerability + Historical Frequency).
- **Optimize**: Generates mathematically optimal crew and budget assignments using Google OR-Tools MILP solvers under capacity, skill, and budgetary constraints.
- **Simulate**: Delivers an interactive What-If scenario engine that allows municipal engineers to evaluate how rainfall surges or preventive culvert desilting will alter risk profiles before deploying resources.

---

## 6. Key Features

- **Multi-Horizon Risk Prediction (24h, 48h, 72h)**: Probabilistic forecasting tailored for operational lead times.
- **Transparent Explainable AI (SHAP TreeExplainer)**: Directional feature contribution charts explaining whether risk is driven by rainfall intensity, terrain depression, or historical blockage.
- **Official Census Population Integration**: Direct ingestion of Census of India Primary Census Abstract (PCA) records retaining genuine administrative levels (District, CD Block, Village, Ward) with strict prohibition of synthetic population values.
- **Critical Facility & POI Exposure Tracking**: Spatial proximity mapping of hospitals, schools, transit terminals, emergency stations, and religious sites.
- **Spatial Drainage Dependency Graph**: Graph-theoretic network modeling spatial risk propagation from upstream blocked canals to downstream roads.
- **Multi-Factor Civic Priority Engine**: Transparent scoring algorithm classifying intervention zones from `P1 — CRITICAL` to `P4 — LOW`.
- **Crew & Budget Allocation Optimizer**: Mixed-Integer Linear Programming (MILP) knapsack solver maximizing risk reduction within municipal workforce and financial bounds.
- **What-If Scenario Simulation**: Non-destructive analytical simulator for rainfall multiplier stress-testing and preventive action evaluation.
- **Interactive Geospatial Command Center**: Multi-layered Leaflet map interface supporting 8 toggleable geospatial layers and geocoding search across 38 Tamil Nadu districts and benchmark municipal wards.

---

## 7. How the System Works

```
1. Select Location / District / Ward
        │
2. Review Forecast & Observed Rainfall (1h, 6h, 24h, 48h, 72h)
        │
3. Evaluate Multi-Horizon Risk Models (24h, 48h, 72h)
        │
4. Inspect SHAP Factor Explanations & Contributing Drivers
        │
5. Quantify Population & Critical Facility Spatial Exposure
        │
6. Review Automated Civic Priority Rankings (P1 to P4)
        │
7. Solve Resource Allocation with Google OR-Tools Optimizer
        │
8. Run What-If Simulations to Test Preventive Intervention Scenarios
```

---

## 8. System Architecture

```text
               DATA SOURCES
    (IMD Rainfall, Census PCA, OSM GIS, Historical Incidents)
                     │
                     ▼
              DATA PROCESSING
    (Pandas / NumPy Cleaning, Feature Aggregation, Validation)
                     │
                     ▼
            GEOSPATIAL ANALYSIS
    (GeoPandas, PostGIS Spatial Joins, Drainage Network Graphs)
                     │
                     ▼
              RISK PREDICTION
    (Multi-Horizon 24h / 48h / 72h Machine Learning Classifiers)
                     │
                     ▼
         IMPACT & EXPOSURE ANALYSIS
    (Census Population Overlay & Critical Facility Proximity)
                     │
                     ▼
             PRIORITY SCORING
    (Multi-Factor Weighted Municipal Urgency Formula P1–P4)
                     │
                     ▼
        CREW & BUDGET OPTIMIZATION
    (Google OR-Tools Mixed-Integer Linear Programming Solver)
                     │
                     ▼
            WHAT-IF SIMULATION
    (Scenario Stress-Testing & Preventive Action Evaluation)
                     │
                     ▼
            MUNICIPAL DASHBOARD
    (Next.js 14 + React 18 + Leaflet Command Center Interface)
```

---

## 9. Technology Stack

### Frontend
- **Framework**: Next.js 14 (App Router)
- **Library**: React 18
- **Language**: TypeScript 5.5
- **Styling**: Tailwind CSS 3.4, PostCSS, Autoprefixer
- **UI Components & Icons**: Lucide React, Clsx, Tailwind Merge
- **Geospatial Mapping**: Leaflet 1.9, React-Leaflet bindings

### Backend
- **Framework**: FastAPI 0.110
- **ASGI Server**: Uvicorn 0.28 (Standard)
- **Language**: Python 3.12
- **Data Validation & Settings**: Pydantic v2, Pydantic-Settings
- **HTTP Client**: HTTPX 0.27

### Database & Spatial Engine
- **Primary Database**: PostgreSQL 15 with PostGIS 3.3 Spatial Extension
- **ORM & Dialect**: SQLAlchemy 2.0, GeoAlchemy2 0.14, Asyncpg, Psycopg2-binary
- **Spatial Geometry Processing**: Shapely 2.0, GeoPandas 0.14
- **Database Migrations**: Alembic 1.13
- **Resilient Fallback Mode**: SQLite engine (`civicpulse_fallback.db`) for immediate offline demonstration when PostgreSQL is unavailable

### Data Processing & Machine Learning
- **Data Manipulation**: Pandas 2.2, NumPy 1.26
- **Machine Learning**: Scikit-Learn 1.4, XGBoost 2.0, LightGBM 4.3, Joblib
- **Explainability (XAI)**: SHAP 0.45 (`shap.TreeExplainer`)
- **Optimization**: Google OR-Tools 9.9 (`ortools.linear_solver.pywraplp`)
- **Testing**: Pytest 8.0

### DevOps & Version Control
- **Containerization**: Docker, Docker Compose
- **Version Control**: Git, GitHub

---

## 10. Project Structure

```text
CivicPulse-Monsoon/
├── .env.example                          # Root environment template
├── docker-compose.yml                    # Multi-container orchestration (PostGIS, Backend, Frontend)
├── civicpulse_fallback.db               # SQLite operational demonstration database
├── README.md                             # Project documentation
│
├── backend/                              # FastAPI Backend Application
│   ├── .env.example                      # Backend environment configuration template
│   ├── requirements.txt                  # Python dependencies
│   ├── alembic/                          # Database schema migration scripts
│   ├── alembic.ini                       # Alembic configuration
│   └── app/
│       ├── main.py                       # FastAPI application entrypoint & middleware
│       ├── core/                         # Configuration settings & environment loader
│       ├── db/                           # Database session factory & PostGIS/SQLite fallback
│       ├── models/                       # SQLAlchemy declarative spatial and relational models
│       ├── schemas/                      # Pydantic schemas for request/response serialization
│       ├── services/                     # Core analytical, spatial, and optimization engines
│       └── api/
│           └── v1/                       # Version 1 REST API routers & modular endpoints
│
├── frontend/                             # Next.js 14 Web Application
│   ├── package.json                      # Node dependencies & execution scripts
│   ├── tsconfig.json                     # TypeScript compiler configuration
│   ├── tailwind.config.ts                # Tailwind CSS design system tokens
│   └── src/
│       ├── app/                          # Next.js App Router pages (layout, dashboard, analytics)
│       └── components/                   # Modular React UI components
│           ├── Dashboard/                # Analytics panels, rainfall gauges, summary cards
│           ├── Map/                      # Interactive Leaflet map container & layer controllers
│           ├── Priority/                 # Priority scoring matrix & ward action tables
│           ├── ResourcePlanner/          # Google OR-Tools crew & budget allocation solver UI
│           ├── Simulator/                # What-If scenario parameter controls & impact diffs
│           ├── XAI/                      # SHAP feature importance charts & evidence narratives
│           └── Graph/                    # Spatial drainage network dependency visualizer
│
├── ml/                                   # Machine Learning & Explainability Engine
│   ├── requirements.txt                  # ML-specific dependency definitions
│   ├── data/                             # Feature-engineered training matrices
│   ├── features/                         # Feature generation pipelines & rolling aggregators
│   ├── models/                           # Serialized model artifacts (.joblib for 24h, 48h, 72h)
│   ├── training/                         # Model training scripts (XGBoost, LightGBM, baselines)
│   ├── evaluation/                       # Model evaluation, calibration, and metrics scripts
│   ├── explainability/                   # SHAP TreeExplainer engine (explainer.py)
│   └── inference/                        # Batch and online inference pipelines
│
├── data/                                 # Central Data Repository
│   ├── raw/                              # Primary inputs (population, rainfall, wards, roads, etc.)
│   ├── processed/                        # Normalized GIS and feature-ready tables
│   ├── schemas/                          # Data validation JSON schemas
│   └── synthetic/                        # Labeled benchmark datasets (incidents, rainfall, wards)
│
├── data1/                                # Additional verified Census 2011 district datasets (Theni)
│   └── PCA_CDB_3323_F_Census.xls         # Official Census 2011 PCA for Theni District
│
├── pipeline/                             # Automated data ingestion & GIS transformation pipelines
└── tests/                                # Comprehensive automated test suite (17 test modules)
```

---

## 11. Data Sources

CivicPulse Monsoon strictly distinguishes data types, sources, and validity states to ensure data integrity:

| Category | Description | Data Year / Type | Provenance / Source |
|:---|:---|:---|:---|
| **Population Data** | Primary Census Abstract (PCA) for The Nilgiris & Theni districts | Census 2011 (Historical Public Data) | Office of the Registrar General & Census Commissioner, India |
| **Administrative Boundaries** | State boundary & all 38 District polygons of Tamil Nadu | Official GIS Data | Tamil Nadu State GIS / Rural Development & Urban Local Bodies |
| **Urban Ward Benchmarks** | Municipal ward boundaries (Chennai, Coimbatore, Salem, Madurai, Kallakurichi) | Official ULB / Benchmark Data | Urban Local Body Portals & Municipal GIS Releases |
| **Road Networks** | Arterial roads, subways, highways, and residential streets | OpenStreetMap (OSM) Data | OpenStreetMap Contributors via Overpass API |
| **Drainage Infrastructure** | Primary outfall canals, stormwater channels, culverts | OSM Waterways & Municipal Records | OpenStreetMap & Municipal Engineering Departments |
| **Waterbodies** | Lakes, reservoirs, retention ponds, and river channels | OSM Hydrographic Layers | OpenStreetMap Hydrography / Natural Earth |
| **Critical Facilities & POIs** | Hospitals, schools, transit terminals, emergency stations | Verified Point-of-Interest Data | OpenStreetMap Amenities & Municipal Facility Directories |
| **Rainfall Records** | Hourly gauge readings and multi-day accumulation forecasts | Observed & Forecast Weather | IMD Standards & Open-Meteo Meteorological APIs |
| **Historical Incidents** | Blocked drains, road submersions, and past waterlogging events | Historical Civic Records | Municipal Complaint Portals & Verified Field Reports |
| **Synthetic / Demo Data** | Stress-testing incident datasets and extreme event rainfall | Synthetic Prototype Data | Explicitly labeled `DEMO PROTOTYPE — SYNTHETIC DATA` |

> ⚠️ **Data Integrity Principles**:
> - **Historical Population**: Census 2011 figures are explicitly cited as *historical public data* and are never represented as current real-time population.
> - **No Fabricated Data**: If a geographic unit (such as a specific rural village) lacks official GIS boundary polygons, it is displayed with status `NO_BOUNDARY_POLYGON` rather than inventing artificial circular buffers.
> - **Missing Data**: When data is missing or incomplete, the system displays `No Data` rather than generating artificial values.

---

## 12. Data Processing

1. **Ingestion & Validation**: Raw tabular data (Excel, CSV) and spatial vectors (GeoJSON, Shapefiles) are validated using Pydantic schemas and Shapely geometry assertions.
2. **Coordinate Reference System (CRS) Normalization**: All spatial coordinates are standardized to WGS 84 (`EPSG:4326`) for global map interoperability, and projected to UTM Zone 44N (`EPSG:32644`) for accurate metric distance calculations.
3. **Temporal Rolling Aggregations**:
   - Short-term rainfall intensity: 1-hour and 6-hour rolling maximums.
   - Cumulative precipitation: 24-hour, 48-hour, and 72-hour forecast and observed accumulations.
   - Historical recurrence: 7-day, 30-day, and 90-day incident counts per drainage catchment.
4. **Derived Spatial Indices**:
   - Distance to nearest primary stormwater outfall (meters).
   - Distance to nearest natural drainage sink / waterbody (meters).
   - Local terrain elevation (meters above sea level).
   - Drainage density (km of drain per km²).
   - Road network density (km of road per km²).

---

## 13. Geospatial Analysis

The geospatial engine (`spatial_query_service.py`) operates across multiple administrative scales:

- **State Level**: Complete boundary polygon representation of Tamil Nadu.
- **District Level**: 38 official district boundaries of Tamil Nadu with administrative headquarters, centroid coordinates, and Census 2011 population totals.
- **Municipal / Ward Level**: Urban ward polygons across key municipal corporations (e.g., Chennai Corporation Wards 109, 102, 177; Coimbatore Ward 62; Madurai Ward 45; Salem Ward 24; Kallakurichi Town).
- **Sub-District Hierarchy**: Multi-level hierarchical decomposition linking Districts ➔ CD Blocks ➔ Towns and Villages (e.g., Nilgiris and Theni Census abstracts).
- **Spatial Relationship Operations**:
  - Point-in-polygon queries associating incidents and facilities with specific administrative wards.
  - Buffer distance calculations identifying road segments within low-lying flood run-off zones.
  - Topological connectivity tracing in drainage canal networks.

---

## 14. Population & Facility Exposure

CivicPulse Monsoon quantifies the human and infrastructural impact of potential inundation:

- **Population Exposure Estimation**:
  - Maps verified Census 2011 population figures to administrative boundaries.
  - Classifies exposure into categorical tiers: `HIGH`, `MEDIUM`, `LOW`, or `NO_DATA`.
  - Estimates the fraction of residents residing in low-lying depression buffers (e.g., ~5% to ~8% in active runoff catchments).
- **Critical Facility Exposure**:
  - Identifies and counts vital infrastructure located within vulnerable catchments:
    - **Healthcare**: Primary health centres, government medical colleges, super-specialty hospitals.
    - **Education**: Primary and secondary schools, colleges.
    - **Transport**: Central bus terminals (e.g., Koyambedu CMBT), suburban railway stations.
    - **Emergency & Public Facilities**: Fire stations, police stations, public administrative headquarters.
- **Decision Value**: Prevents decision-makers from focusing solely on water depth by highlighting whether a blocked road cuts off an emergency medical corridor.

---

## 15. Waterlogging Risk Prediction

Rather than asserting guaranteed future flooding, the system provides **probabilistic risk assessments**:

- **Prediction Horizons**:
  - **24-Hour Horizon**: High-resolution tactical forecast for immediate pre-monsoon crew deployment.
  - **48-Hour Horizon**: Operational forecast for heavy equipment staging and outfall canal desilting.
  - **72-Hour Horizon**: Strategic outlook for inter-departmental disaster preparedness.
- **Model Architecture**:
  - Supervised gradient boosting classifiers (**XGBoost** and **LightGBM**) trained on engineered hydrologic and civic features.
  - Serialized model artifacts stored in `ml/models/` (`waterlogging_risk_24h_v1.joblib`, `waterlogging_risk_48h_v1.joblib`, `waterlogging_risk_72h_v1.joblib`).
- **Risk Categorization**:
  - `HIGH RISK` (Probability ≥ 0.70): Imminent risk of severe waterlogging requiring immediate preventive intervention.
  - `MEDIUM RISK` (0.35 ≤ Probability < 0.70): Moderate risk requiring active monitoring and targeted drain inspection.
  - `LOW RISK` (Probability < 0.35): Normal operational conditions under current drainage capacity.
  - `NO DATA`: Assigned when required hydrological or infrastructure features are unavailable.

---

## 16. Explainable AI (XAI)

Machine learning predictions in disaster management are useless if municipal engineers cannot trust them. CivicPulse Monsoon integrates **SHAP (SHapley Additive exPlanations)** via `ml/explainability/explainer.py`:

- **Local Feature Attribution**: Computes exact SHAP values for every inference using `shap.TreeExplainer`.
- **Directional Impact Visualization**: The frontend displays color-coded feature attribution bars showing whether a feature *increased* (+) or *decreased* (-) the waterlogging probability.
- **Deterministic Natural-Language Narratives**:
  - Translates numeric SHAP contributions into human-readable evidence statements (e.g., *"High accumulated 24h rainfall (112 mm) and low terrain elevation (6.2 m) are the primary drivers increasing risk"*).
- **Auditability**: Municipal engineers can verify whether high risk is caused by extreme rainfall vs. poor drainage infrastructure maintenance.

---

## 17. Priority Scoring

The Civic Priority Engine (`priority.py`) synthesizes multi-dimensional risk into an actionable ranking using a configurable weighted formula:

$$\text{Priority Score} = w_{\text{risk}} \cdot S_{\text{risk}} + w_{\text{pop}} \cdot S_{\text{pop}} + w_{\text{fac}} \cdot S_{\text{fac}} + w_{\text{infra}} \cdot S_{\text{infra}} + w_{\text{hist}} \cdot S_{\text{hist}}$$

### Configurable Weights (Backend Settings)
- **Risk Probability Weight ($w_{\text{risk}}$)**: `0.35`
- **Population Exposure Weight ($w_{\text{pop}}$)**: `0.25`
- **Critical Facility Exposure Weight ($w_{\text{fac}}$)**: `0.20`
- **Infrastructure Vulnerability Weight ($w_{\text{infra}}$)**: `0.10`
- **Historical Recurrence Weight ($w_{\text{hist}}$)**: `0.10`

### Priority Classification Tiers
- **P1 — CRITICAL**: Immediate preventive action required within 12–24 hours (high risk + high population or hospital corridor).
- **P2 — HIGH**: Action required within 24–48 hours (elevated risk with major arterial road exposure).
- **P3 — MEDIUM**: Scheduled inspection and desilting within 48–72 hours.
- **P4 — LOW**: Routine maintenance and monitoring.

---

## 18. Crew & Budget Optimization

Municipalities operate under severe resource constraints during monsoon season. The Resource Optimization Engine (`optimization_service.py`) utilizes **Google OR-Tools** (`pywraplp` Mixed-Integer Linear Programming solver) to solve the multi-choice knapsack allocation problem:

- **Optimization Objective**: Maximize total expected risk reduction across high-priority municipal interventions.
- **Constraints Handled**:
  - **Crew Availability**: Limits total assignments to available municipal teams.
  - **Skill Compatibility**: Matches required action skills (`drainage`, `road_maintenance`, `general_maintenance`) with qualified crews.
  - **Daily Working Hours**: Enforces realistic shift limits (e.g., 8.0 hours per team/day).
  - **Municipal Budget Bounds**: Guarantees total estimated expenditure does not exceed the sanctioned contingency budget.
- **Output**: Generates deterministic, actionable work orders detailing team assignments, estimated duration, expenditure, and projected risk mitigation benefit.

---

## 19. What-If Simulation

The What-If Simulation Engine (`simulation_service.py`) provides an interactive digital sandbox for municipal planners:

- **Simulation Parameters**:
  - **Rainfall Intensity Multiplier**: Simulate 1.25x, 1.5x, or 2.0x surges above forecasted precipitation.
  - **Drain Clearing Intervention**: Simulate clearing choked outfalls (reducing drainage resistance by 30–70%).
  - **Pumping Deployments**: Evaluate temporary high-capacity stormwater dewatering pumps.
- **Isolated Analytical Memory**: Simulations run in an ephemeral analytical layer that **never** overwrites real historical databases.
- **Real-Time Risk Diffing**: Visualizes before-and-after risk probabilities, showing exactly how many wards shift from `P1` to `P3` following simulated preventive actions.

---

## 20. Frontend Architecture

The user interface is built with **Next.js 14** and **Tailwind CSS**, optimized for municipal command center operations:

- **Command Center Map (`MapView.tsx`)**: Leaflet-based interactive spatial interface with 8 switchable layers:
  1. Administrative Boundaries (State, Districts, Wards)
  2. Multi-Horizon Risk Zones (24h, 48h, 72h)
  3. Population Exposure
  4. Road Network Vulnerabilities
  5. Stormwater Drainage & Outfalls
  6. Waterbodies & Natural Sinks
  7. Critical Facilities & POIs
  8. Historical Waterlogging Incidents
- **Rainfall Analytics Panel (`RainfallAnalyticsPanel.tsx`)**: Live gauge visualizers, 72h cumulative graphs, and forecast vs. observed deviations.
- **Explainable AI Modal (`XAI/`)**: Visual feature contribution bars and evidence breakdown cards.
- **Resource Planner (`ResourcePlanner/`)**: Interactive solver console for running Google OR-Tools crew assignments with live budget sliders.
- **What-If Scenario Simulator (`Simulator/`)**: Interactive sliders for rainfall surge stress-testing.

---

## 21. Backend Architecture

The backend is built with **FastAPI** and **Python 3.12**, organized following clean architectural principles:

- **`app/main.py`**: ASGI application initialization, CORS configuration, API router mounting, and health checks.
- **`app/core/config.py`**: Pydantic-Settings environment manager handling database credentials, CORS origins, and engine weights.
- **`app/db/session.py`**: Resilient database engine management with automated fallback to SQLite when PostgreSQL/PostGIS is offline.
- **`app/models/`**: Declarative SQLAlchemy models defining tables for Wards, Roads, Drains, Waterbodies, Facilities, Incidents, Rainfall, Predictions, and Optimizations.
- **`app/schemas/`**: Pydantic v2 schemas providing strict input validation and OpenAPI schema generation.
- **`app/services/`**: Encapsulated domain logic for spatial queries, rainfall aggregations, ML inference, SHAP explanations, priority calculation, and Google OR-Tools optimization.

---

## 22. API Architecture

The REST API is organized under the `/api/v1` prefix with complete interactive Swagger documentation available at `/docs`:

| Endpoint Prefix | Router Module | Description |
|:---|:---|:---|
| `/health` | `health.py` | Service readiness and database connection health check |
| `/api/v1/geojson` | `geojson.py` | GeoJSON layers for districts, wards, roads, drains, and facilities |
| `/api/v1/population` | `population.py` | Census 2011 population queries, CD Block/village hierarchy, and district GeoJSON |
| `/api/v1/predictions` | `predictions.py` | Multi-horizon (24h, 48h, 72h) waterlogging risk predictions |
| `/api/v1/explanations` | `explanations.py` | SHAP TreeExplainer feature attributions and natural-language evidence |
| `/api/v1/priority` | `priority.py` | Multi-factor civic urgency scores (P1 to P4) for municipal action |
| `/api/v1/optimization` | `optimization.py` | Google OR-Tools crew and budget allocation solver execution |
| `/api/v1/simulation` | `simulation.py` | What-If scenario stress-testing and rainfall multiplier modeling |
| `/api/v1/analytics` | `analytics.py` | Historical waterlogging incident analytics and rainfall statistics |
| `/api/v1/osm-search` | `osm_search.py` | Geocoding and administrative search across Tamil Nadu locations |
| `/api/v1/wards` | `wards.py` | Ward administrative CRUD operations |
| `/api/v1/incidents` | `incidents.py` | Waterlogging and blocked drain incident reporting |
| `/api/v1/rainfall` | `rainfall.py` | Rainfall gauge readings and forecast series |
| `/api/v1/roads` | `roads.py` | Road segment infrastructure data |
| `/api/v1/drains` | `drains.py` | Stormwater drainage network queries |
| `/api/v1/waterbodies` | `waterbodies.py` | Waterbody and hydrological sink layers |
| `/api/v1/facilities` | `facilities.py` | Hospital, school, and transit hub point queries |
| `/api/v1/graph` | `graph.py` | Spatial drainage network dependency graph operations |

---

## 23. Database Architecture

The data tier is engineered for hybrid spatial-relational workloads:

```text
               ┌────────────────────────────────────────────────────────┐
               │              Primary Engine: PostgreSQL 15             │
               │             with PostGIS 3.3 Spatial Engine            │
               │   • GEOMETRY(Polygon, 4326) / GEOMETRY(LineString)     │
               │   • Spatial Indexing (GIST) for millisecond queries    │
               └───────────────────────────┬────────────────────────────┘
                                           │ (Connection Error Fallback)
                                           ▼
               ┌────────────────────────────────────────────────────────┐
               │             Resilient Engine: SQLite Database          │
               │             (civicpulse_fallback.db)                   │
               │   • Zero-config local demonstration                    │
               │   • Relational storage with GeoJSON serialization      │
               └────────────────────────────────────────────────────────┘
```

- **Spatial Indexing**: PostGIS `GIST` indices on geometries accelerate bounding-box and spatial intersection queries.
- **Relational Integrity**: Foreign key constraints link incidents, rainfall measurements, and risk predictions to corresponding ward identifiers.
- **Graceful Degradation**: If PostgreSQL is unreachable during a local hackathon demonstration, the session manager automatically falls back to `civicpulse_fallback.db` without crashing the application.

---

## 24. Installation / Setup

### Prerequisites
- **Node.js**: v18.0.0 or higher
- **Python**: v3.12.x
- **PostgreSQL / PostGIS** (Optional for local mode; SQLite fallback is built-in)
- **Docker & Docker Compose** (Optional for containerized execution)

### 1. Clone the Repository
```bash
git clone https://github.com/INNOVEX-DM07/CivicPulse-Monsoon.git
cd CivicPulse-Monsoon
```

### 2. Backend Environment & Dependency Setup
```powershell
# Navigate to backend directory
cd backend

# Create and activate Python virtual environment
python -m venv venv
.\venv\Scripts\Activate.ps1

# Install required Python dependencies
pip install -r requirements.txt

# Configure environment variables
Copy-Item .env.example .env
```

### 3. Frontend Dependency Setup
```powershell
# In a separate terminal, navigate to frontend directory
cd frontend

# Install Node.js dependencies
npm install

# Configure frontend environment
Copy-Item .env.example .env.local
```

---

## 25. Running the Project

### Running Locally (Native Development Mode)

**Terminal 1 — Backend API Server:**
```powershell
cd backend
.\venv\Scripts\Activate.ps1
$env:PYTHONPATH="..;."
python -m uvicorn app.main:app --host 127.0.0.1 --port 8000 --reload
```
- Interactive API Docs (Swagger): [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
- Alternative API Docs (ReDoc): [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc)
- Health Check: [http://127.0.0.1:8000/health](http://127.0.0.1:8000/health)

**Terminal 2 — Frontend Application:**
```powershell
cd frontend
npm run dev
```
- Municipal Command Center Map: [http://localhost:3000](http://localhost:3000)
- Historical Analytics Dashboard: [http://localhost:3000/analytics](http://localhost:3000/analytics)

---

### Running via Docker Compose
To launch the entire platform (PostGIS + FastAPI Backend + Next.js Frontend) in unified containers:
```bash
docker-compose up --build
```
- Next.js Web UI: [http://localhost:3000](http://localhost:3000)
- FastAPI Swagger UI: [http://localhost:8000/docs](http://localhost:8000/docs)

---

### Running Automated Tests
The project includes a 17-file test suite verifying spatial joins, ML inference, SHAP explanations, and OR-Tools solvers:
```powershell
$env:PYTHONPATH=".;backend"
.\backend\venv\Scripts\pytest.exe tests/ -v
```

---

## 26. Environment Variables

The project uses structured environment variables. Sensitive credentials should never be committed to source control.

### Backend (`backend/.env`)
| Variable Name | Description | Default / Example Value |
|:---|:---|:---|
| `PROJECT_NAME` | Name of the backend service | `"CivicPulse Monsoon API"` |
| `ENVIRONMENT` | Runtime mode (`development`, `production`) | `"development"` |
| `DEBUG` | Enable debug logs | `True` |
| `API_V1_STR` | Version 1 API URL prefix | `"/api/v1"` |
| `CORS_ORIGINS` | Permitted cross-origin origins | `["http://localhost:3000"]` |
| `POSTGRES_SERVER` | PostgreSQL server hostname | `"localhost"` |
| `POSTGRES_PORT` | PostgreSQL port | `5432` |
| `POSTGRES_DB` | Database name | `"civicpulse"` |
| `POSTGRES_USER` | Database username | `"civicpulse_admin"` |
| `POSTGRES_PASSWORD` | Database password | Secret string |
| `DATABASE_URL` | Complete async database connection URI | Secret string |
| `PRIORITY_WEIGHT_RISK` | Urgency formula weight for ML risk | `0.35` |
| `PRIORITY_WEIGHT_POPULATION` | Urgency formula weight for population | `0.25` |
| `PRIORITY_WEIGHT_CRITICAL_FACILITIES` | Urgency formula weight for facilities | `0.20` |
| `PRIORITY_WEIGHT_INFRASTRUCTURE` | Urgency formula weight for infrastructure | `0.10` |
| `PRIORITY_WEIGHT_HISTORICAL_RECURRENCE` | Urgency formula weight for past incidents | `0.10` |

### Frontend (`frontend/.env.local`)
| Variable Name | Description | Default / Example Value |
|:---|:---|:---|
| `NEXT_PUBLIC_API_BASE_URL` | Base URL of the FastAPI backend service | `"http://localhost:8000"` |

---

## 27. Current Implementation Status

| Capability / Module | Implementation Status | Notes |
|:---|:---:|:---|
| **Multi-Horizon Risk Prediction (24h, 48h, 72h)** | ✅ Implemented | Pre-trained XGBoost models serialized in `ml/models/` |
| **SHAP Explainable AI Engine** | ✅ Implemented | Real `shap.TreeExplainer` in `ml/explainability/explainer.py` |
| **Google OR-Tools Resource Optimization** | ✅ Implemented | MILP solver allocating crews, hours, and budgets |
| **What-If Scenario Simulation** | ✅ Implemented | In-memory scenario engine with rainfall multipliers |
| **Multi-Factor Priority Scoring Engine** | ✅ Implemented | Configurable weighted urgency ranking (P1 to P4) |
| **Geospatial Command Center (Leaflet Map)** | ✅ Implemented | 8 toggleable spatial layers with custom styling |
| **Tamil Nadu Administrative GIS Boundaries** | ✅ Implemented | State polygon & all 38 district boundary polygons |
| **Historical Census 2011 PCA Ingestion** | ✅ Implemented | District, CD Block, and village data for Nilgiris & Theni |
| **Critical Facility & POI Exposure Tracking** | ✅ Implemented | Hospitals, schools, transit terminals mapped |
| **Drainage Network Dependency Graph** | ✅ Implemented | Node/edge spatial graph of drains and roads |
| **PostgreSQL + PostGIS Spatial Storage** | ✅ Implemented | Containerized PostGIS with spatial schemas |
| **SQLite Resilient Demonstration Fallback** | ✅ Implemented | Automatic seamless failover to `civicpulse_fallback.db` |
| **Automated Test Suite (17 Modules)** | ✅ Implemented | Unit & integration tests in `tests/` directory |
| **Sub-District Boundary Polygon Coverage** | 🟡 Partial | Village/Block polygons missing in public GIS (labeled `NO_BOUNDARY_POLYGON`) |
| **Live IMD Weather API Integration** | 🟡 Partial | Weather pipelines configured; historical/benchmark data active |
| **IoT Real-Time Water-Level Sensor Ingestion** | 🔵 Planned | Architectural interfaces defined for telemetry streams |
| **Mobile Field-Crew Native App** | 🔵 Planned | Field reporting currently supported via web interface |
| **Automated Work-Order Dispatching to Field Units** | 🔵 Planned | Optimization outputs generated; auto-SMS dispatch planned |

---

## 28. Limitations

1. **Sub-District GIS Boundary Availability**: Detailed GIS boundary shapefiles for rural villages and CD blocks are not available in public government GIS repositories. CivicPulse Monsoon adheres to data honesty principles: missing polygons are explicitly marked as unavailable rather than generating misleading synthetic circles.
2. **Census Data Vintage**: Official Primary Census Abstract datasets originate from the 2011 Census of India. The platform uses this as authentic baseline data but clearly identifies it as historical public data.
3. **Weather Forecast Uncertainty**: Hydrological predictions are bounded by meteorological forecast precision. Extreme hyper-local convective cloudbursts cannot be predicted with 100% certainty.
4. **Drainage Attribute Incompleteness**: Comprehensive subterranean stormwater pipe diameters and maintenance states are partially recorded in OpenStreetMap and municipal records.

---

## 29. Future Scope

- **IoT Water-Level Telemetry**: Real-time integration with ultrasonic water-level sensors installed at culverts, canal outfalls, and railway underpasses.
- **Crowdsourced Multi-Modal Evidence**: Mobile app allowing citizens to submit geo-tagged, timestamped photos of localized waterlogging with automated computer-vision depth estimation.
- **Hydrological Inundation Modeling**: Coupling machine learning risk scores with 2D hydrodynamic flood routing engines (e.g., SWMM, HEC-RAS) for physical water velocity simulation.
- **SMS / WhatsApp Disaster Alerts**: Automated bilingual citizen notification engine dispatching preventive alerts to residents within P1 critical catchments.
- **Multi-State Expansion**: Scaling data pipelines beyond Tamil Nadu to Maharashtra, Karnataka, Kerala, and other flood-vulnerable regions.

---

## 30. Team

### Team INNOVEX — Smart India Hackathon 2026

- **Team ID**: `DM07`
- **Problem Statement ID**: `SIH26206`
- **Theme**: Disaster Management
- **Category**: Software

---

## 31. References

1. **India Meteorological Department (IMD)** — Ministry of Earth Sciences, Government of India: Meteorological APIs and rainfall classification standards.
2. **Office of the Registrar General & Census Commissioner, India** — Primary Census Abstract (PCA), Census of India (2011).
3. **OpenStreetMap (OSM)** — OpenStreetMap Foundation: Geospatial infrastructure data, roads, waterways, and public amenities.
4. **National Remote Sensing Centre (NRSC) / NDEM** — ISRO: Flood hazard zonation and geospatial hydrological data.
5. **Greater Chennai Corporation & Tamil Nadu Urban Local Bodies** — Municipal ward boundary definitions and stormwater drainage reports.
6. **Lundberg, S. M., & Lee, S. I. (2017)** — *A Unified Approach to Interpreting Model Predictions (SHAP)*, Advances in Neural Information Processing Systems (NeurIPS).
7. **Google OR-Tools** — Google Optimization Tools for combinatorial optimization and Mixed-Integer Linear Programming.

---

## 32. License

This software is developed as a working prototype for the **Smart India Hackathon 2026** under Problem Statement **SIH26206 (Disaster Management)** by **Team INNOVEX (DM07)**. 

All rights reserved. Unauthorized commercial exploitation is prohibited.
#   c i v i c p u l s e - m o n s o o n  
 