from typing import List, Optional
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.services import drain_service
from app.schemas.drain import DrainResponse

router = APIRouter()

@router.get(
    "/drains",
    response_model=List[DrainResponse],
    summary="Get drainage network features",
    description="Returns stormwater primary nallahs, secondary drains, and roadside gutters."
)
def read_drains(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    ward_id: Optional[int] = Query(None),
    drain_type: Optional[str] = Query(None),
    status: Optional[str] = Query(None),
    db: Session = Depends(get_db)
):
    drains = drain_service.get_drains(
        db=db,
        skip=skip,
        limit=limit,
        ward_id=ward_id,
        drain_type=drain_type,
        status=status
    )
    return drains
