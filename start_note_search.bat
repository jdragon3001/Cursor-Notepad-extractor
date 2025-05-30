@echo off
echo Starting Cursor Note Search GUI...
echo.

REM Check if conda is available
where conda >nul 2>&1
if %errorlevel% neq 0 (
    echo Error: Conda is not installed or not in PATH
    echo Please install Miniconda or Anaconda first
    echo Download from: https://docs.conda.io/en/latest/miniconda.html
    pause
    exit /b 1
)

echo Checking for conda environment...

REM Try to activate the preferred environment name
call conda activate cursor-notepad-browser 2>nul
if %errorlevel% equ 0 (
    echo Using existing cursor-notepad-browser environment
    goto :run_app
)

REM If that doesn't exist, try alternative names
call conda activate cursor-notes 2>nul
if %errorlevel% equ 0 (
    echo Using existing cursor-notes environment
    goto :run_app
)

call conda activate cursor 2>nul
if %errorlevel% equ 0 (
    echo Using existing cursor environment
    goto :run_app
)

REM If no suitable environment exists, create one
echo No suitable conda environment found. Creating new environment...
echo This will take a few minutes the first time.
echo.

call conda create -n cursor-notepad-browser python=3.10 -y
if %errorlevel% neq 0 (
    echo Error: Failed to create conda environment
    pause
    exit /b 1
)

call conda activate cursor-notepad-browser
if %errorlevel% neq 0 (
    echo Error: Failed to activate new environment
    pause
    exit /b 1
)

echo Installing dependencies...
pip install reportlab python-docx
if %errorlevel% neq 0 (
    echo Warning: Failed to install optional dependencies (PDF/DOCX export may not work)
)

:run_app
echo Environment ready!
echo Launching note search GUI...
echo.

python note_search_gui.py

if %errorlevel% neq 0 (
    echo.
    echo Error running the application. Check the console output above.
    echo.
    echo Troubleshooting tips:
    echo - Make sure you're in the correct directory
    echo - Check that all required files are present
    echo - Verify Cursor is installed and has workspace data
    pause
) 