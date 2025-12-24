"""Quick script to check what fields are in session data."""

import sys
import os
from pathlib import Path

# Fix Windows console encoding
if sys.platform == 'win32':
    os.environ['PYTHONIOENCODING'] = 'utf-8'
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')

import sqlite3
import json

# Get database path
user_home = Path.home()
db_path = user_home / "AppData" / "Roaming" / "Cursor" / "User" / "globalStorage" / "state.vscdb"

print(f"Checking database: {db_path}\n")

conn = sqlite3.connect(str(db_path))
cursor = conn.cursor()

# Get some sample sessions
cursor.execute("SELECT key, value FROM cursorDiskKV WHERE key LIKE 'composerData:%' LIMIT 5")
rows = cursor.fetchall()

print("="*80)
print("SAMPLE SESSION DATA STRUCTURE")
print("="*80)

for i, (key, value) in enumerate(rows, 1):
    try:
        if isinstance(value, bytes):
            data = json.loads(value.decode('utf-8'))
        elif isinstance(value, str):
            data = json.loads(value)
        else:
            continue
        
        print(f"\n--- Session {i} ---")
        print(f"Key: {key}")
        print(f"\nTop-level keys ({len(data)} total):")
        for field in sorted(data.keys()):
            field_value = data[field]
            field_type = type(field_value).__name__
            
            # Show preview of value
            if isinstance(field_value, str) and len(field_value) > 50:
                preview = f"{field_value[:50]}..."
            elif isinstance(field_value, dict):
                preview = f"{{...}} ({len(field_value)} keys)"
            elif isinstance(field_value, list):
                preview = f"[...] ({len(field_value)} items)"
            else:
                preview = str(field_value)
            
            print(f"  - {field:<30} ({field_type:<10}): {preview}")
        
        # Check for workspace-related fields
        workspace_fields = [f for f in data.keys() if 'workspace' in f.lower() or 'folder' in f.lower() or 'path' in f.lower() or 'project' in f.lower()]
        if workspace_fields:
            print(f"\n  Workspace-related fields:")
            for field in workspace_fields:
                print(f"    {field}: {data[field]}")
        
    except Exception as e:
        print(f"Error: {e}")

conn.close()

print("\n" + "="*80)
print("Check complete!")

