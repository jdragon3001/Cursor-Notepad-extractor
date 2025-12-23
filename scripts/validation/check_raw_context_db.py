import sys
sys.path.insert(0, '.')

import sqlite3
from pathlib import Path
import json

print("Checking raw database for context fields...")

db_path = Path.home() / 'AppData' / 'Roaming' / 'Cursor' / 'User' / 'globalStorage' / 'state.vscdb'
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# Get all bubbleId entries
cursor.execute("SELECT key, value FROM cursorDiskKV WHERE key LIKE 'bubbleId:%' LIMIT 10000")
rows = cursor.fetchall()

print(f"Checking {len(rows)} messages...")

fields_to_check = ['attachedCodeChunks', 'codebaseContextChunks', 'relevantFiles', 'recentlyViewedFiles', 'webReferences']
counts = {field: 0 for field in fields_to_check}
samples = {field: None for field in fields_to_check}

for key, value in rows:
    try:
        data = json.loads(value.decode('utf-8'))
        for field in fields_to_check:
            if field in data and data[field]:
                counts[field] += 1
                if samples[field] is None:
                    samples[field] = data[field]
    except Exception as e:
        continue

print("\nResults:")
for field in fields_to_check:
    print(f"\n{field}: {counts[field]} messages with data")
    if samples[field]:
        if isinstance(samples[field], list):
            print(f"  Sample (first item): {samples[field][0] if samples[field] else 'empty list'}")
        else:
            print(f"  Sample: {str(samples[field])[:200]}")

conn.close()

