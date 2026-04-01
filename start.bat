@echo off
REM Phishing Shield - Quick Start Script for Windows

echo.
echo ============================================
echo   Phishing Shield - Quick Start
echo ============================================
echo.

REM Check Python installation
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python not found! Please install Python 3.8+
    echo    Download from: https://www.python.org/downloads/
    pause
    exit /b 1
)

echo ✅ Python found
echo.

REM Create virtual environment if not exists
if not exist venv (
    echo 📦 Creating virtual environment...
    python -m venv venv
    echo ✅ Virtual environment created
)

REM Activate virtual environment
echo 🔄 Activating virtual environment...
call venv\Scripts\activate.bat

REM Install dependencies
echo 📥 Installing dependencies...
pip install -r requirements.txt >nul 2>&1
if errorlevel 1 (
    echo ❌ Failed to install dependencies
    pause
    exit /b 1
)
echo ✅ Dependencies installed

REM Run model test
echo.
echo 🧪 Testing ML Model...
python model.py
if errorlevel 1 (
    echo ❌ Model test failed
    pause
    exit /b 1
)

echo.
echo ✅ All tests passed!
echo.
echo 🚀 Starting Phishing Shield API Server...
echo    Server will run on: http://localhost:5001
echo.
echo Instructions:
echo  1. Open Chrome and go to: chrome://extensions/
echo  2. Enable "Developer mode"
echo  3. Click "Load unpacked"
echo  4. Select the "extension" folder
echo  5. Click the extension icon to test
echo.
echo Press Ctrl+C to stop the server
echo.

REM Start Flask app
python app.py
pause
