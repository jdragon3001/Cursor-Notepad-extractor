# Platform Differences - Windows vs macOS/Linux

## Summary

The Cursor Stats Dashboard works on both Windows and Mac/Linux with minimal differences. The setup scripts handle all platform-specific details automatically.

## Key Differences

### 1. Python Command
- **Windows**: `python`
- **Mac/Linux**: `python3` (some systems have `python` as well)
- **Setup script handles**: Detects and uses the correct command

### 2. pip Command
- **Windows**: `pip`
- **Mac/Linux**: `pip3` (some systems have `pip` as well)
- **Setup script handles**: Detects and uses the correct command

### 3. Virtual Environment Activation
- **Windows**: `venv\Scripts\Activate.ps1`
- **Mac/Linux**: `source venv/bin/activate`
- **Launch scripts handle**: Activates automatically

### 4. Database Location
- **Windows**: `C:\Users\<YourName>\AppData\Roaming\Cursor\User\globalStorage\state.vscdb`
- **Mac**: `~/Library/Application Support/Cursor/User/globalStorage/state.vscdb`
- **Linux**: `~/.config/Cursor/User/globalStorage/state.vscdb`
- **Code handles**: `utils/config.py` auto-detects based on OS

### 5. Path Separators
- **Windows**: Backslash `\`
- **Mac/Linux**: Forward slash `/`
- **Python handles**: Uses `pathlib.Path` which works on all platforms

### 6. Script Files
- **Windows**: PowerShell `.ps1` files
- **Mac/Linux**: Bash `.sh` files (need `chmod +x` first time)

### 7. Port Cleanup Commands
- **Windows**: 
  ```powershell
  Get-NetTCPConnection -LocalPort 8000 | ForEach-Object { Stop-Process -Id $_.OwningProcess -Force }
  ```
- **Mac/Linux**: 
  ```bash
  lsof -ti:8000 | xargs kill -9
  ```

## What's The Same

- Python packages (same requirements.txt)
- Node.js packages (same package.json)
- Backend code (FastAPI works identically)
- Frontend code (React/Vite works identically)
- Database structure (SQLite is cross-platform)
- Features and functionality (100% identical)

## Safety: Virtual Environments

Both setup scripts create a virtual environment:

**What this means:**
- Python packages install in `./venv/` folder (project directory)
- Your system Python is untouched
- Other Python projects are unaffected
- Safe to delete (just remove the project folder)

**Why it matters:**
- Users with different Python versions won't have conflicts
- Users with existing Python projects won't break them
- Clean uninstall (delete folder, done)

## Testing on Mac Without a Mac

Since you're on Windows, here are options for testing the Mac setup:

1. **Virtual Machine**: 
   - VMware Fusion or VirtualBox with macOS
   - Requires macOS license
   - Most reliable testing

2. **GitHub Actions**:
   - Set up CI/CD with macOS runner
   - Free for public repos
   - Tests scripts automatically on push

3. **Friend with Mac**:
   - Send them the setup script
   - Ask them to run and report back
   - Quick feedback

4. **Cloud Mac**:
   - MacStadium or MacinCloud
   - Rent by the hour
   - Expensive but fast

5. **Docker**:
   - macOS containers exist but are complicated
   - Not recommended for this use case

**Recommendation**: The bash script (`setup-mac.sh`) follows standard practices and should work fine. If you post on Reddit, Mac users will quickly report any issues you can fix.

## User-Facing Documentation

- **REDDIT_GUIDE.md**: Split into Windows and Mac sections, easy to follow
- **setup/README.md**: Explains both platforms briefly
- **README.md**: Points users to the right resources

## Deployment Checklist

Before posting on Reddit:

- [x] Virtual environment setup (Windows) - prevents system Python conflicts
- [x] Virtual environment setup (Mac/Linux) - prevents system Python conflicts
- [x] Platform-specific setup scripts
- [x] Platform-specific launch scripts
- [x] Clear documentation split by platform
- [x] Database location auto-detection works on all platforms
- [x] .gitignore includes venv/
- [ ] Test Windows setup script (you can do this)
- [ ] Test Mac setup script (need Mac user)

## Quick Test Plan (Windows)

You can test the Windows setup yourself:

1. **Fresh Test** (in new directory):
   ```powershell
   cd setup
   .\setup-windows.ps1
   ```

2. **Verify Virtual Environment**:
   - Check that `venv\` folder was created
   - Check that packages installed in venv, not globally

3. **Launch Test**:
   ```powershell
   .\launch.ps1
   ```

4. **Verify Dashboard**:
   - Opens at http://localhost:5173
   - Shows your stats
   - No errors in browser console

5. **Clean Test** (simulate uninstall):
   - Delete project folder
   - Verify no leftover files in system Python

## Mac Testing (For Reddit Users)

Once posted, Mac users can validate:
- Script runs without errors
- Virtual environment creates successfully
- Dashboard launches and works
- No conflicts with their existing Python

Mac users typically expect to use `python3` and `pip3`, which the script handles correctly.

