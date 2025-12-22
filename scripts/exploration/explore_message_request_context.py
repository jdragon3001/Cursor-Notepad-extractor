"""Explore messageRequestContext for comprehensive context data."""

import sqlite3
import json
from pathlib import Path
from collections import Counter

db_path = Path.home() / "AppData" / "Roaming" / "Cursor" / "User" / "globalStorage" / "state.vscdb"
conn = sqlite3.connect(str(db_path))
cursor = conn.cursor()

print("=" * 60)
print("MESSAGE REQUEST CONTEXT EXPLORATION")
print("=" * 60)

cursor.execute("SELECT COUNT(*) FROM cursorDiskKV WHERE key LIKE 'messageRequestContext:%'")
total = cursor.fetchone()[0]
print(f"\nTotal messageRequestContext entries: {total:,}")

# Get samples to understand structure
cursor.execute("SELECT key, value FROM cursorDiskKV WHERE key LIKE 'messageRequestContext:%' LIMIT 10")
samples = cursor.fetchall()

# Analyze fields
all_fields = Counter()
for key, value_bytes in samples:
    try:
        data = json.loads(value_bytes)
        for field in data.keys():
            all_fields[field] += 1
    except:
        pass

print(f"\n{'='*60}")
print("FIELDS FOUND")
print(f"{'='*60}")
for field, count in all_fields.most_common():
    print(f"{field}: {count}/{len(samples)}")

# Show a full sample
print(f"\n{'='*60}")
print("FULL SAMPLE")
print(f"{'='*60}")
key, value_bytes = samples[0]
print(f"Key: {key}")
data = json.loads(value_bytes)
print(json.dumps(data, indent=2))

# Check for linter errors
print(f"\n{'='*60}")
print("LINTER ERROR ANALYSIS")
print(f"{'='*60}")

cursor.execute("SELECT key, value FROM cursorDiskKV WHERE key LIKE 'messageRequestContext:%' LIMIT 100")
all_samples = cursor.fetchall()

total_with_errors = 0
total_errors = 0

for key, value_bytes in all_samples:
    try:
        data = json.loads(value_bytes)
        errors = data.get('multiFileLinterErrors', [])
        if errors:
            total_with_errors += 1
            total_errors += len(errors)
    except:
        pass

print(f"Contexts with linter errors: {total_with_errors}/{len(all_samples)}")
print(f"Total linter errors found: {total_errors}")

# Show a sample with errors
for key, value_bytes in all_samples:
    try:
        data = json.loads(value_bytes)
        errors = data.get('multiFileLinterErrors', [])
        if errors:
            print(f"\nSample with errors:")
            print(json.dumps(errors[:2], indent=2))
            break
    except:
        pass

conn.close()

print(f"\n{'='*60}")
print("EXPLORATION COMPLETE")
print(f"{'='*60}")

