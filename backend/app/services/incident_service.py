from typing import List, Optional
from sqlalchemy.orm import Session
from app.models.incident import CivicIncident

def get_incidents(
    db: Session,
    skip: int = 0,
    limit: int = 100,
    ward_id: Optional[int] = None,
    incident_type: Optional[str] = None,
    status: Optional[str] = None,
    severity: Optional[str] = None
) -> List[CivicIncident]:
    query = db.query(CivicIncident)
    if ward_id is not None:
        query = query.filter(CivicIncident.ward_id == ward_id)
    if incident_type is not None:
        query = query.filter(CivicIncident.incident_type == incident_type)
    if status is not None:
        query = query.filter(CivicIncident.status == status)
    if severity is not None:
        query = query.filter(CivicIncident.severity == severity)
    return query.order_by(CivicIncident.reported_at.desc()).offset(skip).limit(limit).all()

def get_incident_by_id(db: Session, incident_id: int) -> Optional[CivicIncident]:
    return db.query(CivicIncident).filter(CivicIncident.id == incident_id).first()
