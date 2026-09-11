import os
import pandas as pd
import numpy as np
import geopandas as gpd
from datetime import datetime, timezone, timedelta
from typing import Tuple

PROCESSED_DIR = os.path.abspath("data/processed")
SYNTHETIC_DIR = os.path.abspath("data/synthetic")

def build_temporal_features(rainfall_df: pd.DataFrame, incidents_df: pd.DataFrame) -> pd.DataFrame:
    """Compute rolling temporal rainfall aggregations and historical incident counts."""
    rainfall_df = rainfall_df.copy()
    rainfall_df['timestamp'] = pd.to_datetime(rainfall_df['timestamp'], utc=True)
    
    if not incidents_df.empty:
        incidents_df = incidents_df.copy()
        incidents_df['timestamp'] = pd.to_datetime(incidents_df['timestamp'], utc=True)
        
    # Sort for rolling window calculations
    rainfall_df = rainfall_df.sort_values(['ward_id', 'timestamp'])
    
    # Filter observed gauge readings (forecast_hours == 0)
    obs_rain = rainfall_df[rainfall_df['forecast_hours'] == 0].copy()
    
    # Grid of Ward + Timestamp
    features_list = []
    
    for (ward_id), group in obs_rain.groupby('ward_id'):
        group = group.set_index('timestamp').sort_index()
        
        # Rolling sums for 1h, 6h, 24h, 48h, 72h
        r1h = group['rainfall_mm'].rolling('1h').sum()
        r6h = group['rainfall_mm'].rolling('6h').sum()
        r24h = group['rainfall_mm'].rolling('24h').sum()
        r48h = group['rainfall_mm'].rolling('48h').sum()
        r72h = group['rainfall_mm'].rolling('72h').sum()
        
        ward_incidents = incidents_df[incidents_df['ward_id'] == ward_id] if not incidents_df.empty else pd.DataFrame()
        
        for ts, row in group.iterrows():
            # Incident counts in rolling windows prior to ts
            if not ward_incidents.empty:
                inc_7d = len(ward_incidents[(ward_incidents['timestamp'] <= ts) & (ward_incidents['timestamp'] >= ts - timedelta(days=7))])
                inc_30d = len(ward_incidents[(ward_incidents['timestamp'] <= ts) & (ward_incidents['timestamp'] >= ts - timedelta(days=30))])
                inc_90d = len(ward_incidents[(ward_incidents['timestamp'] <= ts) & (ward_incidents['timestamp'] >= ts - timedelta(days=90))])
                
                prev_waterlog = len(ward_incidents[(ward_incidents['timestamp'] < ts) & (ward_incidents['incident_type'] == 'waterlogging')])
                
                past_incidents = ward_incidents[ward_incidents['timestamp'] < ts]
                if not past_incidents.empty:
                    last_inc_time = past_incidents['timestamp'].max()
                    days_since = round((ts - last_inc_time).total_seconds() / 86400.0, 2)
                else:
                    days_since = 999.0
            else:
                inc_7d, inc_30d, inc_90d, prev_waterlog, days_since = 0, 0, 0, 0, 999.0
                
            features_list.append({
                "ward_id": ward_id,
                "timestamp": ts.isoformat(),
                "rainfall_last_1h": round(float(r1h.loc[ts]), 2),
                "rainfall_last_6h": round(float(r6h.loc[ts]), 2),
                "rainfall_last_24h": round(float(r24h.loc[ts]), 2),
                "rainfall_last_48h": round(float(r48h.loc[ts]), 2),
                "rainfall_last_72h": round(float(r72h.loc[ts]), 2),
                "incident_count_7d": inc_7d,
                "incident_count_30d": inc_30d,
                "incident_count_90d": inc_90d,
                "previous_waterlogging_count": prev_waterlog,
                "days_since_last_incident": days_since,
            })
            
    return pd.DataFrame(features_list)

def merge_spatial_features(df_temporal: pd.DataFrame, wards_gdf: gpd.GeoDataFrame) -> pd.DataFrame:
    """Merge ward-level static spatial features (elevation, density, facility count)."""
    if df_temporal.empty or wards_gdf.empty:
        return df_temporal

    spatial_meta = []
    for idx, ward in wards_gdf.iterrows():
        area = float(ward.get('area_sq_km', 10.0))
        pop = int(ward.get('population', 500000))
        pop_density = round(pop / area, 2) if area > 0 else 0.0
        
        # Spatial proxy calculations
        spatial_meta.append({
            "ward_id": ward.id,
            "elevation_m": float(ward.get('elevation_m', 5.0)),
            "drainage_quality_score": float(ward.get('drainage_quality', 0.5)),
            "distance_to_drain_m": round(np.random.uniform(50.0, 300.0), 1),
            "distance_to_waterbody_m": round(np.random.uniform(200.0, 1500.0), 1),
            "drainage_density_km_sqkm": round(np.random.uniform(1.2, 4.5), 2),
            "road_density_km_sqkm": round(np.random.uniform(5.0, 12.0), 2),
            "population_density_per_sqkm": pop_density,
            "critical_facility_count": int(np.random.randint(5, 25)),
            "historical_incident_density": round(np.random.uniform(0.5, 3.5), 2)
        })
        
    df_spatial = pd.DataFrame(spatial_meta)
    
    # Merge temporal and spatial feature DataFrames
    df_features = pd.merge(df_temporal, df_spatial, on='ward_id', how='left')
    df_features['data_source_type'] = "SYNTHETIC_DEMO_DATA"
    return df_features

def run_feature_generation_pipeline() -> Tuple[pd.DataFrame, str, str]:
    print("================ GENERATING ML-READY FEATURE DATASET ================")
    os.makedirs(PROCESSED_DIR, exist_ok=True)
    
    # Load ingested or synthetic datasets
    wards_path = os.path.join(SYNTHETIC_DIR, "synthetic_wards.geojson")
    rainfall_path = os.path.join(SYNTHETIC_DIR, "synthetic_rainfall.csv")
    incidents_path = os.path.join(SYNTHETIC_DIR, "synthetic_incidents.csv")
    
    if not os.path.exists(rainfall_path):
        from pipeline.generate_synthetic import run_synthetic_generator
        run_synthetic_generator()
        
    wards_gdf = gpd.read_file(wards_path)
    rainfall_df = pd.read_csv(rainfall_path)
    incidents_df = pd.read_csv(incidents_path) if os.path.exists(incidents_path) else pd.DataFrame()
    
    print("[INFO] Computing temporal features (rainfall 1h/6h/24h/48h/72h & incident counters)...")
    temporal_df = build_temporal_features(rainfall_df, incidents_df)
    
    print("[INFO] Merging spatial features (elevation, distances, density scores)...")
    features_df = merge_spatial_features(temporal_df, wards_gdf)
    
    # Export outputs
    parquet_path = os.path.join(PROCESSED_DIR, "features.parquet")
    csv_path = os.path.join(PROCESSED_DIR, "features.csv")
    
    features_df.to_parquet(parquet_path, engine="fastparquet", index=False)
    features_df.to_csv(csv_path, index=False)
    
    print(f"[SUCCESS] Feature dataset compiled: {len(features_df)} rows x {len(features_df.columns)} columns")
    print(f"  - Parquet Output: {parquet_path}")
    print(f"  - CSV Output:     {csv_path}")
    
    return features_df, parquet_path, csv_path

if __name__ == "__main__":
    run_feature_generation_pipeline()
