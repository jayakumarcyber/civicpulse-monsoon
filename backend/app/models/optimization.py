from datetime import datetime, timezone
from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Boolean, Text
from sqlalchemy.orm import relationship

from app.db.base_class import Base

class MunicipalTeam(Base):
    __tablename__ = "municipal_teams"

    id = Column(Integer, primary_key=True, index=True)
    team_id = Column(String(30), unique=True, nullable=False, index=True)  # e.g., TEAM_01, TEAM_02
    team_name = Column(String(100), nullable=False)
    skill_type = Column(String(50), nullable=False, index=True)  # drainage, road_maintenance, general_maintenance, emergency
    daily_capacity_interventions = Column(Integer, nullable=False, default=3)
    working_hours = Column(Float, nullable=False, default=8.0)
    department = Column(String(100), nullable=False, default="Storm Water Drains Dept")
    is_active = Column(Boolean, nullable=False, default=True)
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

class InterventionType(Base):
    __tablename__ = "intervention_types"

    id = Column(Integer, primary_key=True, index=True)
    action_type = Column(String(50), unique=True, nullable=False, index=True)  # drain_inspection, drain_cleaning, desilting, culvert_inspection, pump_deployment
    name = Column(String(100), nullable=False)
    required_skill = Column(String(50), nullable=False)
    estimated_cost_inr = Column(Float, nullable=False, default=5000.0)
    estimated_duration_hours = Column(Float, nullable=False, default=3.0)
    eligibility_rule_description = Column(String(250), nullable=False)

class InterventionCandidate(Base):
    __tablename__ = "intervention_candidates"

    id = Column(Integer, primary_key=True, index=True)
    action_id = Column(String(50), unique=True, nullable=False, index=True)  # ACT_001, ACT_002
    ward_id = Column(Integer, ForeignKey("wards.id", ondelete="CASCADE"), nullable=False, index=True)
    action_type = Column(String(50), ForeignKey("intervention_types.action_type"), nullable=False, index=True)
    estimated_cost = Column(Float, nullable=False, default=5000.0)
    estimated_duration = Column(Float, nullable=False, default=3.0)
    required_skill = Column(String(50), nullable=False)
    expected_benefit = Column(Float, nullable=False, default=50.0)
    evidence_summary = Column(String(250), nullable=False)
    data_quality = Column(String(50), nullable=False, default="DEMO_ELIGIBILITY_EVIDENCE")
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

    # Relationships
    ward = relationship("Ward")

class OptimizationRun(Base):
    __tablename__ = "optimization_runs"

    id = Column(Integer, primary_key=True, index=True)
    run_id = Column(String(50), unique=True, nullable=False, index=True)
    available_budget_inr = Column(Float, nullable=False, default=50000.0)
    available_hours = Column(Float, nullable=False, default=24.0)
    total_teams_count = Column(Integer, nullable=False, default=3)
    used_budget_inr = Column(Float, nullable=False, default=0.0)
    used_teams_count = Column(Integer, nullable=False, default=0)
    selected_actions_count = Column(Integer, nullable=False, default=0)
    optimization_status = Column(String(30), nullable=False, default="OPTIMAL")  # OPTIMAL, FEASIBLE, INFEASIBLE, NO_FEASIBLE_PLAN
    infeasibility_reason = Column(String(250), nullable=True)
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

class OptimizationAssignment(Base):
    __tablename__ = "optimization_assignments"

    id = Column(Integer, primary_key=True, index=True)
    run_id = Column(String(50), ForeignKey("optimization_runs.run_id", ondelete="CASCADE"), nullable=False, index=True)
    action_id = Column(String(50), ForeignKey("intervention_candidates.action_id"), nullable=False, index=True)
    team_id = Column(String(30), ForeignKey("municipal_teams.team_id"), nullable=False, index=True)
    ward_id = Column(Integer, ForeignKey("wards.id", ondelete="CASCADE"), nullable=False, index=True)
    assigned_cost = Column(Float, nullable=False, default=0.0)
    assigned_duration = Column(Float, nullable=False, default=0.0)
    expected_benefit = Column(Float, nullable=False, default=0.0)
    selection_status = Column(String(20), nullable=False, default="SELECTED")  # SELECTED, UNSELECTED
    recommendation_reason = Column(Text, nullable=False)
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

    # Relationships
    ward = relationship("Ward")
