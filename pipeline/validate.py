import pandas as pd
import geopandas as gpd
from typing import Dict, Any

SUPPORTED_INCIDENT_TYPES = {
    'waterlogging', 'blocked_drain', 'road_damage', 'drainage_failure', 'water_leak', 'other'
}

SUPPORTED_SEVERITIES = {'low', 'medium', 'high', 'critical'}

def validate_rainfall_df(df: pd.DataFrame) -> Dict[str, Any]:
    """Validate rainfall records schema and boundary rules."""
    errors = []
    required_cols = ['timestamp', 'latitude', 'longitude', 'rainfall_mm']
    
    for col in required_cols:
        if col not in df.columns:
            errors.append(f"Missing column: {col}")
            
    if errors:
        return {"valid": False, "errors": errors}
        
    invalid_rainfall = (df['rainfall_mm'] < 0).sum()
    invalid_lats = ((df['latitude'] < -90) | (df['latitude'] > 90)).sum()
    invalid_lons = ((df['longitude'] < -180) | (df['longitude'] > 180)).sum()
    
    if invalid_rainfall > 0:
        errors.append(f"Found {invalid_rainfall} rows with negative rainfall_mm.")
    if invalid_lats > 0 or invalid_lons > 0:
        errors.append(f"Found {invalid_lats + invalid_lons} rows with invalid coordinates.")
        
    return {
        "valid": len(errors) == 0,
        "errors": errors,
        "metrics": {
            "invalid_rainfall_count": int(invalid_rainfall),
            "invalid_coord_count": int(invalid_lats + invalid_lons)
        }
    }

def validate_incidents_df(df: pd.DataFrame) -> Dict[str, Any]:
    """Validate incident logs schema, type support, and severity rules."""
    errors = []
    required_cols = ['incident_id', 'incident_type', 'latitude', 'longitude', 'timestamp', 'severity']
    
    for col in required_cols:
        if col not in df.columns:
            errors.append(f"Missing column: {col}")
            
    if errors:
        return {"valid": False, "errors": errors}
        
    unsupported_types = set(df['incident_type'].unique()) - SUPPORTED_INCIDENT_TYPES
    unsupported_severities = set(df['severity'].unique()) - SUPPORTED_SEVERITIES
    
    if unsupported_types:
        errors.append(f"Unsupported incident types: {unsupported_types}")
    if unsupported_severities:
        errors.append(f"Unsupported severities: {unsupported_severities}")
        
    return {
        "valid": len(errors) == 0,
        "errors": errors,
        "unsupported_types": list(unsupported_types),
        "unsupported_severities": list(unsupported_severities)
    }

def validate_geospatial_gdf(gdf: gpd.GeoDataFrame) -> Dict[str, Any]:
    """Validate spatial GeoDataFrame geometry and CRS integrity."""
    errors = []
    if 'geometry' not in gdf.columns:
        return {"valid": False, "errors": ["Missing geometry column"]}
        
    invalid_geoms = (~gdf.geometry.is_valid).sum()
    empty_geoms = (gdf.geometry.is_empty).sum()
    
    if invalid_geoms > 0:
        errors.append(f"Found {invalid_geoms} invalid geometries.")
    if empty_geoms > 0:
        errors.append(f"Found {empty_geoms} empty geometries.")
        
    return {
        "valid": len(errors) == 0,
        "errors": errors,
        "crs": str(gdf.crs),
        "invalid_geometry_count": int(invalid_geoms),
        "empty_geometry_count": int(empty_geoms)
    }

def generate_quality_report(dataset_name: str, raw_df: pd.DataFrame, cleaned_df: pd.DataFrame, duplicates_dropped: int = 0) -> Dict[str, Any]:
    """Generate structured Data Quality Report dictionary."""
    total_records = len(raw_df)
    valid_records = len(cleaned_df)
    invalid_records = total_records - valid_records - duplicates_dropped
    
    return {
        "Dataset": dataset_name,
        "Total Records": total_records,
        "Valid Records": valid_records,
        "Invalid Records": max(0, invalid_records),
        "Duplicates Dropped": duplicates_dropped,
        "Missing Values Handled": int(raw_df.isnull().sum().sum())
    }
