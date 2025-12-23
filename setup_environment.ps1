# Cursor Stats Dashboard - Environment Setup Script
# Run this script once to set up the development environment

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Cursor Stats - Environment Setup" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

$ErrorActionPreference = "Stop"

# Check if conda is available
Write-Host "Checking for conda..." -ForegroundColor Yellow
try {
    $condaVersion = conda --version
    Write-Host "✓ Found: $condaVersion" -ForegroundColor Green
} catch {
    Write-Host "✗ Conda not found. Please install Miniconda or Anaconda first." -ForegroundColor Red
    exit 1
}

Write-Host ""

# Check if environment already exists
Write-Host "Checking for existing cursor-extractor environment..." -ForegroundColor Yellow
$envExists = conda env list | Select-String "cursor-extractor"

if ($envExists) {
    Write-Host "✓ Environment 'cursor-extractor' already exists" -ForegroundColor Green
    $response = Read-Host "Do you want to recreate it? (y/N)"
    if ($response -eq 'y' -or $response -eq 'Y') {
        Write-Host "Removing existing environment..." -ForegroundColor Yellow
        conda env remove -n cursor-extractor -y
        Write-Host "✓ Environment removed" -ForegroundColor Green
    } else {
        Write-Host "Skipping environment creation" -ForegroundColor Yellow
        $skipCreate = $true
    }
}

# Create conda environment
if (-not $skipCreate) {
    Write-Host ""
    Write-Host "Creating conda environment 'cursor-extractor' with Python 3.11..." -ForegroundColor Yellow
    conda create -n cursor-extractor python=3.11 -y
    Write-Host "✓ Environment created" -ForegroundColor Green
}

Write-Host ""

# Activate and install Python dependencies
Write-Host "Installing Python dependencies..." -ForegroundColor Yellow
Write-Host "  - Root level packages (numpy, streamlit, etc.)..." -ForegroundColor Gray

$installScript = @"
conda activate cursor-extractor
pip install -r requirements.txt
pip install -r backend\requirements.txt
"@

# Run pip installs in a subprocess to ensure conda activation works
$process = Start-Process powershell -ArgumentList "-Command", $installScript -Wait -PassThru -NoNewWindow

if ($process.ExitCode -eq 0) {
    Write-Host "✓ Python dependencies installed" -ForegroundColor Green
} else {
    Write-Host "✗ Failed to install Python dependencies" -ForegroundColor Red
    exit 1
}

Write-Host ""

# Check for Node.js/npm
Write-Host "Checking for npm..." -ForegroundColor Yellow
try {
    $npmVersion = npm --version
    Write-Host "✓ Found npm version: $npmVersion" -ForegroundColor Green
} catch {
    Write-Host "✗ npm not found. Please install Node.js first." -ForegroundColor Red
    exit 1
}

Write-Host ""

# Install frontend dependencies
Write-Host "Installing frontend dependencies..." -ForegroundColor Yellow
Push-Location frontend
try {
    npm install
    Write-Host "✓ Frontend dependencies installed" -ForegroundColor Green
} catch {
    Write-Host "✗ Failed to install frontend dependencies" -ForegroundColor Red
    Pop-Location
    exit 1
}
Pop-Location

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Setup Complete! 🎉" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Next steps:" -ForegroundColor Yellow
Write-Host "  1. Activate the environment: " -NoNewline -ForegroundColor Gray
Write-Host "conda activate cursor-extractor" -ForegroundColor White
Write-Host "  2. Run the dashboard: " -NoNewline -ForegroundColor Gray
Write-Host ".\deploy.ps1" -ForegroundColor White
Write-Host ""
Write-Host "For more commands, see cmds.md" -ForegroundColor Gray
Write-Host ""

