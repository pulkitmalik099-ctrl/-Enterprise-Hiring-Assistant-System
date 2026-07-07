@echo off
REM Enterprise Hiring Assistant - Frontend Development Server
REM This script starts the React development server

setlocal enabledelayedexpansion

echo.
echo ========================================
echo Enterprise Hiring Assistant - Frontend
echo ========================================
echo.

REM Check if Node.js is installed
node --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Node.js is not installed or not in PATH
    echo Please install Node.js from https://nodejs.org/
    pause
    exit /b 1
)

echo [1] Checking dependencies...
if not exist "node_modules\" (
    echo [*] Installing dependencies...
    call npm install
    if errorlevel 1 (
        echo [ERROR] Failed to install dependencies
        pause
        exit /b 1
    )
    echo [✓] Dependencies installed
) else (
    echo [✓] Dependencies already installed
)

echo.
echo ========================================
echo Starting Development Server
echo ========================================
echo.
echo [*] Starting React development server...
echo [*] Frontend: http://localhost:3000
echo [*] Backend: http://localhost:8000
echo.
echo Press Ctrl+C to stop the server
echo.

REM Start the development server
call npm start

endlocal
