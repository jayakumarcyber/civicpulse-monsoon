import pytest
import pandas as pd
import geopandas as gpd
from shapely.geometry import Polygon
from pipeline.transform import spatial_join_points_to_wards

def test_spatial_join_points_to_wards():
    wards_gdf = gpd.GeoDataFrame({
        "id": [1],
        "name": ["Dadar"],
        "geometry": [Polygon([(72.80, 19.00), (72.90, 19.00), (72.90, 19.10), (72.80, 19.10), (72.80, 19.00)])]
    }, crs="EPSG:4326")
    
    incidents_df = pd.DataFrame({
        "incident_id": ["INC-01", "INC-OUTSIDE"],
        "latitude": [19.05, 20.50],
        "longitude": [72.85, 75.00]
    })
    
    joined = spatial_join_points_to_wards(incidents_df, wards_gdf)
    assert len(joined) == 2
    assert joined.loc[joined['incident_id'] == 'INC-01', 'ward_id'].values[0] == 1
    assert pd.isna(joined.loc[joined['incident_id'] == 'INC-OUTSIDE', 'ward_id'].values[0])
