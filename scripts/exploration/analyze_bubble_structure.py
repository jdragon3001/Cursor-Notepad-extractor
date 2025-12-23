import sys
sys.path.append('.')

import sqlite3
import json
from utils.config import Config

# Connect to DB
db_path = Config.get_global_db_path()
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# Get some bubble IDs from the same composer
cursor.execute("""
    SELECT key, value 
    FROM cursorDiskKV 
    WHERE key LIKE 'bubbleId:%' 
    LIMIT 30
""")

rows = cursor.fetchall()

print("=== Analyzing Message Structure ===\n")

current_composer = None
for key, value in rows:
    parts = key.split(':')
    composer_id = parts[1] if len(parts) > 1 else 'unknown'
    bubble_part = parts[2] if len(parts) > 2 else 'unknown'
    
    data = json.loads(value)
    msg_type = data.get('type', 0)
    has_text = bool(data.get('text'))
    has_thinking = bool(data.get('thinking'))
    has_tools = bool(data.get('toolResults'))
    created_at = data.get('createdAt', 'unknown')
    
    if composer_id != current_composer:
        if current_composer:
            print("\n" + "="*60 + "\n")
        print(f"SESSION: {composer_id[:20]}...")
        current_composer = composer_id
    
    print(f"\n  Bubble: ...{bubble_part[-10:]}")
    print(f"  Type: {'USER' if msg_type == 1 else 'AI'}")
    print(f"  Created: {created_at}")
    print(f"  Has text: {has_text} ({len(data.get('text', ''))} chars)")
    print(f"  Has thinking: {has_thinking}")
    print(f"  Has tools: {has_tools} ({len(data.get('toolResults', []))} tools)")
    print(f"  Has code: {len(data.get('codeBlocks', []))} blocks")

conn.close()

