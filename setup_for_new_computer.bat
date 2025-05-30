@echo off
echo ========================================
echo  Cursor Note Search GUI - First Time Setup
echo ========================================
echo.

REM Check if we're in the right directory
if not exist "note_search_gui.py" (
    echo Error: This script must be run from the Cursor Notepad extractor directory
    echo Make sure you're in the folder containing note_search_gui.py
    pause
    exit /b 1
)

REM Check if conda is available
where conda >nul 2>&1
if %errorlevel% neq 0 (
    echo Error: Conda is not installed or not in PATH
    echo.
    echo Please install Miniconda first:
    echo 1. Go to: https://docs.conda.io/en/latest/miniconda.html
    echo 2. Download Miniconda3 for Windows
    echo 3. Install it (add to PATH when prompted)
    echo 4. Restart your command prompt
    echo 5. Run this script again
    echo.
    pause
    exit /b 1
)

echo Found conda installation. Setting up environment...
echo.

REM Create conda environment
echo Creating cursor-notepad-browser environment...
call conda create -n cursor-notepad-browser python=3.10 -y
if %errorlevel% neq 0 (
    echo Error: Failed to create conda environment
    pause
    exit /b 1
)

REM Activate environment
echo Activating environment...
call conda activate cursor-notepad-browser
if %errorlevel% neq 0 (
    echo Error: Failed to activate environment
    pause
    exit /b 1
)

REM Install dependencies
echo Installing dependencies for PDF/DOCX export...
pip install reportlab python-docx
if %errorlevel% neq 0 (
    echo Warning: Failed to install optional dependencies
    echo The app will still work but PDF/DOCX export may not be available
)

echo.
echo ========================================
echo  Setup Complete!
echo ========================================
echo.
echo The Cursor Note Search GUI is now ready to use.
echo.
echo To run the application:
echo 1. Double-click "start_note_search.bat"
echo 2. Or run: python note_search_gui.py
echo.
echo The application will automatically:
echo - Find your Cursor workspace databases
echo - Extract and parse your notes
echo - Provide a searchable interface
echo.
echo Press any key to launch the application now...
pause >nul

python note_search_gui.py 