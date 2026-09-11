from datetime import datetime, timezone
from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, JSON
from sqlalchemy.orm import relationship

from app.db.base_class import Base

class ImpactAssessment(Base):
    __tablename__ = "impact_assessments"

    id = Column(Integer, primary_key=True, index=True)
    ward_id = Column(Integer, ForeignKey("wards.id", ondelete="CASCADE"), nullable=False, index=True)
    prediction_id = Column(Integer, ForeignKey("risk_predictions.id", ondelete="SET NULL"), nullable=True, index=True)
    potential_population_exposure = Column(Integer, nullable=False, default=0)
    hospital_count = Column(Integer, nullable=False, default=0)
    school_count = Column(Integer, nullable=False, default=0)
    emergency_facility_count = Column(Integer, nullable=False, default=0)
    transport_facility_count = Column(Integer, nullable=False, default=0)
    critical_facility_count = Column(Integer, nullable=False, default=0)
    exposed_road_count = Column(Integer, nullable=False, default=0)
    exposed_drain_count = Column(Integer, nullable=False, default=0)
    historical_waterlogging_count = Column(Integer, nullable=False, default=0)
    data_quality_status = Column(String(50), nullable=False, default="VERIFIED_SPATIAL_EXPOSURE")
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

    # Relationships
    ward = relationship("Ward")
    prediction = relationship("RiskPrediction")

class PriorityAssessment(Base):
    __tablename__ = "priority_assessments"

    id = Column(Integer, primary_key=True, index=True)
    impact_assessment_id = Column(Integer, ForeignKey("impact_assessments.id", ondelete="CASCADE"), nullable=False, index=True)
    ward_id = Column(Integer, ForeignKey("wards.id", ondelete="CASCADE"), nullable=False, index=True)
    priority_score = Column(Float, nullable=False, default=0.0)
    priority_level = Column(String(20), nullable=False, index=True)  # P1 — CRITICAL, P2 — HIGH, P3 — MEDIUM, P4 — LOW
    priority_reasons = Column(JSON, nullable=False)
    calculation_version = Column(String(50), nullable=False, default="CivicPriority_v1_DEMO")
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

    # Relationships
    impact_assessment = relationship("ImpactAssessment")
    ward = relationship("Ward")
