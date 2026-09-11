import pytest
import pandas as pd
from pipeline.validate import validate_incidents_df

def test_incident_validation_supported_types():
    data = pd.DataFrame({
        "incident_id": ["INC-01", "INC-02"],
        "incident_type": ["waterlogging", "invalid_unsupported_type"],
        "latitude": [19.01, 19.02],
        "longitude": [72.83, 72.84],
        "timestamp": ["2026-08-16T12:00:00Z", "2026-08-16T13:00:00Z"],
        "severity": ["high", "low"]
    })
    val_result = validate_incidents_df(data)
    assert val_result["valid"] is False
    assert "invalid_unsupported_type" in val_result["unsupported_types"]
