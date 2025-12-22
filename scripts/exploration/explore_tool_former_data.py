"""Deep dive into toolFormerData."""

import sys
sys.stdout.reconfigure(encoding='utf-8')
sys.stderr.reconfigure(encoding='utf-8')

from pathlib import Path
import sqlite3
import json
from collections import Counter

print("=" * 60)
print("TOOL FORMER DATA DEEP DIVE")
print("=" * 60)

db_path = Path.home() / "AppData" / "Roaming" / "Cursor" / "User" / "globalStorage" / "state.vscdb"
conn = sqlite3.connect(str(db_path))
cursor = conn.cursor()

cursor.execute("""
    SELECT value FROM cursorDiskKV 
    WHERE key LIKE 'bubbleId:%' 
    AND value LIKE '%"toolFormerData":%'
    AND value NOT LIKE '%"toolFormerData":{}%'
""")

all_statuses = []
all_additional_data_keys = set()
sample_data = []

for (value_bytes,) in cursor.fetchall():
    try:
        data = json.loads(value_bytes)
        tool_former = data.get('toolFormerData', {})
        additional_data = tool_former.get('additionalData', {})
        
        status = additional_data.get('status')
        if status:
            all_statuses.append(status)
        
        all_additional_data_keys.update(additional_data.keys())
        
        if len(sample_data) < 10:
            sample_data.append({
                'toolFormerData': tool_former,
                'messageType': data.get('type'),
                'hasText': bool(data.get('text', '').strip()),
                'hasThinking': bool(data.get('thinking')),
            })
    except json.JSONDecodeError:
        pass

print(f"\nTotal messages with toolFormerData: {len(all_statuses):,}")
print(f"\nStatus distribution:")
status_counts = Counter(all_statuses)
for status, count in status_counts.most_common():
    print(f"  {status}: {count:,} ({count/len(all_statuses)*100:.1f}%)")

print(f"\nAll keys found in additionalData:")
for key in sorted(all_additional_data_keys):
    print(f"  - {key}")

print(f"\n{'='*60}")
print("Sample toolFormerData structures:")
print(f"{'='*60}")
for i, sample in enumerate(sample_data[:5], 1):
    print(f"\nSample {i}:")
    print(json.dumps(sample, indent=2)[:500])

# Check if there are any other tool-related fields with actual data
print(f"\n{'='*60}")
print("Checking other tool-related fields:")
print(f"{'='*60}")

other_fields = [
    'supportedTools',
    'toolResults',
    'interpreterResults',
]

for field in other_fields:
    cursor.execute(f"""
        SELECT COUNT(*) FROM cursorDiskKV 
        WHERE key LIKE 'bubbleId:%' 
        AND value LIKE '%"{field}":%'
        AND value NOT LIKE '%"{field}":[]%'
    """)
    count = cursor.fetchone()[0]
    print(f"\n{field}: {count:,} non-empty")
    
    if count > 0 and count < 100:
        cursor.execute(f"""
            SELECT value FROM cursorDiskKV 
            WHERE key LIKE 'bubbleId:%' 
            AND value LIKE '%"{field}":%'
            AND value NOT LIKE '%"{field}":[]%'
            LIMIT 1
        """)
        result = cursor.fetchone()
        if result:
            data = json.loads(result[0])
            field_data = data.get(field)
            print(f"  Sample: {json.dumps(field_data, indent=4)[:400]}")

conn.close()

print(f"\n{'='*60}")
print("ANALYSIS COMPLETE")
print(f"{'='*60}")
