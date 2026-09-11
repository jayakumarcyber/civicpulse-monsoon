from typing import Dict, Any, List, Optional
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.services import impact_service

router = APIRouter()

@router.get(
    "/rankings",
    response_model=List[Dict[str, Any]],
    summary="Get civic priority queue rankings",
    description="Returns ranked priority list (P1-P4) of administrative wards strictly filtered by district and state."
)
def get_priority_rankings_endpoint(
    district: Optional[str] = Query(None),
    state: Optional[str] = Query(None),
    db: Session = Depends(get_db)
):
    return impact_service.get_priority_rankings(db, district=district, state=state)

@router.get(
    "/ward/{ward_id}",
    response_model=Dict[str, Any],
    summary="Get detailed priority assessment & reasons for ward",
    description="Returns priority score (0-100), priority level (P1-P4), and data-driven rationale."
)
def get_ward_priority_endpoint(ward_id: int, db: Session = Depends(get_db)):
    return impact_service.get_priority_assessment_for_ward(db, ward_id=ward_id)
