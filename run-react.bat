@echo off
REM Batch script to run only the React version of the AI Portal

REM Stop any existing containers from the react compose file
docker-compose -f docker-compose.react.yml down

REM Build and start the React portal services
docker-compose -f docker-compose.react.yml up -d

REM Display status
echo React Portal is starting...
echo Frontend will be accessible at: http://localhost:3000
echo API will be accessible at: http://localhost:8050
echo.
echo To view logs: docker-compose -f docker-compose.react.yml logs -f
echo To stop services: docker-compose -f docker-compose.react.yml down