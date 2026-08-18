import os
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

# Create data directory if it doesn't exist
os.makedirs('data', exist_ok=True)

# Seed for reproducibility
np.random.seed(42)

# Areas in Coimbatore and their coordinates/attributes
areas = [
    {"area": "Gandhipuram", "zone": "Central", "ward": 72, "latitude": 11.0168, "longitude": 76.9689, "area_type": "Commercial Hub"},
    {"area": "RS Puram", "zone": "West", "ward": 23, "latitude": 11.0116, "longitude": 76.9456, "area_type": "Commercial/Residential"},
    {"area": "Saravanampatti", "zone": "North", "ward": 2, "latitude": 11.0784, "longitude": 76.9984, "area_type": "IT Corridor"},
    {"area": "Peelamedu", "zone": "East", "ward": 37, "latitude": 11.0267, "longitude": 77.0108, "area_type": "Educational Hub"},
    {"area": "Town Hall", "zone": "Central", "ward": 80, "latitude": 10.9964, "longitude": 76.9603, "area_type": "Heritage Commercial"},
    {"area": "Ukkadam", "zone": "South", "ward": 86, "latitude": 10.9878, "longitude": 76.9628, "area_type": "Transport Hub"},
    {"area": "Singanallur", "zone": "East", "ward": 57, "latitude": 11.0022, "longitude": 77.0236, "area_type": "Residential/Industrial"},
    {"area": "Saibaba Colony", "zone": "West", "ward": 11, "latitude": 11.0283, "longitude": 76.9472, "area_type": "Residential"},
    {"area": "Ramanathapuram", "zone": "South", "ward": 75, "latitude": 10.9988, "longitude": 76.9882, "area_type": "Mixed Residential"},
    {"area": "Hopes College", "zone": "East", "ward": 39, "latitude": 11.0367, "longitude": 77.0094, "area_type": "Commercial/Educational"}
]

# 1. Generate 05_area_master.csv
df_area = pd.DataFrame(areas)
df_area.to_csv('data/05_area_master.csv', index=False)
print("Generated 05_area_master.csv")

# Date Range: Past 30 days
end_date = datetime(2026, 8, 12)
start_date = end_date - timedelta(days=29)
date_list = [start_date + timedelta(days=x) for x in range(30)]

# 2. Generate 02_weather.csv
weather_records = []
for d in date_list:
    date_str = d.strftime('%Y-%m-%d')
    # Coimbatore temperature usually ranges from 22 to 34 degrees C
    temp = round(np.random.uniform(24.0, 33.0), 1)
    humidity = int(np.random.uniform(60, 85))
    # Rainfall: occasional spikes (monsoon days)
    is_rainy = np.random.choice([0, 1], p=[0.8, 0.2])
    rainfall = round(np.random.exponential(15.0), 1) if is_rainy else 0.0
    wind_speed = round(np.random.uniform(5.0, 20.0), 1)
    weather_records.append({
        "date": date_str,
        "temperature": temp,
        "humidity": humidity,
        "rainfall": rainfall,
        "wind_speed": wind_speed
    })
df_weather = pd.DataFrame(weather_records)
df_weather.to_csv('data/02_weather.csv', index=False)
print("Generated 02_weather.csv")

# 3. Generate 03_traffic.csv
traffic_records = []
time_slots = ["08:30 AM", "02:00 PM", "06:30 PM"]

