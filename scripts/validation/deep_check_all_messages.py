import sys
sys.path.insert(0, '.')

import sqlite3
from pathlib import Path
import json

print("Deep check: scanning all messages for references/suggestions...")

db_path = Path.home() / 'AppData' / 'Roaming' / 'Cursor' / 'User' / 'globalStorage' / 'state.vscdb'
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

cursor.execute("SELECT COUNT(*) FROM cursorDiskKV WHERE key LIKE 'bubbleId:%'")
total = cursor.fetchone()[0]
print(f"Total messages in DB: {total}")

# Check ALL messages
cursor.execute("SELECT value FROM cursorDiskKV WHERE key LIKE 'bubbleId:%'")

fields_found = {
    'webReferences': 0,
    'docsReferences': 0,
    'aiWebSearchResults': 0,
    'suggestedCodeBlocks': 0,
    'assistantSuggestedDiffs': 0,
    'userResponsesToSuggestedCodeBlocks': 0,
    'useWeb': 0,
}

samples = {}
checked = 0

for row in cursor:
    checked += 1
    if checked % 10000 == 0:
        print(f"  Checked {checked}/{total}...")
    
    try:
        data = json.loads(row[0].decode('utf-8'))
        for field in fields_found.keys():
            if field in data and data[field]:
                # Check if it's a non-empty value
                val = data[field]
                if isinstance(val, list) and len(val) > 0:
                    fields_found[field] += 1
                    if field not in samples:
                        samples[field] = val
                elif isinstance(val, dict) and len(val) > 0:
                    fields_found[field] += 1
                    if field not in samples:
                        samples[field] = val
                elif isinstance(val, bool) and val:
                    fields_found[field] += 1
                    if field not in samples:
                        samples[field] = val
                elif isinstance(val, (int, float)) and val != 0:
                    fields_found[field] += 1
                    if field not in samples:
                        samples[field] = val
    except:
        continue

print(f"\nResults from {checked} messages:")
for field, count in fields_found.items():
    print(f"\n{field}: {count} messages with non-empty data")
    if field in samples:
        sample = samples[field]
        if isinstance(sample, list):
            print(f"  Sample (first item): {sample[0] if sample else 'empty'}")
        else:
            print(f"  Sample: {str(sample)[:200]}")

conn.close()

