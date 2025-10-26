@echo off
REM Wanggan GPS GUI Launcher for Windows
REM Double-click this file to launch the GUI interface

echo.
echo ========================================
echo   Wanggan GPS Data Downloader
echo ========================================
echo.
echo Starting GUI interface...
echo.

REM Check if Python is available
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python 3.8 or higher from python.org
    echo.
    pause
    exit /b 1
)

REM Check if easygui is installed
python -c "import easygui" >nul 2>&1
if errorlevel 1 (
    echo Installing required GUI library...
    pip install easygui
    echo.
)

REM Launch the GUI
python wanggan_gps_gui.py

if errorlevel 1 (
    echo.
    echo An error occurred while running the GUI.
    echo.
    pause
)
