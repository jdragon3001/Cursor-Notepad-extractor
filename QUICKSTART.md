# Cursor Stats Dashboard - Quick Start Guide

## Prerequisites

### Required Software
1. **Python 3.10+** with Conda
2. **Node.js 18+** with npm
3. **PowerShell** (Windows) or **Bash** (Mac/Linux)

### Conda Environment
```bash
conda create -n cursor-notepad-browser python=3.10
conda activate cursor-notepad-browser
```

## Installation

### 1. Install Backend Dependencies
```bash
cd backend
pip install -r requirements.txt
cd ..
```

### 2. Install Frontend Dependencies
```bash
cd frontend
npm install
cd ..
```

## Running the Dashboard

### Option 1: PowerShell Script (Recommended for Windows)
```powershell
.\deploy.ps1
```
This will:
- Clean up any processes on ports 8000 and 5173
- Start the FastAPI backend in a new window
- Start the React frontend in a new window
- Display URLs for both services

### Option 2: Manual Start

**Backend (Terminal 1):**
```bash
cd backend
conda activate cursor-notepad-browser
python main.py
```

**Frontend (Terminal 2):**
```bash
cd frontend
npm run dev
```

## Access the Dashboard

- **Frontend UI**: http://localhost:5173
- **Backend API**: http://127.0.0.1:8000
- **API Docs**: http://127.0.0.1:8000/docs

## Available API Endpoints

- `GET /` - Health check
- `GET /api/health` - Detailed health check
- `GET /api/summary` - Data extraction summary
- `GET /api/stats/all` - All calculated statistics
- `GET /api/stats/{category}` - Stats by category
- `GET /api/stats/{category}/{stat_id}` - Single stat
- `POST /api/cache/clear` - Clear stats cache

## Troubleshooting

### Port Already in Use
The `deploy.ps1` script automatically cleans up ports. If manual cleanup is needed:

**Windows:**
```powershell
# Find process on port
netstat -ano | findstr :8000
netstat -ano | findstr :5173

# Kill process by PID
taskkill /PID <PID> /F
```

**Mac/Linux:**
```bash
# Find and kill process
lsof -ti:8000 | xargs kill -9
lsof -ti:5173 | xargs kill -9
```

### Database Not Found
Ensure Cursor IDE has been used and the database exists at:
- **Windows**: `%USERPROFILE%\AppData\Roaming\Cursor\User\globalStorage\state.vscdb`
- **Mac**: `~/Library/Application Support/Cursor/User/globalStorage/state.vscdb`

### Tailwind Not Loading
If styles don't appear:
1. Stop the frontend (Ctrl+C)
2. Run `npm run dev` again
3. Hard refresh browser (Ctrl+Shift+R)

## Development Commands

### Backend
```bash
cd backend
python main.py          # Start server
```

### Frontend
```bash
cd frontend
npm run dev            # Development server
npm run build          # Production build
npm run preview        # Preview production build
npm run lint           # Run ESLint
```

## Project Structure

```
cursor-notepad-extractor/
├── backend/           # FastAPI backend
│   ├── main.py       # API server
│   └── requirements.txt
├── frontend/         # React frontend
│   ├── src/
│   │   ├── App.jsx   # Main component
│   │   └── index.css # Tailwind styles
│   └── package.json
├── stats/            # Data extraction & calculation
│   ├── extractors/   # Data extraction modules
│   ├── calculators/  # Stats calculation modules
│   ├── models/       # Data models
│   └── orchestrator.py
└── deploy.ps1        # Deployment script
```

## Next Steps

After running the dashboard:
1. View the summary stats on the homepage
2. Explore different stat categories
3. Use the API docs at http://127.0.0.1:8000/docs

## Need Help?

- Check `STRUCTURE.md` for architecture details
- Check `docs/planning/` for implementation plans
- Check `PROBLEM_LOG.txt` for known issues
