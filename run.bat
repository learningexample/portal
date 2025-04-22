@echo off
setlocal enabledelayedexpansion

:: Enterprise AI Portal management script
:: Usage: run.bat [stop|build|run|restart]

if "%1"=="" (
    goto :usage
) else if "%1"=="stop" (
    call :stop_app
) else if "%1"=="build" (
    call :build_app
) else if "%1"=="run" (
    call :run_full
) else if "%1"=="restart" (
    call :restart_app
) else (
    goto :usage
)

goto :end

:stop_app
    echo Stopping any running AI Portal containers...
    docker-compose down
    echo All containers stopped.
    goto :eof

:build_app
    echo Building AI Portal Docker image...
    docker-compose build
    echo Build completed.
    goto :eof

:run_app
    echo Starting AI Portal...
    docker-compose up -d
    echo AI Portal is running at http://localhost:8050
    goto :eof

:restart_app
    echo Restarting AI Portal...
    docker-compose restart
    echo AI Portal has been restarted and is available at http://localhost:8050
    goto :eof

:run_full
    echo === Performing full deployment process ===
    call :stop_app
    call :build_app
    call :run_app
    echo === Full deployment completed ===
    goto :eof

:usage
    echo Usage: %~nx0 {stop^|build^|run^|restart}
    echo.
    echo Commands:
    echo   stop     - Stop all running containers
    echo   build    - Build the Docker image
    echo   run      - Stop any running containers, build, and then run the application (full deployment)
    echo   restart  - Restart the application without rebuilding
    echo.
    echo To run locally without Docker, use: python app.py
    goto :eof

:end
endlocal