"""
Script to check if linter, console log, and terminal interaction data exists in the database.
"""

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

# Get all bubbleId entries
cursor.execute("SELECT key, value FROM cursorDiskKV WHERE key LIKE 'bubbleId:%' LIMIT 10000")
rows = cursor.fetchall()

print("="*80)
print(f"CHECKING {len(rows)} MESSAGES FOR ERROR/LOG/TERMINAL DATA")
print("="*80)

# Track what we find
fields_found = {
    'lints': 0,
    'consoleLogs': 0,
    'consoleLog': 0,
    'terminalInteractions': 0,
    'terminal': 0,
    'toolResults': 0,
    'toolFormerData': 0,
    'errors': 0,
    'error': 0,
}

# Track all unique top-level keys
all_keys = set()

for key, value in rows:
    try:
        if isinstance(value, bytes):
            data = json.loads(value.decode('utf-8'))
        elif isinstance(value, str):
            data = json.loads(value)
        else:
            continue
        
        # Track all keys
        for field in data.keys():
            all_keys.add(field)
        
        # Check specific fields
        for field in fields_found.keys():
            if field in data:
                value = data[field]
                # Count if not empty/null
                if value:
                    if isinstance(value, list) and len(value) > 0:
                        fields_found[field] += 1
                    elif isinstance(value, dict) and len(value) > 0:
                        fields_found[field] += 1
                    elif isinstance(value, (str, int, float, bool)) and value:
                        fields_found[field] += 1
        
    except Exception as e:
        pass

print(f"\n📊 FIELD OCCURRENCE IN {len(rows)} MESSAGES:\n")
for field, count in sorted(fields_found.items(), key=lambda x: x[1], reverse=True):
    if count > 0:
        percentage = (count / len(rows)) * 100
        print(f"  {field:25} {count:>6} messages ({percentage:>5.1f}%)")

if sum(fields_found.values()) == 0:
    print("  ❌ NONE of these fields found with non-empty values!")
    print("\n🔍 This explains why all stats show 0.")

print(f"\n📋 ALL UNIQUE TOP-LEVEL KEYS FOUND ({len(all_keys)} total):\n")
for key in sorted(all_keys):
    print(f"  - {key}")

# Look for error/lint/log related keys
error_related = [k for k in all_keys if any(term in k.lower() for term in ['error', 'lint', 'log', 'terminal', 'console', 'tool'])]
if error_related:
    print(f"\n🔍 ERROR/LOG/TOOL RELATED KEYS FOUND:\n")
    for key in sorted(error_related):
        print(f"  - {key}")

# Sample a few messages with toolResults to see structure
print(f"\n📝 SAMPLE MESSAGE WITH toolResults:\n")
cursor.execute("SELECT key, value FROM cursorDiskKV WHERE key LIKE 'bubbleId:%' LIMIT 5000")
rows = cursor.fetchall()

found_sample = False
for key, value in rows:
    try:
        if isinstance(value, bytes):
            data = json.loads(value.decode('utf-8'))
        elif isinstance(value, str):
            data = json.loads(value)
        else:
            continue
        
        if 'toolResults' in data and data['toolResults']:
            print(f"Key: {key[:60]}...")
            print(f"toolResults: {json.dumps(data['toolResults'][:2], indent=2)[:500]}...")
            found_sample = True
            break
    except:
        pass

if not found_sample:
    print("  ❌ No messages with toolResults found in sample")

conn.close()

print("\n" + "="*80)
print("Check complete!")

