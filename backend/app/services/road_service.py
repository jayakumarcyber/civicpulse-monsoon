from typing import List, Optional
from sqlalchemy.orm import Session
from app.models.road import Road

def get_roads(
    db: Session,
    skip: int = 0,
    limit: int = 100,
    ward_id: Optional[int] = None,
    road_type: Optional[str] = None
) -> List[Road]:
    query = db.query(Road)
    if ward_id is not None:
        query = query.filter(Road.ward_id == ward_id)
    if road_type is not None:
        query = query.filter(Road.road_type == road_type)
    return query.offset(skip).limit(limit).all()
