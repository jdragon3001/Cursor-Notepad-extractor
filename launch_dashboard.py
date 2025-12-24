"""Launch script for Cursor Stats Dashboard."""

import subprocess
import sys
import time
from pathlib import Path
import webbrowser

def main():
    print("=" * 60)
    print("🚀 Cursor Stats Dashboard Launcher".center(60))
    print("=" * 60)
    print()
    
    project_root = Path(__file__).parent
    backend_dir = project_root / "backend"
    frontend_dir = project_root / "frontend"
    
    # Start backend
    print("Starting backend server...")
    backend_process = subprocess.Popen(
        [sys.executable, "main.py"],
        cwd=backend_dir,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )
    
    # Wait for backend to start
    print("Waiting for backend to initialize...")
    time.sleep(3)
    
    # Start frontend
    print("Starting frontend...")
    frontend_process = subprocess.Popen(
        ["npm", "run", "dev"],
        cwd=frontend_dir,
        shell=True
    )
    
    # Wait for frontend to start
    time.sleep(3)
    
    print()
    print("=" * 60)
    print("✅ Dashboard is running!".center(60))
    print("=" * 60)
    print()
    print("Backend API:  http://localhost:8000")
    print("Frontend UI:  http://localhost:5173")
    print()
    print("Press Ctrl+C to stop both servers")
    print()
    
    # Open browser
    webbrowser.open("http://localhost:5173")
    
    try:
        # Keep running until interrupted
        backend_process.wait()
        frontend_process.wait()
    except KeyboardInterrupt:
        print("\n\n🛑 Shutting down...")
        backend_process.terminate()
        frontend_process.terminate()
        backend_process.wait()
        frontend_process.wait()
        print("✅ Stopped successfully")


if __name__ == "__main__":
    main()
