# 🚀 Installation & Setup Guide

## Quick Start (3 Steps)

### 1️⃣ Install Dependencies

Run these commands in order:

```bash
# Step 1: Install Python packages for the stats engine
pip install -r requirements.txt

# Step 2: Install Python packages for the API backend
pip install -r backend/requirements.txt

# Step 3: Install Node.js packages for the frontend
cd frontend
npm install
cd ..
```

**Notes:**
- On some systems, use `pip3` instead of `pip`
- On some systems, use `python3` instead of `python`
- This installs: numpy, FastAPI, React, and all dependencies

---

### 2️⃣ Launch the Dashboard

Choose **ONE** of these methods:

#### **Option A: Easy Launch (Cross-Platform)**
```bash
python launch_dashboard.py
```
This auto-opens the dashboard in your browser!

#### **Option B: Windows PowerShell Script**
```powershell
.\deploy.ps1
```
Opens backend and frontend in separate windows.

#### **Option C: Manual (Two Terminals)**

**Terminal 1 - Backend:**
```bash
cd backend
python main.py
```

**Terminal 2 - Frontend:**
```bash
cd frontend
npm run dev
```

Then open http://localhost:5173

---

### 3️⃣ View Your Stats

The dashboard will open automatically, or go to:
- **Dashboard:** http://localhost:5173
- **API:** http://localhost:8000

---

## Platform-Specific Tips

### Windows
- ✅ Use `deploy.ps1` for the best experience (opens separate windows)
- ✅ Or use `python launch_dashboard.py`
- 📝 Database auto-detected at: `C:\Users\YourName\AppData\Roaming\Cursor\User\globalStorage\state.vscdb`

### macOS
- ✅ Use `python3 launch_dashboard.py` (might need `python3` not `python`)
- ✅ Use `pip3` instead of `pip` if `pip` doesn't work
- 📝 Database auto-detected at: `~/Library/Application Support/Cursor/User/globalStorage/state.vscdb`

### Linux
- ✅ Use `python3 launch_dashboard.py`
- ✅ Use `pip3` instead of `pip`
- 📝 Database auto-detected at: `~/.config/Cursor/User/globalStorage/state.vscdb`

---

## Troubleshooting Installation

### "pip: command not found"
```bash
# Try pip3 instead
pip3 install -r requirements.txt
```

### "python: command not found"
```bash
# Try python3 instead
python3 launch_dashboard.py
```

### "npm: command not found"
Download and install Node.js from: https://nodejs.org/

### "Port already in use"
**Windows:**
```powershell
# Kill process on port 8000
$proc = (Get-NetTCPConnection -LocalPort 8000 -ErrorAction SilentlyContinue).OwningProcess
if ($proc) { Stop-Process -Id $proc -Force }
```

**Mac/Linux:**
```bash
# Kill process on port 8000
lsof -ti:8000 | xargs kill -9
```

---

## What Gets Installed?

### Python Packages (requirements.txt):
- `numpy` - Statistical calculations
- `fastapi` - Backend API server
- `uvicorn` - ASGI server
- `pydantic` - Data validation

### Frontend Packages (npm):
- `react` - UI framework
- `vite` - Build tool
- `tailwindcss` - Styling
- `axios` - API requests
- `lucide-react` - Icons

**Total Install Size:** ~500MB (mostly Node.js packages)

---

## Verifying Installation

Test each component:

```bash
# 1. Test Python
python --version  # Should be 3.8+

# 2. Test pip packages
python -c "import numpy, fastapi; print('✓ Python packages OK')"

# 3. Test Node.js
node --version  # Should be 16+
npm --version

# 4. Test frontend packages
cd frontend
npm list react  # Should show react installed
cd ..
```

---

## Next Steps

Once installed:
1. Run `python launch_dashboard.py`
2. Dashboard opens at http://localhost:5173
3. Explore your Cursor stats!

See `USER_GUIDE.md` for how to use the dashboard.
See `TROUBLESHOOTING.md` if you encounter issues.

