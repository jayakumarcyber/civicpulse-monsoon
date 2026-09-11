from datetime import datetime, timezone
from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Text
from sqlalchemy.orm import relationship

from app.db.base_class import Base

class Inspection(Base):
    __tablename__ = "inspections"

    id = Column(Integer, primary_key=True, index=True)
    asset_id = Column(Integer, ForeignKey("infrastructure_assets.id", ondelete="CASCADE"), nullable=False, index=True)
    inspection_date = Column(DateTime(timezone=True), nullable=False, default=lambda: datetime.now(timezone.utc))
    inspection_type = Column(String(50), nullable=False, default="routine")  # routine, post_monsoon, emergency
    findings = Column(Text, nullable=True)
    condition_score = Column(Float, nullable=False, default=5.0)  # 1.0 to 10.0 scale
    inspector = Column(String(100), nullable=False)
    latitude = Column(Float, nullable=True)
    longitude = Column(Float, nullable=True)

    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

    # Relationships
    asset = relationship("InfrastructureAsset", back_populates="inspections")
