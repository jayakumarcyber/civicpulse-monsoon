from datetime import datetime, timezone
from sqlalchemy import Column, Integer, String, Float, DateTime
from sqlalchemy.orm import relationship
from geoalchemy2 import Geometry

from app.db.base_class import Base

class Ward(Base):
    __tablename__ = "wards"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(150), nullable=False)
    city = Column(String(100), nullable=False, default="Chennai")
    district = Column(String(100), nullable=False, default="Chennai", index=True)
    state = Column(String(50), nullable=False, default="Tamil Nadu", index=True)
    ward_code = Column(String(50), unique=True, nullable=False, index=True)
    
    # Requirement 8: Geographic Hierarchy Fields
    administrative_type = Column(String(50), nullable=False, default="Urban")  # Urban vs Rural
    local_body = Column(String(150), nullable=True, index=True)  # Corporation / Municipality / Town Panchayat
    taluk = Column(String(100), nullable=True, index=True)
    block = Column(String(100), nullable=True, index=True)
    village_panchayat = Column(String(150), nullable=True, index=True)
    ward_number = Column(Integer, nullable=True, index=True)
    village = Column(String(150), nullable=True, index=True)
    locality = Column(String(150), nullable=True, index=True)
    
    data_source = Column(String(150), nullable=False, default="Tamil Nadu GIS / ULB Portal")
    data_status = Column(String(100), nullable=False, default="Official Data")

    population = Column(Integer, nullable=True)
    area_sq_km = Column(Float, nullable=True)
    
    # Polygon / MultiPolygon Geometry in WGS84 (SRID 4326)
    geometry = Column(Geometry("MULTIPOLYGON", srid=4326), nullable=True)

    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    updated_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

    # Relationships
    incidents = relationship("CivicIncident", back_populates="ward", cascade="all, delete-orphan")
    rainfall_records = relationship("RainfallRecord", back_populates="ward")
    roads = relationship("Road", back_populates="ward")
    drains = relationship("Drain", back_populates="ward")
    waterbodies = relationship("Waterbody", back_populates="ward")
    population_zones = relationship("PopulationZone", back_populates="ward")
    critical_facilities = relationship("CriticalFacility", back_populates="ward")
    infrastructure_assets = relationship("InfrastructureAsset", back_populates="ward")
