@echo off
chcp 65001 >nul
setlocal enabledelayedexpansion

:: Ask for port
set /p PORT=Enter port: 

echo ================================
echo Searching for processes on port %PORT%...
echo ================================

:: Find PIDs for the given port
for /f "tokens=5" %%a in ('netstat -ano ^| findstr ":%PORT%"') do (
    set PID=%%a
    if !PID! NEQ 0 (
        echo Found PID: !PID!
        echo Killing process !PID!...
        taskkill /PID !PID! /F >nul 2>&1
        if errorlevel 1 (
            echo [ERROR] Could not kill process !PID!
        ) else (
            echo [OK] Process !PID! killed.
        )
    )
)

echo ================================
echo Done.
pause
