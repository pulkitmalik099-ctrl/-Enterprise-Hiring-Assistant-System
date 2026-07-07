@echo off
REM Local Database Cleanup Script
REM This script stops and removes PostgreSQL and Redis containers

setlocal enabledelayedexpansion

echo.
echo ========================================
echo Local Database Cleanup
echo ========================================
echo.

echo [1] Stopping PostgreSQL container...
docker stop hiring-postgres 2>nul
if %errorlevel% equ 0 (
    echo [✓] PostgreSQL stopped
) else (
    echo [!] PostgreSQL not running
)

echo.
echo [2] Stopping Redis container...
docker stop hiring-redis 2>nul
if %errorlevel% equ 0 (
    echo [✓] Redis stopped
) else (
    echo [!] Redis not running
)

echo.
echo [3] Options:
echo    a) Keep containers (for later restart)
echo    b) Remove containers (clean slate)
echo.
set /p choice="Enter choice (a/b): "

if /i "%choice%"=="b" (
    echo.
    echo [*] Removing containers...
    docker rm hiring-postgres 2>nul
    docker rm hiring-redis 2>nul

    echo [?] Remove data volumes as well? (y/n)
    set /p remove_volumes="Enter choice: "

    if /i "%remove_volumes%"=="y" (
        echo [*] Removing data volumes...
        docker volume rm postgres_data 2>nul
        echo [✓] Volumes removed
    )

    echo [✓] Containers removed
) else (
    echo [✓] Containers stopped (not removed)
    echo    You can restart them with: docker start hiring-postgres hiring-redis
)

echo.
echo ========================================
echo Cleanup Complete!
echo ========================================
echo.

pause
