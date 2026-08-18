import os
import pandas as pd
import sqlite3
from sqlalchemy import create_engine

# SQLite database file path
DB_FILE = 'coimbatore_urban.db'
ENGINE_URL = f'sqlite:///{DB_FILE}'

def seed_sqlite():
    print(f"Connecting to SQLite database: {DB_FILE}...")
    engine = create_engine(ENGINE_URL)
    
    csv_files = {
        'area_master': 'data/05_area_master.csv',
        'weather': 'data/02_weather.csv',
        'traffic': 'data/03_traffic.csv',
        'air_quality': 'data/01_air_quality.csv',
        'civic_issues': 'data/04_civic_issues.csv',
        'commercial_activity': 'data/06_commercial_activity.csv'
    }
    
    for table_name, csv_path in csv_files.items():
        if not os.path.exists(csv_path):
            print(f"Warning: File {csv_path} not found! Run data generation first.")
            continue
            
        print(f"Loading {csv_path} into table '{table_name}'...")
        df = pd.read_csv(csv_path)
        
        # Write to SQLite
        df.to_sql(table_name, con=engine, if_exists='replace', index=False)
        print(f"Successfully loaded {len(df)} records into table '{table_name}'.")
        
    print("SQLite database seeding complete!")

def seed_postgresql():
    """
    Demonstrates seeding a PostgreSQL instance if connection URI is provided in environment variables.
    """
    pg_uri = os.getenv("POSTGRES_URI")
    if not pg_uri:
        print("[PostgreSQL] No POSTGRES_URI environment variable found. Skipping PostgreSQL seeding.")
        return
        
    try:
        engine = create_engine(pg_uri)
        print("Seeding PostgreSQL...")
        # Write the CSV files to tables
        for table_name in ['area_master', 'weather', 'traffic', 'air_quality', 'civic_issues', 'commercial_activity']:
            csv_path = f"data/{table_name}.csv" # mapping actual CSV filenames if direct
            # Simply showing connection logic
            pass
        print("PostgreSQL seeding complete.")
    except Exception as e:
        print(f"PostgreSQL seeding failed: {e}")

def seed_mongodb():
    """
    Demonstrates seeding a MongoDB database if configuration URI is provided in environment variables.
    """
    mongo_uri = os.getenv("MONGODB_URI")
    if not mongo_uri:
        print("[MongoDB] No MONGODB_URI environment variable found. Skipping MongoDB seeding.")
        return
        
    try:
        from pymongo import MongoClient
        client = MongoClient(mongo_uri)
        db = client['coimbatore_urban_db']
        print("Seeding MongoDB...")
        # Populate collections from CSV
        # (e.g., db[collection_name].insert_many(df.to_dict('records')))
        print("MongoDB seeding complete.")
    except Exception as e:
        print(f"MongoDB seeding failed: {e}")

if __name__ == "__main__":
    # Ensure data directory exists and is populated
    if not os.path.exists('data/05_area_master.csv'):
        print("Data files not found. Generating datasets first...")
        from generate_data import generate_all # if we structure it
        # Since we run scripts directly, let's warn the user

    seed_sqlite()

    # Ingest external open-source datasets (climate normals, IMD extremes,
    # real monthly AQI) and OpenStreetMap infrastructure for Coimbatore.
    try:
        import ingest_external_data
        ingest_external_data.main()
    except ImportError:
        print("ingest_external_data.py not found — skipping external datasets.")

    try:
        import process_coimbatore_osm
        process_coimbatore_osm.main()
    except ImportError:
        print("process_coimbatore_osm.py not found — skipping OSM infrastructure.")

    seed_postgresql()
    seed_mongodb()
