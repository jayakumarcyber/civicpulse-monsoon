from typing import List, Optional
from sqlalchemy.orm import Session
from geoalchemy2.shape import to_shape
import shapely.geometry
import json

from app.models.ward import Ward

def get_wards(db: Session, skip: int = 0, limit: int = 100) -> List[Ward]:
    return db.query(Ward).offset(skip).limit(limit).all()

def get_ward_by_id(db: Session, ward_id: int) -> Optional[Ward]:
    return db.query(Ward).filter(Ward.id == ward_id).first()

def get_ward_by_code(db: Session, ward_code: str) -> Optional[Ward]:
    return db.query(Ward).filter(Ward.ward_code == ward_code).first()

def serialize_ward_geojson(ward: Ward) -> dict:
    geojson_dict = None
    if ward.geometry is not None:
        shape = to_shape(ward.geometry)
        geojson_dict = shapely.geometry.mapping(shape)
    return {
        "id": ward.id,
        "name": ward.name,
        "city": ward.city,
        "state": ward.state,
        "ward_code": ward.ward_code,
        "population": ward.population,
        "area_sq_km": ward.area_sq_km,
        "geometry": geojson_dict,
        "created_at": ward.created_at.isoformat() if ward.created_at else None,
        "updated_at": ward.updated_at.isoformat() if ward.updated_at else None,
    }
