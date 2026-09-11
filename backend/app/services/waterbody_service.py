from typing import List, Optional
from sqlalchemy.orm import Session
from app.models.waterbody import Waterbody

def get_waterbodies(
    db: Session,
    skip: int = 0,
    limit: int = 100,
    ward_id: Optional[int] = None
) -> List[Waterbody]:
    query = db.query(Waterbody)
    if ward_id is not None:
        query = query.filter(Waterbody.ward_id == ward_id)
    return query.offset(skip).limit(limit).all()
