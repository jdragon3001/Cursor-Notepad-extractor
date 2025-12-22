"""Explore aiCodeTrackingLines structure."""

import sqlite3
import json
from pathlib import Path

# Connect to database
db_path = Path.home() / "AppData" / "Roaming" / "Cursor" / "User" / "globalStorage" / "state.vscdb"
conn = sqlite3.connect(str(db_path))
cursor = conn.cursor()

print("=" * 60)
print("AICODETRACKINLINES STRUCTURE EXPLORATION")
print("=" * 60)

# Check ItemTable for aiCodeTrackingLines
cursor.execute("SELECT COUNT(*) FROM ItemTable WHERE key LIKE '%aiCodeTrackingLines%'")
count = cursor.fetchone()[0]
print(f"\nTotal aiCodeTrackingLines entries in ItemTable: {count:,}\n")

# Get sample
cursor.execute("SELECT key, value FROM ItemTable WHERE key LIKE '%aiCodeTrackingLines%' LIMIT 1")
row = cursor.fetchone()

if row:
    key, value = row
    print(f"Key: {key}\n")
    
    try:
        data = json.loads(value)
        print(f"Data type: {type(data).__name__}")
        
        if isinstance(data, dict):
            print(f"Top-level keys: {list(data.keys())[:10]}")
            print(f"\nTotal keys: {len(data)}")
            
            # Sample a few entries
            sample_keys = list(data.keys())[:3]
            for k in sample_keys:
                print(f"\n--- Sample: {k} ---")
                print(json.dumps(data[k], indent=2)[:500])
        elif isinstance(data, list):
            print(f"List length: {len(data)}")
            if data:
                print(f"\nFirst item:")
                print(json.dumps(data[0], indent=2))
                
    except Exception as e:
        print(f"Error parsing: {e}")
        print(f"Raw value (first 500 chars): {value[:500]}")
else:
    print("No aiCodeTrackingLines entries found")

conn.close()
print(f"\n{'='*60}")
print("EXPLORATION COMPLETE")
print(f"{'='*60}")

