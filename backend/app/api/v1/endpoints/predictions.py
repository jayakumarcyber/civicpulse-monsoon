import os
from typing import Dict, Any, List, Optional
from datetime import datetime, timezone
from fastapi import APIRouter, Depends, Query, HTTPException, status
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.services import prediction_service
from ml.inference.predictor import RiskPredictor
from ml.inference.batch_predictor import run_batch_prediction

router = APIRouter()

class RiskRequest(BaseModel):
    ward_id: int
    horizon_hours: int = 24  # 24, 48, 72
    rainfall_last_24h: Optional[float] = 0.0
    rainfall_last_72h: Optional[float] = 0.0
    elevation_m: Optional[float] = 5.0
    drainage_quality_score: Optional[float] = 0.5
    historical_incident_density: Optional[float] = 1.0

class RiskResponse(BaseModel):
    ward_id: int
    horizon_hours: int
    predicted_probability: float
    risk_level: str
    model_version: str
    data_provenance: str

@router.post(
    "/risk",
    response_model=RiskResponse,
    summary="Predict waterlogging risk for ward & horizon",
    description="Returns live calibrated waterlogging probability and risk level (LOW, MEDIUM, HIGH, CRITICAL)."
)
def predict_risk_endpoint(request: RiskRequest):
    if request.horizon_hours not in [24, 48, 72]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="horizon_hours must be 24, 48, or 72"
        )
    
    predictor = RiskPredictor(horizon_hours=request.horizon_hours)
    res = predictor.predict_risk(request.model_dump())
    return res

@router.get(
    "/ward/{ward_id}",
    response_model=List[Dict[str, Any]],
    summary="Get predictions for a specific ward",
    description="Returns 24h, 48h, 72h waterlogging risk forecasts for the ward."
)
def get_ward_predictions_endpoint(ward_id: int, db: Session = Depends(get_db)):
    preds = prediction_service.get_ward_predictions(db, ward_id)
    if not preds:
        # Generate live predictions if not in DB yet
        results = []
        for h in [24, 48, 72]:
            predictor = RiskPredictor(horizon_hours=h)
            res = predictor.predict_risk({"ward_id": ward_id})
            results.append(res)
        return results

    return [
        {
            "id": p.id,
            "ward_id": p.ward_id,
            "prediction_timestamp": p.prediction_timestamp.isoformat() if p.prediction_timestamp else None,
            "horizon_hours": p.horizon_hours,
            "predicted_probability": p.predicted_probability,
            "risk_level": p.risk_level,
            "model_version": p.model_version,
            "data_provenance": "DEMO MODEL — TRAINED ON SYNTHETIC DATA"
        }
        for p in preds
    ]

@router.get(
    "",
    response_model=List[Dict[str, Any]],
    summary="Get multi-horizon predictions",
    description="Returns predictions filtered by horizon (hours=24, 48, or 72)."
)
def get_predictions_endpoint(
    hours: Optional[int] = Query(None, description="Horizon hours (24, 48, 72)"),
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    db: Session = Depends(get_db)
):
    if hours is not None and hours not in [24, 48, 72]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="hours filter must be 24, 48, or 72"
        )
    
    preds = prediction_service.get_predictions(db, horizon_hours=hours, skip=skip, limit=limit)
    if not preds:
        # Fallback batch simulation
        batch = run_batch_prediction()
        if hours is not None:
            batch = [p for p in batch if p['horizon_hours'] == hours]
        return batch

    return [
        {
            "id": p.id,
            "ward_id": p.ward_id,
            "prediction_timestamp": p.prediction_timestamp.isoformat() if p.prediction_timestamp else None,
            "horizon_hours": p.horizon_hours,
            "predicted_probability": p.predicted_probability,
            "risk_level": p.risk_level,
            "model_version": p.model_version,
            "data_provenance": "DEMO MODEL — TRAINED ON SYNTHETIC DATA"
        }
        for p in preds
    ]

@router.post(
    "/batch/run",
    response_model=Dict[str, Any],
    summary="Run batch risk prediction pipeline",
    description="Executes multi-horizon batch predictions for all wards and persists results to PostgreSQL."
)
def run_batch_prediction_endpoint():
    results = run_batch_prediction()
    return {
        "status": "success",
        "total_predictions_generated": len(results),
        "horizons_covered": [24, 48, 72],
        "model_version": "XGBoost_v1_DEMO",
        "data_provenance": "DEMO MODEL — TRAINED ON SYNTHETIC DATA"
    }
