#!/usr/bin/env python3
"""
FINAL COMPREHENSIVE CHECK
Make sure we haven't missed ANY data sources
"""

import sqlite3
from pathlib import Path
import json
from collections import defaultdict
from datetime import datetime

CURSOR_BASE = Path.home() / 'AppData/Roaming/Cursor'

def safe_json(val):
    if val is None: return None
    if isinstance(val, bytes):
        try: return json.loads(val.decode('utf-8'))
        except: return None
    if isinstance(val, str):
        try: return json.loads(val)
        except: return val
    return val

print("=" * 70)
print("FINAL COMPREHENSIVE DATA CHECK")
print("=" * 70)

db_path = CURSOR_BASE / 'User/globalStorage/state.vscdb'
conn = sqlite3.connect(str(db_path))
cursor = conn.cursor()

# 1. Check if there are ANY other tables we missed
print("\n### 1. ALL TABLES IN GLOBAL DATABASE ###")
cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
all_tables = cursor.fetchall()
print(f"Tables: {[t[0] for t in all_tables]}")

for table in all_tables:
    table_name = table[0]
    cursor.execute(f"SELECT COUNT(*) FROM {table_name}")
    count = cursor.fetchone()[0]
    cursor.execute(f"PRAGMA table_info({table_name})")
    columns = [c[1] for c in cursor.fetchall()]
    print(f"\n{table_name}:")
    print(f"  Rows: {count:,}")
    print(f"  Columns: {columns}")

# 2. Get EVERY key from ItemTable and categorize
print("\n" + "=" * 70)
print("### 2. ALL ItemTable KEYS (Categorized) ###")

cursor.execute("SELECT key, length(value) FROM ItemTable ORDER BY length(value) DESC")
all_keys = cursor.fetchall()

categories = {
    'chat': [],
    'ai': [],
    'terminal': [],
    'workspace': [],
    'settings': [],
    'auth': [],
    'tracking': [],
    'history': [],
    'other': []
}

keywords = {
    'chat': ['chat', 'bubble', 'composer', 'conversation', 'message'],
    'ai': ['ai', 'aiCode', 'model', 'gpt', 'claude'],
    'terminal': ['terminal', 'command', 'shell'],
    'workspace': ['workspace', 'panel', 'workbench', 'editor'],
    'settings': ['setting', 'config', 'preference'],
    'auth': ['auth', 'token', 'secret', 'github'],
    'tracking': ['tracking', 'stats', 'usage', 'metric'],
    'history': ['history', 'recent', 'mru']
}

for key, size in all_keys:
    categorized = False
    for cat, kwds in keywords.items():
        if any(kw in key.lower() for kw in kwds):
            categories[cat].append((key, size))
            categorized = True
            break
    if not categorized:
        categories['other'].append((key, size))

for cat, items in categories.items():
    if items:
        print(f"\n{cat.upper()} ({len(items)} keys):")
        for key, size in items[:10]:  # Top 10 per category
            print(f"  [{size:>8} bytes] {key[:60]}")
        if len(items) > 10:
            print(f"  ... and {len(items) - 10} more")

# 3. Check for conversation data in bubbleId
print("\n" + "=" * 70)
print("### 3. BUBBLE MESSAGE CONTENT CHECK ###")

cursor.execute("SELECT value FROM cursorDiskKV WHERE key LIKE 'bubbleId:%' LIMIT 100")
bubble_samples = cursor.fetchall()

text_count = 0
codeblocks_count = 0
thinking_count = 0
tool_results_count = 0

for (value,) in bubble_samples:
    data = safe_json(value)
    if data:
        if data.get('text'):
            text_count += 1
        if data.get('codeBlocks'):
            codeblocks_count += 1
        if data.get('thinking'):
            thinking_count += 1
        if data.get('toolResults'):
            tool_results_count += 1

