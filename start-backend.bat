@echo off
chcp 65001 > nul
cls
color 0A

echo.
echo ╔════════════════════════════════════════════════════════════════╗
echo ║                  🚀 INSTAGRAM AGENT BACKEND 🚀                ║
echo ╠════════════════════════════════════════════════════════════════╣
echo ║ Starting FastAPI Backend Server...                             ║
echo ║ Backend will run on: http://localhost:8000                     ║
echo ║ Documentation:    http://localhost:8000/docs                   ║
echo ╚════════════════════════════════════════════════════════════════╝
echo.

echo ⚙️  STEP 1: Checking Python environment...
cd /d %~dp0/backend
if not exist venv (
    echo ❌ Virtual environment not found!
    echo ✅ Creating virtual environment...
    python -m venv venv
)
echo ✅ Virtual environment found
echo.

echo ⚙️  STEP 2: Activating virtual environment...
call venv\Scripts\activate.bat
echo ✅ Virtual environment activated
echo.

echo ⚙️  STEP 3: Starting FastAPI server...
echo.
echo 📌 IMPORTANT: Make sure you have also started:
echo    1. 🎨 Stable Diffusion WebUI on http://localhost:7860
echo    2. Run webui-user.bat in AUTOMATIC1111 folder
echo.

uvicorn main:app --reload --host 0.0.0.0 --port 8000

echo.
echo ❌ Backend stopped!
pause
