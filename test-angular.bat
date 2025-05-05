@echo off
echo Testing Angular Portal...

cd angular-portal

REM Check if Node.js is installed
where node >nul 2>nul
if %ERRORLEVEL% neq 0 (
    echo Error: Node.js is not installed or not in PATH. Please install Node.js and try again.
    exit /b 1
)

REM Check if npm is installed
where npm >nul 2>nul
if %ERRORLEVEL% neq 0 (
    echo Error: npm is not installed or not in PATH. Please install npm and try again.
    exit /b 1
)

echo Running Angular development server using npx...
call npm run dev

cd ..