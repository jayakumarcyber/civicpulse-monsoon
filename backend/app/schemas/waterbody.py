from typing import Optional, Any, Dict
from pydantic import BaseModel
from datetime import datetime

class WaterbodyBase(BaseModel):
    name: str
    type: str = "lake"  # lake, pond, river, retention_basin
    ward_id: int

class WaterbodyCreate(WaterbodyBase):
    geometry: Dict[str, Any]

class WaterbodyResponse(WaterbodyBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
