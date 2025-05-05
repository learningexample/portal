@echo off
echo Building React portal for Apache deployment...

cd react-portal

REM Install dependencies if needed
call npm install

REM Build the React application with correct base path
call npm run build -- --public-url=/react-portal/

echo React portal build complete.
echo.
echo To deploy to Apache:
echo 1. Copy the contents of the 'react-portal/build' folder to your Apache htdocs/react-portal directory
echo 2. Add an .htaccess file in the root with the following content:
echo    Options -MultiViews
echo    RewriteEngine On
echo    RewriteCond %%{REQUEST_FILENAME} !-f
echo    RewriteRule ^ index.html [QSA,L]
echo.
echo Your React portal will be available at: http://your-apache-server/react-portal/

cd ..