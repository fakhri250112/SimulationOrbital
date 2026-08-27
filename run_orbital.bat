@echo off
title ORBITAL 3D Satellite Energy Simulation
cd /d "%~dp0"

where py >nul 2>nul
if %errorlevel%==0 (
    set PY=py
) else (
    set PY=python
)

%PY% -c "import numpy, matplotlib" >nul 2>nul
if not %errorlevel%==0 (
    echo Installing required Python packages...
    %PY% -m pip install -r requirements.txt
)

echo Starting ORBITAL...
%PY% orbital_simulation.py

if not %errorlevel%==0 (
    echo.
    echo Program ended with an error.
    pause
)
