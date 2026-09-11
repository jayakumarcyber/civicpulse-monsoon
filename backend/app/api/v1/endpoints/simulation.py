from typing import Dict, Any, List, Optional
from fastapi import APIRouter, Depends, Query, Body
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.services import simulation_service

router = APIRouter()

class SimulationRequest(BaseModel):
    rainfall_multiplier: float = Field(1.0, ge=0.0, le=5.0, description="Rainfall scenario intensity multiplier (e.g. 0.5x, 1.5x, 2.0x)")
    available_budget: float = Field(50000.0, ge=0.0, description="Available municipal budget in INR")
    available_hours: float = Field(24.0, ge=0.0, description="Available crew working hours")
    available_teams: int = Field(3, ge=0, le=10, description="Number of available maintenance teams")

@router.post(
    "/run",
    response_model=Dict[str, Any],
    summary="Run interactive What-If scenario simulation",
    description="Recalculates ML risk, civic priority, and OR-Tools optimization under scenario parameters and returns baseline comparison."
)
def run_simulation_endpoint(
    request: SimulationRequest = Body(...),
    db: Session = Depends(get_db)
):
    return simulation_service.run_what_if_simulation(
        rainfall_multiplier=request.rainfall_multiplier,
        available_budget=request.available_budget,
        available_hours=request.available_hours,
        available_teams=request.available_teams,
        db=db
    )

@router.get(
    "/scenarios",
    response_model=List[Dict[str, Any]],
    summary="Get preset simulation scenarios",
    description="Returns predefined scenario triggers (Normal Rain, Heavy Rain, Extreme Rain, Limited Workforce, Limited Budget, Combined Worst Case)."
)
def get_scenarios_endpoint():
    return simulation_service.get_preset_scenarios()

@router.get(
    "/{scenario_id}",
    response_model=Dict[str, Any],
    summary="Get simulation results by scenario ID",
    description="Returns simulation output and baseline comparison for a specific scenario."
)
def get_scenario_by_id_endpoint(scenario_id: str, db: Session = Depends(get_db)):
    # Find matching preset or run default
    presets = simulation_service.get_preset_scenarios()
    for p in presets:
        if p["preset_id"] == scenario_id:
            return simulation_service.run_what_if_simulation(
                rainfall_multiplier=p["rainfall_multiplier"],
                available_budget=p["available_budget_inr"],
                available_hours=p["available_hours"],
                available_teams=p["available_teams"],
                db=db
            )
    return simulation_service.run_what_if_simulation(db=db)

@router.post(
    "/reset",
    response_model=Dict[str, Any],
    summary="Reset simulator to original baseline state",
    description="Restores baseline state without modifying any database records."
)
def reset_simulation_endpoint():
    return {
        "status": "RESET_SUCCESS",
        "simulation_mode": "INACTIVE",
        "baseline": simulation_service.BASELINE_STATE,
        "message": "Simulator state restored to original baseline observations."
    }
