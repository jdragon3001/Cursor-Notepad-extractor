#!/usr/bin/env python3
"""Deep exploration of cursorDiskKV table - THE GOLDMINE!"""

import sqlite3
from pathlib import Path
import json
from collections import defaultdict
from datetime import datetime

db_path = Path.home() / 'AppData/Roaming/Cursor/User/globalStorage/state.vscdb'
conn = sqlite3.connect(str(db_path))
cursor = conn.cursor()

print("=" * 70)
print("cursorDiskKV TABLE DEEP DIVE")
print("=" * 70)

# Count by key prefix
cursor.execute("SELECT key FROM cursorDiskKV")
all_keys = [row[0] for row in cursor.fetchall()]

prefixes = defaultdict(int)
for key in all_keys:
    if key is None:
        prefixes['(null)'] += 1
        continue
    prefix = key.split(':')[0] if ':' in key else key.split('-')[0]
    prefixes[prefix] += 1

print(f"\nTotal rows: {len(all_keys)}")
print(f"\nKey types by prefix:")
for prefix, count in sorted(prefixes.items(), key=lambda x: x[1], reverse=True)[:20]:
    print(f"  {prefix}: {count}")

# Explore composerData entries (the chat data!)
print("\n" + "=" * 70)
print("COMPOSER DATA ANALYSIS (Chat Sessions)")
print("=" * 70)

cursor.execute("SELECT key, value FROM cursorDiskKV WHERE key LIKE 'composerData:%' AND value IS NOT NULL LIMIT 5")
rows = cursor.fetchall()

print(f"\nSample composerData entries:")
for key, value in rows:
    print(f"\n--- {key} ---")
    if value:
        try:
            data = json.loads(value)
            print(f"Keys: {list(data.keys())}")
            
            # Look for important fields
            if 'text' in data:
                text_preview = data['text'][:200] if data['text'] else "(empty)"
                print(f"Text: {text_preview}...")
            
            if 'conversation' in data:
                conv = data['conversation']
                print(f"Conversation messages: {len(conv) if isinstance(conv, list) else 'N/A'}")
                if conv and isinstance(conv, list) and conv:
                    print(f"  First message keys: {list(conv[0].keys()) if isinstance(conv[0], dict) else conv[0]}")
            
            if 'bubbles' in data:
                bubbles = data['bubbles']
                print(f"Bubbles (messages): {len(bubbles) if isinstance(bubbles, list) else 'N/A'}")
                if bubbles and isinstance(bubbles, list) and bubbles:
                    first_bubble = bubbles[0]
                    if isinstance(first_bubble, dict):
                        print(f"  Bubble keys: {list(first_bubble.keys())}")
                        if 'type' in first_bubble:
                            print(f"  Type: {first_bubble['type']}")
                        if 'modelType' in first_bubble:
                            print(f"  Model: {first_bubble['modelType']}")
            
            # Check for model info
            for model_key in ['model', 'modelType', 'selectedModel', 'currentModel']:
                if model_key in data:
                    print(f"{model_key}: {data[model_key]}")
                    
        except json.JSONDecodeError:
            print(f"(Not JSON: {value[:100]}...)")

# Count total messages and models used
print("\n" + "=" * 70)
print("AGGREGATE STATISTICS")
print("=" * 70)

cursor.execute("SELECT value FROM cursorDiskKV WHERE key LIKE 'composerData:%' AND value IS NOT NULL")
all_composer_data = cursor.fetchall()

total_bubbles = 0
total_conversations = 0
models_used = defaultdict(int)
message_types = defaultdict(int)

for (value,) in all_composer_data:
    if not value:
        continue
    try:
        data = json.loads(value)
        
        # Count bubbles (messages)
        bubbles = data.get('bubbles', [])
        if isinstance(bubbles, list):
            total_bubbles += len(bubbles)
            for bubble in bubbles:
                if isinstance(bubble, dict):
                    # Track model usage
                    model = bubble.get('modelType', bubble.get('model', 'unknown'))
                    if model:
                        models_used[model] += 1
                    # Track message types
                    msg_type = bubble.get('type', 'unknown')
                    message_types[msg_type] += 1
        
        # Count conversations
        conv = data.get('conversation', [])
        if isinstance(conv, list):
            total_conversations += len(conv)
            
    except:
        continue

print(f"\nTotal composer sessions with data: {len(all_composer_data)}")
print(f"Total bubbles (message turns): {total_bubbles}")
print(f"Total conversation messages: {total_conversations}")

print(f"\nModels used:")
for model, count in sorted(models_used.items(), key=lambda x: x[1], reverse=True):
    print(f"  {model}: {count}")

print(f"\nMessage types:")
for msg_type, count in sorted(message_types.items(), key=lambda x: x[1], reverse=True):
    print(f"  {msg_type}: {count}")

# Explore bubbleId entries (individual messages?)
print("\n" + "=" * 70)
print("BUBBLE DATA (Individual Messages)")
print("=" * 70)

cursor.execute("SELECT COUNT(*) FROM cursorDiskKV WHERE key LIKE 'bubbleId:%'")
bubble_count = cursor.fetchone()[0]
print(f"Total bubbleId entries: {bubble_count}")

cursor.execute("SELECT key, value FROM cursorDiskKV WHERE key LIKE 'bubbleId:%' AND value IS NOT NULL LIMIT 3")
for key, value in cursor.fetchall():
    print(f"\n--- {key} ---")
    if value:
        try:
            data = json.loads(value)
            print(f"Keys: {list(data.keys())}")
            if 'text' in data:
                print(f"Text preview: {data['text'][:150]}...")
            if 'type' in data:
                print(f"Type: {data['type']}")
            if 'modelType' in data:
                print(f"Model: {data['modelType']}")
        except:
            print(f"Raw: {value[:200]}...")

# Explore inline diffs
print("\n" + "=" * 70)
print("INLINE DIFFS (Code Changes)")
print("=" * 70)

cursor.execute("SELECT COUNT(*) FROM cursorDiskKV WHERE key LIKE 'inlineDiffs%'")
diff_count = cursor.fetchone()[0]
print(f"Total inlineDiff entries: {diff_count}")

cursor.execute("SELECT key, value FROM cursorDiskKV WHERE key LIKE 'inlineDiffs%' AND value IS NOT NULL LIMIT 2")
for key, value in cursor.fetchall():
    print(f"\n--- {key} ---")
    if value:
        try:
            data = json.loads(value)
            if isinstance(data, list):
                print(f"Number of diffs: {len(data)}")
                if data:
                    first = data[0]
                    print(f"Diff keys: {list(first.keys()) if isinstance(first, dict) else first}")
        except:
            print(f"Raw: {value[:200]}...")

conn.close()

print("\n" + "=" * 70)
print("SUMMARY: What We Found in cursorDiskKV")
print("=" * 70)
print("""
KEY DATA SOURCES DISCOVERED:

1. composerData:{uuid} - Chat session data
   - Contains: text, bubbles (messages), model info
   - Can extract: prompts, responses, model usage

2. bubbleId:{uuid} - Individual message data
   - Contains: message text, type, model used
   - Can extract: full conversation history

3. inlineDiffs-{workspace} - Code change data
   - Contains: diff information, file URIs
   - Can extract: AI-generated code changes

This is THE source for chat analytics!
""")

