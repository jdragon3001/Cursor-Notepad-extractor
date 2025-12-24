# Cursor Stats Dashboard - Setup Scripts

This folder contains automated setup scripts for Windows and macOS/Linux.

## Quick Start

**Windows:**
```powershell
.\setup-windows.ps1
```

**macOS/Linux:**
```bash
chmod +x setup-mac.sh
./setup-mac.sh
```

## What These Scripts Do

1. Check for Python 3.8+ and Node.js 16+
2. Create a virtual environment (isolated Python installation)
3. Install Python dependencies in the virtual environment
4. Install Node.js dependencies in the project folder
5. Verify installation
6. Create platform-specific launch script

## Why Virtual Environment?

Virtual environments keep Python packages isolated:
- Won't conflict with other Python projects
- Won't affect your system Python installation
- Safe to delete (just remove the project folder)

## After Setup

**Windows:**
```powershell
cd setup
.\launch.ps1
```

**macOS/Linux:**
```bash
cd setup
./launch.sh
```

Dashboard opens at: http://localhost:5173

## Manual Setup

If scripts don't work, see INSTALLATION.md for manual step-by-step instructions.
