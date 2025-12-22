#!/usr/bin/env python3
"""Deep analysis of cursorDiskKV table - where chat data lives!"""

import sqlite3
from pathlib import Path
import json
from collections import Counter

db_path = Path.home() / 'AppData/Roaming/Cursor/User/globalStorage/state.vscdb'
conn = sqlite3.connect(str(db_path))
cursor = conn.cursor()

print("=" * 70)
print("cursorDiskKV DEEP DIVE (119,521 rows!)")
print("=" * 70)

# Analyze key patterns
cursor.execute("SELECT key FROM cursorDiskKV")
all_keys = [r[0] for r in cursor.fetchall()]

# Categorize by prefix
prefixes = Counter()
for key in all_keys:
    if key is None:
        continue
    if ':' in key:
        prefix = key.split(':')[0]
    elif '-' in key:
        prefix = key.split('-')[0]
    else:
        prefix = key
    prefixes[prefix] += 1

print("\nKey prefixes (data categories):")
for prefix, count in prefixes.most_common(20):
    print(f"  {count:>6} x {prefix}")

print("\n" + "=" * 70)
print("SAMPLING composerData ENTRIES")
print("=" * 70)

# Get one non-null composerData entry with actual content
cursor.execute("SELECT key, value FROM cursorDiskKV WHERE key LIKE 'composerData:%' AND value IS NOT NULL AND length(value) > 100 LIMIT 1")
result = cursor.fetchone()

if result:
    key, val = result
    print(f"\nKey: {key}")
    try:
        data = json.loads(val)
        print(f"Top-level keys: {list(data.keys())}")
        
        # Look for messages/conversation
        for msg_key in ['conversation', 'messages', 'bubbles', 'chat']:
            if msg_key in data:
                conv = data[msg_key]
                if isinstance(conv, list):
                    print(f"\n{msg_key}: {len(conv)} items")
                    if conv:
                        item = conv[0]
                        if isinstance(item, dict):
                            print(f"  Item keys: {list(item.keys())}")
                            # Try to extract content
                            for ck in ['text', 'content', 'message', 'value']:
                                if ck in item:
                                    print(f"  {ck}: {str(item[ck])[:150]}...")
                                    break
        
        # Look for model info
        for model_key in ['richModelInfo', 'model', 'modelId', 'selectedModel']:
            if model_key in data:
                print(f"\n{model_key}: {data[model_key]}")
        
        # Show all top-level values (non-list/dict)
        print("\nOther fields:")
        for k, v in data.items():
            if not isinstance(v, (list, dict)):
                print(f"  {k}: {v}")
                
    except Exception as e:
        print(f"Error parsing: {e}")
        print(f"Raw preview: {val[:500]}")

print("\n" + "=" * 70)
print("ANALYZING ALL composerData FOR MODELS")
print("=" * 70)

cursor.execute("SELECT value FROM cursorDiskKV WHERE key LIKE 'composerData:%' AND value IS NOT NULL")
all_composers = cursor.fetchall()

models_used = Counter()
total_messages = 0
total_conversations = 0

for (val,) in all_composers:
    if not val:
        continue
    try:
        data = json.loads(val)
        total_conversations += 1
        
        # Count messages
        for msg_key in ['conversation', 'messages', 'bubbles']:
            if msg_key in data and isinstance(data[msg_key], list):
                total_messages += len(data[msg_key])
                break
        
        # Track models
        model_info = data.get('richModelInfo', {})
        if isinstance(model_info, dict):
            model_name = model_info.get('modelName', model_info.get('title', ''))
            if model_name:
                models_used[model_name] += 1
        
        # Also check direct model field
        model = data.get('model', data.get('modelId', ''))
        if model and not model_info:
            models_used[str(model)] += 1
            
    except:
        continue

print(f"\nTotal conversations analyzed: {total_conversations}")
print(f"Total messages found: {total_messages}")
print(f"\nModels used:")
for model, count in models_used.most_common(10):
    print(f"  {count:>5} x {model}")

print("\n" + "=" * 70)
print("CHECKING inlineDiffs DATA")
print("=" * 70)

cursor.execute("SELECT key, length(value) FROM cursorDiskKV WHERE key LIKE 'inlineDiffs%' ORDER BY length(value) DESC LIMIT 5")
for key, size in cursor.fetchall():
    print(f"  [{size:>8} bytes] {key}")

# Sample one inline diff
cursor.execute("SELECT value FROM cursorDiskKV WHERE key LIKE 'inlineDiffs%' AND value IS NOT NULL LIMIT 1")
result = cursor.fetchone()
if result and result[0]:
    try:
        data = json.loads(result[0])
        if isinstance(data, list) and data:
            print(f"\nInline diff structure (first item):")
            item = data[0]
            if isinstance(item, dict):
                print(f"  Keys: {list(item.keys())}")
    except:
        pass

conn.close()

print("\n" + "=" * 70)
print("MAJOR FINDINGS")
print("=" * 70)
print("""
1. cursorDiskKV contains 119,521 individual entries!
2. composerData entries have the actual chat conversations
3. Each conversation may have model info in 'richModelInfo'
4. inlineDiffs tracks AI code edits per workspace

This is WHERE THE GOLD IS for analytics!
""")

