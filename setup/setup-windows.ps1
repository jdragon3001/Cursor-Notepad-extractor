# Cursor Stats Dashboard - Windows Setup Script
# This script creates a virtual environment and installs all dependencies safely
# Virtual environments keep packages isolated and won't mess with your system Python!

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  Cursor Stats Dashboard - Setup" -ForegroundColor Cyan
Write-Host "  Windows Installation" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

$ErrorActionPreference = "Continue"
$ROOT_DIR = Split-Path -Parent $PSScriptRoot

# Step 1: Check Python
Write-Host "[1/7] Checking Python..." -ForegroundColor Yellow
try {
    $pythonVersion = python --version 2>&1
    Write-Host "  OK Found: $pythonVersion" -ForegroundColor Green
    
    # Check version number
    $versionMatch = $pythonVersion -match "Python (\d+)\.(\d+)"
    if ($versionMatch) {
        $major = [int]$Matches[1]
        $minor = [int]$Matches[2]
        if ($major -lt 3 -or ($major -eq 3 -and $minor -lt 8)) {
            Write-Host "  ERROR Python 3.8+ required (found $pythonVersion)" -ForegroundColor Red
            Write-Host "  Download from: https://www.python.org/downloads/" -ForegroundColor Yellow
            exit 1
        }
    }
} catch {
    Write-Host "  ERROR Python not found" -ForegroundColor Red
    Write-Host "  Download from: https://www.python.org/downloads/" -ForegroundColor Yellow
    exit 1
}

# Step 2: Check Node.js
Write-Host ""
Write-Host "[2/7] Checking Node.js..." -ForegroundColor Yellow
try {
    $nodeVersion = node --version 2>&1
    Write-Host "  OK Found Node.js: $nodeVersion" -ForegroundColor Green
    
    # Check version number
    $versionMatch = $nodeVersion -match "v(\d+)\."
    if ($versionMatch) {
        $major = [int]$Matches[1]
        if ($major -lt 16) {
            Write-Host "  ERROR Node.js 16+ required (found $nodeVersion)" -ForegroundColor Red
            Write-Host "  Download from: https://nodejs.org/" -ForegroundColor Yellow
            exit 1
        }
    }
    
    $npmVersion = npm --version 2>&1
    Write-Host "  OK Found npm: v$npmVersion" -ForegroundColor Green
} catch {
    Write-Host "  ERROR Node.js not found" -ForegroundColor Red
    Write-Host "  Download from: https://nodejs.org/" -ForegroundColor Yellow
    exit 1
}

# Step 3: Create virtual environment
Write-Host ""
Write-Host "[3/7] Creating isolated Python environment..." -ForegroundColor Yellow
Write-Host "  (This keeps packages separate from your system Python)" -ForegroundColor Gray
Push-Location $ROOT_DIR

if (Test-Path "venv") {
    Write-Host "  OK Virtual environment already exists" -ForegroundColor Green
} else {
    try {
        python -m venv venv
        if ($LASTEXITCODE -eq 0) {
            Write-Host "  OK Virtual environment created" -ForegroundColor Green
        } else {
            throw "venv creation failed"
        }
    } catch {
        Write-Host "  ERROR Failed to create virtual environment" -ForegroundColor Red
        Pop-Location
        exit 1
    }
}

# Activate virtual environment
& "$ROOT_DIR\venv\Scripts\Activate.ps1"

# Step 4: Install Python dependencies (root)
Write-Host ""
Write-Host "[4/7] Installing Python packages (stats engine)..." -ForegroundColor Yellow
try {
    pip install -r requirements.txt 2>&1 | Out-Null
    if ($LASTEXITCODE -eq 0) {
        Write-Host "  OK Python packages installed" -ForegroundColor Green
    } else {
        throw "pip install failed"
    }
} catch {
    Write-Host "  ERROR Failed to install Python packages" -ForegroundColor Red
    Write-Host "  Try running manually after activating venv" -ForegroundColor Yellow
    Pop-Location
    exit 1
}

