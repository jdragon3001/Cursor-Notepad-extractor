# Cursor Stats Dashboard - Deployment Script
# This script starts both the FastAPI backend and React frontend

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Cursor Stats Dashboard - Starting..." -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Store the root directory
$ROOT_DIR = $PSScriptRoot

# Function to check if a process is running on a port
function Test-PortInUse {
    param($Port)
    $connections = Get-NetTCPConnection -LocalPort $Port -ErrorAction SilentlyContinue
    return $connections.Count -gt 0
}

# Function to kill process on a port
function Stop-ProcessOnPort {
    param($Port)
    $connections = Get-NetTCPConnection -LocalPort $Port -ErrorAction SilentlyContinue
    foreach ($conn in $connections) {
        $process = Get-Process -Id $conn.OwningProcess -ErrorAction SilentlyContinue
        if ($process) {
            Write-Host "Killing process $($process.Name) (PID: $($process.Id)) on port $Port" -ForegroundColor Yellow
            Stop-Process -Id $process.Id -Force -ErrorAction SilentlyContinue
        }
    }
}

# Check and clean up ports if needed
Write-Host "Checking ports..." -ForegroundColor Yellow
if (Test-PortInUse 8000) {
    Write-Host "Port 8000 (Backend) is in use. Cleaning up..." -ForegroundColor Yellow
    Stop-ProcessOnPort 8000
    Start-Sleep -Seconds 2
}
if (Test-PortInUse 5173) {
    Write-Host "Port 5173 (Frontend) is in use. Cleaning up..." -ForegroundColor Yellow
    Stop-ProcessOnPort 5173
    Start-Sleep -Seconds 2
}

Write-Host ""
Write-Host "Starting Backend (FastAPI on port 8000)..." -ForegroundColor Green

# Start backend in a new PowerShell window
$backendScript = @"
cd '$ROOT_DIR\backend'
conda activate cursor-notepad-browser
Write-Host 'Backend: Activating conda environment...' -ForegroundColor Green
Write-Host 'Backend: Starting FastAPI server on http://127.0.0.1:8000' -ForegroundColor Green
python main.py
"@

Start-Process powershell -ArgumentList "-NoExit", "-Command", $backendScript

Write-Host "Backend started in new window" -ForegroundColor Green
Write-Host ""

# Wait a moment for backend to start
Write-Host "Waiting for backend to initialize..." -ForegroundColor Yellow
Start-Sleep -Seconds 3

Write-Host ""
Write-Host "Starting Frontend (React on port 5173)..." -ForegroundColor Green

# Start frontend in a new PowerShell window
$frontendScript = @"
cd '$ROOT_DIR\frontend'
Write-Host 'Frontend: Starting Vite dev server on http://localhost:5173' -ForegroundColor Green
npm run dev
"@

Start-Process powershell -ArgumentList "-NoExit", "-Command", $frontendScript

Write-Host "Frontend started in new window" -ForegroundColor Green
Write-Host ""

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Dashboard is starting up!" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Backend API:  http://127.0.0.1:8000" -ForegroundColor Yellow
Write-Host "Frontend UI:  http://localhost:5173" -ForegroundColor Yellow
Write-Host ""
Write-Host "Press Ctrl+C in each window to stop the servers" -ForegroundColor Gray
Write-Host ""

