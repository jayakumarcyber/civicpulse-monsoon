from typing import Optional, List, Dict, Any
from pydantic import BaseModel
from datetime import datetime

class RainfallBase(BaseModel):
    recorded_at: datetime
    rainfall_mm: float
    forecast_hours: int = 0  # 0, 24, 48, 72
    source: str = "sensor"
    is_forecast: bool = False
    ward_id: Optional[int] = None

class RainfallCreate(RainfallBase):
    pass

class RainfallResponse(RainfallBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True

class HistoricalRainfallRecordSchema(BaseModel):
    id: int
    source_file: str
    year: str
    period_or_season: Optional[str] = None
    state: str
    district_or_subdivision: str
    actual_rainfall_mm: float
    normal_rainfall_mm: Optional[float] = None
    percentage_deviation: Optional[float] = None
    rainfall_type: str
    data_source_type: str = "Historical Government/Public Dataset"

    class Config:
        from_attributes = True

class RainfallSummaryResponse(BaseModel):
    district_or_subdivision: str
    total_records: int
    available_years: List[str]
    sources_used: List[str]
    min_rainfall_mm: float
    max_rainfall_mm: float
    avg_rainfall_mm: float
    historical_records: List[HistoricalRainfallRecordSchema]
