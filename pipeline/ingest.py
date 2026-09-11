import os
import json
import pandas as pd
import geopandas as gpd
from typing import Dict, Any, Tuple

from pipeline.clean import (
    clean_coordinates, clean_timestamps, clean_rainfall_values,
    deduplicate_records, clean_geometries, normalize_crs
)
from pipeline.validate import (
    validate_rainfall_df, validate_incidents_df,
    validate_geospatial_gdf, generate_quality_report
)

RAW_DIR = os.path.abspath("data/raw")
PROCESSED_DIR = os.path.abspath("data/processed")

def ingest_rainfall(file_path: str) -> Tuple[pd.DataFrame, Dict[str, Any]]:
    """Ingest, clean, and validate rainfall CSV/JSON files."""
    if file_path.endswith('.json'):
        raw_df = pd.read_json(file_path)
    else:
        raw_df = pd.read_csv(file_path)
        
    initial_len = len(raw_df)
    df = clean_timestamps(raw_df, 'timestamp')
    df = clean_coordinates(df, 'latitude', 'longitude')
    df = clean_rainfall_values(df, 'rainfall_mm')
    
    dedup_subset = ['timestamp', 'latitude', 'longitude', 'forecast_hours']
    dedup_subset = [c for c in dedup_subset if c in df.columns]
    
    df_clean = deduplicate_records(df, subset=dedup_subset)
    duplicates_dropped = initial_len - len(df_clean)
    
    val_report = validate_rainfall_df(df_clean)
    quality_report = generate_quality_report("rainfall", raw_df, df_clean, duplicates_dropped)
    
    return df_clean, quality_report

def ingest_incidents(file_path: str) -> Tuple[pd.DataFrame, Dict[str, Any]]:
    """Ingest, clean, and validate historical civic incidents."""
    if file_path.endswith('.json'):
        raw_df = pd.read_json(file_path)
    else:
        raw_df = pd.read_csv(file_path)
        
    initial_len = len(raw_df)
    df = clean_timestamps(raw_df, 'timestamp')
    df = clean_coordinates(df, 'latitude', 'longitude')
    
    dedup_subset = ['incident_id'] if 'incident_id' in df.columns else ['latitude', 'longitude', 'timestamp', 'incident_type']
    df_clean = deduplicate_records(df, subset=dedup_subset)
    duplicates_dropped = initial_len - len(df_clean)
    
    quality_report = generate_quality_report("incidents", raw_df, df_clean, duplicates_dropped)
    return df_clean, quality_report

def ingest_geospatial(file_path: str, dataset_name: str) -> Tuple[gpd.GeoDataFrame, Dict[str, Any]]:
    """Ingest, clean, repair, and reproject GeoJSON/Shapefile features into EPSG:4326."""
    raw_gdf = gpd.read_file(file_path)
    initial_len = len(raw_gdf)
    
    gdf = normalize_crs(raw_gdf, "EPSG:4326")
    gdf = clean_geometries(gdf)
    
    duplicates_dropped = initial_len - len(gdf)
    quality_report = generate_quality_report(dataset_name, raw_gdf, gdf, duplicates_dropped)
    return gdf, quality_report

def run_ingest_pipeline():
    print("================ RUNNING DATA INGESTION PIPELINE ================")
    # Check if raw files exist, run ingestion
    print("[INFO] Checking data/raw/ folders...")
    for category in ['rainfall', 'incidents', 'wards', 'roads', 'drains', 'waterbodies', 'facilities']:
        cat_dir = os.path.join(RAW_DIR, category)
        files = [f for f in os.listdir(cat_dir) if not f.startswith('.')]
        print(f"  - Category '{category}': {len(files)} files found.")
        
    print("[INFO] Ingestion module ready.")

if __name__ == "__main__":
    run_ingest_pipeline()
