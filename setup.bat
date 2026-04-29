@echo off
REM ============================================================================
REM AI-Based EMI Affordability & Product Recommendation System
REM Automated Setup Script for Windows
REM ============================================================================

echo.
echo ========================================================================
echo    AI-Based EMI Affordability System - Automated Setup
echo ========================================================================
echo.

REM Check Python installation
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Python is not installed or not in PATH
    echo Please install Python 3.8+ from https://www.python.org/
    pause
    exit /b 1
)

echo [1/5] Checking Python installation...
python --version
echo.

REM Create virtual environment
echo [2/5] Creating virtual environment...
if exist venv (
    echo Virtual environment already exists. Skipping...
) else (
    python -m venv venv
    echo Virtual environment created successfully!
)
echo.

REM Activate virtual environment
echo [3/5] Activating virtual environment...
call venv\Scripts\activate.bat
echo.

REM Install dependencies
echo [4/5] Installing dependencies...
echo This may take a few minutes...
pip install -r requirements.txt
if %errorlevel% neq 0 (
    echo [ERROR] Failed to install dependencies
    pause
    exit /b 1
)
echo Dependencies installed successfully!
echo.

REM Create necessary directories
echo [5/5] Ensuring directories exist...
python src\utils.py
echo.

echo ========================================================================
echo    Setup Complete!
echo ========================================================================
echo.
echo Next steps:
echo   1. Run the pipeline: python run_pipeline.py
echo   2. Launch web app: streamlit run app\streamlit_app.py
echo.
echo For detailed instructions, see QUICKSTART.md
echo.

pause
