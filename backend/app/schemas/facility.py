from typing import Optional
from pydantic import BaseModel
from datetime import datetime

class FacilityBase(BaseModel):
    name: str
    facility_type: str  # school, hospital, healthcare, emergency_service, transport, government, other
    latitude: float
    longitude: float
    capacity: Optional[int] = None
    ward_id: int

class FacilityCreate(FacilityBase):
    pass

class FacilityResponse(FacilityBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
