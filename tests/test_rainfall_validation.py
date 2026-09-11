import pytest
import pandas as pd
from pipeline.clean import clean_rainfall_values, clean_coordinates, clean_timestamps
from pipeline.validate import validate_rainfall_df

def test_clean_rainfall_negative_values():
    raw_data = pd.DataFrame({
        "timestamp": ["2026-08-16T12:00:00Z", "2026-08-16T13:00:00Z"],
        "latitude": [19.01, 19.02],
        "longitude": [72.83, 72.84],
        "rainfall_mm": [-5.0, 45.0]
    })
    df_clean = clean_rainfall_values(raw_data)
    assert len(df_clean) == 1
    assert (df_clean["rainfall_mm"] >= 0).all()

def test_validate_rainfall_schema():
    valid_data = pd.DataFrame({
        "timestamp": ["2026-08-16T12:00:00Z"],
        "latitude": [19.01],
        "longitude": [72.83],
        "rainfall_mm": [25.5]
    })
    val_result = validate_rainfall_df(valid_data)
    assert val_result["valid"] is True
