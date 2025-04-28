@echo off
setlocal enabledelayedexpansion

:: Enterprise AI Portal management script
:: Usage: run.bat [stop|build|run|restart|status|scale|test|test-tabbed|test-bysection|test-appstore]

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
) else if "%1"=="test-appstore" (
    call :test_appstore_app
) else (
    goto :usage
)

goto :end

:stop_app
    echo Stopping any running AI Portal containers...
    docker-compose down
    if %ERRORLEVEL% NEQ 0 (
        echo Error: Failed to stop containers. Is Docker running?
    ) else (
        echo All containers stopped.
    )
    goto :eof

:build_app
    echo Building AI Portal Docker image...
    docker-compose build --no-cache
    if %ERRORLEVEL% NEQ 0 (
        echo Error: Failed to build image. Check the Docker build logs.
    ) else (
        echo Build completed.
    )
    goto :eof

:run_app
    echo Starting AI Portal...
    docker-compose up -d
    if %ERRORLEVEL% NEQ 0 (
        echo Error: Failed to start containers. Check docker-compose logs.
    ) else (
        echo AI Portal is running at http://localhost:8050
    )
    goto :eof

:restart_app
    echo Restarting AI Portal...
    docker-compose restart
    if %ERRORLEVEL% NEQ 0 (
        echo Error: Failed to restart containers. Is Docker running?
    ) else (
        echo AI Portal has been restarted and is available at http://localhost:8050
    )
    goto :eof

:status_app
    echo === AI Portal Status ===
    echo Running containers:
    docker-compose ps
    if %ERRORLEVEL% NEQ 0 (
        echo Error: Docker-compose failed. Is Docker running?
        goto :eof
    )
    echo.
    echo Current connections to Apache:
    docker exec portal-apache bash -c "apachectl status | grep 'requests currently'" 2>nul
    if %ERRORLEVEL% NEQ 0 (
        echo Unable to get Apache status. Is the container running?
    )
    echo.
    echo Container resource usage:
    docker stats --no-stream --format "table {{.Name}}\t{{.CPUPerc}}\t{{.MemUsage}}\t{{.NetIO}}"
    goto :eof

:scale_info
    echo === AI Portal Scaling Information ===
    echo CPU Cores available: %NUMBER_OF_PROCESSORS%
    set /a workers=%NUMBER_OF_PROCESSORS% * 2 + 1
    echo Estimated Gunicorn workers per container: !workers!
    set /a total_workers=workers * 4
    echo Total estimated workers across all portals: !total_workers!
    echo.
    echo Estimated concurrent user capacity:
    set /a basic_capacity=workers * 4 * 10
    set /a max_capacity=workers * 4 * 20
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
    gunicorn --workers=4 --threads=2 --bind=0.0.0.0:8050 app-bysection:server
    if %ERRORLEVEL% NEQ 0 (
        echo Error: Failed to start app-bysection with Gunicorn.
        echo Trying alternative syntax...
        python -m gunicorn --workers=4 --threads=2 --bind=0.0.0.0:8050 app-bysection:server
    )
    goto :eof

:test_appstore_app
    echo === Testing app store version locally with Gunicorn ===
    echo Starting Gunicorn with app_store.py...
    gunicorn --workers=4 --threads=2 --bind=0.0.0.0:8050 app_store:server
    goto :eof

:usage
    echo Usage: %~nx0 {stop^|build^|run^|restart^|status^|scale^|test^|test-tabbed^|test-bysection^|test-appstore}
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
    echo   test-appstore - Run the app store version locally with Gunicorn
    goto :eof

:end
endlocal