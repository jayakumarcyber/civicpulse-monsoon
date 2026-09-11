from typing import List, Optional
from sqlalchemy.orm import Session
from app.models.facility import CriticalFacility

def get_facilities(
    db: Session,
    skip: int = 0,
    limit: int = 100,
    ward_id: Optional[int] = None,
    facility_type: Optional[str] = None
) -> List[CriticalFacility]:
    query = db.query(CriticalFacility)
    if ward_id is not None:
        query = query.filter(CriticalFacility.ward_id == ward_id)
    if facility_type is not None:
        query = query.filter(CriticalFacility.facility_type == facility_type)
    return query.offset(skip).limit(limit).all()
