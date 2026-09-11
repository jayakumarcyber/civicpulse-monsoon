from datetime import datetime, timezone
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from geoalchemy2 import Geometry

from app.db.base_class import Base

class InfrastructureAsset(Base):
    __tablename__ = "infrastructure_assets"

    id = Column(Integer, primary_key=True, index=True)
    asset_type = Column(String(50), nullable=False, index=True)  # pumping_station, floodgate, culvert, sluice_gate, stormwater_pump
    name = Column(String(100), nullable=False)
    age_years = Column(Integer, nullable=True)
    condition = Column(String(30), nullable=False, default="good")  # good, fair, poor, critical
    owner_department = Column(String(100), nullable=False, default="Storm Water Drains Dept", index=True)
    
    # Point Geometry in SRID 4326
    geometry = Column(Geometry("POINT", srid=4326), nullable=False)
    
    ward_id = Column(Integer, ForeignKey("wards.id", ondelete="CASCADE"), nullable=False, index=True)

    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    updated_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

    # Relationships
    ward = relationship("Ward", back_populates="infrastructure_assets")
    inspections = relationship("Inspection", back_populates="asset", cascade="all, delete-orphan")
    repair_records = relationship("RepairRecord", back_populates="asset", cascade="all, delete-orphan")
