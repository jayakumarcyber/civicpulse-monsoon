from datetime import datetime, timezone
from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Text
from sqlalchemy.orm import relationship

from app.db.base_class import Base

class RepairRecord(Base):
    __tablename__ = "repair_records"

    id = Column(Integer, primary_key=True, index=True)
    asset_id = Column(Integer, ForeignKey("infrastructure_assets.id", ondelete="CASCADE"), nullable=False, index=True)
    repair_date = Column(DateTime(timezone=True), nullable=False, default=lambda: datetime.now(timezone.utc))
    repair_type = Column(String(50), nullable=False)  # desilting, structural_fix, pump_replacement
    description = Column(Text, nullable=True)
    cost = Column(Float, nullable=False, default=0.0)
    status = Column(String(30), nullable=False, default="scheduled")  # scheduled, in_progress, completed
    completed_by = Column(String(100), nullable=True)

    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

    # Relationships
    asset = relationship("InfrastructureAsset", back_populates="repair_records")
