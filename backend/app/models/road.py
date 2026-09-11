from datetime import datetime, timezone
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from geoalchemy2 import Geometry

from app.db.base_class import Base

class Road(Base):
    __tablename__ = "roads"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    road_type = Column(String(50), nullable=False, default="local")  # arterial, collector, local, highway
    importance = Column(String(20), nullable=False, default="medium")  # critical, high, medium, low
    
    # LineString Geometry in SRID 4326
    geometry = Column(Geometry("LINESTRING", srid=4326), nullable=False)
    
    ward_id = Column(Integer, ForeignKey("wards.id", ondelete="CASCADE"), nullable=False, index=True)

    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    updated_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

    # Relationships
    ward = relationship("Ward", back_populates="roads")
