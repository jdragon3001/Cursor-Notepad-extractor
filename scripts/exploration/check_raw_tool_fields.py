"""Check raw message data for tool-related fields."""

import sqlite3
import json
from pathlib import Path

db_path = Path.home() / "AppData" / "Roaming" / "Cursor" / "User" / "globalStorage" / "state.vscdb"
conn = sqlite3.connect(str(db_path))
cursor = conn.cursor()

print("=" * 60)
print("RAW MESSAGE TOOL FIELD ANALYSIS")
print("=" * 60)

# Get a few AI messages to check their structure
cursor.execute("""
    SELECT key, value FROM cursorDiskKV 
    WHERE key LIKE 'bubbleId:%' 
    LIMIT 100
""")

results = cursor.fetchall()

# Check for any tool-related fields
tool_fields_found = {}
messages_checked = 0

for key, value_bytes in results:
    try:
        value = json.loads(value_bytes)
        messages_checked += 1
        
        # Look for any field with "tool" in the name
        for field in value.keys():
            if 'tool' in field.lower():
                if field not in tool_fields_found:
                    tool_fields_found[field] = 0
                tool_fields_found[field] += 1
                
                # Show sample
                if tool_fields_found[field] <= 2:
                    print(f"\nFound field: {field}")
                    print(f"Sample value: {json.dumps(value[field], indent=2)[:300]}")
    except:
        pass

print(f"\n{'='*60}")
print(f"SUMMARY")
print(f"{'='*60}")
print(f"Messages checked: {messages_checked}")
print(f"Tool-related fields found: {tool_fields_found}")

conn.close()

