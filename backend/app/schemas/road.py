from typing import Optional, Any, Dict
from pydantic import BaseModel
from datetime import datetime

class RoadBase(BaseModel):
    name: str
    road_type: str = "local"  # arterial, collector, local, highway
    importance: str = "medium"  # critical, high, medium, low
    ward_id: int

class RoadCreate(RoadBase):
    geometry: Dict[str, Any]

class RoadResponse(RoadBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
