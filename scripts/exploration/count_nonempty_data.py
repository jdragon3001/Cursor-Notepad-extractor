"""Count non-empty console logs, lints, and tool results."""

import sys
sys.stdout.reconfigure(encoding='utf-8')
sys.stderr.reconfigure(encoding='utf-8')

from pathlib import Path
import sqlite3
import json

print("=" * 60)
print("NON-EMPTY DATA COUNTS")
print("=" * 60)

db_path = Path.home() / "AppData" / "Roaming" / "Cursor" / "User" / "globalStorage" / "state.vscdb"
conn = sqlite3.connect(str(db_path))
cursor = conn.cursor()

# Count messages with non-empty arrays
fields_to_check = [
    ('consoleLogs', 'Console Logs'),
    ('lints', 'Lints'),
    ('toolResults', 'Tool Results'),
    ('multiFileLinterErrors', 'Multi-file Linter Errors'),
    ('toolFormerData', 'Tool Former Data'),
    ('approximateLintErrors', 'Approximate Lint Errors'),
]

for field_db, field_label in fields_to_check:
    cursor.execute(f"""
        SELECT COUNT(*) FROM cursorDiskKV 
        WHERE key LIKE 'bubbleId:%' 
        AND value LIKE '%"{field_db}":%'
        AND value NOT LIKE '%"{field_db}":[]%'
        AND value NOT LIKE '%"{field_db}":{{}}%'
    """)
    count = cursor.fetchone()[0]
    print(f"\n{field_label}: {count:,} messages")
    
    if count > 0 and count < 20:
        # Get samples if count is small
        cursor.execute(f"""
            SELECT value FROM cursorDiskKV 
            WHERE key LIKE 'bubbleId:%' 
            AND value LIKE '%"{field_db}":%'
            AND value NOT LIKE '%"{field_db}":[]%'
            AND value NOT LIKE '%"{field_db}":{{}}%'
            LIMIT 3
        """)
        print(f"  Sample structures:")
        for (value_bytes,) in cursor.fetchall():
            data = json.loads(value_bytes)
            field_data = data.get(field_db)
            if isinstance(field_data, list):
                print(f"    - Array with {len(field_data)} items")
                if field_data and len(field_data) > 0:
                    print(json.dumps(field_data[0], indent=6)[:300])
            elif isinstance(field_data, dict):
                print(f"    - Dict with keys: {list(field_data.keys())}")
                print(json.dumps(field_data, indent=6)[:300])
    elif count > 0:
        # Get one sample for larger counts
        cursor.execute(f"""
            SELECT value FROM cursorDiskKV 
            WHERE key LIKE 'bubbleId:%' 
            AND value LIKE '%"{field_db}":%'
            AND value NOT LIKE '%"{field_db}":[]%'
            AND value NOT LIKE '%"{field_db}":{{}}%'
            LIMIT 1
        """)
        result = cursor.fetchone()
        if result:
            data = json.loads(result[0])
            field_data = data.get(field_db)
            if isinstance(field_data, list):
                print(f"  Sample: Array with {len(field_data)} items")
                if field_data:
                    print(f"  First item keys: {list(field_data[0].keys()) if isinstance(field_data[0], dict) else type(field_data[0])}")
                    print(json.dumps(field_data[0], indent=4)[:400])
            elif isinstance(field_data, dict):
                print(f"  Sample: Dict with keys: {list(field_data.keys())}")
                print(json.dumps(field_data, indent=4)[:400])

conn.close()

print(f"\n{'='*60}")
print("COUNTS COMPLETE")
print(f"{'='*60}")

