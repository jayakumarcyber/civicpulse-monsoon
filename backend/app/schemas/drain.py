from typing import Optional, Any, Dict
from pydantic import BaseModel
from datetime import datetime

class DrainBase(BaseModel):
    name: str
    drain_type: str = "secondary_drain"  # primary_nallah, secondary_drain, roadside_gutter
    capacity: Optional[float] = None
    status: str = "operational"  # operational, partially_blocked, blocked, damaged
    ward_id: int

class DrainCreate(DrainBase):
    geometry: Dict[str, Any]

class DrainResponse(DrainBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
