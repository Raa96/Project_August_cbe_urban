"""
fetch_coimbatore_osm.py
-----------------------
Collects open-source infrastructure data for Coimbatore from the
OpenStreetMap Overpass API (same approach as urban-intel-main, adapted
to Coimbatore city bounds).

Categories fetched:
  * hospitals   — hospitals / clinics
  * schools     — schools / colleges / universities
  * traffic_nodes — traffic signals / crossings / junctions
  * pharmacies  — pharmacies / doctors
  * parks       — public parks / green spaces (urban amenity)

Outputs JSON files into `data/osm_coimbatore/`.

Usage:
    python scripts/fetch_coimbatore_osm.py
"""

import json
import os
import sys
import time

import requests

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUTPUT_DIR = os.path.join(PROJECT_ROOT, "data", "osm_coimbatore")

# Coimbatore city bounding box (south, west, north, east)
BBOX = "10.95,76.85,11.15,77.10"

OVERPASS_MIRRORS = [
    "https://overpass-api.de/api/interpreter",
    "https://overpass.kumi.systems/api/interpreter",
]

HEADERS = {"User-Agent": "CoimbatoreUrbanIntelligence/1.0 (student project)"}

QUERIES = {
    "hospitals": f"""
        [out:json][timeout:90];
        (
          node["amenity"="hospital"]({BBOX});
          way["amenity"="hospital"]({BBOX});
          node["amenity"="clinic"]({BBOX});
          way["amenity"="clinic"]({BBOX});
          node["healthcare"="hospital"]({BBOX});
        );
        out center;
    """,
    "schools": f"""
        [out:json][timeout:90];
        (
          node["amenity"="school"]({BBOX});
          way["amenity"="school"]({BBOX});
          node["amenity"="college"]({BBOX});
          way["amenity"="college"]({BBOX});
          node["amenity"="university"]({BBOX});
        );
        out center;
    """,
    "traffic_nodes": f"""
        [out:json][timeout:90];
        (
          node["highway"="traffic_signals"]({BBOX});
          node["highway"="crossing"]({BBOX});
          node["highway"="junction"]({BBOX});
        );
        out body;
    """,
    "pharmacies": f"""
        [out:json][timeout:90];
        (
          node["amenity"="pharmacy"]({BBOX});
          way["amenity"="pharmacy"]({BBOX});
          node["amenity"="doctors"]({BBOX});
        );
        out center;
    """,
    "parks": f"""
        [out:json][timeout:90];
        (
          node["leisure"="park"]({BBOX});
          way["leisure"="park"]({BBOX});
          node["leisure"="garden"]({BBOX});
          way["leisure"="garden"]({BBOX});
        );
        out center;
    """,
}


def fetch_with_retry(query, max_retries=4):
    for attempt in range(1, max_retries + 1):
        print(f"    attempt {attempt}/{max_retries}...", end=" ", flush=True)
        for mirror in OVERPASS_MIRRORS:
            try:
                response = requests.post(
                    mirror, data={"data": query}, headers=HEADERS, timeout=180
                )
                if response.status_code == 429:
                    print(f"rate limited ({mirror}). ", end="", flush=True)
                    continue
                if response.status_code in (502, 503, 504):
                    print(f"gateway timeout ({mirror}). ", end="", flush=True)
                    continue
                response.raise_for_status()
                data = response.json()
                print(f"OK ({len(data.get('elements', []))} elements).")
                return data
            except Exception as exc:  # noqa: BLE001
                print(f"err {type(exc).__name__} ({mirror}). ", end="", flush=True)
                time.sleep(2 * attempt)
        time.sleep(10 * attempt)
    print("ALL FAILED.")
    return None


def extract_features(raw, category):
    features = []
    for el in raw.get("elements", []):
        lat = el.get("lat") or (el.get("center") or {}).get("lat")
        lon = el.get("lon") or (el.get("center") or {}).get("lon")
        if lat is None or lon is None:
            continue
        tags = el.get("tags", {})
        name = (
            tags.get("name")
            or tags.get("name:en")
            or tags.get("operator")
            or f"Unnamed {category.rstrip('s')}"
        )
        features.append({
            "id": el.get("id"),
            "type": el.get("type"),
            "category": category,
            "name": name,
            "lat": round(lat, 6),
            "lon": round(lon, 6),
        })
    return features


def save_json(data, filename):
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    filepath = os.path.join(OUTPUT_DIR, filename)
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    print(f"    saved -> {os.path.relpath(filepath, PROJECT_ROOT)} ({len(data)} records)")


def already_fetched(category):
    filepath = os.path.join(OUTPUT_DIR, f"cbe_{category}.json")
    if not os.path.exists(filepath):
        return False
    try:
        with open(filepath, encoding="utf-8") as f:
            data = json.load(f)
        return len(data) > 0
    except Exception:
        return False


def main():
    print("=" * 60)
    print("  Urban Intelligence — Coimbatore OSM Data Collection")
    print("  Bounding box:", BBOX)
    print("=" * 60)

    summary = {}

    for i, (category, query) in enumerate(QUERIES.items()):
        print(f"\n[{i + 1}/{len(QUERIES)}] {category.upper()}")
        if already_fetched(category):
            filepath = os.path.join(OUTPUT_DIR, f"cbe_{category}.json")
            with open(filepath, encoding="utf-8") as f:
                summary[category] = len(json.load(f))
            print(f"    already cached ({summary[category]} records). Skipping.")
            continue

        raw = fetch_with_retry(query)
        if raw is None:
            summary[category] = 0
            continue

        features = extract_features(raw, category)
        save_json(features, f"cbe_{category}.json")
        summary[category] = len(features)

        if i < len(QUERIES) - 1:
            time.sleep(8)

    print("\n" + "=" * 60)
    print("  SUMMARY")
    print("=" * 60)
    total = 0
    for cat, count in summary.items():
        status = "OK" if count > 0 else "FAIL"
        print(f"  [{status:4}] {cat:<14} {count:>6} records")
        total += count
    print(f"\n  Total OSM records collected: {total}")

    summary_path = os.path.join(OUTPUT_DIR, "collection_summary.json")
    with open(summary_path, "w", encoding="utf-8") as f:
        json.dump({"city": "Coimbatore", "bbox": BBOX, "categories": summary,
                   "total_records": total}, f, indent=2)
    print(f"  Summary -> {os.path.relpath(summary_path, PROJECT_ROOT)}")


if __name__ == "__main__":
    sys.exit(main())
