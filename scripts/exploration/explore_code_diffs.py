"""Explore codeBlockDiff structure."""

import sqlite3
import json
from pathlib import Path

# Connect to database
db_path = Path.home() / "AppData" / "Roaming" / "Cursor" / "User" / "globalStorage" / "state.vscdb"
conn = sqlite3.connect(str(db_path))
cursor = conn.cursor()

# Get sample codeBlockDiff entries
print("=" * 60)
print("CODEBOCKDIFF STRUCTURE EXPLORATION")
print("=" * 60)

cursor.execute("SELECT COUNT(*) FROM cursorDiskKV WHERE key LIKE 'codeBlockDiff:%'")
count = cursor.fetchone()[0]
print(f"\nTotal codeBlockDiff entries: {count:,}\n")

# Get first 3 samples
cursor.execute("SELECT key, value FROM cursorDiskKV WHERE key LIKE 'codeBlockDiff:%' LIMIT 3")
samples = cursor.fetchall()

for i, (key, value) in enumerate(samples, 1):
    print(f"\n{'='*60}")
    print(f"SAMPLE {i}")
    print(f"{'='*60}")
    print(f"Key: {key}")
    
    try:
        data = json.loads(value)
        print(f"\nData keys: {list(data.keys())}")
        print(f"\nFull structure:")
        print(json.dumps(data, indent=2)[:1000])
        
        # Show types of values
        print(f"\n\nField types:")
        for k, v in data.items():
            print(f"  {k}: {type(v).__name__} = {v if not isinstance(v, (list, dict)) else f'<{type(v).__name__} with {len(v)} items>'}")
            
    except Exception as e:
        print(f"Error parsing: {e}")

# Get field frequency
print(f"\n\n{'='*60}")
print("FIELD FREQUENCY ANALYSIS")
print(f"{'='*60}")

cursor.execute("SELECT value FROM cursorDiskKV WHERE key LIKE 'codeBlockDiff:%' LIMIT 100")
field_counts = {}

for (value,) in cursor.fetchall():
    try:
        data = json.loads(value)
        for key in data.keys():
            field_counts[key] = field_counts.get(key, 0) + 1
    except:
        pass

print("\nFields found (in 100 samples):")
for field, count in sorted(field_counts.items(), key=lambda x: x[1], reverse=True):
    print(f"  {field}: {count}/100")

conn.close()
print(f"\n{'='*60}")
print("EXPLORATION COMPLETE")
print(f"{'='*60}")

