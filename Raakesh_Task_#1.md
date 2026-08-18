## Coimbatore Urban Intelligence — Data Analysis & Tableau Dashboard

## Assigned to : RAAKESH M (SCOPE)

Problem statement : Analyze Coimbatore's urban environment using real-world data and identify patterns, relationships, problem areas, and actionable insights through Python, Plotly, Streamlit, and Tableau.

Task : To build a data-driven analysis of Coimbatore city, combining data from multiple sources and answering meaningful urban questions.

Data Collection → Preprocessing → EDA → Statistical Analysis → Plotly → Flask Application → Tableau → Insights

## Recommended Data Sheets :

| Sheet / Dataset | Suggested Data |
| --- | --- |
| 1. Traffic & Transportation | Area, road, vehicle count, peak hour, traffic density, bus |
| availability |   |
| 2. Weather & Air Quality | Date, temperature, rainfall, humidity, AQI/PM2.5 |
| 3. Public Transport | Route, bus count, stops, frequency, area, operating hours |
| 4. Waste Management | Zone, ward, waste generated, waste collected, collection |
| frequency |   |
| 5. Water / Civic Issues | Area, complaint type, complaint count, resolution time |
| 6. Education / Student | Area, institution type, student count, institution count |
| Population |   |
| 7. Commercial / Business Areas Area, business type, business count, footfall/population |   |
| indicators |   |


## Coimbatore Urban Intelligence — Data Analysis & Tableau Dashboard

Build a Coimbatore Urban Intelligence Platform that collects real-world Coimbatore data from multiple sources, performs preprocessing and EDA using Python/Pandas, stores data using PostgreSQL/MongoDB, creates interactive Plotly visualizations, develops a Streamlit analytics application, and presents executive-level insights through Tableau.

## Minimum final product

Data collection + preprocessing + EDA

Data storage

Interactive visualizations

Interactive analytical web application

Executive dashboard

Insights + recommendations

## 1. Python Notebook

## 2. PostgreSQL + MongoDB

## 3. Plotly

## 4. Streamlit

## 5. Tableau

## 6. Final Report


## Coimbatore Urban Intelligence — Data Analysis & Tableau Dashboard

## UI / Dashboard Requirements

| S.No Module / |   | Required UI | Mandatory Visualizations / Features |
| --- | --- | --- | --- |
|   | Page | Components |   |
| 1 | Overview | KPI cards, filters, | Total Areas, Total Records, Average Traffic, |
|   |   | summary section | Average AQI, Total Civic Complaints, Overall |
|   |   |   | Urban Insights |
| 2 | Traffic | KPI cards, area/date | Average Traffic, Peak Traffic Area, Peak |
|   | Analysis | filters, interactive | Traffic Hour, Total Vehicles; Traffic by Area, |
|   |   | charts | Traffic by Hour, Traffic by Day, Peak-Hour |
|   |   |   | Analysis, Area vs Traffic, Traffic Trend |
| 3 | Environmen | KPI cards, date/area | Average AQI, Average Temperature, Total |
|   | t Analysis | filters, trend analysis | Rainfall; AQI Trend, Temperature Trend, |
|   |   |   | Rainfall Trend, AQI vs Traffic, AQI by Area, |
|   |   |   | Weather vs AQI |
| 4 | Civic Issues | KPI cards, | Total Complaints, Resolved %, Average |
|   |   | issue/category filters, | Resolution Time; Complaints by Category, |
|   |   | area filters | Complaints by Area, Resolution Time |
|   |   |   | Analysis, Monthly Complaint Trend, Top |
|   |   |   | Problematic Areas |
| 5 | Area | Area selection | Compare two areas based on Traffic, AQI, |
|   | Comparison | controls, comparison | Complaints, Resolution Time, Public |
|   |   | cards, comparison | Transport, and other available metrics |
|   |   | charts |   |
| 6 | Cross-Doma | Multi-dataset filters, | Traffic vs AQI, Traffic vs Complaints, |
|   | in Analysis | relationship analysis | Commercial Activity vs Traffic, Weather vs |
|   |   |   | AQI, Correlation Analysis |
| 7 | Data | Dataset selector, | Raw/Cleaned/Combined Dataset View, |
|   | Explorer | filters, interactive data | Record Count, Column Information, |
|   |   | table | Filter/Search, Download Processed Dataset |


## Coimbatore Urban Intelligence — Data Analysis & Tableau Dashboard

| 8 | Insights | Insight cards, findings | Minimum 10 Data-Driven Insights and 5 |
| --- | --- | --- | --- |
|   |   | section, | Actionable Recommendations |
|   |   | recommendation |   |
|   |   | section |   |

## Sidebar Navigation :

| S.No | Navigation Item | Purpose |
| --- | --- | --- |
| 1 | Overview | Overall Coimbatore urban summary |
| 2 | Traffic Analysis | Analyze traffic patterns and congestion |
| 3 | Environment Analysis Analyze AQI, weather and environmental |   |
|   | patterns |   |
| 4 | Civic Issues | Analyze complaints and civic problems |
| 5 | Area Comparison | Compare different Coimbatore areas |
| 6 | Cross-Domain | Identify relationships across multiple datasets |
|   | Analysis |   |
| 7 | Data Explorer | Explore collected and processed datasets |
| 8 | Insights | Present findings and recommendations |

