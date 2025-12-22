"""Check actual structure of bubbleId messages for tool-related fields."""

import sys
sys.stdout.reconfigure(encoding='utf-8')
sys.stderr.reconfigure(encoding='utf-8')

from pathlib import Path
import sqlite3
import json

print("=" * 60)
print("BUBBLEID STRUCTURE ANALYSIS")
print("=" * 60)

db_path = Path.home() / "AppData" / "Roaming" / "Cursor" / "User" / "globalStorage" / "state.vscdb"
conn = sqlite3.connect(str(db_path))
cursor = conn.cursor()

# Get a few AI messages to see their structure
cursor.execute("""
    SELECT value FROM cursorDiskKV 
    WHERE key LIKE 'bubbleId:%' 
    AND value LIKE '%"type":2%'
    LIMIT 5
""")

all_keys = set()
for (value_bytes,) in cursor.fetchall():
    try:
        data = json.loads(value_bytes)
        all_keys.update(data.keys())
    except json.JSONDecodeError:
        pass

print(f"\nAll keys found in bubbleId messages:")
for key in sorted(all_keys):
    print(f"  - {key}")

# Get one full message to see structure
cursor.execute("""
    SELECT value FROM cursorDiskKV 
    WHERE key LIKE 'bubbleId:%' 
    AND value LIKE '%"type":2%'
    LIMIT 1
""")

result = cursor.fetchone()
if result:
    data = json.loads(result[0])
    print(f"\n{'='*60}")
    print("Sample AI message structure:")
    print(f"{'='*60}")
    # Print just the keys and their types
    for key, value in sorted(data.items()):
        value_type = type(value).__name__
        if isinstance(value, list):
            value_desc = f"list[{len(value)}]"
        elif isinstance(value, dict):
            value_desc = f"dict with keys: {list(value.keys())[:5]}"
        elif isinstance(value, str) and len(value) > 100:
            value_desc = f"str[{len(value)} chars]"
        else:
            value_desc = repr(value)[:100]
        print(f"  {key}: {value_type} = {value_desc}")

# Check for console/log related fields
print(f"\n{'='*60}")
print("Messages with console/log fields:")
print(f"{'='*60}")

patterns = [
    ('consoleLogs', '%consoleLogs%'),
    ('console', '%console%'),
    ('logs', '%"logs"%'),
    ('lints', '%lints%'),
    ('errors', '%"errors"%'),
]

for field_name, pattern in patterns:
    cursor.execute(f"""
        SELECT COUNT(*) FROM cursorDiskKV 
        WHERE key LIKE 'bubbleId:%' 
        AND value LIKE ?
    """, (pattern,))
    count = cursor.fetchone()[0]
    print(f"  {field_name}: {count} messages")

conn.close()

print(f"\n{'='*60}")
print("ANALYSIS COMPLETE")
print(f"{'='*60}")

