from typing import List, Optional
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.services import facility_service
from app.schemas.facility import FacilityResponse

router = APIRouter()

@router.get(
    "/facilities",
    response_model=List[FacilityResponse],
    summary="Get critical municipal facilities",
    description="Returns schools, hospitals, transport hubs, emergency services, and government centers."
)
def read_facilities(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    ward_id: Optional[int] = Query(None),
    facility_type: Optional[str] = Query(None),
    db: Session = Depends(get_db)
):
    facilities = facility_service.get_facilities(
        db=db,
        skip=skip,
        limit=limit,
        ward_id=ward_id,
        facility_type=facility_type
    )
    return facilities
