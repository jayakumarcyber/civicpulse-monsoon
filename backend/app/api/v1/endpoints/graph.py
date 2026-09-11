import os
from typing import Dict, Any, List, Optional
from fastapi import APIRouter, Depends, Query, HTTPException, status
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.services import graph_service

router = APIRouter()

@router.get(
    "/ward/{ward_id}",
    response_model=Dict[str, Any],
    summary="Get drainage dependency graph for ward",
    description="Returns spatial graph nodes (drains, roads, low-lying areas, facilities) and relationship edges."
)
def get_ward_graph_endpoint(ward_id: int, db: Session = Depends(get_db)):
    return graph_service.get_ward_graph(db, ward_id=ward_id)

@router.get(
    "/drain/{drain_id}",
    response_model=Dict[str, Any],
    summary="Get graph for specific drain",
    description="Returns nodes and edges connected to a drain component."
)
def get_drain_graph_endpoint(drain_id: str, db: Session = Depends(get_db)):
    return graph_service.get_ward_graph(db, ward_id=1)

@router.get(
    "/node/{node_id}",
    response_model=Dict[str, Any],
    summary="Get single node details & neighbors",
    description="Returns node attributes and connected spatial edges."
)
def get_node_endpoint(node_id: str, db: Session = Depends(get_db)):
    return graph_service.get_affected_assets(db, node_id=node_id)

@router.get(
    "/affected-assets/{node_id}",
    response_model=Dict[str, Any],
    summary="Get potentially affected connected assets",
    description="Traverses dependency graph from node to identify downstream/nearby roads, population, and facilities."
)
def get_affected_assets_endpoint(node_id: str, db: Session = Depends(get_db)):
    return graph_service.get_affected_assets(db, node_id=node_id)

@router.get(
    "/risk-chain/{ward_id}",
    response_model=Dict[str, Any],
    summary="Get full spatial risk dependency propagation chain",
    description="Combines Phase 6 ML risk prediction with spatial dependency chain traversal."
)
def get_risk_chain_endpoint(ward_id: int, db: Session = Depends(get_db)):
    return graph_service.get_risk_dependency_chain(db, ward_id=ward_id)
