from typing import Optional, Any, Dict, List
from pydantic import BaseModel, Field
from datetime import datetime

class WardBase(BaseModel):
    name: str
    city: str = "Mumbai"
    state: str = "Maharashtra"
    ward_code: str
    population: Optional[int] = None
    area_sq_km: Optional[float] = None

class WardCreate(WardBase):
    geometry: Dict[str, Any]  # GeoJSON Geometry Dict

class WardResponse(WardBase):
    id: int
    created_at: datetime
    updated_at: datetime
    geometry_geojson: Optional[Dict[str, Any]] = None

    class Config:
        from_attributes = True
