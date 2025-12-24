# Cursor Stats Dashboard Launcher
# Activate virtual environment and launch dashboard
$ROOT = Split-Path -Parent $PSScriptRoot
Push-Location $ROOT
& "venv\Scripts\Activate.ps1"
python launch_dashboard.py
Pop-Location
