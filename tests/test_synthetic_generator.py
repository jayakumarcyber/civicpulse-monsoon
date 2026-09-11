import pytest
from pipeline.generate_synthetic import generate_synthetic_wards, generate_synthetic_rainfall, generate_synthetic_incidents

def test_synthetic_generator_domain_logic():
    wards_gdf = generate_synthetic_wards()
    assert len(wards_gdf) == 4
    assert (wards_gdf['data_source_type'] == 'SYNTHETIC_DEMO_DATA').all()
    
    rainfall_df = generate_synthetic_rainfall(wards_gdf, days=2)
    assert len(rainfall_df) > 0
    assert (rainfall_df['data_source_type'] == 'SYNTHETIC_DEMO_DATA').all()
    
    incidents_df = generate_synthetic_incidents(wards_gdf, rainfall_df)
    assert len(incidents_df) > 0
    assert (incidents_df['data_source_type'] == 'SYNTHETIC_DEMO_DATA').all()