for d in date_list:
    date_str = d.strftime('%Y-%m-%d')
    day_name = d.strftime('%A')
    is_weekend = day_name in ['Saturday', 'Sunday']
    
    for area_info in areas:
        area_name = area_info["area"]
        area_type = area_info["area_type"]
        
        for slot in time_slots:
            # Base vehicles dependent on area type and time of day
            base_count = 300
            if area_type in ["Commercial Hub", "Heritage Commercial", "Transport Hub"]:
                base_count = 500
            elif area_type == "IT Corridor":
                base_count = 450
            
            # Time multiplier: peak hours (morning/evening) get much more traffic
            if "08:30 AM" in slot or "06:30 PM" in slot:
                time_mult = np.random.uniform(1.6, 2.2)
            else:
                time_mult = np.random.uniform(0.7, 1.1)
                
            # Weekend multiplier: Commercial higher, IT Corridor lower
            weekend_mult = 1.0
            if is_weekend:
                if area_type in ["Commercial Hub", "Heritage Commercial"]:
                    weekend_mult = 1.3
                elif area_type == "IT Corridor":
                    weekend_mult = 0.4
                else:
                    weekend_mult = 0.8
                    
            total_vehicles = int(base_count * time_mult * weekend_mult)
            
            # Split into vehicle types
            bikes = int(total_vehicles * np.random.uniform(0.45, 0.55))
            cars = int(total_vehicles * np.random.uniform(0.20, 0.30))
            autos = int(total_vehicles * np.random.uniform(0.10, 0.15))
            buses = int(total_vehicles * np.random.uniform(0.04, 0.08))
            trucks = total_vehicles - (bikes + cars + autos + buses)
            if trucks < 0:
                trucks = 0
            
            # Recalculate total vehicles to match sum exactly
            total_vehicles = cars + bikes + buses + autos + trucks
            
            traffic_records.append({
                "date": date_str,
                "time": slot,
                "area": area_name,
                "vehicle_count": total_vehicles,
                "cars": cars,
                "bikes": bikes,
                "buses": buses,
                "autos": autos,
                "trucks": trucks
            })

df_traffic = pd.DataFrame(traffic_records)
df_traffic.to_csv('data/03_traffic.csv', index=False)
print("Generated 03_traffic.csv")

# 4. Generate 01_air_quality.csv
# Air quality correlates with traffic density, weather parameters (rain clears air, humidity/wind moves air)
aq_records = []
stations = {
    "Gandhipuram": "Gandhipuram-CCMC",
    "RS Puram": "RS Puram-WestZone",
    "Saravanampatti": "Saravanampatti-CHILSEZ",
    "Peelamedu": "PSG-Tech-Peelamedu",
    "Town Hall": "TownHall-DistrictCourt",
    "Ukkadam": "Ukkadam-BusStand",
    "Singanallur": "Singanallur-TrichyRoad",
    "Saibaba Colony": "Saibaba-MettupalayamRoad",
    "Ramanathapuram": "Ramanathapuram-Nanjundapuram",
    "Hopes College": "Hopes-AvinashiRoad"
}

# Load generated traffic and weather to calculate realistic AQI values
traffic_grouped = df_traffic.groupby(['date', 'area'])['vehicle_count'].mean().reset_index()
weather_dict = df_weather.set_index('date').to_dict('index')

for _, row in traffic_grouped.iterrows():
    date_str = row['date']
    area_name = row['area']
    avg_veh = row['vehicle_count']
    
    w_info = weather_dict[date_str]
    rain = w_info['rainfall']
    wind = w_info['wind_speed']
    
    # Calculate pollutants based on traffic and weather
    # Base levels + Traffic factor - Rain wash factor - Wind dispersion factor
    base_pm25 = 35.0
    traffic_factor = (avg_veh / 800) * 40
    rain_factor = min(rain * 1.5, 30)
    wind_factor = min(wind * 0.8, 15)
    
    pm25 = max(10.0, round(base_pm25 + traffic_factor - rain_factor - wind_factor + np.random.normal(0, 5), 1))
    pm10 = max(20.0, round(pm25 * np.random.uniform(1.4, 1.8), 1))
    no2 = max(5.0, round(12.0 + (avg_veh / 800) * 20 - rain_factor*0.3 + np.random.normal(0, 2), 1))
    so2 = max(2.0, round(4.0 + (avg_veh / 800) * 5 + np.random.normal(0, 0.8), 1))
    o3 = max(5.0, round(15.0 + w_info['temperature']*0.5 - wind_factor*0.2 + np.random.normal(0, 3), 1))
    
    aq_records.append({
        "date": date_str,
        "station": stations[area_name],
        "area": area_name,
        "pm25": pm25,
        "pm10": pm10,
        "no2": no2,
        "so2": so2,
        "o3": o3
    })

