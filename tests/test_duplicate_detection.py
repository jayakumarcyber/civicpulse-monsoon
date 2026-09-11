import pytest
import pandas as pd
from pipeline.clean import deduplicate_records

def test_deduplicate_records():
    df = pd.DataFrame({
        "timestamp": ["2026-08-16T12:00:00Z", "2026-08-16T12:00:00Z", "2026-08-16T13:00:00Z"],
        "latitude": [19.01, 19.01, 19.02],
        "longitude": [72.83, 72.83, 72.84],
        "rainfall_mm": [10.0, 10.0, 15.0]
    })
    df_dedup = deduplicate_records(df, subset=["timestamp", "latitude", "longitude"])
    assert len(df_dedup) == 2
