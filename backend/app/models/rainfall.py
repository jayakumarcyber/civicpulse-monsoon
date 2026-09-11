from datetime import datetime, timezone
from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from geoalchemy2 import Geometry

from app.db.base_class import Base

class RainfallRecord(Base):
    __tablename__ = "rainfall_records"

    id = Column(Integer, primary_key=True, index=True)
    location = Column(Geometry("POINT", srid=4326), nullable=True)
    recorded_at = Column(DateTime(timezone=True), nullable=False, index=True)
    rainfall_mm = Column(Float, nullable=False)
    forecast_hours = Column(Integer, nullable=False, default=0)  # 0 (observed), 24, 48, 72
    source = Column(String(100), nullable=False, default="sensor")  # imd, sensor, forecast_api
    is_forecast = Column(Boolean, nullable=False, default=False)
    
    ward_id = Column(Integer, ForeignKey("wards.id", ondelete="SET NULL"), nullable=True, index=True)
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

    # Relationships
    ward = relationship("Ward", back_populates="rainfall_records")


class HistoricalRainfallRecord(Base):
    __tablename__ = "historical_rainfall_records"

    id = Column(Integer, primary_key=True, index=True)
    source_file = Column(String(255), nullable=False, index=True)
    year = Column(String(50), nullable=False, index=True)
    period_or_season = Column(String(100), nullable=True, index=True)
    state = Column(String(100), nullable=False, default="Tamil Nadu", index=True)
    district_or_subdivision = Column(String(100), nullable=False, index=True)
    actual_rainfall_mm = Column(Float, nullable=False)
    normal_rainfall_mm = Column(Float, nullable=True)
    percentage_deviation = Column(Float, nullable=True)
    rainfall_type = Column(String(100), nullable=False, default="HISTORICAL_DISTRICT")
    data_source_type = Column(String(100), nullable=False, default="Historical Government/Public Dataset")
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
