import pytest
import geopandas as gpd
from shapely.geometry import Polygon
from pipeline.clean import clean_geometries, normalize_crs
from pipeline.validate import validate_geospatial_gdf

def test_geometry_validation_and_cleaning():
    # Create self-intersecting polygon (bowtie)
    invalid_poly = Polygon([(0, 0), (0, 2), (2, 0), (2, 2), (0, 0)])
    valid_poly = Polygon([(0, 0), (0, 1), (1, 1), (1, 0), (0, 0)])
    
    gdf = gpd.GeoDataFrame({'id': [1, 2], 'geometry': [invalid_poly, valid_poly]}, crs="EPSG:4326")
    
    val_before = validate_geospatial_gdf(gdf)
    assert val_before['valid'] is False
    assert val_before['invalid_geometry_count'] == 1
    
    gdf_clean = clean_geometries(gdf)
    val_after = validate_geospatial_gdf(gdf_clean)
    assert val_after['valid'] is True
