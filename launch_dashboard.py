"""Launch the Cursor Stats Dashboard."""

import subprocess
import sys
from pathlib import Path

# Get the streamlit_app directory
app_dir = Path(__file__).parent / "streamlit_app"
app_file = app_dir / "app.py"

if not app_file.exists():
    print(f"Error: {app_file} not found!")
    sys.exit(1)

print("=" * 60)
print("Starting Cursor Stats Dashboard...".center(60))
print("=" * 60)
print(f"\nApp location: {app_file}")
print("\n📊 The dashboard will open in your browser")
print("🔄 Press Ctrl+C to stop the server\n")
print("=" * 60)

# Launch streamlit
try:
    subprocess.run([
        sys.executable, "-m", "streamlit", "run",
        str(app_file),
        "--server.port=8501",
        "--server.address=localhost",
        "--browser.gatherUsageStats=false"
    ])
except KeyboardInterrupt:
    print("\n\n" + "=" * 60)
    print("Dashboard stopped.".center(60))
    print("=" * 60)
except Exception as e:
    print(f"\n❌ Error: {e}")
    sys.exit(1)

