import os
import json
import numpy as np
import pandas as pd
import geopandas as gpd
from shapely.geometry import Polygon, Point, LineString
from datetime import datetime, timezone, timedelta

SYNTHETIC_DIR = os.path.abspath("data/synthetic")

def generate_synthetic_wards() -> gpd.GeoDataFrame:
    """Generate sample municipal wards (Mumbai areas) with elevation & population parameters."""
    wards_data = [
        {
            "id": 1, "name": "Dadar West (DEMO)", "ward_code": "MUM-GN-01",
            "population": 450000, "area_sq_km": 9.07, "elevation_m": 4.2, "drainage_quality": 0.45,
            "geometry": Polygon([[72.830, 19.010], [72.850, 19.010], [72.850, 19.030], [72.830, 19.030], [72.830, 19.010]])
        },
        {
            "id": 2, "name": "Kurla West (DEMO)", "ward_code": "MUM-L-02",
            "population": 900000, "area_sq_km": 15.88, "elevation_m": 2.8, "drainage_quality": 0.25,
            "geometry": Polygon([[72.870, 19.060], [72.890, 19.060], [72.890, 19.080], [72.870, 19.080], [72.870, 19.060]])
        },
        {
            "id": 3, "name": "Andheri East (DEMO)", "ward_code": "MUM-K-03",
            "population": 850000, "area_sq_km": 24.50, "elevation_m": 18.5, "drainage_quality": 0.70,
            "geometry": Polygon([[72.840, 19.110], [72.870, 19.110], [72.870, 19.140], [72.840, 19.140], [72.840, 19.110]])
        },
        {
            "id": 4, "name": "Sion Circle (DEMO)", "ward_code": "MUM-FN-04",
            "population": 380000, "area_sq_km": 7.12, "elevation_m": 2.1, "drainage_quality": 0.30,
            "geometry": Polygon([[72.850, 19.030], [72.870, 19.030], [72.870, 19.050], [72.850, 19.050], [72.850, 19.030]])
        }
    ]
    gdf = gpd.GeoDataFrame(wards_data, crs="EPSG:4326")
    gdf['data_source_type'] = "SYNTHETIC_DEMO_DATA"
    return gdf

def generate_synthetic_rainfall(wards_gdf: gpd.GeoDataFrame, days: int = 14) -> pd.DataFrame:
    """Generate hourly rainfall records (observed & 24/48/72h forecast) with spatial & temporal variation."""
    records = []
    base_time = datetime.now(timezone.utc) - timedelta(days=days)
    
    np.random.seed(42)
    
    for day in range(days):
        # Simulate monsoon storm peaks
        is_heavy_day = day in [3, 7, 8, 12]
        
        for hour in range(24):
            current_time = base_time + timedelta(days=day, hours=hour)
            
            for idx, ward in wards_gdf.iterrows():
                # Base rainfall intensity
                if is_heavy_day and (12 <= hour <= 18):
                    # Extreme monsoon downpour
                    rainfall_mm = np.random.uniform(45.0, 110.0)
                elif is_heavy_day:
                    rainfall_mm = np.random.uniform(10.0, 35.0)
                else:
                    rainfall_mm = np.random.exponential(scale=3.0)
                    
                rainfall_mm = round(max(0.0, float(rainfall_mm)), 2)
                
                # Centroid coords for gauge
                centroid = ward.geometry.centroid
                
                records.append({
                    "timestamp": current_time.isoformat(),
                    "latitude": round(centroid.y, 5),
                    "longitude": round(centroid.x, 5),
                    "rainfall_mm": rainfall_mm,
                    "forecast_hours": 0,
                    "source": "synthetic_sensor",
                    "is_forecast": False,
                    "ward_id": ward.id,
                    "data_source_type": "SYNTHETIC_DEMO_DATA"
                })
                
                # Generate 24h, 48h, 72h forecasts
                for f_hours in [24, 48, 72]:
                    forecast_time = current_time + timedelta(hours=f_hours)
                    # Add forecast noise (+- 15%)
                    f_rainfall = round(max(0.0, float(rainfall_mm * np.random.uniform(0.85, 1.15))), 2)
                    records.append({
                        "timestamp": forecast_time.isoformat(),
                        "latitude": round(centroid.y, 5),
                        "longitude": round(centroid.x, 5),
                        "rainfall_mm": f_rainfall,
                        "forecast_hours": f_hours,
                        "source": "synthetic_imd_forecast",
                        "is_forecast": True,
                        "ward_id": ward.id,
                        "data_source_type": "SYNTHETIC_DEMO_DATA"
                    })
                    
    return pd.DataFrame(records)

