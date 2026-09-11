from datetime import datetime, timezone
from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Boolean, JSON
from sqlalchemy.orm import relationship

from app.db.base_class import Base

class SimulationScenario(Base):
    __tablename__ = "simulation_scenarios"

    id = Column(Integer, primary_key=True, index=True)
    scenario_id = Column(String(50), unique=True, nullable=False, index=True)  # e.g., SIM_EXTREME_RAIN, SIM_LIMITED_BUDGET
    name = Column(String(100), nullable=False)
    rainfall_multiplier = Column(Float, nullable=False, default=1.0)
    rainfall_24h_mm = Column(Float, nullable=False, default=140.0)
    rainfall_48h_mm = Column(Float, nullable=False, default=180.0)
    rainfall_72h_mm = Column(Float, nullable=False, default=220.0)
    available_teams = Column(Integer, nullable=False, default=3)
    available_hours = Column(Float, nullable=False, default=24.0)
    available_budget_inr = Column(Float, nullable=False, default=50000.0)
    is_preset = Column(Boolean, nullable=False, default=False)
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

class SimulationResult(Base):
    __tablename__ = "simulation_results"

    id = Column(Integer, primary_key=True, index=True)
    scenario_id = Column(String(50), ForeignKey("simulation_scenarios.scenario_id", ondelete="CASCADE"), nullable=False, index=True)
    high_risk_wards_count = Column(Integer, nullable=False, default=0)
    critical_priority_wards_count = Column(Integer, nullable=False, default=0)
    total_potential_exposure = Column(Integer, nullable=False, default=0)
    selected_actions_count = Column(Integer, nullable=False, default=0)
    used_budget_inr = Column(Float, nullable=False, default=0.0)
    used_teams_count = Column(Integer, nullable=False, default=0)
    baseline_vs_scenario_summary = Column(JSON, nullable=False)
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

    # Relationships
    scenario = relationship("SimulationScenario")