df_aq = pd.DataFrame(aq_records)
df_aq.to_csv('data/01_air_quality.csv', index=False)
print("Generated 01_air_quality.csv")

# 5. Generate 04_civic_issues.csv
# Fields: issue_id, date, area, issue_type, severity, status, resolution_days
issue_types = ["Waste Management", "Water Supply", "Road Damage", "Streetlights", "Traffic Congestion", "Sewage Overflow"]
severities = ["Low", "Medium", "High"]
statuses = ["Resolved", "In Progress", "Pending"]

civic_records = []
issue_counter = 1001

for d in date_list:
    date_str = d.strftime('%Y-%m-%d')
    
    # Random number of complaints filed per day (0 to 5)
    num_complaints = np.random.randint(0, 6)
    for _ in range(num_complaints):
        area_name = np.random.choice([a["area"] for a in areas])
        issue = np.random.choice(issue_types)
        severity = np.random.choice(severities, p=[0.4, 0.4, 0.2])
        
        # Older issues are more likely to be resolved, newer issues might be pending or in progress
        days_since = (end_date - d).days
        if days_since > 15:
            status = np.random.choice(statuses, p=[0.8, 0.15, 0.05])
        elif days_since > 5:
            status = np.random.choice(statuses, p=[0.5, 0.35, 0.15])
        else:
            status = np.random.choice(statuses, p=[0.1, 0.6, 0.3])
            
        if status == "Resolved":
            # Resolution days depends on severity
            base_days = 2 if severity == "Low" else (5 if severity == "Medium" else 10)
            res_days = int(max(1, base_days + np.random.normal(0, 1.5)))
        else:
            res_days = ""  # Represents NaN or empty in CSV
            
        civic_records.append({
            "issue_id": f"C{issue_counter}",
            "date": date_str,
            "area": area_name,
            "issue_type": issue,
            "severity": severity,
            "status": status,
            "resolution_days": res_days
        })
        issue_counter += 1

df_civic = pd.DataFrame(civic_records)
df_civic.to_csv('data/04_civic_issues.csv', index=False)
print("Generated 04_civic_issues.csv")

# 6. Generate 06_commercial_activity.csv
# Fields: area, business_count, commercial_category, estimated_footfall
comm_records = []
categories = ["Retail & Markets", "IT & Corporate Offices", "Shopping Mall / High Street", "Educational & Residential"]

for area_info in areas:
    area_name = area_info["area"]
    area_type = area_info["area_type"]
    
    if area_type == "Commercial Hub":
        biz_count = np.random.randint(400, 600)
        cat = "Shopping Mall / High Street"
        footfall = np.random.randint(15000, 30000)
    elif area_type == "Heritage Commercial":
        biz_count = np.random.randint(500, 800)
        cat = "Retail & Markets"
        footfall = np.random.randint(20000, 40000)
    elif area_type == "IT Corridor":
        biz_count = np.random.randint(150, 300)
        cat = "IT & Corporate Offices"
        footfall = np.random.randint(10000, 20000)
    elif area_type == "Transport Hub":
        biz_count = np.random.randint(200, 400)
        cat = "Retail & Markets"
        footfall = np.random.randint(25000, 50000)
    elif "Educational" in area_type or "Commercial/Educational" in area_type:
        biz_count = np.random.randint(250, 450)
        cat = "Shopping Mall / High Street"
        footfall = np.random.randint(12000, 22000)
    else: # Residential or Mixed
        biz_count = np.random.randint(100, 250)
        cat = "Educational & Residential"
        footfall = np.random.randint(5000, 10000)
        
    comm_records.append({
        "area": area_name,
        "business_count": biz_count,
        "commercial_category": cat,
        "estimated_footfall": footfall
    })

df_comm = pd.DataFrame(comm_records)
df_comm.to_csv('data/06_commercial_activity.csv', index=False)
print("Generated 06_commercial_activity.csv")
print("All dataset generation completed successfully!")
