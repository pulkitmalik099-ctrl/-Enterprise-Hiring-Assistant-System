@echo off
REM Enterprise Hiring Assistant System - Test Script
REM This script runs the test suite

setlocal enabledelayedexpansion

echo.
echo ========================================
echo Running Tests
echo ========================================
echo.

REM Get the directory where this script is located
set SCRIPT_DIR=%~dp0
cd /d "%SCRIPT_DIR%"

REM Check if virtual environment exists
if not exist "venv\" (
    echo [ERROR] Virtual environment not found
    echo Please run 'setup.bat' first
    pause
    exit /b 1
)

echo [*] Activating virtual environment...
call venv\Scripts\activate.bat

echo [*] Running pytest...
echo.

REM Run pytest with coverage
pytest tests/ -v --cov=app --cov-report=html --cov-report=term-missing

if errorlevel 1 (
    echo.
    echo [ERROR] Some tests failed
    pause
    exit /b 1
)

echo.
echo [✓] All tests passed!
echo [*] Coverage report available in htmlcov/index.html
echo.

endlocal
pause
