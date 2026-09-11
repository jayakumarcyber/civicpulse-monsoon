from datetime import datetime, timezone
from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.orm import relationship

from app.db.base_class import Base

class DrainageNode(Base):
    __tablename__ = "drainage_nodes"

    id = Column(Integer, primary_key=True, index=True)
    node_id = Column(String(50), unique=True, nullable=False, index=True)  # e.g., DRAIN_001, ROAD_014, WARD_1
    node_type = Column(String(30), nullable=False, index=True)  # drain, road, ward, population_zone, waterbody, critical_facility, low_lying_area
    name = Column(String(150), nullable=False)
    ward_id = Column(Integer, ForeignKey("wards.id", ondelete="CASCADE"), nullable=False, index=True)
    status = Column(String(30), nullable=True, default="unknown")
    data_source = Column(String(50), nullable=False, default="SYNTHETIC_DEMO_DATA")
    confidence = Column(String(50), nullable=False, default="INFERRED_SPATIAL_RELATIONSHIP")
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

    # Relationships
    ward = relationship("Ward")

class DrainageEdge(Base):
    __tablename__ = "drainage_edges"

    id = Column(Integer, primary_key=True, index=True)
    edge_id = Column(String(50), unique=True, nullable=False, index=True)
    source_node_id = Column(String(50), ForeignKey("drainage_nodes.node_id", ondelete="CASCADE"), nullable=False, index=True)
    target_node_id = Column(String(50), ForeignKey("drainage_nodes.node_id", ondelete="CASCADE"), nullable=False, index=True)
    edge_type = Column(String(30), nullable=False, index=True)  # drains_to, near, serves, flows_toward, intersects, affects, located_in
    distance_m = Column(Float, nullable=False, default=0.0)
    relationship_strength = Column(Float, nullable=False, default=1.0)
    relationship_label = Column(String(50), nullable=False, default="INFERRED_SPATIAL_RELATIONSHIP")
    data_source = Column(String(50), nullable=False, default="SYNTHETIC_DEMO_DATA")
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
