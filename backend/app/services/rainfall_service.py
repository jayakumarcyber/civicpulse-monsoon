import os
from typing import List, Optional, Dict, Any
import pandas as pd
from sqlalchemy.orm import Session
from app.models.rainfall import RainfallRecord, HistoricalRainfallRecord

# Raw CSV file paths
DATA_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "data", "raw", "rainfall"))

CSV1_NAME = "rainfall_occurred_during_north-east_monsoon_by_districts_in_tamil_nadu_2017_18.csv"
CSV2_NAME = "time_series_data_rainfall_by_seasons_in_tamil_nadu_2020.csv"
CSV3_NAME = "Sub_Division_IMD_2017.csv"

DISTRICT_NAME_MAP = {
    "kancheepuram": "Kanchipuram",
    "the nilgiris": "Nilgiris",
    "kanniyakumari": "Kanyakumari",
    "tiruchirappalli": "Tiruchirappalli",
    "thiruchirappalli": "Tiruchirappalli",
    "trichy": "Tiruchirappalli",
}

def load_and_clean_historical_rainfall() -> List[Dict[str, Any]]:
    """Clean & normalize records from all 3 uploaded CSV datasets."""
    records = []

    # 1. Dataset 1: NE Monsoon by Districts TN (2017-18)
    p1 = os.path.join(DATA_DIR, CSV1_NAME)
    if os.path.exists(p1):
        df1 = pd.read_csv(p1)
        for _, row in df1.iterrows():
            dist_raw = str(row.get("District", "")).strip()
            if not dist_raw or dist_raw.lower() == "state average":
                continue
            
            dist_clean = DISTRICT_NAME_MAP.get(dist_raw.lower(), dist_raw)
            
            # Monthly rows for Oct 17, Nov 17, Dec 17, Total
            months = [
                ("October'17", "Actual Rainfall occurred in October'17 during North-East Monsoon (in mm)", "Normal Rainfall occurred in October'17 during North-East Monsoon (in mm)", "Percentage Deviation from Actual to Normal during North-East Monsoon in October'17"),
                ("November'17", "Actual Rainfall occurred in November'17 during North-East Monsoon (in mm)", "Normal Rainfall occurred in November'17 during North-East Monsoon (in mm)", "Percentage Deviation from Actual to Normal during North-East Monsoon in November'17"),
                ("December'17", "Actual Rainfall occurred in December'17 during North-East Monsoon (in mm)", "Normal Rainfall occurred in December'17 during North-East Monsoon (in mm)", "Percentage Deviation from Actual to Normal during North-East Monsoon in December'17"),
                ("Total North-East Monsoon 2017-18", "Total Actual Rainfall occurred during North-East Monsoon (in mm)", "Total Normal Rainfall occurred during North-East Monsoon (in mm)", "Percentage Deviation from Total Actual to Total Normal Rainfall during North-East Monsoon")
            ]

            for period, act_col, norm_col, dev_col in months:
                if act_col in row and pd.notna(row[act_col]):
                    try:
                        records.append({
                            "source_file": CSV1_NAME,
                            "year": "2017-18",
                            "period_or_season": period,
                            "state": "Tamil Nadu",
                            "district_or_subdivision": dist_clean,
                            "actual_rainfall_mm": float(row[act_col]),
                            "normal_rainfall_mm": float(row[norm_col]) if norm_col in row and pd.notna(row[norm_col]) else None,
                            "percentage_deviation": float(row[dev_col]) if dev_col in row and pd.notna(row[dev_col]) else None,
                            "rainfall_type": "MONTHLY_DISTRICT_NE_MONSOON",
                            "data_source_type": "Historical Government/Public Dataset"
                        })
                    except (ValueError, TypeError):
                        pass

    # 2. Dataset 2: Seasonal Time Series TN (2005-2019)
    p2 = os.path.join(DATA_DIR, CSV2_NAME)
    if os.path.exists(p2):
        df2 = pd.read_csv(p2)
        for _, row in df2.iterrows():
            year_val = str(row.get("Year", "")).strip()
            if not year_val:
                continue
            
            seasons = [
                ("South West Monsoon", "Actual Rainfall in South West Monsoon (in mm)", "Normal Rainfall in South West Monsoon (in mm)"),
                ("North East Monsoon", "Actual Rainfall in North East Monsoon (in mm)", "Normal Rainfall in North East Monsoon (in mm)"),
                ("Winter Season", "Actual Rainfall in Winter Season (in mm)", "Normal Rainfall in Winter Season (in mm)"),
                ("Hot Weather Season", "Actual Rainfall in Hot Weather Season (in mm)", "Normal Rainfall in Hot Weather Season (in mm)"),
                ("Annual Total", "Total Actual Rainfall (in mm)", "Total Normal Rainfall (in mm)")
            ]

            for season, act_col, norm_col in seasons:
                if act_col in row and pd.notna(row[act_col]):
                    try:
                        records.append({
                            "source_file": CSV2_NAME,
                            "year": year_val,
                            "period_or_season": season,
                            "state": "Tamil Nadu",
                            "district_or_subdivision": "Tamil Nadu State",
                            "actual_rainfall_mm": float(row[act_col]),
                            "normal_rainfall_mm": float(row[norm_col]) if norm_col in row and pd.notna(row[norm_col]) else None,
                            "percentage_deviation": float(row["Percentage Deviation from Normal"]) if "Percentage Deviation from Normal" in row and pd.notna(row["Percentage Deviation from Normal"]) else None,
                            "rainfall_type": "SEASONAL_TIME_SERIES_STATE",
                            "data_source_type": "Historical Government/Public Dataset"
                        })
                    except (ValueError, TypeError):
                        pass

    # 3. Dataset 3: Sub Division IMD 2017
    p3 = os.path.join(DATA_DIR, CSV3_NAME)
    if os.path.exists(p3):
        df3 = pd.read_csv(p3)
        month_cols = ["JAN", "FEB", "MAR", "APR", "MAY", "JUN", "JUL", "AUG", "SEP", "OCT", "NOV", "DEC", "ANNUAL"]
        for _, row in df3.iterrows():
            sub = str(row.get("SUBDIVISION", "")).strip()
            yr = str(row.get("YEAR", "")).strip()
            if not sub or not yr:
                continue

            for m in month_cols:
                if m in row and pd.notna(row[m]):
                    try:
                        records.append({
                            "source_file": CSV3_NAME,
                            "year": yr,
                            "period_or_season": m,
                            "state": "Tamil Nadu" if sub == "Tamil Nadu" else "India",
                            "district_or_subdivision": sub,
                            "actual_rainfall_mm": float(row[m]),
                            "normal_rainfall_mm": None,
                            "percentage_deviation": None,
                            "rainfall_type": "SUBDIVISIONAL_MONTHLY_IMD",
                            "data_source_type": "Historical Government/Public Dataset"
                        })
                    except (ValueError, TypeError):
                        pass

    return records

