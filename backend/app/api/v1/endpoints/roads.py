from typing import List, Optional
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.services import road_service
from app.schemas.road import RoadResponse

router = APIRouter()

@router.get(
    "/roads",
    response_model=List[RoadResponse],
    summary="Get road network segments",
    description="Returns municipal road segments filtered by ward or road type."
)
def read_roads(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    ward_id: Optional[int] = Query(None),
    road_type: Optional[str] = Query(None),
    db: Session = Depends(get_db)
):
    roads = road_service.get_roads(
        db=db,
        skip=skip,
        limit=limit,
        ward_id=ward_id,
        road_type=road_type
    )
    return roads
