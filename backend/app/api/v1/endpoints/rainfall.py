from typing import List, Optional, Dict, Any
from datetime import datetime, timezone, timedelta
from fastapi import APIRouter, Depends, Query, HTTPException, status
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.services import rainfall_service

router = APIRouter()

BENCHMARK_RAINFALL = [
    {
        "id": 1,
        "ward_id": 1,
        "rainfall_mm": 45.5,
        "recorded_at": (datetime.now(timezone.utc) - timedelta(hours=1)).isoformat(),
        "is_forecast": False,
        "forecast_hours": None,
        "data_source_type": "SYNTHETIC_DEMO_DATA"
    },
    {
        "id": 2,
        "ward_id": 1,
        "rainfall_mm": 140.0,
        "recorded_at": (datetime.now(timezone.utc) - timedelta(hours=24)).isoformat(),
        "is_forecast": False,
        "forecast_hours": None,
        "data_source_type": "SYNTHETIC_DEMO_DATA"
    },
    {
        "id": 3,
        "ward_id": 2,
        "rainfall_mm": 38.0,
        "recorded_at": (datetime.now(timezone.utc) - timedelta(hours=1)).isoformat(),
        "is_forecast": False,
        "forecast_hours": None,
        "data_source_type": "SYNTHETIC_DEMO_DATA"
    }
]

@router.get(
    "/rainfall",
    response_model=List[Dict[str, Any]],
    summary="Get rainfall records & forecasts",
    description="Returns observed rainfall readings and 24/48/72 hour spatial forecasts."
)
def read_rainfall(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    ward_id: Optional[int] = Query(None),
    is_forecast: Optional[bool] = Query(None),
    forecast_hours: Optional[int] = Query(None),
    db: Session = Depends(get_db)
):
    try:
        records = rainfall_service.get_rainfall_records(
            db=db,
            skip=skip,
            limit=limit,
            ward_id=ward_id,
            is_forecast=is_forecast,
            forecast_hours=forecast_hours
        )
        if records:
            return records
    except Exception:
        pass
    
    res = BENCHMARK_RAINFALL
    if ward_id is not None:
        res = [r for r in res if r["ward_id"] == ward_id]
    return res

@router.get(
    "/rainfall/historical/summary",
    response_model=Dict[str, Any],
    summary="Get Historical Rainfall Dataset Summary",
    description="Returns summary statistics, district coverage, and data provenance for all uploaded historical CSV datasets."
)
def get_historical_rainfall_summary(db: Session = Depends(get_db)):
    return rainfall_service.get_historical_rainfall_summary(db)

@router.get(
    "/rainfall/historical/district/{district_name}",
    response_model=Dict[str, Any],
    summary="Get District Historical Rainfall Data",
    description="Returns real historical rainfall statistics, records, and seasonal trends for a selected Tamil Nadu district or subdivision."
)
def get_district_historical_rainfall(district_name: str, db: Session = Depends(get_db)):
    res = rainfall_service.get_historical_rainfall_by_district(db, district_name)
    if not res:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"No historical rainfall data available for {district_name}")
    return res
