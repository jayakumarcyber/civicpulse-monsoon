from datetime import datetime, timezone
from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Text, Index
from sqlalchemy.orm import relationship
from geoalchemy2 import Geometry

from app.db.base_class import Base

class CivicIncident(Base):
    __tablename__ = "civic_incidents"

    id = Column(Integer, primary_key=True, index=True)
    incident_type = Column(String(50), nullable=False, index=True)  # waterlogging, blocked_drain, road_damage, drainage_failure, water_leak, other
    description = Column(Text, nullable=True)
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)
    
    # Point Geometry in SRID 4326
    location = Column(Geometry("POINT", srid=4326), nullable=False)
    
    reported_at = Column(DateTime(timezone=True), nullable=False, index=True)
    severity = Column(String(20), nullable=False, default="medium")  # low, medium, high, critical
    source = Column(String(50), nullable=False, default="citizen")  # citizen, municipal_worker, sensor, automated
    status = Column(String(20), nullable=False, default="reported", index=True)  # reported, investigating, resolved, closed
    
    ward_id = Column(Integer, ForeignKey("wards.id", ondelete="CASCADE"), nullable=False, index=True)
    evidence_quality = Column(Float, nullable=True, default=1.0)

    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    updated_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

    # Relationships
    ward = relationship("Ward", back_populates="incidents")
