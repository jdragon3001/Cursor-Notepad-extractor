"""Check aiCodeTrackingLines - this links code blocks to files!"""

import sqlite3
import json

db_path = r"C:\Users\jackw\AppData\Roaming\Cursor\User\globalStorage\state.vscdb"

conn = sqlite3.connect(db_path)
cursor = conn.cursor()

print("=== Checking aiCodeTrackingLines ===\n")

# Query for aiCodeTrackingLines
query = "SELECT value FROM ItemTable WHERE key = 'aiCodeTrackingLines' LIMIT 1"
rows = cursor.execute(query).fetchall()

if rows:
    data = json.loads(rows[0][0])
    print(f"Total tracking lines: {len(data)}\n")
    
    # Show first 3 examples
    for i, item in enumerate(data[:3]):
        print(f"\n{'='*60}")
        print(f"Tracking Line {i+1}")
        print(f"{'='*60}\n")
        print(f"Keys: {list(item.keys())}\n")
        print(json.dumps(item, indent=2))
        print("\n")
else:
    print("No aiCodeTrackingLines found")

conn.close()

