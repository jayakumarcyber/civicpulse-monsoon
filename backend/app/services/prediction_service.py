from typing import List, Optional, Dict, Any
from datetime import datetime, timezone
from sqlalchemy.orm import Session

from app.models.prediction import RiskPrediction

def create_prediction(
    db: Session,
    ward_id: int,
    prediction_timestamp: datetime,
    horizon_hours: int,
    predicted_probability: float,
    risk_level: str,
    model_version: str = "XGBoost_v1_DEMO"
) -> RiskPrediction:
    pred = RiskPrediction(
        ward_id=ward_id,
        prediction_timestamp=prediction_timestamp,
        horizon_hours=horizon_hours,
        predicted_probability=predicted_probability,
        risk_level=risk_level,
        model_version=model_version
    )
    db.add(pred)
    db.commit()
    db.refresh(pred)
    return pred

def get_predictions(
    db: Session,
    ward_id: Optional[int] = None,
    horizon_hours: Optional[int] = None,
    skip: int = 0,
    limit: int = 100
) -> List[RiskPrediction]:
    query = db.query(RiskPrediction)
    if ward_id is not None:
        query = query.filter(RiskPrediction.ward_id == ward_id)
    if horizon_hours is not None:
        query = query.filter(RiskPrediction.horizon_hours == horizon_hours)
    return query.order_by(RiskPrediction.prediction_timestamp.desc()).offset(skip).limit(limit).all()

def get_ward_predictions(db: Session, ward_id: int) -> List[RiskPrediction]:
    return db.query(RiskPrediction).filter(RiskPrediction.ward_id == ward_id).order_by(RiskPrediction.horizon_hours.asc()).all()
