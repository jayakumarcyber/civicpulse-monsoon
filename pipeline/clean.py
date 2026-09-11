import pandas as pd
import geopandas as gpd
from shapely.geometry import shape
from shapely.validation import make_valid
from typing import Tuple, Optional

def clean_coordinates(df: pd.DataFrame, lat_col: str = 'latitude', lon_col: str = 'longitude') -> pd.DataFrame:
    """Filter valid coordinates within realistic WGS84 range."""
    if lat_col not in df.columns or lon_col not in df.columns:
        return df
    
    df = df.dropna(subset=[lat_col, lon_col])
    valid_mask = (
        (df[lat_col] >= -90.0) & (df[lat_col] <= 90.0) &
        (df[lon_col] >= -180.0) & (df[lon_col] <= 180.0) &
        ~((df[lat_col] == 0.0) & (df[lon_col] == 0.0))
    )
    return df[valid_mask].copy()

def clean_timestamps(df: pd.DataFrame, timestamp_col: str = 'timestamp') -> pd.DataFrame:
    """Parse timestamps to UTC ISO format, dropping unparseable rows."""
    if timestamp_col not in df.columns:
        return df
    
    df = df.copy()
    df[timestamp_col] = pd.to_datetime(df[timestamp_col], errors='coerce', utc=True)
    return df.dropna(subset=[timestamp_col])

def clean_rainfall_values(df: pd.DataFrame, rainfall_col: str = 'rainfall_mm') -> pd.DataFrame:
    """Ensure non-negative rainfall values and cap non-physical extreme outliers (> 1000mm/hr)."""
    if rainfall_col not in df.columns:
        return df
    
    df = df.copy()
    df = df[df[rainfall_col] >= 0.0]
    df[rainfall_col] = df[rainfall_col].clip(upper=1000.0)
    return df

def deduplicate_records(df: pd.DataFrame, subset: Optional[list] = None) -> pd.DataFrame:
    """Remove exact duplicate rows based on subset keys."""
    if subset is None:
        return df.drop_duplicates().copy()
    return df.drop_duplicates(subset=subset).copy()

def normalize_crs(gdf: gpd.GeoDataFrame, target_crs: str = "EPSG:4326") -> gpd.GeoDataFrame:
    """Ensure GeoDataFrame is in target CRS (default WGS84 EPSG:4326)."""
    if gdf.crs is None:
        gdf = gdf.set_crs(target_crs)
    elif gdf.crs.to_string() != target_crs:
        gdf = gdf.to_crs(target_crs)
    return gdf

def clean_geometries(gdf: gpd.GeoDataFrame) -> gpd.GeoDataFrame:
    """Filter out empty geometries and repair invalid polygons using shapely make_valid."""
    if 'geometry' not in gdf.columns:
        return gdf
    
    gdf = gdf[gdf.geometry.notnull() & ~gdf.geometry.is_empty].copy()
    gdf['geometry'] = gdf.geometry.apply(lambda geom: make_valid(geom) if not geom.is_valid else geom)
    return gdf