print(f"Out of 100 sample bubbles:")
print(f"  - With text: {text_count}")
print(f"  - With codeBlocks: {codeblocks_count}")
print(f"  - With thinking: {thinking_count}")
print(f"  - With toolResults: {tool_results_count}")

# 4. Check agentKv - what is this really?
print("\n" + "=" * 70)
print("### 4. agentKv DATA INVESTIGATION ###")

cursor.execute("SELECT key FROM cursorDiskKV WHERE key LIKE 'agentKv:%'")
agent_keys = [k[0] for k in cursor.fetchall()]
print(f"Total agentKv entries: {len(agent_keys)}")

# Categorize agent keys
agent_types = defaultdict(int)
for key in agent_keys:
    parts = key.split(':')
    if len(parts) >= 2:
        agent_types[parts[1]] += 1

print("Agent key types:")
for atype, count in sorted(agent_types.items(), key=lambda x: x[1], reverse=True):
    print(f"  {atype}: {count}")

# Sample some agent data
cursor.execute("SELECT key, value FROM cursorDiskKV WHERE key LIKE 'agentKv:bubbleCheckpoint:%' LIMIT 3")
for key, value in cursor.fetchall():
    data = safe_json(value)
    if data and isinstance(data, dict):
        print(f"\nSample bubbleCheckpoint:")
        print(f"  Keys: {list(data.keys())[:10]}")

# 5. Check messageRequestContext
print("\n" + "=" * 70)
print("### 5. messageRequestContext INVESTIGATION ###")

cursor.execute("SELECT key, value FROM cursorDiskKV WHERE key LIKE 'messageRequestContext:%' LIMIT 3")
for key, value in cursor.fetchall():
    data = safe_json(value)
    if data and isinstance(data, dict):
        print(f"\nSample messageRequestContext:")
        print(f"  Keys: {list(data.keys())[:15]}")
        # Check if it has useful data
        for k in ['model', 'modelType', 'tokens', 'timestamp', 'context']:
            if k in data:
                print(f"  {k}: {str(data[k])[:100]}")

# 6. Check fullConversationHeadersOnly in composerData
print("\n" + "=" * 70)
print("### 6. CONVERSATION HEADERS CHECK ###")

cursor.execute("SELECT value FROM cursorDiskKV WHERE key LIKE 'composerData:%' LIMIT 10")
headers_found = 0
messages_in_headers = 0

for (value,) in cursor.fetchall():
    data = safe_json(value)
    if data and isinstance(data, dict):
        headers = data.get('fullConversationHeadersOnly', [])
        if headers and isinstance(headers, list):
            headers_found += 1
            messages_in_headers += len(headers)
            if headers_found == 1:  # Print first sample
                print("Sample fullConversationHeadersOnly:")
                for h in headers[:3]:
                    if isinstance(h, dict):
                        print(f"  {list(h.keys())}")

print(f"\nOut of 10 composerData samples:")
print(f"  - With conversation headers: {headers_found}")
print(f"  - Total message headers: {messages_in_headers}")

# 7. Check all timestamp fields
print("\n" + "=" * 70)
print("### 7. ALL TIMESTAMP FIELDS ###")

timestamp_fields = set()
cursor.execute("SELECT value FROM cursorDiskKV WHERE key LIKE 'bubbleId:%' LIMIT 500")
for (value,) in cursor.fetchall():
    data = safe_json(value)
    if data and isinstance(data, dict):
        for key, val in data.items():
            if 'time' in key.lower() or 'date' in key.lower() or 'at' in key.lower():
                if isinstance(val, (int, str)):
                    timestamp_fields.add(key)

print("Timestamp-related fields in bubbles:")
for field in sorted(timestamp_fields):
    print(f"  - {field}")

# 8. Check workspace for ALL keys
print("\n" + "=" * 70)
print("### 8. WORKSPACE DATABASE ALL KEYS ###")