def get_rainfall_records(
    db: Session,
    skip: int = 0,
    limit: int = 100,
    ward_id: Optional[int] = None,
    is_forecast: Optional[bool] = None,
    forecast_hours: Optional[int] = None
) -> List[RainfallRecord]:
    query = db.query(RainfallRecord)
    if ward_id is not None:
        query = query.filter(RainfallRecord.ward_id == ward_id)
    if is_forecast is not None:
        query = query.filter(RainfallRecord.is_forecast == is_forecast)
    if forecast_hours is not None:
        query = query.filter(RainfallRecord.forecast_hours == forecast_hours)
    return query.order_by(RainfallRecord.recorded_at.desc()).offset(skip).limit(limit).all()

def get_historical_rainfall_by_district(
    db: Session,
    district_name: str
) -> Dict[str, Any]:
    """Retrieve cleaned historical rainfall for a specific district (e.g. Chennai, Coimbatore, Salem, Madurai)."""
    norm_district = DISTRICT_NAME_MAP.get(district_name.lower(), district_name)

    # Ingest from CSV records
    all_records = load_and_clean_historical_rainfall()
    
    # Filter matching district or state level
    matching = [
        r for r in all_records
        if r["district_or_subdivision"].lower() == norm_district.lower()
        or (norm_district.lower() in ["tamil nadu", "tn"] and "tamil nadu" in r["district_or_subdivision"].lower())
    ]

    if not matching:
        # Fallback to state average or general records if specific district not found
        matching = [r for r in all_records if r["district_or_subdivision"] in ["Tamil Nadu", "Tamil Nadu State"]]

    if not matching:
        return {
            "district_or_subdivision": district_name,
            "total_records": 0,
            "available_years": [],
            "sources_used": [],
            "min_rainfall_mm": 0.0,
            "max_rainfall_mm": 0.0,
            "avg_rainfall_mm": 0.0,
            "historical_records": []
        }

    rain_vals = [r["actual_rainfall_mm"] for r in matching]
    years = sorted(list(set(r["year"] for r in matching)))
    sources = sorted(list(set(r["source_file"] for r in matching)))

    return {
        "district_or_subdivision": norm_district,
        "total_records": len(matching),
        "available_years": years,
        "sources_used": sources,
        "min_rainfall_mm": round(min(rain_vals), 2),
        "max_rainfall_mm": round(max(rain_vals), 2),
        "avg_rainfall_mm": round(sum(rain_vals) / len(rain_vals), 2),
        "historical_records": matching[:20]
    }

def get_historical_rainfall_summary(db: Session) -> Dict[str, Any]:
    """Summary statistics for all uploaded historical datasets."""
    all_records = load_and_clean_historical_rainfall()
    districts = sorted(list(set(r["district_or_subdivision"] for r in all_records)))
    years = sorted(list(set(r["year"] for r in all_records)))
    sources = sorted(list(set(r["source_file"] for r in all_records)))

    return {
        "total_datasets": 3,
        "total_records": len(all_records),
        "data_source_label": "Historical Government/Public Dataset",
        "districts_covered": districts,
        "years_covered": years,
        "source_files": sources,
    }
