from typing import Optional, Any, Dict
from pydantic import BaseModel
from datetime import datetime

class IncidentBase(BaseModel):
    incident_type: str  # waterlogging, blocked_drain, road_damage, drainage_failure, water_leak, other
    description: Optional[str] = None
    latitude: float
    longitude: float
    reported_at: datetime
    severity: str = "medium"  # low, medium, high, critical
    source: str = "citizen"  # citizen, municipal_worker, sensor, automated
    status: str = "reported"  # reported, investigating, resolved, closed
    ward_id: int
    evidence_quality: Optional[float] = 1.0

class IncidentCreate(IncidentBase):
    pass

class IncidentResponse(IncidentBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
