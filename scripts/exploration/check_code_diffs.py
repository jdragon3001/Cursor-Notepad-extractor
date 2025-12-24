"""Check codeBlockDiff structure - this is where file edits are stored!"""

import sqlite3
import json

db_path = r"C:\Users\jackw\AppData\Roaming\Cursor\User\globalStorage\state.vscdb"

conn = sqlite3.connect(db_path)
cursor = conn.cursor()

print("=== Checking codeBlockDiff Structure ===\n")

# Query for codeBlockDiff entries
query = "SELECT key, value FROM cursorDiskKV WHERE key LIKE 'codeBlockDiff:%' LIMIT 3"
rows = cursor.execute(query).fetchall()

print(f"Found {len(rows)} codeBlockDiff entries\n")

for i, (key, value) in enumerate(rows):
    print(f"\n{'='*60}")
    print(f"Entry {i+1}: {key}")
    print(f"{'='*60}\n")
    
    try:
        data = json.loads(value)
        print(f"Keys: {list(data.keys())}\n")
        print("Full structure:")
        print(json.dumps(data, indent=2))
        print("\n\n")
            
    except Exception as e:
        print(f"Error: {e}")

conn.close()

