#!/usr/bin/env python3
"""Quick analysis of key data structures."""

import sqlite3
from pathlib import Path
import json

db_path = Path.home() / 'AppData/Roaming/Cursor/User/globalStorage/state.vscdb'
conn = sqlite3.connect(str(db_path))
cursor = conn.cursor()

print("=" * 70)
print("1. aiCodeTrackingLines (2.8MB) - What is this?")
print("=" * 70)

cursor.execute("SELECT value FROM ItemTable WHERE key = 'aiCodeTrackingLines'")
result = cursor.fetchone()
if result:
    val = result[0]
    data = json.loads(val.decode('utf-8') if isinstance(val, bytes) else val)
    print(f"Type: {type(data).__name__}")
    if isinstance(data, dict):
        print(f"Number of entries: {len(data)}")
        keys = list(data.keys())[:5]
        print(f"Sample keys:")
        for k in keys:
            print(f"  - {k[:80]}")
        
        # Analyze first entry
        first_key = list(data.keys())[0]
        first_val = data[first_key]
        print(f"\nFirst entry value type: {type(first_val).__name__}")
        if isinstance(first_val, list):
            print(f"  List length: {len(first_val)}")
            if first_val:
                print(f"  First item: {first_val[0]}")

print("\n" + "=" * 70)
print("2. cursorDiskKV Table - Hidden storage?")
print("=" * 70)

cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
tables = [t[0] for t in cursor.fetchall()]
print(f"All tables: {tables}")

if 'cursorDiskKV' in tables:
    cursor.execute("SELECT COUNT(*) FROM cursorDiskKV")
    count = cursor.fetchone()[0]
    print(f"cursorDiskKV has {count} rows")
    
    cursor.execute("PRAGMA table_info(cursorDiskKV)")
    cols = [c[1] for c in cursor.fetchall()]
    print(f"Columns: {cols}")
    
    cursor.execute("SELECT * FROM cursorDiskKV LIMIT 10")
    rows = cursor.fetchall()
    print("Sample rows:")
    for row in rows:
        key = row[0] if len(row) > 0 else "?"
        val_preview = str(row[1])[:100] if len(row) > 1 else "?"
        print(f"  Key: {key[:60]}")
        print(f"  Val: {val_preview}...")

print("\n" + "=" * 70)
print("3. Terminal Command History")
print("=" * 70)

cursor.execute("SELECT value FROM ItemTable WHERE key = 'terminal.history.entries.commands'")
result = cursor.fetchone()
if result:
    val = result[0]
    data = json.loads(val.decode('utf-8') if isinstance(val, bytes) else val)
    print(f"Type: {type(data).__name__}")
    if isinstance(data, list):
        print(f"Total commands: {len(data)}")
        print("Last 5 commands:")
        for cmd in data[-5:]:
            print(f"  - {cmd[:80] if isinstance(cmd, str) else cmd}")

print("\n" + "=" * 70)
print("4. Looking for Chat/Model Data in Global DB")
print("=" * 70)

# Search for chat-related keys
cursor.execute("SELECT key, length(value) FROM ItemTable WHERE key LIKE '%chat%' OR key LIKE '%composer%' ORDER BY length(value) DESC LIMIT 20")
results = cursor.fetchall()
print(f"Chat/Composer keys found: {len(results)}")
for key, size in results[:10]:
    print(f"  [{size:>6} bytes] {key[:60]}")

conn.close()

# Now check workspace databases for chat data
print("\n" + "=" * 70)
print("5. Workspace Chat Data (composer.composerData)")
print("=" * 70)

ws_path = Path.home() / 'AppData/Roaming/Cursor/User/workspaceStorage'
total_composers = 0
total_chats = 0

for ws in list(ws_path.iterdir())[:50]:  # Check first 50 workspaces
    db_file = ws / 'state.vscdb'
    if not db_file.exists():
        continue
    
    try:
        conn = sqlite3.connect(str(db_file))
        cursor = conn.cursor()
        cursor.execute("SELECT value FROM ItemTable WHERE key = 'composer.composerData'")
        result = cursor.fetchone()
        
        if result:
            val = result[0]
            data = json.loads(val.decode('utf-8') if isinstance(val, bytes) else val)
            composers = data.get('allComposers', [])
            total_composers += len(composers)
            
            for comp in composers:
                if isinstance(comp, dict):
                    msgs = comp.get('conversation', comp.get('messages', []))
                    if isinstance(msgs, list):
                        total_chats += len(msgs)
        
        conn.close()
    except:
        continue

print(f"Across 50 workspaces:")
print(f"  Total composer sessions: {total_composers}")
print(f"  Total messages: {total_chats}")

print("\n" + "=" * 70)
print("SUMMARY: What Data Can We Extract?")
print("=" * 70)
print("""
CONFIRMED AVAILABLE:
  [x] AI Code Tracking - Files modified by AI
  [x] Terminal Commands - Full command history  
  [x] Chat Sessions - Per-workspace composer data
  [x] Message History - Chat messages per session
  [x] File Edit History - 2,600+ files tracked
  [x] Recent Projects - Recently opened folders

NEEDS MORE EXPLORATION:
  [ ] Model selection per chat (check composer structure)
  [ ] Timestamps on messages (check message structure)
  [ ] Token counts (might be server-side only)
  
LIKELY SERVER-SIDE ONLY:
  [ ] Usage ranking vs other users
  [ ] Total token usage / billing
  [ ] Streak data
""")
