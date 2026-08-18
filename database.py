import os
import sqlite3
import pandas as pd
from sqlalchemy import create_engine

# SQLite settings
DB_FILE = 'coimbatore_urban.db'

# Fallback paths to handle running from root vs within app/ directory
if not os.path.exists(DB_FILE) and os.path.exists('../' + DB_FILE):
    DB_FILE = '../' + DB_FILE

def get_connection():
    """
    Returns a connection. In a production environment, this would read from environment 
    variables to connect to PostgreSQL or MongoDB. Here it connects to SQLite as a fallback.
    """
    pg_uri = os.getenv("POSTGRES_URI")
    if pg_uri:
        try:
            engine = create_engine(pg_uri)
            return engine.connect()
        except Exception as e:
            print(f"Failed to connect to PostgreSQL, falling back to SQLite: {e}")
            
    # Default SQLite connection
    return sqlite3.connect(DB_FILE)

def query_dataframe(query, params=None):
    """
    Utility function to run query and return pandas DataFrame.
    """
    conn = get_connection()
    try:
        if isinstance(conn, sqlite3.Connection):
            df = pd.read_sql_query(query, conn, params=params)
        else:
            # SQLAlchemy connection
            df = pd.read_sql_query(query, conn, params=params)
        return df
    finally:
        conn.close()

def get_areas():
    df = query_dataframe("SELECT * FROM area_master ORDER BY area")
    return df

def get_weather(start_date=None, end_date=None):
    query = "SELECT * FROM weather"
    conditions = []
    params = []
    
    if start_date:
        conditions.append("date >= ?")
        params.append(start_date)
    if end_date:
        conditions.append("date <= ?")
        params.append(end_date)
        
    if conditions:
        query += " WHERE " + " AND ".join(conditions)
        
    query += " ORDER BY date"
    return query_dataframe(query, params)

def get_traffic(area=None, start_date=None, end_date=None):
    query = "SELECT * FROM traffic"
    conditions = []
    params = []
    
    if area:
        conditions.append("area = ?")
        params.append(area)
    if start_date:
        conditions.append("date >= ?")
        params.append(start_date)
    if end_date:
        conditions.append("date <= ?")
        params.append(end_date)
        
    if conditions:
        query += " WHERE " + " AND ".join(conditions)
        
    query += " ORDER BY date, time"
    return query_dataframe(query, params)

def get_air_quality(area=None, start_date=None, end_date=None):
    query = "SELECT * FROM air_quality"
    conditions = []
    params = []
    
    if area:
        conditions.append("area = ?")
        params.append(area)
    if start_date:
        conditions.append("date >= ?")
        params.append(start_date)
    if end_date:
        conditions.append("date <= ?")
        params.append(end_date)
        
    if conditions:
        query += " WHERE " + " AND ".join(conditions)
        
    query += " ORDER BY date"
    return query_dataframe(query, params)

def get_civic_issues(area=None, start_date=None, end_date=None):
    query = "SELECT * FROM civic_issues"
    conditions = []
    params = []
    
    if area:
        conditions.append("area = ?")
        params.append(area)
    if start_date:
        conditions.append("date >= ?")
        params.append(start_date)
    if end_date:
        conditions.append("date <= ?")
        params.append(end_date)
        
    if conditions:
        query += " WHERE " + " AND ".join(conditions)
        
    query += " ORDER BY date"
    return query_dataframe(query, params)

def get_commercial_activity(area=None):
    query = "SELECT * FROM commercial_activity"
    params = []
    
    if area:
        query += " WHERE area = ?"
        params.append(area)
        
    return query_dataframe(query, params)

def get_climate_normals():
    """
    IMD monthly climatological normals (1981-2010) for Coimbatore.
    """
    return query_dataframe("SELECT * FROM climate_normals")

def get_extreme_weather():
    """
    IMD April extreme weather events (per year) for Coimbatore.
    """
    return query_dataframe("SELECT * FROM extreme_weather")

def get_monthly_air_quality():
    """
    Real monthly mean pollutant concentrations for Coimbatore
    (CPCB / data.gov.in based, 2017-2018).
    """
    return query_dataframe("SELECT * FROM monthly_air_quality")

def get_osm_infrastructure(category=None, area=None):
    """
    OpenStreetMap points-of-interest collected for Coimbatore.
    """
    query = "SELECT * FROM osm_infrastructure"
    conditions = []
    params = []

    if category:
        conditions.append("category = ?")
        params.append(category)
    if area:
        conditions.append("area = ?")
        params.append(area)

    if conditions:
        query += " WHERE " + " AND ".join(conditions)

    query += " ORDER BY category, area"
    return query_dataframe(query, params)

def get_overview_kpis():
    """
    Fetch high-level metrics for overview cards.
    """
    total_areas = query_dataframe("SELECT COUNT(DISTINCT area) as count FROM area_master")['count'].iloc[0]
    total_records = query_dataframe(
        "SELECT (SELECT COUNT(*) FROM traffic) + (SELECT COUNT(*) FROM air_quality) + (SELECT COUNT(*) FROM civic_issues) as count"
    )['count'].iloc[0]
    avg_traffic = query_dataframe("SELECT AVG(vehicle_count) as avg FROM traffic")['avg'].iloc[0]
    avg_aqi = query_dataframe("SELECT AVG(pm25) as avg FROM air_quality")['avg'].iloc[0]
    total_complaints = query_dataframe("SELECT COUNT(*) as count FROM civic_issues")['count'].iloc[0]
    
    return {
        "total_areas": int(total_areas) if total_areas else 0,
        "total_records": int(total_records) if total_records else 0,
        "avg_traffic": int(avg_traffic) if avg_traffic else 0,
        "avg_aqi": round(avg_aqi, 1) if avg_aqi else 0.0,
        "total_complaints": int(total_complaints) if total_complaints else 0
    }
