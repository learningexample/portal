@echo off
setlocal enabledelayedexpansion

echo AI Portal Test Runner
echo ====================

if "%1"=="" (
    echo Usage: test.bat [command]
    echo.
    echo Available commands:
    echo   build    - Build test Docker images
    echo   up       - Start test environment
    echo   down     - Stop test environment
    echo   run      - Build and start test environment
    echo   test     - Run all automated tests
    echo   e2e      - Run end-to-end tests
    echo   unit     - Run unit tests
    echo   stop     - Stop and remove all containers
    echo   logs     - View container logs
    echo   shell    - Open shell in portal container
    exit /b 0
)

set command=%1

if "%command%"=="build" (
    echo Building test Docker images...
    docker-compose -f docker-compose.test.yml build
    echo Build complete.
    exit /b 0
)

if "%command%"=="up" (
    echo Starting test environment...
    docker-compose -f docker-compose.test.yml up -d
    echo.
    echo Test environment is running at http://localhost:8051
    echo.
    echo Test dashboard available at:
    echo - Standard version: http://localhost:8051/portal-1/
    exit /b 0
)

if "%command%"=="down" (
    echo Stopping test environment...
    docker-compose -f docker-compose.test.yml down
    exit /b 0
)

if "%command%"=="run" (
    echo Building and starting test environment...
    docker-compose -f docker-compose.test.yml up --build -d
    echo.
    echo Test environment is running at http://localhost:8051
    echo.
    echo Test dashboard available at:
    echo - Standard version: http://localhost:8051/portal-1/
    exit /b 0
)

if "%command%"=="test" (
    echo Running all tests...
    docker exec -it ai-portal-test python -m pytest -xvs
    exit /b 0
)

if "%command%"=="e2e" (
    echo Running end-to-end tests...
    docker exec -it ai-portal-test python -m pytest test_portal_e2e.py -xvs
    exit /b 0
)

if "%command%"=="unit" (
    echo Running unit tests...
    docker exec -it ai-portal-test python -m pytest test_portal.py -xvs
    exit /b 0
)

if "%command%"=="stop" (
    echo Stopping all test containers...
    docker-compose -f docker-compose.test.yml down
    exit /b 0
)

if "%command%"=="logs" (
    echo Viewing test container logs...
    docker-compose -f docker-compose.test.yml logs -f
    exit /b 0
)

if "%command%"=="shell" (
    echo Opening shell in portal test container...
    docker exec -it ai-portal-test /bin/bash
    exit /b 0
)

echo Unknown command: %command%
echo Run 'test.bat' without arguments to see available commands.
exit /b 1