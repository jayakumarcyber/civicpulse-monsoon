from typing import List, Optional
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.services import waterbody_service
from app.schemas.waterbody import WaterbodyResponse

router = APIRouter()

@router.get(
    "/waterbodies",
    response_model=List[WaterbodyResponse],
    summary="Get municipal waterbodies",
    description="Returns lakes, ponds, rivers, and retention basins acting as drainage outfalls."
)
def read_waterbodies(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    ward_id: Optional[int] = Query(None),
    db: Session = Depends(get_db)
):
    waterbodies = waterbody_service.get_waterbodies(
        db=db,
        skip=skip,
        limit=limit,
        ward_id=ward_id
    )
    return waterbodies
