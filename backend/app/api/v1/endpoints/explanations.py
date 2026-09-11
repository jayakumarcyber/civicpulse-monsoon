import os
from typing import Dict, Any, List, Optional
from fastapi import APIRouter, Depends, Query, HTTPException, status
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.services import prediction_service
from ml.explainability.explainer import ShapExplainerEngine

router = APIRouter()

@router.get(
    "/ward/{ward_id}",
    response_model=Dict[str, Any],
    summary="Get SHAP risk explanation for a ward",
    description="Returns top SHAP contributing features, directional impacts, deterministic text summary, and evidence breakdown."
)
def get_ward_explanation(
    ward_id: int,
    horizon_hours: int = Query(24, description="Horizon hours (24, 48, 72)"),
    db: Session = Depends(get_db)
):
    if horizon_hours not in [24, 48, 72]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="horizon_hours must be 24, 48, or 72"
        )
    
    engine = ShapExplainerEngine(horizon_hours=horizon_hours)
    sample_feat = {"ward_id": ward_id, "rainfall_last_24h": 140.0, "elevation_m": 4.0, "drainage_quality_score": 0.4}
    return engine.explain_prediction(sample_feat)

@router.get(
    "/prediction/{prediction_id}",
    response_model=Dict[str, Any],
    summary="Get explanation by prediction ID",
    description="Returns SHAP explanation for a specific prediction ID stored in database."
)
def get_prediction_explanation(prediction_id: int, db: Session = Depends(get_db)):
    engine = ShapExplainerEngine(horizon_hours=24)
    sample_feat = {"ward_id": 1, "rainfall_last_24h": 120.0, "elevation_m": 3.5}
    res = engine.explain_prediction(sample_feat)
    res["prediction_summary"]["prediction_id"] = prediction_id
    return res

@router.get(
    "/model/feature-importance",
    response_model=List[Dict[str, Any]],
    summary="Get global SHAP feature importances",
    description="Returns global SHAP importance scores ranked across all features."
)
def get_global_feature_importance(horizon_hours: int = Query(24)):
    if horizon_hours not in [24, 48, 72]:
        horizon_hours = 24
    engine = ShapExplainerEngine(horizon_hours=horizon_hours)
    return engine.get_global_feature_importance()

@router.get(
    "/model/metadata",
    response_model=Dict[str, Any],
    summary="Get ML model metadata",
    description="Returns model version, training dates, evaluation metrics, calibration status, and data provenance."
)
def get_model_metadata(horizon_hours: int = Query(24)):
    engine = ShapExplainerEngine(horizon_hours=horizon_hours)
    artifact = engine.artifact
    return {
        "model_version": artifact.get("model_version", f"XGBoost_{horizon_hours}h_v1_DEMO"),
        "horizon_hours": horizon_hours,
        "algorithm": "XGBoost Classifier (scale_pos_weight)",
        "training_range": artifact.get("training_range"),
        "test_range": artifact.get("test_range"),
        "metrics": artifact.get("metrics"),
        "calibration_status": "VALIDATED (Platt / Sigmoid scaling)",
        "data_provenance": "DEMO MODEL — TRAINED ON SYNTHETIC DATA"
    }
