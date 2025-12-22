"""Comprehensive search for console logs."""

import sys
sys.stdout.reconfigure(encoding='utf-8')
sys.stderr.reconfigure(encoding='utf-8')

from pathlib import Path
import sqlite3
import json

# Check multiple locations
locations_to_check = [
    Path.home() / "AppData" / "Roaming" / "Cursor" / "logs",
    Path.home() / "AppData" / "Roaming" / "Cursor" / "User" / "logs",
    Path.home() / "AppData" / "Local" / "Cursor" / "logs",
]

print("=" * 60)
print("CONSOLE LOGS SEARCH")
print("=" * 60)

for location in locations_to_check:
    print(f"\nChecking: {location}")
    if location.exists():
        print("  ✓ EXISTS")
        files = list(location.glob("**/*"))
        log_files = [f for f in files if f.is_file() and ('.log' in f.name or 'console' in f.name.lower())]
        print(f"  Log files found: {len(log_files)}")
        if log_files:
            print(f"  Samples:")
            for log_file in log_files[:5]:
                print(f"    - {log_file.name} ({log_file.stat().st_size} bytes)")
    else:
        print("  ✗ NOT FOUND")

# Check database for console logs
print(f"\n{'='*60}")
print("DATABASE SEARCH")
print(f"{'='*60}")

db_path = Path.home() / "AppData" / "Roaming" / "Cursor" / "User" / "globalStorage" / "state.vscdb"
conn = sqlite3.connect(str(db_path))
cursor = conn.cursor()

# Search for console-related keys
patterns = ['%console%', '%log%', '%error%', '%warning%']
for pattern in patterns:
    cursor.execute(f"SELECT COUNT(*) FROM cursorDiskKV WHERE key LIKE ?", (pattern,))
    count = cursor.fetchone()[0]
    if count > 0:
        print(f"\nKeys matching '{pattern}': {count}")
        cursor.execute(f"SELECT key FROM cursorDiskKV WHERE key LIKE ? LIMIT 5", (pattern,))
        samples = cursor.fetchall()
        for key, in samples:
            print(f"  - {key}")

# Check ItemTable
cursor.execute("SELECT key FROM ItemTable WHERE key LIKE '%console%' OR key LIKE '%log%' LIMIT 10")
item_keys = cursor.fetchall()
if item_keys:
    print(f"\nItemTable keys with console/log:")
    for key, in item_keys:
        print(f"  - {key}")

# Check messages for console logs (the field we have in Message model)
cursor.execute("""
    SELECT COUNT(*) FROM cursorDiskKV 
    WHERE key LIKE 'bubbleId:%' 
    AND value LIKE '%consoleLogs%'
    AND value NOT LIKE '%"consoleLogs":[]%'
""")
count = cursor.fetchone()[0]
print(f"\n{'='*60}")
print(f"Messages with non-empty consoleLogs: {count}")
print(f"{'='*60}")

if count > 0:
    cursor.execute("""
        SELECT key, value FROM cursorDiskKV 
        WHERE key LIKE 'bubbleId:%' 
        AND value LIKE '%consoleLogs%'
        AND value NOT LIKE '%"consoleLogs":[]%'
        LIMIT 1
    """)
    result = cursor.fetchone()
    if result:
        key, value_bytes = result
        data = json.loads(value_bytes)
        console_logs = data.get('consoleLogs', [])
        print(f"\nSample consoleLogs:")
        print(json.dumps(console_logs[:2], indent=2)[:500])

conn.close()

print(f"\n{'='*60}")
print("SEARCH COMPLETE")
print(f"{'='*60}")

