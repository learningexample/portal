@echo off
setlocal enabledelayedexpansion

:: Enterprise AI Portal management script
:: Usage: run.bat [stop|build|run|restart|test|test-tabbed|test-bysection]

if "%1"=="" (
    call :restart_app
) else if "%1"=="stop" (
    call :stop_app
) else if "%1"=="build" (
    call :build_app
) else if "%1"=="run" (
    call :run_full
) else if "%1"=="restart" (
    call :restart_app
) else if "%1"=="test" (
    call :test_app
) else if "%1"=="test-tabbed" (
    call :test_tabbed_app
) else if "%1"=="test-bysection" (
    call :test_bysection_app
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

:test_app
    echo === Testing standard app locally ===
    echo Starting Python app.py...
    python app.py
    goto :eof

:test_tabbed_app
    echo === Testing tabbed version locally ===
    echo Starting Python app_bytab.py...
    python app_bytab.py
    goto :eof

:test_bysection_app
    echo === Testing collapsible sections version locally ===
    echo Starting Python app-bysection.py...
    python app-bysection.py
    goto :eof

:usage
    echo Usage: %~nx0 {stop^|build^|run^|restart^|test^|test-tabbed^|test-bysection}
    echo.
    echo Commands:
    echo   stop          - Stop all running containers
    echo   build         - Build the Docker image
    echo   run           - Stop any running containers, build, and then run the application (full deployment)
    echo   restart       - Restart the application without rebuilding (default if no command is specified)
    echo   test          - Run the standard app locally without Docker (python app.py)
    echo   test-tabbed   - Run the tabbed app locally without Docker (python app_bytab.py)
    echo   test-bysection - Run the collapsible sections app locally without Docker (python app-bysection.py)
    goto :eof

:end
endlocal