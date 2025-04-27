@echo off
setlocal enabledelayedexpansion

:: Enterprise AI Portal management script
:: Usage: run.bat [stop|build|run|restart|status|scale|test|test-tabbed|test-bysection]

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
) else if "%1"=="status" (
    call :status_app
) else if "%1"=="scale" (
    call :scale_info
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

:status_app
    echo === AI Portal Status ===
    echo Running containers:
    docker-compose ps
    echo.
    echo Current connections to Apache:
    docker exec portal-apache cmd /c "apachectl status | findstr "requests currently""
    echo.
    echo Container resource usage:
    docker stats --no-stream --format "table {{.Name}}\t{{.CPUPerc}}\t{{.MemUsage}}"
    goto :eof

:scale_info
    echo === AI Portal Scaling Information ===
    echo CPU Cores available: %NUMBER_OF_PROCESSORS%
    echo Estimated Gunicorn workers per container: !workers!
    set /a workers=%NUMBER_OF_PROCESSORS% * 2 + 1
    echo Estimated Gunicorn workers per container: !workers!
    set /a total_workers=workers * 3
    echo Total estimated workers across all portals: !total_workers!
    echo.
    echo Estimated concurrent user capacity:
    set /a basic_capacity=workers * 3 * 10
    set /a max_capacity=workers * 3 * 20
    echo - Basic capacity: ~!basic_capacity! users
    echo - Maximum capacity: ~!max_capacity! users
    echo.
    echo Current container limits (from docker-compose.yml):
    findstr /C:"cpus" /C:"memory" docker-compose.yml
    goto :eof

:run_full
    echo === Performing full deployment process ===
    call :stop_app
    call :build_app
    call :run_app
    echo === Full deployment completed ===
    goto :eof

:test_app
    echo === Testing standard app locally with Gunicorn ===
    echo Starting Gunicorn with app.py...
    gunicorn --workers=4 --threads=2 --bind=0.0.0.0:8050 app:server
    goto :eof

:test_tabbed_app
    echo === Testing tabbed version locally with Gunicorn ===
    echo Starting Gunicorn with app_bytab.py...
    gunicorn --workers=4 --threads=2 --bind=0.0.0.0:8050 app_bytab:server
    goto :eof

:test_bysection_app
    echo === Testing collapsible sections version locally with Gunicorn ===
    echo Starting Gunicorn with app-bysection.py...
    gunicorn --workers=4 --threads=2 --bind=0.0.0.0:8050 "app-bysection:server"
    goto :eof

:usage
    echo Usage: %~nx0 {stop^|build^|run^|restart^|status^|scale^|test^|test-tabbed^|test-bysection}
    echo.
    echo Commands:
    echo   stop          - Stop all running containers
    echo   build         - Build the Docker image
    echo   run           - Stop any running containers, build, and then run the application (full deployment)
    echo   restart       - Restart the application without rebuilding (default if no command is specified)
    echo   status        - Show current status, connections, and resource usage
    echo   scale         - Show information about scaling capabilities
    echo   test          - Run the standard app locally with Gunicorn
    echo   test-tabbed   - Run the tabbed app locally with Gunicorn
    echo   test-bysection - Run the collapsible sections app locally with Gunicorn
    goto :eof

:end
endlocal