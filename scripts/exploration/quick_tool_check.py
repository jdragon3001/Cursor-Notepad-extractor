"""Directly query tool results from database."""

import sqlite3
import json

db_path = r"C:\Users\jackw\AppData\Roaming\Cursor\User\globalStorage\state.vscdb"

conn = sqlite3.connect(db_path)
cursor = conn.cursor()

print("=== Analyzing Tool Results Structure ===\n")

# Query for messages with toolResults
query = "SELECT key, value FROM cursorDiskKV WHERE key LIKE 'bubbleId:%' AND value LIKE '%toolResults%' LIMIT 5"
rows = cursor.execute(query).fetchall()

print(f"Found {len(rows)} messages with toolResults\n")

for i, (key, value) in enumerate(rows):
    print(f"\n{'='*60}")
    print(f"Message {i+1}: {key}")
    print(f"{'='*60}\n")
    
    try:
        data = json.loads(value)
        tool_results = data.get('toolResults', [])
        
        print(f"Tool results count: {len(tool_results)}\n")
        
        for j, tool in enumerate(tool_results[:3]):  # First 3 tools
            print(f"\n--- Tool {j+1} ---")
            print(f"Keys: {list(tool.keys())}")
            print(f"\nFull structure:")
            print(json.dumps(tool, indent=2))
            print("\n")
            
    except Exception as e:
        print(f"Error parsing: {e}")

conn.close()

