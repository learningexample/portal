@echo off
echo Building Angular portal for Apache deployment...

cd angular-portal

REM Install dependencies if needed
call npm install

REM Build the Angular application
call npm run build -- --base-href=/angular-portal/

echo Angular portal build complete.
echo.
echo To deploy to Apache:
echo 1. Copy the contents of the 'angular-portal/dist/angular-portal' folder to your Apache htdocs/angular-portal directory
echo 2. Ensure your Apache configuration allows .htaccess files or configure URL rewriting for Angular routing
echo.
echo Your Angular portal will be available at: http://your-apache-server/angular-portal/

cd ..