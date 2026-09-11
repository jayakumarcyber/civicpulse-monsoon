import sys
import os
import pytest
from datetime import datetime, timezone, timedelta

sys.path.insert(0, os.path.dirname(r"d:\CivicPulse-Monsoon\backend"))
sys.path.insert(0, r"d:\CivicPulse-Monsoon\backend")

from app.services.analytics_service import (
    calculate_rolling_rainfall_stats,
    calculate_incident_stats,
    get_chronological_time_splits
)

def test_rolling_rainfall_calculations():
    now = datetime.now(timezone.utc)
    records = [
        {"recorded_at": (now - timedelta(hours=70)).isoformat(), "rainfall_mm": 50.0, "is_forecast": False},
        {"recorded_at": (now - timedelta(hours=20)).isoformat(), "rainfall_mm": 30.0, "is_forecast": False},
        {"recorded_at": (now - timedelta(hours=2)).isoformat(), "rainfall_mm": 20.0, "is_forecast": False},
    ]
    stats = calculate_rolling_rainfall_stats(records)
    assert stats["rainfall_1h"] == 20.0
    assert stats["rainfall_6h"] == 20.0
    assert stats["rainfall_24h"] == 50.0
    assert stats["rainfall_72h"] == 100.0
    assert stats["cumulative_rainfall"] == 100.0

def test_incident_stats_and_window_counters():
    now = datetime.now(timezone.utc)
    incidents = [
        {"reported_at": (now - timedelta(days=5)).isoformat(), "incident_type": "waterlogging", "severity": "high"},
        {"reported_at": (now - timedelta(days=20)).isoformat(), "incident_type": "blocked_drain", "severity": "medium"},
        {"reported_at": (now - timedelta(days=80)).isoformat(), "incident_type": "waterlogging", "severity": "critical"},
    ]
    stats = calculate_incident_stats(incidents)
    assert stats["total_incidents"] == 3
    assert stats["waterlogging_count"] == 2
    assert stats["incident_count_7d"] == 1
    assert stats["incident_count_30d"] == 2
    assert stats["incident_count_90d"] == 3

def test_data_leakage_safeguards_and_chronological_splits():
    splits = get_chronological_time_splits()
    assert splits["total_records"] > 0
    assert "train" in splits["splits"]
    assert "validation" in splits["splits"]
    assert "test" in splits["splits"]
    assert splits["splits"]["train"]["ratio"] == "60%"
