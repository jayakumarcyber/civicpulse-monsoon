from datetime import datetime, timezone
from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from geoalchemy2 import Geometry

from app.db.base_class import Base

class Drain(Base):
    __tablename__ = "drains"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    drain_type = Column(String(50), nullable=False, default="secondary_drain")  # primary_nallah, secondary_drain, roadside_gutter
    capacity = Column(Float, nullable=True)  # Hydraulic capacity (e.g. m3/s)
    status = Column(String(30), nullable=False, default="operational")  # operational, partially_blocked, blocked, damaged
    
    # LineString Geometry in SRID 4326
    geometry = Column(Geometry("LINESTRING", srid=4326), nullable=False)
    
    ward_id = Column(Integer, ForeignKey("wards.id", ondelete="CASCADE"), nullable=False, index=True)

    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    updated_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

    # Relationships
    ward = relationship("Ward", back_populates="drains")