ws_path = CURSOR_BASE / 'User/workspaceStorage'
all_ws_keys = set()

for ws in list(ws_path.iterdir())[:100]:
    db_file = ws / 'state.vscdb'
    if not db_file.exists():
        continue
    
    try:
        ws_conn = sqlite3.connect(str(db_file))
        ws_cursor = ws_conn.cursor()
        ws_cursor.execute("SELECT key FROM ItemTable")
        for (key,) in ws_cursor.fetchall():
            all_ws_keys.add(key)
        ws_conn.close()
    except:
        continue

print(f"Unique keys across 100 workspaces: {len(all_ws_keys)}")

# Categorize workspace keys
ws_categories = {
    'chat': [],
    'ai': [],
    'notepad': [],
    'terminal': [],
    'editor': [],
    'other': []
}

for key in all_ws_keys:
    if 'composer' in key.lower() or 'chat' in key.lower():
        ws_categories['chat'].append(key)
    elif 'ai' in key.lower():
        ws_categories['ai'].append(key)
    elif 'notepad' in key.lower():
        ws_categories['notepad'].append(key)
    elif 'terminal' in key.lower():
        ws_categories['terminal'].append(key)
    elif 'editor' in key.lower() or 'file' in key.lower():
        ws_categories['editor'].append(key)
    else:
        ws_categories['other'].append(key)

for cat, keys in ws_categories.items():
    if keys:
        print(f"\n{cat.upper()} ({len(keys)} keys):")
        for key in sorted(keys)[:15]:
            print(f"  - {key}")
        if len(keys) > 15:
            print(f"  ... and {len(keys) - 15} more")

# 9. Check for any SQLite databases we haven't explored
print("\n" + "=" * 70)
print("### 9. ALL SQLITE DATABASES ###")

all_dbs = []
for db_file in CURSOR_BASE.rglob('*.vscdb'):
    size = db_file.stat().st_size
    all_dbs.append((db_file, size))

all_dbs.sort(key=lambda x: x[1], reverse=True)

print(f"\nFound {len(all_dbs)} .vscdb files:")
for db, size in all_dbs[:20]:
    rel_path = db.relative_to(CURSOR_BASE)
    print(f"  {size / 1024 / 1024:>8.1f} MB  {rel_path}")

# 10. Final data inventory
conn.close()

print("\n" + "=" * 70)
print("COMPLETE DATA INVENTORY")
print("=" * 70)

print("""
DATABASE TABLES:
  - ItemTable (1,286 keys)
  - cursorDiskKV (119,605 rows)

KEY DATA STRUCTURES:
  cursorDiskKV:
    - bubbleId: 68,657 (messages with text, code, thinking)
    - composerData: 1,076 (session metadata, headers)
    - agentKv: 17,962 (agent state, checkpoints)
    - codeBlockDiff: 10,527 (code diffs)
    - checkpointId: 14,220 (session checkpoints)
    - messageRequestContext: 4,339 (request metadata)
  
  ItemTable:
    - aiCodeTrackingLines: 10,000 entries
    - aiCodeTracking.dailyStats: 28 days
    - aiCodeTrackingScoredCommits: 386 commits
    - terminal.history: command history
    - history.recentlyOpenedPathsList: recent projects
    - freeBestOfN.promptCount: 1,477 prompts

WORKSPACE DATABASES (245 total):
  - composer.composerData: per-workspace sessions
  - notepadData: notepad content
  - aiService.prompts: AI prompts
  - terminal: terminal state
  - editor state keys

FILE HISTORY (2,621 files):
  - User/History/{hash}/entries.json

OTHER:
  - WebStorage (1.3 GB)
  - Local Storage LevelDB
  - IndexedDB partitions
  - Backups folder
""")

print("\nNEXT STEPS:")
print("1. Build extractors for each data source")
print("2. Create unified data model")
print("3. Build export/analysis layer")
print("4. Create visualization dashboard")

