"""
process_coimbatore_osm.py
-------------------------
Loads the OSM JSON files collected for Coimbatore into the SQLite database
as a single `osm_infrastructure` table (one row per point of interest).

Also computes a lightweight per-area infrastructure count summary for use
in the dashboard (matching the 10 dashboard areas from 05_area_master.csv).

Usage:
    python scripts/process_coimbatore_osm.py
"""

import json
import math
import os
import sqlite3

import pandas as pd

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(PROJECT_ROOT, "data", "osm_coimbatore")
DB_FILE = os.path.join(PROJECT_ROOT, "coimbatore_urban.db")

CATEGORIES = ["hospitals", "schools", "traffic_nodes", "pharmacies", "parks"]


def load_category(category):
    path = os.path.join(DATA_DIR, f"cbe_{category}.json")
    if not os.path.exists(path):
        return []
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def haversine_km(lat1, lon1, lat2, lon2):
    R = 6371.0
    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)
    a = (math.sin(dlat / 2) ** 2
         + math.cos(math.radians(lat1)) * math.cos(math.radians(lat2))
         * math.sin(dlon / 2) ** 2)
    return R * 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))


def nearest_area(feature, areas_df):
    """Assign each POI to the nearest of the 10 dashboard areas."""
    best, best_dist = None, float("inf")
    for _, row in areas_df.iterrows():
        d = haversine_km(feature["lat"], feature["lon"], row["latitude"], row["longitude"])
        if d < best_dist:
            best_dist = d
            best = row["area"]
    return best, round(best_dist, 2)


def main():
    areas_path = os.path.join(PROJECT_ROOT, "data", "05_area_master.csv")
    if not os.path.exists(areas_path):
        print(f"SKIP: {areas_path} not found.")
        return

    areas_df = pd.read_csv(areas_path)

    records = []
    for category in CATEGORIES:
        features = load_category(category)
        print(f"  {category:<14} {len(features):>5} features")
        for f in features:
            area, dist = nearest_area(f, areas_df)
            records.append({
                "osm_id": f.get("id"),
                "category": category,
                "name": f.get("name"),
                "lat": f.get("lat"),
                "lon": f.get("lon"),
                "area": area,
                "distance_to_area_km": dist,
            })

    df = pd.DataFrame(records)
    print(f"\n  Total POI records: {len(df)}")

    conn = sqlite3.connect(DB_FILE)
    try:
        df.to_sql("osm_infrastructure", con=conn, if_exists="replace", index=False)
        conn.commit()
        print("  osm_infrastructure ->", len(df), "rows")
    finally:
        conn.close()


if __name__ == "__main__":
    main()
