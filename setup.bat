@echo off
setlocal enabledelayedexpansion
title Coimbatore Urban Intelligence - Setup & Launch
cd /d "%~dp0"

echo ============================================================
echo    Coimbatore Urban Intelligence  -  Setup  &  Launch
echo ============================================================
echo.

REM ---------- 1. Check Python ----------
where python >nul 2>nul
if errorlevel 1 (
    echo [ERROR] Python not found on PATH. Install Python 3.9+ first.
    pause
    exit /b 1
)

REM ---------- 2. Create / reuse virtual environment ----------
if not exist "venv\Scripts\python.exe" (
    echo [1/5] Creating virtual environment...
    python -m venv venv
    if errorlevel 1 (
        echo [ERROR] Failed to create virtual environment.
        pause
        exit /b 1
    )
) else (
    echo [1/5] Virtual environment already present - reusing.
)

set "PY=venv\Scripts\python.exe"

REM ---------- 3. Install dependencies ----------
echo [2/5] Installing dependencies...
"%PY%" -m pip install --upgrade pip >nul 2>nul
"%PY%" -m pip install -r requirements.txt
if errorlevel 1 (
    echo [ERROR] Dependency installation failed.
    pause
    exit /b 1
)

REM ---------- 4. Generate + seed data ----------
echo [3/5] Generating base telemetry datasets...
"%PY%" scripts\generate_data.py

echo [4/5] Seeding database (base + external + OSM)...
"%PY%" scripts\seed_db.py

REM Fetch live OpenStreetMap data only if not already cached
if not exist "data\osm_coimbatore\cbe_hospitals.json" (
    echo [4b/5] Fetching OpenStreetMap data for Coimbatore...
    "%PY%" scripts\fetch_coimbatore_osm.py
    "%PY%" scripts\process_coimbatore_osm.py
)

REM ---------- 5. Launch dashboard ----------
echo [5/5] Launching dashboard...
echo.
echo    Starting Streamlit server...
echo    Opening browser at http://localhost:8501
echo    Press Ctrl+C in this window to stop the server.
echo.

start "" "%PY%" -m streamlit run app\main.py

REM Wait for the server to boot, then open the browser
timeout /t 8 /nobreak >nul
start "" "http://localhost:8501"

endlocal