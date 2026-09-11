from datetime import datetime, timezone
from typing import Any, Dict
from fastapi import APIRouter, Depends, status
from sqlalchemy import text
from sqlalchemy.orm import Session

from app.core.config import settings
from app.db.session import get_db

router = APIRouter()

@router.get(
    "/health",
    status_code=status.HTTP_200_OK,
    response_model=Dict[str, Any],
    summary="Health check endpoint",
    description="Returns backend service operational status, timestamp, and PostGIS database connection check."
)
def check_health(db: Session = Depends(get_db)) -> Dict[str, Any]:
    db_status = "unreachable"
    postgis_version = None

    try:
        result = db.execute(text("SELECT PostGIS_Full_Version();")).scalar()
        if result:
            db_status = "connected"
            postgis_version = str(result).split('"')[1] if '"' in str(result) else str(result)[:60]
    except Exception:
        try:
            # Fallback check if postgis extension is not enabled on db yet
            db.execute(text("SELECT 1;"))
            db_status = "connected (postgresql)"
        except Exception as e:
            db_status = f"error: {str(e)}"

    return {
        "status": "online",
        "service": settings.PROJECT_NAME,
        "version": settings.VERSION,
        "environment": settings.ENVIRONMENT,
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "database": {
            "status": db_status,
            "postgis_info": postgis_version
        }
    }
