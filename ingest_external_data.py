"""
ingest_external_data.py
------------------------
Ingests the open-source / real-world Coimbatore datasets found in `dataset/`
into the SQLite database as three new tables:

  * climate_normals      <- climatological_table_1981_2010.csv   (IMD monthly normals)
  * extreme_weather      <- extreme_weather_events_april.csv     (IMD April extremes)
  * monthly_air_quality  <- D04-Environment_25(Sheet1).csv       (CPCB/data.gov.in monthly AQI)

Usage:
    python scripts/ingest_external_data.py
"""

import os
import sys
import sqlite3

import pandas as pd

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATASET_DIR = os.path.join(PROJECT_ROOT, "dataset")
DB_FILE = os.path.join(PROJECT_ROOT, "coimbatore_urban.db")


def safe_float(val):
    """Convert 'NA' / '' / non-numeric values to NaN."""
    try:
        if val is None or str(val).strip() in ("", "NA", "na"):
            return None
        return float(str(val).replace(",", "").strip())
    except (ValueError, TypeError):
        return None


def parse_month(month_str):
    """Normalise month names to title-case without trailing punctuation."""
    if not isinstance(month_str, str):
        return month_str
    cleaned = month_str.strip()
    cleaned = cleaned.replace("Sept", "Sep")
    return cleaned


def ingest_climate_normals(conn):
    path = os.path.join(DATASET_DIR, "climatological_table_1981_2010.csv")
    if not os.path.exists(path):
        print(f"  SKIP: {os.path.basename(path)} not found.")
        return 0

    df = pd.read_csv(path)
    df = df.rename(columns={
        "Month": "month",
        "Daily Minimum Temp (oC)": "daily_min_temp",
        "Daily Maximum Temp (oC)": "daily_max_temp",
        "Mean Total Rainfall (mm)": "mean_total_rainfall",
        "Mean Number of Rainy Days": "mean_rainy_days",
        "Mean Number of Days with Hail": "mean_hail_days",
        "Mean Number of Days with Thunder": "mean_thunder_days",
        "Mean Number of Days with Fog": "mean_fog_days",
        "Mean Number of Days with Squall": "mean_squall_days",
    })

    # Keep only monthly rows (drop 'Annual' summary for a cleaner table)
    df = df[~df["month"].str.contains("Annual", na=False)]

    numeric_cols = ["daily_min_temp", "daily_max_temp", "mean_total_rainfall",
                    "mean_rainy_days", "mean_hail_days", "mean_thunder_days",
                    "mean_fog_days", "mean_squall_days"]
    for col in numeric_cols:
        df[col] = df[col].apply(safe_float)

    df = df.dropna(subset=["daily_min_temp", "daily_max_temp"])

    df.to_sql("climate_normals", con=conn, if_exists="replace", index=False)
    print(f"  climate_normals  -> {len(df)} rows")
    return len(df)


def ingest_extreme_weather(conn):
    path = os.path.join(DATASET_DIR, "extreme_weather_events_april.csv")
    if not os.path.exists(path):
        print(f"  SKIP: {os.path.basename(path)} not found.")
        return 0

    df = pd.read_csv(path)
    df = df.rename(columns={
        "Year": "year",
        "Highest Maximum Temp (oC)": "highest_max_temp",
        "Highest Maximum Temp Date": "highest_max_temp_date",
        "Lowest Minimum Temp (oC)": "lowest_min_temp",
        "Lowest Minimum Temp Date": "lowest_min_temp_date",
        "Rainfall 24 Hours Highest (mm)": "rainfall_24h_highest",
        "Rainfall 24 Hours Highest Date": "rainfall_24h_date",
        "Rainfall Monthly Total (mm)": "rainfall_monthly_total",
    })

    # Drop the 'ALL TIME RECORD' summary row (keeps per-year records only)
    df = df[df["year"].astype(str).str.isdigit()]

    numeric_cols = ["highest_max_temp", "lowest_min_temp",
                    "rainfall_24h_highest", "rainfall_monthly_total"]
    for col in numeric_cols:
        df[col] = df[col].apply(safe_float)

    for col in ["highest_max_temp_date", "lowest_min_temp_date", "rainfall_24h_date"]:
        df[col] = df[col].replace({float("nan"): None, "": None})

    df["year"] = df["year"].astype(int)
    df = df.sort_values("year").reset_index(drop=True)

    df.to_sql("extreme_weather", con=conn, if_exists="replace", index=False)
    print(f"  extreme_weather   -> {len(df)} rows")
    return len(df)


def ingest_monthly_air_quality(conn):
    path = os.path.join(DATASET_DIR, "D04-Environment_25(Sheet1).csv")
    if not os.path.exists(path):
        print(f"  SKIP: {os.path.basename(path)} not found.")
        return 0

    df = pd.read_csv(path, encoding="utf-8-sig")
    df = df.rename(columns={
        "City Name": "city",
        "Month -Year": "month_year",
        "Monthly mean/average concentration - PM2.5": "pm25",
        "Monthly mean concentration - PM10": "pm10",
        "Monthly mean concentration - NO2": "no2",
        "Monthly mean concentration - SO2": "so2",
        "Monthly mean concentration - O3": "o3",
    })

    keep_cols = ["city", "month_year", "pm25", "pm10", "no2", "so2", "o3"]
    df = df[[c for c in keep_cols if c in df.columns]]

    # Forward-fill city (blank cells repeat 'Coimbatore')
    df["city"] = df["city"].ffill()

    # Drop fully empty / month-missing rows
    df = df.dropna(subset=["month_year"])
    df = df[df["month_year"].astype(str).str.strip() != ""]

    for col in ["pm25", "pm10", "no2", "so2", "o3"]:
        df[col] = df[col].apply(safe_float)

    # Add a sortable numeric year-month key
    def ym_to_key(m):
        try:
            name, year = str(m).strip().split()
            months = {"Jan":1,"Feb":2,"Mar":3,"Apr":4,"May":5,"Jun":6,
                      "Jul":7,"Aug":8,"Sep":9,"Oct":10,"Nov":11,"Dec":12}
            return int(year) * 100 + months.get(name[:3], 0)
        except (ValueError, AttributeError):
            return 0

    df["ym_key"] = df["month_year"].apply(ym_to_key)
    df = df.sort_values("ym_key").reset_index(drop=True)

    df.to_sql("monthly_air_quality", con=conn, if_exists="replace", index=False)
    print(f"  monthly_air_quality -> {len(df)} rows")
    return len(df)


def main():
    print("Ingesting external Coimbatore datasets...")
    print(f"  Dataset dir: {DATASET_DIR}")
    print(f"  DB file    : {DB_FILE}")

    conn = sqlite3.connect(DB_FILE)
    try:
        n1 = ingest_climate_normals(conn)
        n2 = ingest_extreme_weather(conn)
        n3 = ingest_monthly_air_quality(conn)
        conn.commit()
        print(f"\nDone! Loaded {n1 + n2 + n3} external records.")
    finally:
        conn.close()


if __name__ == "__main__":
    main()
