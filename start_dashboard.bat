@echo off
REM ============================================================================
REM  Fraud Detection Dashboard - Windows Startup Script
REM  
REM  Starts both backend API and frontend React app
REM  
REM  Author: Masood Nazari
REM  GitHub: github.com/michaeltheanalyst
REM ============================================================================

title Fraud Detection Dashboard

echo.
echo ╔════════════════════════════════════════════════════════════════╗
echo ║                                                                ║
echo ║        🚀 FRAUD DETECTION DASHBOARD - AUTO STARTUP 🚀          ║
echo ║                                                                ║
echo ║  Starting Backend + Frontend...                                ║
echo ║                                                                ║
echo ╚════════════════════════════════════════════════════════════════╝
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python not found!
    echo    Please install Python 3.9+ from python.org
    pause
    exit /b 1
)

REM Check if Node.js is installed
node --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Node.js not found!
    echo    Please install Node.js from nodejs.org
    pause
    exit /b 1
)

echo ✅ Python and Node.js found
echo.

REM Start Backend in new window
echo 🔧 Starting Backend API Server...
start "Backend API" cmd /k "python -m uvicorn backend.main:app --reload --host 0.0.0.0 --port 8000"
timeout /t 5 /nobreak >nul

REM Start Frontend in new window
echo 🎨 Starting Frontend React App...
cd frontend
start "Frontend Dashboard" cmd /k "npm run dev"
cd ..
timeout /t 5 /nobreak >nul

echo.
echo ╔════════════════════════════════════════════════════════════════╗
echo ║                                                                ║
echo ║              ✅ DASHBOARD STARTED SUCCESSFULLY! ✅              ║
echo ║                                                                ║
echo ╚════════════════════════════════════════════════════════════════╝
echo.
echo 🌐 Access Points:
echo.
echo    📊 Dashboard:     http://localhost:3000
echo    🔌 Backend API:   http://localhost:8000
echo    📖 API Docs:      http://localhost:8000/docs
echo.
echo ⌨️  Two new windows opened:
echo    1. Backend API (Python/FastAPI)
echo    2. Frontend Dashboard (React/Vite)
echo.
echo 💡 Tip: Close those windows to stop the servers
echo.
pause