def generate_synthetic_incidents(wards_gdf: gpd.GeoDataFrame, rainfall_df: pd.DataFrame) -> pd.DataFrame:
    """Generate log-consistent civic incidents.
    Higher rainfall + lower elevation + poor drainage -> higher waterlogging probability.
    """
    incidents = []
    inc_id = 1000
    
    np.random.seed(42)
    
    for idx, ward in wards_gdf.iterrows():
        ward_rain = rainfall_df[(rainfall_df['ward_id'] == ward.id) & (~rainfall_df['is_forecast'])]
        
        # Risk probability formula
        elevation_factor = max(0.1, (20.0 - ward.elevation_m) / 20.0)
        drainage_vulnerability = 1.0 - ward.drainage_quality
        
        for _, row in ward_rain.iterrows():
            rain = row['rainfall_mm']
            
            # Risk score calculation
            waterlog_prob = (rain / 100.0) * elevation_factor * drainage_vulnerability * 2.5
            
            if np.random.rand() < waterlog_prob and rain > 15.0:
                inc_id += 1
                # Random point inside ward
                minx, miny, maxx, maxy = ward.geometry.bounds
                p_x = np.random.uniform(minx, maxx)
                p_y = np.random.uniform(miny, maxy)
                
                severity = "critical" if rain > 60.0 else ("high" if rain > 35.0 else "medium")
                
                incidents.append({
                    "incident_id": f"INC-SYN-{inc_id}",
                    "incident_type": "waterlogging" if rain > 25.0 else "blocked_drain",
                    "description": f"Synthetic incident simulated at rainfall {rain}mm/hr [DEMO DATA]",
                    "latitude": round(p_y, 5),
                    "longitude": round(p_x, 5),
                    "timestamp": row['timestamp'],
                    "severity": severity,
                    "source": "synthetic_citizen_report",
                    "status": "investigating" if np.random.rand() > 0.5 else "reported",
                    "ward_id": ward.id,
                    "data_source_type": "SYNTHETIC_DEMO_DATA"
                })
                
    # Fallback to guarantee sample data for short test runs
    if not incidents:
        ward = wards_gdf.iloc[0]
        minx, miny, maxx, maxy = ward.geometry.bounds
        incidents.append({
            "incident_id": "INC-SYN-1001",
            "incident_type": "waterlogging",
            "description": "Synthetic waterlogging incident baseline [DEMO DATA]",
            "latitude": round((miny + maxy) / 2.0, 5),
            "longitude": round((minx + maxx) / 2.0, 5),
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "severity": "high",
            "source": "synthetic_citizen_report",
            "status": "investigating",
            "ward_id": ward.id,
            "data_source_type": "SYNTHETIC_DEMO_DATA"
        })
        
    return pd.DataFrame(incidents)

def run_synthetic_generator():
    print("================ GENERATING SYNTHETIC DEMO DATASET ================")
    os.makedirs(SYNTHETIC_DIR, exist_ok=True)
    os.makedirs("data/raw/wards", exist_ok=True)
    os.makedirs("data/raw/rainfall", exist_ok=True)
    os.makedirs("data/raw/incidents", exist_ok=True)
    
    # 1. Wards
    wards_gdf = generate_synthetic_wards()
    wards_path = os.path.join(SYNTHETIC_DIR, "synthetic_wards.geojson")
    wards_gdf.to_file(wards_path, driver="GeoJSON")
    wards_gdf.to_file(os.path.join("data/raw/wards", "wards.geojson"), driver="GeoJSON")
    print(f"  - Generated {len(wards_gdf)} synthetic wards -> {wards_path}")
    
    # 2. Rainfall
    rainfall_df = generate_synthetic_rainfall(wards_gdf, days=7)
    rainfall_path = os.path.join(SYNTHETIC_DIR, "synthetic_rainfall.csv")
    rainfall_df.to_csv(rainfall_path, index=False)
    rainfall_df.to_csv(os.path.join("data/raw/rainfall", "rainfall.csv"), index=False)
    print(f"  - Generated {len(rainfall_df)} synthetic rainfall records -> {rainfall_path}")
    
    # 3. Incidents
    incidents_df = generate_synthetic_incidents(wards_gdf, rainfall_df)
    incidents_path = os.path.join(SYNTHETIC_DIR, "synthetic_incidents.csv")
    incidents_df.to_csv(incidents_path, index=False)
    incidents_df.to_csv(os.path.join("data/raw/incidents", "incidents.csv"), index=False)
    print(f"  - Generated {len(incidents_df)} log-consistent synthetic incidents -> {incidents_path}")
    
    print("[SUCCESS] All synthetic benchmark datasets created with source: 'SYNTHETIC_DEMO_DATA'")

if __name__ == "__main__":
    run_synthetic_generator()
