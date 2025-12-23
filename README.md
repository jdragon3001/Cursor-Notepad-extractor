# Cursor Stats Dashboard - React + FastAPI

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- Node.js 16+
- npm

### Installation

1. **Install Python dependencies**:
```bash
pip install -r backend/requirements.txt
```

2. **Install Frontend dependencies**:
```bash
cd frontend
npm install
cd ..
```

### Running the Dashboard

**Easy Way** (Recommended):
```bash
python launch_dashboard.py
```

This will start both backend and frontend servers and open the dashboard in your browser.

**Manual Way**:

Terminal 1 (Backend):
```bash
cd backend
python main.py
```

Terminal 2 (Frontend):
```bash
cd frontend
npm run dev
```

Then open http://localhost:5173 in your browser.

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
