from datetime import datetime, timezone
from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from geoalchemy2 import Geometry

from app.db.base_class import Base

class PopulationZone(Base):
    __tablename__ = "population_zones"

    id = Column(Integer, primary_key=True, index=True)
    zone_name = Column(String(100), nullable=False)
    population = Column(Integer, nullable=False, default=0)
    density = Column(Float, nullable=True)  # People per sq km
    
    # Polygon Geometry in SRID 4326
    geometry = Column(Geometry("POLYGON", srid=4326), nullable=False)
    
    ward_id = Column(Integer, ForeignKey("wards.id", ondelete="CASCADE"), nullable=False, index=True)

    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    updated_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

    # Relationships
    ward = relationship("Ward", back_populates="population_zones")
