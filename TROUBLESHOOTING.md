# Troubleshooting Guide

## Common Issues

### 1. "Database not found" Error

**Problem**: The app can't find your Cursor database.

**Solution**:
1. Make sure Cursor IDE is installed and you've used it at least once
2. Check if the database exists at:
   - **Windows**: `C:\Users\<YourName>\AppData\Roaming\Cursor\User\globalStorage\state.vscdb`
   - **macOS**: `~/Library/Application Support/Cursor/User/globalStorage/state.vscdb`
   - **Linux**: `~/.config/Cursor/User/globalStorage/state.vscdb`
3. If using VS Code instead of Cursor, the database won't exist

### 2. Backend Won't Start (Port 8000 Already in Use)

**Problem**: Another process is using port 8000.

**Solution**:

**Windows**:
```powershell
# Find what's using port 8000
netstat -ano | findstr :8000

# Kill the process (replace PID with actual process ID)
taskkill /F /PID <PID>
```

**macOS/Linux**:
```bash
# Find and kill process on port 8000
lsof -ti:8000 | xargs kill -9
```

### 3. Frontend Shows "Failed to fetch" or Connection Errors

**Problem**: Frontend can't connect to backend API.

**Solution**:
1. Make sure backend is running (check http://localhost:8000)
2. Check for CORS errors in browser console
3. Restart both frontend and backend
4. Clear browser cache

### 4. Stats Show Zero or Incorrect Values

**Problem**: Some statistics appear incorrect or show 0.

**Known Issues**:
- **Edit Distance (0)**: This is a placeholder stat not yet implemented
- **Similarity Ratio (0)**: This is a placeholder stat not yet implemented  
- **Tracked Code Lines (10,000)**: Cursor's database caps at 10,000 entries

**Solution for other stats**:
1. Click "Clear Cache" in the dashboard (if available)
2. Restart the backend server
3. Check backend terminal for any error messages

### 5. Python Import Errors

**Problem**: `ModuleNotFoundError` or import errors.

**Solution**:
```bash
# Make sure you installed BOTH requirements files
pip install -r requirements.txt
pip install -r backend/requirements.txt
```

### 6. npm Install Fails

**Problem**: Frontend dependencies won't install.

**Solution**:
```bash
# Clear npm cache and retry
cd frontend
rm -rf node_modules package-lock.json
npm cache clean --force
npm install
```

### 7. Dashboard is Blank or Shows No Data

**Problem**: Dashboard loads but no statistics appear.

**Solution**:
1. Open browser DevTools (F12) and check Console for errors
2. Check Network tab - is the API call to `/api/stats/all` working?
3. Try accessing http://localhost:8000/api/stats/all directly in browser
4. Check backend terminal for error messages

## Getting Help

If you're still stuck:
1. Check the backend terminal for detailed error messages
2. Check browser console (F12) for frontend errors
3. Make sure you're using compatible versions:
   - Python 3.8 or higher
   - Node.js 16 or higher
   - Cursor IDE (not VS Code)

## Debugging Mode

To get more detailed logs:

**Backend**:
```python
# In backend/main.py, change logging level
logging.basicConfig(level=logging.DEBUG)
```

**Frontend**:
Check browser DevTools Console tab for errors.

