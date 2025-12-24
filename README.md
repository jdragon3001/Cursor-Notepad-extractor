# Cursor Stats Dashboard

A beautiful web dashboard to visualize and analyze your Cursor IDE usage statistics. Works on **Windows, macOS, and Linux**.

## 🚀 Quick Start

### Prerequisites
- **Python 3.8+** with pip ([Download](https://www.python.org/downloads/))
- **Node.js 16+** with npm ([Download](https://nodejs.org/))
- **Cursor IDE** with some usage history

### Installation & Launch

**Step 1: Install Dependencies**
```bash
# Install Python packages
pip install -r requirements.txt
pip install -r backend/requirements.txt

# Install Node.js packages
cd frontend
npm install
cd ..
```

**Step 2: Launch**

Choose your preferred method:

**🎯 Option A: Easy Launch (Recommended)**
```bash
python launch_dashboard.py
```

**🪟 Option B: Windows PowerShell**
```powershell
.\deploy.ps1
```

**📋 Option C: Manual (Two Terminals)**
```bash
# Terminal 1
cd backend
python main.py

# Terminal 2
cd frontend
npm run dev
```

**That's it!** Open http://localhost:5173 to see your stats.

> 💡 **First time?** See `INSTALLATION.md` for detailed setup instructions and troubleshooting.

## 📍 Database Locations

The dashboard automatically finds your Cursor database at:

- **Windows**: `C:\Users\<YourName>\AppData\Roaming\Cursor\User\globalStorage\state.vscdb`
- **macOS**: `~/Library/Application Support/Cursor/User/globalStorage/state.vscdb`
- **Linux**: `~/.config/Cursor/User/globalStorage/state.vscdb`

No configuration needed - it just works!

## 📊 Features

- **139 Stats** - All calculated statistics from your Cursor usage
- **Search & Filter** - Find specific stats quickly
- **Category Organization** - Stats organized into 6 categories
- **Real-time Data** - Live connection to your Cursor database
- **Beautiful UI** - Modern, professional React interface

## 🏗️ Architecture

```
┌─────────────────┐         ┌──────────────────┐
│  React Frontend │ ◄─────► │  FastAPI Backend │
│  (Port 5173)    │  REST   │  (Port 8000)     │
└─────────────────┘         └──────────────────┘
                                     │
                                     ▼
                            ┌─────────────────┐
                            │ StatsOrchestrator│
                            │   Extractors     │
                            │   Calculators    │
                            └─────────────────┘
```

## 📁 Project Structure

```
cursor-notepad-extractor/
├── backend/
│   ├── main.py              # FastAPI server
│   ├── requirements.txt     # Python dependencies
│   └── api/
├── frontend/
│   ├── src/
│   │   ├── App.jsx         # Main React component
│   │   └── index.css       # TailwindCSS styles
│   ├── package.json
│   └── vite.config.js
├── stats/                   # Your existing stats code
│   ├── orchestrator.py
│   ├── calculators/
│   ├── extractors/
│   └── models/
└── launch_dashboard.py      # Easy launcher
```

## 🎯 API Endpoints

- `GET /` - Health check
- `GET /api/summary` - Data summary
- `GET /api/stats/all` - All statistics
- `GET /api/stats/{category}` - Stats by category
- `GET /api/stats/{category}/{stat_id}` - Single stat
- `POST /api/cache/clear` - Clear cache

## 🔧 Development

**Backend (FastAPI)**:
```bash
cd backend
uvicorn main:app --reload
```

**Frontend (React + Vite)**:
```bash
cd frontend
npm run dev
```

## 🎨 Technology Stack

- **Frontend**: React 18, Vite, TailwindCSS, Axios, Lucide Icons
- **Backend**: FastAPI, Python 3.8+, Pydantic
- **Data**: SQLite, NumPy, Your existing stats system

## 📝 Notes

- Backend runs on `http://localhost:8000`
- Frontend runs on `http://localhost:5173`
- CORS is configured for local development
- All your existing Python stats code is preserved and used
