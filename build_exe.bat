@echo off
echo ========================================
echo  Building Cursor Note Search Executable
echo ========================================
echo.

REM Check if we're in the right directory
if not exist "note_search_gui.py" (
    echo Error: This script must be run from the project directory
    echo Make sure you're in the folder containing note_search_gui.py
    pause
    exit /b 1
)

REM Check if conda environment exists
call conda activate cursor-notepad-browser 2>nul
if %errorlevel% neq 0 (
    echo Error: cursor-notepad-browser environment not found
    echo Please run setup_for_new_computer.bat first
    pause
    exit /b 1
)

echo Environment activated successfully!
echo.

REM Check if PyInstaller is installed
python -c "import PyInstaller" 2>nul
if %errorlevel% neq 0 (
    echo PyInstaller not found. Installing...
    pip install pyinstaller
    if %errorlevel% neq 0 (
        echo Error: Failed to install PyInstaller
        pause
        exit /b 1
    )
)

echo Building executable with PyInstaller...
echo This may take 2-3 minutes...
echo.

REM Clean previous builds
if exist "build" (
    echo Cleaning previous build...
    rmdir /s /q build
)

if exist "dist" (
    echo Cleaning previous dist...
    rmdir /s /q dist
)

REM Build the executable
pyinstaller cursor_note_search.spec

if %errorlevel% neq 0 (
    echo.
    echo Error: Build failed!
    echo Check the output above for details.
    pause
    exit /b 1
)

echo.
echo ========================================
echo  Build Complete!
echo ========================================
echo.

REM Check if executable was created
if exist "dist\CursorNoteSearch.exe" (
    echo Executable created successfully:
    echo Location: dist\CursorNoteSearch.exe
    
    REM Get file size
    for %%I in ("dist\CursorNoteSearch.exe") do echo Size: %%~zI bytes (~16MB)
    echo.
    echo Ready for distribution!
    echo.
    
    REM Ask if user wants to test
    set /p test_exe="Test the executable now? (y/n): "
    if /i "%test_exe%"=="y" (
        echo Launching executable...
        start "" "dist\CursorNoteSearch.exe"
    )
) else (
    echo Error: Executable was not created!
    echo Check the build output for errors.
)

echo.
echo Press any key to exit...
pause >nul 