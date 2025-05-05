@echo off
echo Testing Angular Portal with Docker...

REM Build the Angular Docker image
echo Building Angular Docker image...
docker build -t angular-portal-test ./angular-portal

REM Run the container
echo Starting Angular Portal container...
docker run -d -p 4200:80 --name angular-portal-container angular-portal-test

echo Angular Portal should now be available at http://localhost:4200
echo Press any key to stop the container and cleanup...
pause

REM Cleanup
docker stop angular-portal-container
docker rm angular-portal-container