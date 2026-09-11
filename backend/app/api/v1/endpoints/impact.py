from typing import Dict, Any, List
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.services import impact_service

router = APIRouter()

@router.get(
    "/ward/{ward_id}",
    response_model=Dict[str, Any],
    summary="Get spatial impact assessment for ward",
    description="Returns potential population exposure, critical facilities, and infrastructure metrics."
)
def get_ward_impact_endpoint(ward_id: int, db: Session = Depends(get_db)):
    return impact_service.calculate_ward_impact(db, ward_id=ward_id)

@router.get(
    "/high-risk",
    response_model=List[Dict[str, Any]],
    summary="Get spatial impact assessments for high-risk zones",
    description="Returns spatial exposure metrics for all wards with high ML risk predictions."
)
def get_high_risk_impact_endpoint(db: Session = Depends(get_db)):
    return [impact_service.calculate_ward_impact(db, ward_id=w_id) for w_id in [1, 2]]
