@echo off
REM ANN Stock Prediction App - Docker Build Script for Windows
REM Usage: build.bat [option]
REM Options: build, run, dev, stop, clean, logs

setlocal enabledelayedexpansion

set APP_NAME=ann-stock-app
set CONTAINER_NAME=ann-stock-prediction
set PORT=8501
set DEV_PORT=8502

REM Check if Docker is running
docker info >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Docker is not running. Please start Docker and try again.
    exit /b 1
)

if "%1"=="" goto help
if "%1"=="help" goto help
if "%1"=="--help" goto help
if "%1"=="-h" goto help
if "%1"=="build" goto build
if "%1"=="run" goto run
if "%1"=="dev" goto dev
if "%1"=="stop" goto stop
if "%1"=="clean" goto clean
if "%1"=="logs" goto logs

echo [ERROR] Unknown option: %1
goto help

:build
echo [INFO] Building ANN Stock Prediction App...
docker-compose build --no-cache
if errorlevel 1 (
    echo [ERROR] Build failed!
    exit /b 1
)
echo [SUCCESS] Build completed successfully!
goto end

:run
echo [INFO] Building and starting ANN Stock Prediction App...
docker-compose build --no-cache
if errorlevel 1 (
    echo [ERROR] Build failed!
    exit /b 1
)
docker-compose up -d
if errorlevel 1 (
    echo [ERROR] Failed to start app!
    exit /b 1
)
echo [SUCCESS] App is running at http://localhost:%PORT%
echo [INFO] Use 'docker-compose logs -f' to view logs
goto end

:dev
echo [INFO] Starting ANN Stock Prediction App in development mode...
docker-compose build --no-cache
if errorlevel 1 (
    echo [ERROR] Build failed!
    exit /b 1
)
docker-compose --profile dev up -d ann-stock-app-dev
if errorlevel 1 (
    echo [ERROR] Failed to start development app!
    exit /b 1
)
echo [SUCCESS] Development app is running at http://localhost:%DEV_PORT%
echo [INFO] Files are mounted for hot reload
goto end

:stop
echo [INFO] Stopping ANN Stock Prediction App...
docker-compose down
echo [SUCCESS] App stopped successfully!
goto end

:clean
echo [WARNING] This will remove all containers, images, and volumes for this app.
set /p confirm="Are you sure? (y/N): "
if /i "!confirm!"=="y" (
    echo [INFO] Cleaning up Docker resources...
    docker-compose down -v --rmi all --remove-orphans
    echo [SUCCESS] Cleanup completed!
) else (
    echo [INFO] Cleanup cancelled.
)
goto end

:logs
echo [INFO] Showing application logs (Ctrl+C to exit)...
docker-compose logs -f
goto end

:help
echo ANN Stock Prediction App - Docker Build Script for Windows
echo.
echo Usage: %0 [OPTION]
echo.
echo Options:
echo   build     Build the Docker image
echo   run       Build and run the application
echo   dev       Run in development mode with hot reload
echo   stop      Stop the running application
echo   clean     Remove all Docker resources for this app
echo   logs      Show application logs
echo   help      Show this help message
echo.
echo Examples:
echo   %0 run      # Build and start the app
echo   %0 dev      # Start in development mode
echo   %0 logs     # View logs
echo   %0 stop     # Stop the app
goto end

:end
endlocal
