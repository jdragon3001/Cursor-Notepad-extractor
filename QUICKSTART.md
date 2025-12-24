# 🎯 For New Users: How to Use This

## What You Need
1. ✅ Cursor IDE installed (not VS Code)
2. ✅ Python 3.8+ installed
3. ✅ Node.js 16+ installed

---

## Installation (Copy-Paste These Commands)

```bash
# 1. Install Python packages
pip install -r requirements.txt
pip install -r backend/requirements.txt

# 2. Install Node.js packages
cd frontend
npm install
cd ..

# 3. Launch the dashboard
python launch_dashboard.py
```

**⏱️ Time:** ~5 minutes (downloading packages)

---

## What Happens When You Launch?

1. 🖥️ **Backend starts** → API server on port 8000
2. 🌐 **Frontend starts** → Web dashboard on port 5173  
3. 🚀 **Browser opens** → Shows your Cursor stats!

---

## What You'll See

A beautiful dashboard showing:
- 💬 **51 Message Stats** - Your AI chat usage
- 📝 **27 Session Stats** - Your coding sessions  
- 🔧 **10 Tool Stats** - File edits, searches, etc.
- 📊 **12 Code Stats** - Your code changes
- 📅 **6 Daily Stats** - Usage patterns
- 🔍 **18 Context Stats** - What context you provide

**Total: 124 statistics about your Cursor usage!**

---

## Common Issues & Quick Fixes

### "pip: command not found"
```bash
pip3 install -r requirements.txt  # Try pip3 instead
```

### "python: command not found"
```bash
python3 launch_dashboard.py  # Try python3 instead
```

### "Port 8000 already in use"
Close other apps using that port, or restart your computer.

### "No stats showing"
Make sure you've actually used Cursor IDE - you need some history!

---

## Platform Notes

### 🪟 Windows Users
- Use `.\deploy.ps1` for best experience
- Database location: `C:\Users\YourName\AppData\Roaming\Cursor\User\globalStorage\state.vscdb`

### 🍎 macOS Users  
- Use `python3` and `pip3` in commands
- Database location: `~/Library/Application Support/Cursor/User/globalStorage/state.vscdb`

### 🐧 Linux Users
- Use `python3` and `pip3` in commands
- Database location: `~/.config/Cursor/User/globalStorage/state.vscdb`

---

## 🆘 Need Help?

1. **INSTALLATION.md** - Detailed setup guide
2. **TROUBLESHOOTING.md** - Fix common problems
3. **USER_GUIDE.md** - Learn how to use the dashboard

---

## 📸 What It Looks Like

After launching, you'll see:
- A clean, modern web interface
- Search box to find specific stats
- Category filters (Messages, Sessions, Tools, etc.)
- Individual stat cards with values and details
- All running locally on your computer (your data stays private!)

---

## That's It!

Three commands to install, one command to launch. Enjoy exploring your Cursor stats! 🎉