# Step 5: Install backend dependencies
Write-Host ""
Write-Host "[5/7] Installing backend packages (FastAPI)..." -ForegroundColor Yellow
try {
    pip install -r backend\requirements.txt 2>&1 | Out-Null
    if ($LASTEXITCODE -eq 0) {
        Write-Host "  OK Backend packages installed" -ForegroundColor Green
    } else {
        throw "pip install failed"
    }
} catch {
    Write-Host "  ERROR Failed to install backend packages" -ForegroundColor Red
    Pop-Location
    exit 1
}

# Step 6: Install frontend dependencies
Write-Host ""
Write-Host "[6/7] Installing frontend packages (React)..." -ForegroundColor Yellow
Write-Host "  This may take a few minutes..." -ForegroundColor Gray
Push-Location "$ROOT_DIR\frontend"
try {
    npm install 2>&1 | Out-Null
    if ($LASTEXITCODE -eq 0) {
        Write-Host "  OK Frontend packages installed" -ForegroundColor Green
    } else {
        throw "npm install failed"
    }
} catch {
    Write-Host "  ERROR Failed to install frontend packages" -ForegroundColor Red
    Write-Host "  Try running manually: cd frontend && npm install" -ForegroundColor Yellow
    Pop-Location
    Pop-Location
    exit 1
}
Pop-Location

# Step 7: Verify installation
Write-Host ""
Write-Host "[7/7] Verifying installation..." -ForegroundColor Yellow
$allGood = $true

# Check Python packages (still in venv)
try {
    python -c "import numpy, fastapi, uvicorn" 2>&1 | Out-Null
    if ($LASTEXITCODE -eq 0) {
        Write-Host "  OK Python packages verified" -ForegroundColor Green
    } else {
        throw "Import failed"
    }
} catch {
    Write-Host "  ERROR Python packages not working" -ForegroundColor Red
    $allGood = $false
}

# Check frontend packages
if (Test-Path "$ROOT_DIR\frontend\node_modules\react") {
    Write-Host "  OK Frontend packages verified" -ForegroundColor Green
} else {
    Write-Host "  ERROR Frontend packages not found" -ForegroundColor Red
    $allGood = $false
}

# Deactivate venv
deactivate

# Create launch script in setup folder
$launchScript = @"
# Cursor Stats Dashboard Launcher
# Activate virtual environment and launch dashboard
`$ROOT = Split-Path -Parent `$PSScriptRoot
Push-Location `$ROOT
& "venv\Scripts\Activate.ps1"
python launch_dashboard.py
Pop-Location
"@
$launchScript | Out-File -FilePath "$PSScriptRoot\launch.ps1" -Encoding UTF8

Pop-Location

# Final message
Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
if ($allGood) {
    Write-Host "  Setup Complete!" -ForegroundColor Green
    Write-Host "========================================" -ForegroundColor Cyan
    Write-Host ""
    Write-Host "  OK Virtual environment created (safe and isolated)" -ForegroundColor Cyan
    Write-Host "  OK All packages installed" -ForegroundColor Cyan
    Write-Host "  OK Ready to use!" -ForegroundColor Cyan
    Write-Host ""
    Write-Host "To launch the dashboard:" -ForegroundColor Yellow
    Write-Host "  cd setup" -ForegroundColor Cyan
    Write-Host "  .\launch.ps1" -ForegroundColor Cyan
    Write-Host ""
    Write-Host "  Or manually:" -ForegroundColor White
    Write-Host "  cd .." -ForegroundColor Cyan
    Write-Host "  venv\Scripts\Activate.ps1" -ForegroundColor Cyan
    Write-Host "  python launch_dashboard.py" -ForegroundColor Cyan
    Write-Host ""
    Write-Host "The dashboard will open at http://localhost:5173" -ForegroundColor Gray
} else {
    Write-Host "  Setup Had Issues" -ForegroundColor Yellow
    Write-Host "========================================" -ForegroundColor Cyan
    Write-Host ""
    Write-Host "Some packages may not be installed correctly." -ForegroundColor Yellow
    Write-Host "See INSTALLATION.md for manual setup steps" -ForegroundColor Yellow
}
Write-Host ""
