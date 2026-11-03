@echo off
setlocal
cd /d "%~dp0"
title EV Planner - Local Server

echo Starting EV Planner...
py -3 --version >nul 2>&1
if errorlevel 1 (
    echo.
    echo Python 3 was not found. Install Python from https://www.python.org/downloads/
    echo During installation, enable the Python launcher and Add Python to PATH.
    echo Then run this file again.
    pause
    exit /b 1
)

if not exist ".venv\Scripts\python.exe" (
    echo Creating a virtual environment...
    py -3 -m venv .venv
    if errorlevel 1 goto error
)

echo Installing or checking dependencies...
".venv\Scripts\python.exe" -m pip install -r requirements.txt
if errorlevel 1 goto error

echo.
echo Open http://127.0.0.1:5000 in your browser after the server starts.
echo Keep this window open. Press Ctrl+C to stop the server.
echo.
".venv\Scripts\python.exe" app.py
if errorlevel 1 goto error
exit /b 0

:error
echo.
echo The app could not start. Please share the error message shown above.
pause
exit /b 1
