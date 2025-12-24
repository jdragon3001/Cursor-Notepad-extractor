"""Check how code blocks link to codeBlockDiff entries."""

import sqlite3
import json

db_path = r"C:\Users\jackw\AppData\Roaming\Cursor\User\globalStorage\state.vscdb"

conn = sqlite3.connect(db_path)
cursor = conn.cursor()

print("=== Analyzing Code Block to Diff Linking ===\n")

# Get a message with code blocks
query = "SELECT key, value FROM cursorDiskKV WHERE key LIKE 'bubbleId:%' AND value LIKE '%codeBlocks%' LIMIT 3"
rows = cursor.execute(query).fetchall()

print(f"Found {len(rows)} messages with codeBlocks\n")

for i, (key, value) in enumerate(rows):
    try:
        data = json.loads(value)
        code_blocks = data.get('codeBlocks', [])
        
        if code_blocks:
            print(f"\n{'='*60}")
            print(f"Message: {key}")
            print(f"Code blocks count: {len(code_blocks)}")
            print(f"{'='*60}\n")
            
            for j, block in enumerate(code_blocks[:2]):  # First 2
                print(f"\nCode Block {j+1}:")
                print(f"Keys: {list(block.keys())}")
                print(f"\nSample:")
                print(json.dumps(block, indent=2)[:500])
                print("...\n")
            
            # Extract composer_id
            composer_id = key.split(':')[1]
            
            # Look for matching codeBlockDiff entries
            diff_query = f"SELECT key, value FROM cursorDiskKV WHERE key LIKE 'codeBlockDiff:{composer_id}:%' LIMIT 3"
            diff_rows = cursor.execute(diff_query).fetchall()
            
            print(f"\nFound {len(diff_rows)} codeBlockDiff entries for this session")
            
            if diff_rows and i == 0:  # Just show first example
                for dk, dv in diff_rows[:1]:
                    print(f"\nDiff key: {dk}")
                    diff_data = json.loads(dv)
                    print(f"Diff keys: {list(diff_data.keys())}")
            
            break  # Just show first message with details
            
    except Exception as e:
        print(f"Error: {e}")

conn.close()

