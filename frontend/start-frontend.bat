@echo off
echo Starting Frontend Development Server...
echo.
echo Make sure the backend is running on http://localhost:5000
echo.
cd /d "%~dp0"
call npm run dev
pause

