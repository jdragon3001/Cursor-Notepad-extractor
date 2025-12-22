"""Explore dailyUsageStats structure."""

import sqlite3
import json
from pathlib import Path

# Connect to database
db_path = Path.home() / "AppData" / "Roaming" / "Cursor" / "User" / "globalStorage" / "state.vscdb"
conn = sqlite3.connect(str(db_path))
cursor = conn.cursor()

print("=" * 60)
print("DAILYUSAGESTATS STRUCTURE EXPLORATION")
print("=" * 60)

# Check ItemTable for dailyUsageStats
cursor.execute("SELECT COUNT(*) FROM ItemTable WHERE key LIKE '%dailyUsageStats%'")
count = cursor.fetchone()[0]
print(f"\nTotal dailyUsageStats entries in ItemTable: {count:,}\n")

# Get all keys with dailyUsageStats
cursor.execute("SELECT key FROM ItemTable WHERE key LIKE '%dailyUsageStats%'")
keys = cursor.fetchall()
print(f"Keys found:")
for key, in keys:
    print(f"  - {key}")

# Get sample
cursor.execute("SELECT key, value FROM ItemTable WHERE key LIKE '%dailyUsageStats%' LIMIT 1")
row = cursor.fetchone()

if row:
    key, value = row
    print(f"\nKey: {key}\n")
    
    try:
        data = json.loads(value)
        print(f"Data type: {type(data).__name__}")
        
        if isinstance(data, dict):
            print(f"Top-level keys: {list(data.keys())}")
            
            # Show structure of first few entries
            for i, (date_key, date_data) in enumerate(list(data.items())[:3]):
                print(f"\n{'='*50}")
                print(f"Sample {i+1}: Date = {date_key}")
                print(f"{'='*50}")
                print(json.dumps(date_data, indent=2))
                
        elif isinstance(data, list):
            print(f"List length: {len(data)}")
            if data:
                print(f"\nFirst item:")
                print(json.dumps(data[0], indent=2))
                
    except Exception as e:
        print(f"Error parsing: {e}")
        print(f"Raw value (first 1000 chars): {value[:1000]}")
else:
    print("No dailyUsageStats entries found")

conn.close()
print(f"\n{'='*60}")
print("EXPLORATION COMPLETE")
print(f"{'='*60}")