## Visualization Requirements:

| S.No | Visualizatio | Requirement |
| --- | --- | --- |
|   | n |   |
| 1 | Bar Chart Mandatory |   |
| 2 | Line Chart Mandatory |   |
| 3 | Scatter Plot Mandatory |   |
| 4 | Heatmap Mandatory |   |
| 5 | Box Plot | Mandatory |
| 6 | Histogram Mandatory |   |


## Coimbatore Urban Intelligence — Data Analysis & Tableau Dashboard

| 7 | Interactive | Recommende |
| --- | --- | --- |
|   | Map | d |
| 8 | KPI Cards Mandatory |   |
| 9 | Interactive | Mandatory |
|   | Filters |   |
| 10 | Data Table Mandatory |   |

Plotly must be used for the interactive visualizations.

## Global Dashboard Requirements

| Requirement | Details |
| --- | --- |
| UI Type | Dashboard |
| Framework | Streamlit |
| Visualization | Plotly |
| Responsive UI | Required |
| Sidebar Navigation | Required |
| Interactive Filters | Required |
| Area Filter | Required wherever |
|   | applicable |
| Date Filter | Required wherever |
|   | applicable |
| Interactive Charts | Required |
| Tooltips / Hover | Required |
| Information |   |
| Data Tables | Required |
| Download Option | Required |
| KPI Cards | Required |


## Coimbatore Urban Intelligence — Data Analysis & Tableau Dashboard

Error / Empty Data Handling

Required


## Coimbatore Urban Intelligence — Data Analysis & Tableau Dashboard

## Expected User Flow

Overview → Traffic → Environment → Civic Issues → Area Comparison → Cross-Domain Analysis → Data Explorer → Insights

## Recommended Coimbatore Data Sources :

| S.No | Dataset | What students can collect | Source / URL | Use in |
| --- | --- | --- | --- | --- |
|   |   |   |   | Dashboard |
| 1 | Air Quality – | PM2.5, PM10, NO2, SO2 and | https://www.data.gov. | Environment |
|   | Coimbatore | other pollutants | in/resource/environm | Analysis |
|   |   |   | ent-air-quality-data |   |
| 2 | Coimbatore | Monthly pollutant | Derive pollution from | AQI / Pollution |
|   | Pollution Data | concentration data | air quality | Trends |
| 3 | Coimbatore | Temperature, rainfall, rainy | https://city.imd.gov.in/ | Environment |
|   | Weather & Rainfall | days, monthly climatology | citywx/extreme/APR/c | Analysis |
|   |   |   | oimbatore2.htm |   |
| 4 | Government | Search additional | https://www.data.gov. | Data Collection |
|   | Open Data Portal | Coimbatore/Tamil Nadu | in/ |   |
|   |   | datasets |   |   |
| 5 | Coimbatore | Corporation/ward/zone | https://ccmc.gov.in/ | Civic Issues / |
|   | Corporation | information and civic |   | Area Analysis |
|   |   | information |   |   |
| 6 | CPCB | Air-quality monitoring | https://cpcb.gov.in/ | Environment |
|   |   | information |   | Analysis |
| 7 | IMD | Historical weather/rainfall |   | Check Public Docs Weather |
|   |   | information |   | Analysis |
| 8 | Google Maps / | Roads, locations, POIs and | https://www.openstre | Area / Map |
|   | OpenStreetMap | geographic information | etmap.org/#map=5/2 | Analysis |
|   |   |   | 1.84/82.79 |   |


## Coimbatore Urban Intelligence — Data Analysis & Tableau Dashboard

## Traffic Data :

| Date | Time | Area | Vehicle Count Vehicle Type Traffic Level |
| --- | --- | --- | --- |
| 10-08-2026 8:00 AM Gandhipuram 820 |   |   | Mixed High |
|   |   | 10-08-2026 8:00 AM RS Puram | 640 Mixed Medium |
| 10-08-2026 6:00 PM Saravanampatti 920 |   |   | Mixed High |

## Require:

- Minimum 10 locations

- Minimum 3 time slots/day

- Minimum 3 different days

- Cars

- Bikes

- Buses

- Autos

- Trucks

- Total vehicles

## That gives them an actual dataset for:

Traffic by Area → Traffic by Hour → Peak Hour → Area Comparison.

specifically require these 6 sheets:

## 01_air_quality.csv

date station area pm25 pm10 no2 so2 o3

## 02_weather.csv

date


## Coimbatore Urban Intelligence — Data Analysis & Tableau Dashboard

temperature humidity rainfall wind_speed

## 03_traffic.csv

date time area vehicle_count cars bikes buses autos trucks

## 04_civic_issues.csv

issue_id date area issue_type severity status resolution_days

## 05_area_master.csv

area

zone ward latitude longitude area_type

## 06_commercial_activity.csv

area

business_count commercial_category estimated_footfall


