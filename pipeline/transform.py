import pandas as pd
import geopandas as gpd
from shapely.geometry import Point

def spatial_join_points_to_wards(
    df_points: pd.DataFrame,
    wards_gdf: gpd.GeoDataFrame,
    lat_col: str = 'latitude',
    lon_col: str = 'longitude'
) -> pd.DataFrame:
    """Perform spatial join assigning point entities (incidents, rainfall gauges, facilities) to wards."""
    if df_points.empty or wards_gdf.empty:
        return df_points

    geometry = [Point(xy) for xy in zip(df_points[lon_col], df_points[lat_col])]
    gdf_points = gpd.GeoDataFrame(df_points, geometry=geometry, crs="EPSG:4326")
    
    # Ensure wards_gdf is in EPSG:4326
    if wards_gdf.crs and wards_gdf.crs.to_string() != "EPSG:4326":
        wards_gdf = wards_gdf.to_crs("EPSG:4326")

    # Select key ward columns to join
    ward_cols = [c for c in ['id', 'ward_code', 'name'] if c in wards_gdf.columns]
    wards_subset = wards_gdf[ward_cols + ['geometry']].rename(columns={'id': 'ward_id', 'name': 'ward_name'})

    joined = gpd.sjoin(gdf_points, wards_subset, how="left", predicate="intersects")
    
    # Drop index_right and temporary geometry if needed
    if 'index_right' in joined.columns:
        joined = joined.drop(columns=['index_right'])
        
    return pd.DataFrame(joined.drop(columns=['geometry']))

def spatial_join_lines_to_wards(
    lines_gdf: gpd.GeoDataFrame,
    wards_gdf: gpd.GeoDataFrame
) -> gpd.GeoDataFrame:
    """Perform spatial join associating line features (roads, drains) to wards."""
    if lines_gdf.empty or wards_gdf.empty:
        return lines_gdf

    if lines_gdf.crs and lines_gdf.crs.to_string() != "EPSG:4326":
        lines_gdf = lines_gdf.to_crs("EPSG:4326")
    if wards_gdf.crs and wards_gdf.crs.to_string() != "EPSG:4326":
        wards_gdf = wards_gdf.to_crs("EPSG:4326")

    ward_cols = [c for c in ['id', 'ward_code', 'name'] if c in wards_gdf.columns]
    wards_subset = wards_gdf[ward_cols + ['geometry']].rename(columns={'id': 'ward_id', 'name': 'ward_name'})

    joined = gpd.sjoin(lines_gdf, wards_subset, how="left", predicate="intersects")
    if 'index_right' in joined.columns:
        joined = joined.drop(columns=['index_right'])
        
    return joined

def run_transform_pipeline():
    print("================ RUNNING SPATIAL TRANSFORM PIPELINE ================")
    print("[INFO] Spatial Join module ready.")

if __name__ == "__main__":
    run_transform_pipeline()
