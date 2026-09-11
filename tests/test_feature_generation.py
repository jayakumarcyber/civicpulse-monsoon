import pytest
import pandas as pd
from pipeline.generate_features import build_temporal_features

def test_build_temporal_features():
    rainfall_df = pd.DataFrame({
        "ward_id": [1, 1, 1],
        "timestamp": [
            "2026-08-16T10:00:00Z",
            "2026-08-16T11:00:00Z",
            "2026-08-16T12:00:00Z"
        ],
        "rainfall_mm": [10.0, 20.0, 30.0],
        "forecast_hours": [0, 0, 0]
    })
    incidents_df = pd.DataFrame()
    
    features = build_temporal_features(rainfall_df, incidents_df)
    assert len(features) == 3
    assert "rainfall_last_1h" in features.columns
    assert "rainfall_last_24h" in features.columns
    assert features.iloc[-1]["rainfall_last_24h"] == 60.0
