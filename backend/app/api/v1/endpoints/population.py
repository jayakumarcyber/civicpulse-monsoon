from typing import Dict, List, Any
from fastapi import APIRouter, Depends, HTTPException, status
from app.services.population_service import PopulationService

router = APIRouter()

@router.get(
    "/nilgiris/hierarchy",
    response_model=Dict[str, List[Dict[str, Any]]],
    summary="Get The Nilgiris CD Block & Village Population Hierarchy",
    description="Returns list of CD Blocks mapping to their constituent villages and towns with Census 2011 population."
)
def get_nilgiris_population_hierarchy():
    try:
        return PopulationService.get_nilgiris_hierarchy()
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Could not load Census population dataset: {str(e)}"
        )

@router.get(
    "/theni/hierarchy",
    response_model=Dict[str, List[Dict[str, Any]]],
    summary="Get Theni CD Block & Village Population Hierarchy",
    description="Returns list of CD Blocks mapping to their constituent villages with Census 2011 population from data1."
)
def get_theni_population_hierarchy():
    try:
        return PopulationService.get_theni_hierarchy()
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Could not load Theni Census population dataset: {str(e)}"
        )
