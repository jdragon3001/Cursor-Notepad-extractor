# Cursor Stats Dashboard - Reddit Installation Guide

## What This Is

A local web dashboard that visualizes your Cursor IDE usage statistics. Shows 124+ metrics including:
- Message and session counts
- Tool usage patterns
- Code changes and diffs
- Daily usage trends
- Context provided to AI

**Important:** Your data stays on your computer. This runs 100% locally.

---

## Requirements

- **Cursor IDE** (not VS Code) with some usage history
- **Python 3.8+** ([Download](https://www.python.org/downloads/))
- **Node.js 16+** ([Download](https://nodejs.org/))
- **5-10 minutes** for setup

---

## How It Works

**Windows vs Mac/Linux:**
- **Database Location:** Automatically detected at OS-specific paths
- **Python Command:** Windows uses `python`, Mac/Linux uses `python3`
- **Setup Scripts:** PowerShell for Windows, Bash for Mac/Linux
- **Virtual Environment:** Creates isolated Python environment (won't affect your system Python)

The setup scripts handle everything platform-specific for you.

---

## Installation - Windows

### Step 1: Download and Extract
Download the repository and extract to a folder.

### Step 2: Run Setup Script
Open PowerShell in the project folder:
```powershell
cd setup
.\setup-windows.ps1
```

This script will:
- Check Python and Node.js versions
- Create a virtual environment (isolated, safe)
- Install all dependencies
- Verify installation

### Step 3: Launch Dashboard
Stay in the setup folder and run:
```powershell
.\launch.ps1
```

Dashboard opens at: http://localhost:5173

### Troubleshooting Windows

**"Execution policy" error:**
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

**Port already in use:**
```powershell
Get-NetTCPConnection -LocalPort 8000 | ForEach-Object { Stop-Process -Id $_.OwningProcess -Force }
```

---

## Installation - Mac/Linux

### Step 1: Download and Extract
Download the repository and extract to a folder.

### Step 2: Run Setup Script
Open Terminal in the project folder:
```bash
cd setup
chmod +x setup-mac.sh
./setup-mac.sh
```

This script will:
- Check Python and Node.js versions
- Create a virtual environment (isolated, safe)
- Install all dependencies
- Verify installation

### Step 3: Launch Dashboard
Stay in the setup folder and run:
```bash
./launch.sh
```

Dashboard opens at: http://localhost:5173

### Troubleshooting Mac/Linux

**"python3: command not found":**
Install Python from python.org

**"node: command not found":**
Install Node.js from nodejs.org

**Port already in use:**
```bash
lsof -ti:8000 | xargs kill -9
```

**Permission denied on scripts:**
```bash
chmod +x setup/setup-mac.sh
chmod +x launch.sh
```

---

## What Gets Installed

**Virtual Environment (Isolated Python):**
- numpy - Statistical calculations
- fastapi - API backend
- uvicorn - Web server

**Frontend (Node modules in project folder):**
- react - UI framework
- vite - Build tool
- tailwindcss - Styling

**Total size:** ~500MB (mostly Node packages)

**Safety:** All packages install in the project folder's virtual environment. Your system Python is untouched.

---

## Database Locations (Auto-detected)

- **Windows:** `C:\Users\<YourName>\AppData\Roaming\Cursor\User\globalStorage\state.vscdb`
- **Mac:** `~/Library/Application Support/Cursor/User/globalStorage/state.vscdb`
- **Linux:** `~/.config/Cursor/User/globalStorage/state.vscdb`

No configuration needed - works automatically.

---

## Common Issues

**No stats showing:**
You need Cursor IDE usage history. Use Cursor for a few days first.

**Database not found:**
Make sure you're using Cursor IDE, not VS Code.

**Installation fails:**
Try manual installation (see INSTALLATION.md in the repo).

**Different Python version needed:**
The virtual environment uses whatever Python you have installed. As long as it's 3.8+, you're fine.

---

## Testing on Mac Without a Mac

**Options:**
1. **Virtual Machine:** Run macOS in VMware/VirtualBox (requires macOS license)
2. **GitHub Actions:** Set up CI/CD with macOS runner to test scripts
3. **Friend with Mac:** Ask someone to test and provide feedback
4. **Cloud Mac:** Rent a Mac in the cloud (MacStadium, MacinCloud)

The bash script follows standard practices and should work on any Mac/Linux system with Python 3.8+ and Node.js 16+.

---

## Architecture

```
Frontend (React) <-> Backend (FastAPI) <-> Stats Engine <-> Cursor DB (SQLite)
Port 5173            Port 8000              Python          Read-only
```

---

## Stopping the Dashboard

**Windows:** Close the PowerShell windows or press Ctrl+C

**Mac/Linux:** Press Ctrl+C in the terminal

---

## Uninstalling

Delete the project folder. Everything is contained there. No system changes made.

---

For detailed documentation, see the INSTALLATION.md and TROUBLESHOOTING.md files in the repository.

