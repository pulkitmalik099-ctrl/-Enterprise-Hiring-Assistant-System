@echo off
REM Enterprise Hiring Assistant System - Setup Only Script
REM This script sets up the environment without running the application

setlocal enabledelayedexpansion

echo.
echo ========================================
echo Enterprise Hiring Assistant Setup
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
echo [2] Installing dependencies...
call venv\Scripts\activate.bat
pip install -q -r requirements.txt
if errorlevel 1 (
    echo [ERROR] Failed to install dependencies
    pause
    exit /b 1
)
echo [✓] Dependencies installed

echo.
echo [3] Setting up environment configuration...
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
echo [✓] Setup complete!
echo.
echo Next steps:
echo 1. Update your API keys in the .env file
echo 2. Run 'run.bat' to start the application
echo.

endlocal
pause
