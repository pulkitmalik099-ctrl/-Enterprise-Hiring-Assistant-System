@echo off
REM Enterprise Hiring Assistant System - Stop Script
REM This script stops the application and Docker services

setlocal enabledelayedexpansion

echo.
echo Stopping Enterprise Hiring Assistant System...
echo.

REM Get the directory where this script is located
set SCRIPT_DIR=%~dp0
cd /d "%SCRIPT_DIR%"

echo [*] Stopping Docker services...
docker-compose down

if errorlevel 1 (
    echo [ERROR] Failed to stop Docker services
    pause
    exit /b 1
)

echo [✓] All services stopped successfully
echo.

endlocal
