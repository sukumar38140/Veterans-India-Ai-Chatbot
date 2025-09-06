@echo off
REM Veterans India AI Assistant - Quick Start Script
echo Veterans India AI Assistant - Quick Start
echo ============================================

REM Check if already running
for /f "tokens=5" %%a in ('netstat -ano ^| find ":8501"') do (
    if "%%a" NEQ "" (
        echo Application already running at http://localhost:8501
        start http://localhost:8501
        exit /b 0
    )
)

REM Start application
echo Starting application...
python run_app.py

pause
