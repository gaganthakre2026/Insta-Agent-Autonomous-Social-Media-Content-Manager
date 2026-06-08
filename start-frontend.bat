@echo off
chcp 65001 > nul
cls
color 0A

echo.
echo ╔════════════════════════════════════════════════════════════════╗
echo ║                  🎨 INSTAGRAM AGENT FRONTEND 🎨               ║
echo ╠════════════════════════════════════════════════════════════════╣
echo ║ Starting React Development Server...                           ║
echo ║ Frontend will run on: http://localhost:3000                    ║
echo ╚════════════════════════════════════════════════════════════════╝
echo.

echo ⚙️  STEP 1: Verifying dependencies...
cd /d %~dp0/frontend
if not exist node_modules (
    echo ❌ node_modules not found!
    echo ✅ Installing dependencies...
    npm install
)
echo ✅ Dependencies ready
echo.

echo ⚙️  STEP 2: Starting development server...
echo.
echo 📌 IMPORTANT: Make sure you have also started:
echo    1. ⚙️  Backend on http://localhost:8000
echo    2. 🎨 Stable Diffusion on http://localhost:7860
echo.
echo 🚀 Frontend will open automatically in your browser...
echo.

npm start

echo.
echo ❌ Frontend stopped!
pause
