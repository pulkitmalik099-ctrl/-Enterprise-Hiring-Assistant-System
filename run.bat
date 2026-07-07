@echo off
REM Enterprise Hiring Assistant System - Setup and Run Script
REM This script automates the setup and launch of the application

setlocal enabledelayedexpansion

echo.
echo ========================================
echo Enterprise Hiring Assistant System
echo ========================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python is not installed or not in PATH
    echo Please install Python 3.10+ from https://www.python.org/
    pause
    exit /b 1
)

REM Check if Docker is installed
docker --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Docker is not installed or not in PATH
    echo Please install Docker Desktop from https://www.docker.com/products/docker-desktop
    pause
    exit /b 1
)

REM Get the directory where this script is located
set SCRIPT_DIR=%~dp0
cd /d "%SCRIPT_DIR%"

echo [1] Checking virtual environment...
if not exist "venv\" (
    echo [*] Creating virtual environment...
    python -m venv venv
    if errorlevel 1 (
        echo [ERROR] Failed to create virtual environment
        pause
        exit /b 1
    )
    echo [✓] Virtual environment created
) else (
    echo [✓] Virtual environment already exists
)

echo.
echo [2] Activating virtual environment...
call venv\Scripts\activate.bat
if errorlevel 1 (
    echo [ERROR] Failed to activate virtual environment
    pause
    exit /b 1
)
echo [✓] Virtual environment activated

echo.
echo [3] Installing dependencies...
pip install -q -r requirements.txt
if errorlevel 1 (
    echo [ERROR] Failed to install dependencies
    pause
    exit /b 1
)
echo [✓] Dependencies installed

echo.
echo [4] Setting up environment configuration...
if not exist ".env" (
    if exist ".env.example" (
        copy .env.example .env >nul
        echo [*] Created .env from .env.example
        echo.
        echo [!] IMPORTANT: Update your API keys in .env file:
        echo    - ANTHROPIC_API_KEY=your_actual_key_here
        echo    - OPENAI_API_KEY=your_actual_key_here (if using OpenAI)
        echo.
        echo Do you want to edit .env now? (Y/N)
        set /p EDIT_ENV=
        if /i "!EDIT_ENV!"=="Y" (
            notepad .env
        )
    )
) else (
    echo [✓] .env file already exists
)

echo.
echo [5] Starting Docker services...
echo [*] Starting PostgreSQL and Redis...
docker-compose up -d
if errorlevel 1 (
    echo [ERROR] Failed to start Docker services
    echo Make sure Docker Desktop is running
    pause
    exit /b 1
)
echo [✓] Docker services started

REM Wait for services to be ready
echo [*] Waiting for services to be ready...
timeout /t 5 /nobreak

echo.
echo ========================================
echo Starting Application...
echo ========================================
echo.
echo [✓] Application is starting...
echo [*] API Documentation: http://localhost:8000/api/docs
echo [*] ReDoc: http://localhost:8000/api/redoc
echo.
echo Press Ctrl+C to stop the server
echo.

REM Run the application
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

REM Cleanup on exit
echo.
echo [*] Application stopped
echo [*] Stopping Docker services...
docker-compose down
echo [✓] Docker services stopped

endlocal
