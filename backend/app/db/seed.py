import sys
import os
from datetime import datetime, timezone, timedelta
from sqlalchemy.orm import Session
from geoalchemy2.elements import WKTElement

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

from app.db.session import engine, SessionLocal
from app.models.ward import Ward
from app.models.incident import CivicIncident
from app.models.rainfall import RainfallRecord
from app.models.road import Road
from app.models.drain import Drain
from app.models.waterbody import Waterbody
from app.models.population_zone import PopulationZone
from app.models.facility import CriticalFacility
from app.models.infrastructure import InfrastructureAsset
from app.models.inspection import Inspection
from app.models.repair import RepairRecord

def seed_demo_data():
    print("[INFO] Seeding DEMO / SYNTHETIC data for CivicPulse Monsoon...")
    db: Session = SessionLocal()

    try:
        # Check if seed data already exists
        if db.query(Ward).count() > 0:
            print("[INFO] Database already contains records. Skipping seed.")
            return

        # 1. Create Sample Wards (Mumbai DEMO / SYNTHETIC)
        ward_g_north = Ward(
            name="Ward G/North (Dadar - DEMO)",
            city="Mumbai",
            state="Maharashtra",
            ward_code="MUM-GN-DEMO",
            population=450000,
            area_sq_km=9.07,
            geometry=WKTElement("MULTIPOLYGON(((72.830 19.010, 72.850 19.010, 72.850 19.030, 72.830 19.030, 72.830 19.010)))", srid=4326)
        )
        ward_l_west = Ward(
            name="Ward L/West (Kurla - DEMO)",
            city="Mumbai",
            state="Maharashtra",
            ward_code="MUM-L-DEMO",
            population=900000,
            area_sq_km=15.88,
            geometry=WKTElement("MULTIPOLYGON(((72.870 19.060, 72.890 19.060, 72.890 19.080, 72.870 19.080, 72.870 19.060)))", srid=4326)
        )

        db.add_all([ward_g_north, ward_l_west])
        db.commit()
        db.refresh(ward_g_north)
        db.refresh(ward_l_west)

        # 2. Create Sample Roads
        road1 = Road(
            name="Senapati Bapat Marg (DEMO / SYNTHETIC)",
            road_type="arterial",
            importance="critical",
            geometry=WKTElement("LINESTRING(72.832 19.012, 72.842 19.025)", srid=4326),
            ward_id=ward_g_north.id
        )
        road2 = Road(
            name="LBS Marg (DEMO / SYNTHETIC)",
            road_type="highway",
            importance="critical",
            geometry=WKTElement("LINESTRING(72.872 19.062, 72.885 19.075)", srid=4326),
            ward_id=ward_l_west.id
        )
        db.add_all([road1, road2])

        # 3. Create Sample Drains
        drain1 = Drain(
            name="Dadar Main Nallah (DEMO / SYNTHETIC)",
            drain_type="primary_nallah",
            capacity=45.5,
            status="partially_blocked",
            geometry=WKTElement("LINESTRING(72.835 19.015, 72.845 19.028)", srid=4326),
            ward_id=ward_g_north.id
        )
        drain2 = Drain(
            name="Mithi River Tributary Drain (DEMO / SYNTHETIC)",
            drain_type="primary_nallah",
            capacity=85.0,
            status="blocked",
            geometry=WKTElement("LINESTRING(72.875 19.065, 72.888 19.078)", srid=4326),
            ward_id=ward_l_west.id
        )
        db.add_all([drain1, drain2])

        # 4. Create Sample Waterbodies
        wb1 = Waterbody(
            name="Mahim Bay (Outfall DEMO / SYNTHETIC)",
            type="sea_outfall",
            geometry=WKTElement("POLYGON((72.830 19.020, 72.838 19.020, 72.838 19.028, 72.830 19.028, 72.830 19.020))", srid=4326),
            ward_id=ward_g_north.id
        )
        wb2 = Waterbody(
            name="Mithi River Basin (DEMO / SYNTHETIC)",
            type="river",
            geometry=WKTElement("POLYGON((72.870 19.065, 72.880 19.065, 72.880 19.075, 72.870 19.075, 72.870 19.065))", srid=4326),
            ward_id=ward_l_west.id
        )
        db.add_all([wb1, wb2])

        # 5. Create Sample Population Zones
        pz1 = PopulationZone(
            zone_name="Dadar West Commercial Zone (DEMO / SYNTHETIC)",
            population=120000,
            density=25000.0,
            geometry=WKTElement("POLYGON((72.832 19.015, 72.842 19.015, 72.842 19.025, 72.832 19.025, 72.832 19.015))", srid=4326),
            ward_id=ward_g_north.id
        )
        pz2 = PopulationZone(
            zone_name="Kurla Station East Settlement (DEMO / SYNTHETIC)",
            population=250000,
            density=45000.0,
            geometry=WKTElement("POLYGON((72.875 19.065, 72.885 19.065, 72.885 19.075, 72.875 19.075, 72.875 19.065))", srid=4326),
            ward_id=ward_l_west.id
        )
        db.add_all([pz1, pz2])

        # 6. Create Sample Critical Facilities
        fac1 = CriticalFacility(
            name="KEM Hospital (DEMO / SYNTHETIC)",
            facility_type="hospital",
            latitude=19.002,
            longitude=72.841,
            location=WKTElement("POINT(72.841 19.002)", srid=4326),
            capacity=1800,
            ward_id=ward_g_north.id
        )
        fac2 = CriticalFacility(
            name="Kurla Railway Junction (DEMO / SYNTHETIC)",
            facility_type="transport",
            latitude=19.065,
            longitude=72.879,
            location=WKTElement("POINT(72.879 19.065)", srid=4326),
            capacity=50000,
            ward_id=ward_l_west.id
        )
        fac3 = CriticalFacility(
            name="Don Bosco High School (DEMO / SYNTHETIC)",
            facility_type="school",
            latitude=19.022,
            longitude=72.855,
            location=WKTElement("POINT(72.855 19.022)", srid=4326),
            capacity=3000,
            ward_id=ward_g_north.id
        )
        db.add_all([fac1, fac2, fac3])

        # 7. Create Sample Infrastructure Assets, Inspections & Repairs
        asset1 = InfrastructureAsset(
            name="Irla Pumping Station (DEMO / SYNTHETIC)",
            asset_type="pumping_station",
            age_years=12,
            condition="fair",
            owner_department="Storm Water Drains Dept",
            geometry=WKTElement("POINT(72.835 19.018)", srid=4326),
            ward_id=ward_g_north.id
        )
        db.add(asset1)
        db.commit()
        db.refresh(asset1)

        insp1 = Inspection(
            asset_id=asset1.id,
            inspection_date=datetime.now(timezone.utc) - timedelta(days=7),
            inspection_type="pre_monsoon",
            findings="Pump 2 showing impeller wear, desilting needed near intake bay. [DEMO / SYNTHETIC LOG]",
            condition_score=6.5,
            inspector="Junior Engineer A. Sharma (DEMO)",
            latitude=19.018,
            longitude=72.835
        )
        repair1 = RepairRecord(
            asset_id=asset1.id,
            repair_date=datetime.now(timezone.utc) - timedelta(days=3),
            repair_type="desilting",
            description="Cleared 150 metric tons of sludge from pump intake bay. [DEMO / SYNTHETIC LOG]",
            cost=250000.0,
            status="completed",
            completed_by="Municipal Contractor Alpha (DEMO)"
        )
        db.add_all([insp1, repair1])

        # 8. Create Sample Incidents
        inc1 = CivicIncident(
            incident_type="waterlogging",
            description="Severe 1.5 ft waterlogging near Dadar TT Circle underpass. [DEMO / SYNTHETIC REPORT]",
            latitude=19.018,
            longitude=72.842,
            location=WKTElement("POINT(72.842 19.018)", srid=4326),
            reported_at=datetime.now(timezone.utc) - timedelta(hours=4),
            severity="high",
            source="citizen",
            status="investigating",
            ward_id=ward_g_north.id,
            evidence_quality=0.9
        )
        inc2 = CivicIncident(
            incident_type="blocked_drain",
            description="Plastic trash choking secondary drain near LBS Marg junction. [DEMO / SYNTHETIC REPORT]",
            latitude=19.068,
            longitude=72.877,
            location=WKTElement("POINT(72.877 19.068)", srid=4326),
            reported_at=datetime.now(timezone.utc) - timedelta(hours=2),
            severity="critical",
            source="municipal_worker",
            status="reported",
            ward_id=ward_l_west.id,
            evidence_quality=1.0
        )
        db.add_all([inc1, inc2])

        # 9. Create Sample Rainfall Records (Observed & Forecast)
        rain_obs = RainfallRecord(
            location=WKTElement("POINT(72.840 19.020)", srid=4326),
            recorded_at=datetime.now(timezone.utc) - timedelta(hours=1),
            rainfall_mm=68.5,
            forecast_hours=0,
            source="sensor",
            is_forecast=False,
            ward_id=ward_g_north.id
        )
        rain_f24 = RainfallRecord(
            location=WKTElement("POINT(72.840 19.020)", srid=4326),
            recorded_at=datetime.now(timezone.utc) + timedelta(hours=24),
            rainfall_mm=120.0,
            forecast_hours=24,
            source="imd_forecast",
            is_forecast=True,
            ward_id=ward_g_north.id
        )
        rain_f48 = RainfallRecord(
            location=WKTElement("POINT(72.840 19.020)", srid=4326),
            recorded_at=datetime.now(timezone.utc) + timedelta(hours=48),
            rainfall_mm=165.0,
            forecast_hours=48,
            source="imd_forecast",
            is_forecast=True,
            ward_id=ward_g_north.id
        )
        rain_f72 = RainfallRecord(
            location=WKTElement("POINT(72.840 19.020)", srid=4326),
            recorded_at=datetime.now(timezone.utc) + timedelta(hours=72),
            rainfall_mm=85.0,
            forecast_hours=72,
            source="imd_forecast",
            is_forecast=True,
            ward_id=ward_g_north.id
        )
        db.add_all([rain_obs, rain_f24, rain_f48, rain_f72])

        db.commit()
        print("[SUCCESS] DEMO / SYNTHETIC data successfully seeded into database!")

    except Exception as e:
        db.rollback()
        print(f"[ERROR] Failed to seed database: {e}")
        raise e
    finally:
        db.close()

if __name__ == "__main__":
    seed_demo_data()
