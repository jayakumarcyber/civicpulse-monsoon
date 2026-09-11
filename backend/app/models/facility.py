from datetime import datetime, timezone
from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from geoalchemy2 import Geometry

from app.db.base_class import Base

class CriticalFacility(Base):
    __tablename__ = "critical_facilities"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(150), nullable=False)
    facility_type = Column(String(50), nullable=False, index=True)  # school, hospital, healthcare, emergency_service, transport, government, other
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)
    
    # Point Geometry in SRID 4326
    location = Column(Geometry("POINT", srid=4326), nullable=False)
    capacity = Column(Integer, nullable=True)
    
    ward_id = Column(Integer, ForeignKey("wards.id", ondelete="CASCADE"), nullable=False, index=True)

    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    updated_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

    # Relationships
    ward = relationship("Ward", back_populates="critical_facilities")
