import sys
import os
from datetime import datetime, timezone, timedelta

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

from app.db.session import engine, SessionLocal
from app.models.ward import Ward
from app.models.incident import CivicIncident
from app.models.rainfall import RainfallRecord
from app.models.prediction import RiskPrediction

def seed_fallback_database():
    print("[INFO] Creating database tables for fallback SQLite DB...")
    
    # Create tables individually to avoid Spatialite DDL triggers
    for model in [Ward, CivicIncident, RainfallRecord, RiskPrediction]:
        try:
            model.__table__.create(bind=engine, checkfirst=True)
        except Exception as e:
            print(f"[WARN] Table creation notice for {model.__tablename__}: {e}")

    db = SessionLocal()

    try:
        if db.query(Ward).count() == 0:
            print("[INFO] Seeding benchmark Wards for Tamil Nadu and Demo districts...")
            w1 = Ward(id=1, name="Ward G/North (Dadar)", city="Mumbai", district="Mumbai", state="Maharashtra", ward_code="MUM-GN", administrative_type="Urban", local_body="Brihanmumbai Municipal Corporation", ward_number=1, population=450000, area_sq_km=9.07, data_source="Municipal Demo", data_status="Sample Public Data")
            w2 = Ward(id=2, name="Ward F/North (Matunga)", city="Mumbai", district="Mumbai", state="Maharashtra", ward_code="MUM-FN", administrative_type="Urban", local_body="Brihanmumbai Municipal Corporation", ward_number=2, population=520000, area_sq_km=10.5, data_source="Municipal Demo", data_status="Sample Public Data")
            w3 = Ward(id=3, name="Ward H/East (Bandra East)", city="Mumbai", district="Mumbai", state="Maharashtra", ward_code="MUM-HE", administrative_type="Urban", local_body="Brihanmumbai Municipal Corporation", ward_number=3, population=610000, area_sq_km=12.3, data_source="Municipal Demo", data_status="Sample Public Data")
            w4 = Ward(id=4, name="Ward K/East (Andheri East)", city="Mumbai", district="Mumbai", state="Maharashtra", ward_code="MUM-KE", administrative_type="Urban", local_body="Brihanmumbai Municipal Corporation", ward_number=4, population=820000, area_sq_km=16.4, data_source="Municipal Demo", data_status="Sample Public Data")
            w5 = Ward(id=5, name="Ward 109 (T. Nagar)", city="Chennai", district="Chennai", state="Tamil Nadu", ward_code="CHE-109", administrative_type="Urban", local_body="Greater Chennai Corporation", ward_number=109, locality="T. Nagar", population=380000, area_sq_km=8.2, data_source="Tamil Nadu ULB Portal", data_status="Official Data")
            w6 = Ward(id=6, name="Ward 102 (Anna Nagar)", city="Chennai", district="Chennai", state="Tamil Nadu", ward_code="CHE-102", administrative_type="Urban", local_body="Greater Chennai Corporation", ward_number=102, locality="Anna Nagar", population=410000, area_sq_km=11.0, data_source="Tamil Nadu ULB Portal", data_status="Official Data")
            w7 = Ward(id=7, name="Ward 177 (Velachery)", city="Chennai", district="Chennai", state="Tamil Nadu", ward_code="CHE-177", administrative_type="Urban", local_body="Greater Chennai Corporation", ward_number=177, locality="Velachery", population=490000, area_sq_km=14.1, data_source="Tamil Nadu ULB Portal", data_status="Official Data")
            w8 = Ward(id=8, name="Ward 62 (Gandhipuram)", city="Coimbatore", district="Coimbatore", state="Tamil Nadu", ward_code="CBE-062", administrative_type="Urban", local_body="Coimbatore City Municipal Corporation", ward_number=62, locality="Gandhipuram", population=290000, area_sq_km=7.5, data_source="Tamil Nadu ULB Portal", data_status="Official Data")
            w9 = Ward(id=9, name="Ward 24 (Hasthampatti)", city="Salem", district="Salem", state="Tamil Nadu", ward_code="SLM-024", administrative_type="Urban", local_body="Salem City Municipal Corporation", ward_number=24, locality="Hasthampatti", population=210000, area_sq_km=6.8, data_source="Tamil Nadu ULB Portal", data_status="Official Data")
            w10 = Ward(id=10, name="Ward 45 (Goripalayam)", city="Madurai", district="Madurai", state="Tamil Nadu", ward_code="MDU-045", administrative_type="Urban", local_body="Madurai City Municipal Corporation", ward_number=45, locality="Goripalayam", population=260000, area_sq_km=7.2, data_source="Tamil Nadu ULB Portal", data_status="Official Data")
            w11 = Ward(id=11, name="Kallakurichi Town Ward 1", city="Kallakurichi", district="Kallakurichi", state="Tamil Nadu", ward_code="KLK-001", administrative_type="Urban", local_body="Kallakurichi Municipality", ward_number=1, locality="Kallakurichi Town", population=45000, area_sq_km=4.5, data_source="Tamil Nadu Municipal Admin", data_status="Official Data")
            w12 = Ward(id=12, name="Ariyalur Town Ward 1", city="Ariyalur", district="Ariyalur", state="Tamil Nadu", ward_code="ARI-001", administrative_type="Urban", local_body="Ariyalur Municipality", ward_number=1, locality="Ariyalur Town", population=38000, area_sq_km=3.8, data_source="Tamil Nadu Municipal Admin", data_status="Official Data")

            db.add_all([w1, w2, w3, w4, w5, w6, w7, w8, w9, w10, w11, w12])
            db.commit()

        if db.query(CivicIncident).count() == 0:
            print("[INFO] Seeding benchmark Civic Incidents...")
            now = datetime.now(timezone.utc)
            inc1 = CivicIncident(incident_type="waterlogging", severity="critical", status="reported", ward_id=1, latitude=19.018, longitude=72.842, reported_at=now - timedelta(hours=4), description="Severe waterlogging near Dadar TT circle", data_source_type="SYNTHETIC_DEMO_DATA")
            inc2 = CivicIncident(incident_type="blocked_drain", severity="high", status="in_progress", ward_id=2, latitude=19.028, longitude=72.855, reported_at=now - timedelta(hours=12), description="Major drain choked with plastic debris", data_source_type="SYNTHETIC_DEMO_DATA")
            inc3 = CivicIncident(incident_type="waterlogging", severity="high", status="reported", ward_id=3, latitude=19.060, longitude=72.850, reported_at=now - timedelta(days=1), description="Kalanagar junction waterlogged", data_source_type="SYNTHETIC_DEMO_DATA")
            inc4 = CivicIncident(incident_type="waterlogging", severity="critical", status="reported", ward_id=5, latitude=13.0418, longitude=80.2341, reported_at=now - timedelta(hours=2), description="Usman Road underpass submerged in 3ft water", data_source_type="SYNTHETIC_DEMO_DATA")
            inc5 = CivicIncident(incident_type="waterlogging", severity="high", status="reported", ward_id=7, latitude=12.9815, longitude=80.2180, reported_at=now - timedelta(hours=5), description="Velachery main road inundated near lake outlet", data_source_type="SYNTHETIC_DEMO_DATA")
            inc6 = CivicIncident(incident_type="blocked_drain", severity="medium", status="reported", ward_id=8, latitude=11.0168, longitude=76.9558, reported_at=now - timedelta(hours=8), description="Cross Cut road storm drain blockage", data_source_type="SYNTHETIC_DEMO_DATA")
            inc7 = CivicIncident(incident_type="waterlogging", severity="high", status="reported", ward_id=11, latitude=11.7380, longitude=78.9620, reported_at=now - timedelta(hours=3), description="Kallakurichi Bus Stand water accumulation", data_source_type="SYNTHETIC_DEMO_DATA")
            db.add_all([inc1, inc2, inc3, inc4, inc5, inc6, inc7])
            db.commit()

        if db.query(RainfallRecord).count() == 0:
            print("[INFO] Seeding benchmark Rainfall Records...")
            now = datetime.now(timezone.utc)
            r1 = RainfallRecord(ward_id=1, rainfall_mm=45.5, recorded_at=now - timedelta(hours=1), is_forecast=False, data_source_type="SYNTHETIC_DEMO_DATA")
            r2 = RainfallRecord(ward_id=1, rainfall_mm=140.0, recorded_at=now - timedelta(hours=24), is_forecast=False, data_source_type="SYNTHETIC_DEMO_DATA")
            r3 = RainfallRecord(ward_id=5, rainfall_mm=165.0, recorded_at=now - timedelta(hours=24), is_forecast=False, data_source_type="SYNTHETIC_DEMO_DATA")
            r4 = RainfallRecord(ward_id=7, rainfall_mm=180.0, recorded_at=now - timedelta(hours=24), is_forecast=False, data_source_type="SYNTHETIC_DEMO_DATA")
            db.add_all([r1, r2, r3, r4])
            db.commit()

        if db.query(RiskPrediction).count() == 0:
            print("[INFO] Seeding benchmark ML Risk Predictions...")
            now = datetime.now(timezone.utc)
            p1 = RiskPrediction(ward_id=1, prediction_timestamp=now, horizon_hours=24, predicted_probability=0.825, risk_level="HIGH", model_version="XGBoost_24h_v1_DEMO")
            p2 = RiskPrediction(ward_id=5, prediction_timestamp=now, horizon_hours=24, predicted_probability=0.910, risk_level="HIGH", model_version="XGBoost_24h_v1_DEMO")
            p3 = RiskPrediction(ward_id=7, prediction_timestamp=now, horizon_hours=24, predicted_probability=0.880, risk_level="HIGH", model_version="XGBoost_24h_v1_DEMO")
            p4 = RiskPrediction(ward_id=2, prediction_timestamp=now, horizon_hours=24, predicted_probability=0.620, risk_level="MEDIUM", model_version="XGBoost_24h_v1_DEMO")
            p5 = RiskPrediction(ward_id=8, prediction_timestamp=now, horizon_hours=24, predicted_probability=0.350, risk_level="LOW", model_version="XGBoost_24h_v1_DEMO")
            p6 = RiskPrediction(ward_id=11, prediction_timestamp=now, horizon_hours=24, predicted_probability=0.850, risk_level="HIGH", model_version="XGBoost_24h_v1_DEMO")
            db.add_all([p1, p2, p3, p4, p5, p6])
            db.commit()

        print("[SUCCESS] Benchmark fallback database initialized.")
    except Exception as e:
        print(f"[ERROR] Database seeding error: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    seed_fallback_database()
