from typing import List, Optional
from sqlalchemy.orm import Session
from app.models.drain import Drain

def get_drains(
    db: Session,
    skip: int = 0,
    limit: int = 100,
    ward_id: Optional[int] = None,
    drain_type: Optional[str] = None,
    status: Optional[str] = None
) -> List[Drain]:
    query = db.query(Drain)
    if ward_id is not None:
        query = query.filter(Drain.ward_id == ward_id)
    if drain_type is not None:
        query = query.filter(Drain.drain_type == drain_type)
    if status is not None:
        query = query.filter(Drain.status == status)
    return query.offset(skip).limit(limit).all()
