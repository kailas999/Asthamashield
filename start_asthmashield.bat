@echo off
REM start_asthmashield.bat

REM This script starts both the backend and frontend servers

REM Start the backend server in a new command prompt
start "AsthmaShield Backend" cmd /k "cd backend && call init_db.bat"

REM Start the frontend server in a new command prompt
start "AsthmaShield Frontend" cmd /k "cd frontend && streamlit run app.py"

echo AsthmaShield application starting...
echo Backend will be available at http://localhost:8000
echo Frontend will be available at http://localhost:8501
pause