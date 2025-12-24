"""Check toolFormerData structure."""

import sqlite3
import json

db_path = r"C:\Users\jackw\AppData\Roaming\Cursor\User\globalStorage\state.vscdb"

conn = sqlite3.connect(db_path)
cursor = conn.cursor()

print("=== Checking toolFormerData Structure ===\n")

# Query for messages with toolFormerData
query = "SELECT key, value FROM cursorDiskKV WHERE key LIKE 'bubbleId:%' AND value LIKE '%toolFormerData%' LIMIT 5"
rows = cursor.execute(query).fetchall()

print(f"Found {len(rows)} messages with toolFormerData\n")

for i, (key, value) in enumerate(rows):
    print(f"\n{'='*60}")
    print(f"Message {i+1}: {key.split(':')[-1][:20]}...")
    print(f"{'='*60}\n")
    
    try:
        data = json.loads(value)
        tool_former = data.get('toolFormerData')
        
        if tool_former:
            print(f"toolFormerData keys: {list(tool_former.keys())}\n")
            print("Full toolFormerData:")
            print(json.dumps(tool_former, indent=2))
            print("\n")
            break  # Just show first one
            
    except Exception as e:
        print(f"Error: {e}")

conn.close()

