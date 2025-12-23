# Command Reference

## Environment Setup

### Initial Setup (One-time)
```powershell
# Create conda environment with Python 3.11
conda create -n cursor-extractor python=3.11 -y

# Activate environment
conda activate cursor-extractor

# Install Python dependencies (root level)
pip install -r requirements.txt

# Install backend dependencies
pip install -r backend\requirements.txt

# Install frontend dependencies
cd frontend
npm install
cd ..
```

### Activate Environment
```powershell
conda activate cursor-extractor
```

## Running the Application

### Deploy Full Stack (Recommended)
```powershell
# Make sure you're in the project root and conda env is activated
.\deploy.ps1
```

This will:
- Clean up any processes on ports 8000 and 5173
- Start FastAPI backend on http://127.0.0.1:8000
- Start React frontend on http://localhost:5173
- Open both in separate PowerShell windows

### Manual Start (Alternative)

#### Backend Only
```powershell
cd backend
python main.py
```
Runs on: http://127.0.0.1:8000

#### Frontend Only
```powershell
cd frontend
npm run dev
```
Runs on: http://localhost:5173

## Development Commands

### Frontend
```powershell
cd frontend

# Start development server
npm run dev

# Build for production
npm run build

# Preview production build
npm run preview

# Lint code
npm run lint
```

### Backend
```powershell
cd backend

# Start FastAPI server (main.py handles this)
python main.py

# For development with auto-reload
uvicorn main:app --reload --host 127.0.0.1 --port 8000
```

## Testing & Exploration Scripts

### Stats Pipeline Testing
```powershell
python test_stats_pipeline.py
python test_tool_stats.py
```

### Data Exploration
```powershell
cd scripts\exploration

# Comprehensive data explorer
python comprehensive_data_explorer.py

# Explore specific data sources
python explore_cursorDiskKV.py
python explore_daily_stats.py
python explore_workspaces.py
```

### Validation Scripts
```powershell
cd scripts\validation
# Various validation scripts available
```

## Conda Environment Management

### List all environments
```powershell
conda env list
```

### Deactivate current environment
```powershell
conda deactivate
```

### Remove environment (if needed)
```powershell
conda env remove -n cursor-extractor
```

### Export environment
```powershell
conda env export > environment.yml
```

## Troubleshooting

### Port Already in Use
If ports 8000 or 5173 are already in use:
```powershell
# Check what's using the port
Get-NetTCPConnection -LocalPort 8000
Get-NetTCPConnection -LocalPort 5173

# Kill process by PID
Stop-Process -Id <PID> -Force
```

### Clear npm cache
```powershell
cd frontend
npm cache clean --force
rm -r node_modules
npm install
```

### Reinstall Python packages
```powershell
pip install --force-reinstall -r requirements.txt
pip install --force-reinstall -r backend\requirements.txt
```

## Notes
- Always activate the `cursor-extractor` conda environment before running any Python commands
- The deploy.ps1 script handles port cleanup automatically
- Backend and frontend run in separate PowerShell windows for easy monitoring

