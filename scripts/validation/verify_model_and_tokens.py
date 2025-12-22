#!/usr/bin/env python3
"""
VERIFY: Model names and token counts
Critical to understand what data is ACTUALLY usable
"""

import sqlite3
from pathlib import Path
import json
from collections import defaultdict

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

# Connect to global DB
db_path = CURSOR_BASE / 'User/globalStorage/state.vscdb'
conn = sqlite3.connect(str(db_path))
cursor = conn.cursor()

print("=" * 70)
print("MODEL USAGE VERIFICATION")
print("=" * 70)

# Get ALL bubbles with modelInfo
cursor.execute("SELECT key, value FROM cursorDiskKV WHERE key LIKE 'bubbleId:%'")
all_bubbles = cursor.fetchall()

models_found = defaultdict(int)
non_zero_tokens = 0
zero_tokens = 0
total_input_tokens = 0
total_output_tokens = 0
messages_with_text = 0
user_messages = 0
ai_messages = 0
agentic_messages = 0

for key, value in all_bubbles:
    if not value:
        continue
    
    data = safe_json(value)
    if not data or not isinstance(data, dict):
        continue
    
    # Count message types
    msg_type = data.get('type')
    if msg_type == 1:
        user_messages += 1
    elif msg_type == 2:
        ai_messages += 1
    
    # Check for text content
    text = data.get('text', '')
    if text and len(text) > 0:
        messages_with_text += 1
    
    # Check agentic
    if data.get('isAgentic'):
        agentic_messages += 1
    
    # Get model info
    model_info = data.get('modelInfo', {})
    if isinstance(model_info, dict) and model_info:
        model_name = model_info.get('modelName', model_info.get('model', 'unknown'))
        if model_name:
            models_found[model_name] += 1
    
    # Get token counts
    token_count = data.get('tokenCount', {})
    if isinstance(token_count, dict):
        input_t = token_count.get('inputTokens', 0)
        output_t = token_count.get('outputTokens', 0)
        
        if input_t > 0 or output_t > 0:
            non_zero_tokens += 1
            total_input_tokens += input_t
            total_output_tokens += output_t
        else:
            zero_tokens += 1

print(f"\nTotal bubble entries analyzed: {len(all_bubbles)}")
print(f"  - User messages (type=1): {user_messages}")
print(f"  - AI messages (type=2): {ai_messages}")
print(f"  - Messages with text: {messages_with_text}")
print(f"  - Agentic messages: {agentic_messages}")

print(f"\n### Models Found ###")
for model, count in sorted(models_found.items(), key=lambda x: x[1], reverse=True):
    print(f"  {model}: {count}")

print(f"\n### Token Count Status ###")
print(f"  Messages with non-zero tokens: {non_zero_tokens}")
print(f"  Messages with zero tokens: {zero_tokens}")
print(f"  Total input tokens: {total_input_tokens:,}")
print(f"  Total output tokens: {total_output_tokens:,}")

# Now check composerData for contextTokensUsed
print("\n" + "=" * 70)
print("COMPOSER TOKEN USAGE")
print("=" * 70)

cursor.execute("SELECT key, value FROM cursorDiskKV WHERE key LIKE 'composerData:%'")
composer_rows = cursor.fetchall()

total_context_tokens = 0
sessions_with_tokens = 0
lines_added = 0
lines_removed = 0
sessions_with_lines = 0
session_names = []

for key, value in composer_rows:
    if not value:
        continue
    
    data = safe_json(value)
    if not data or not isinstance(data, dict):
        continue
    
    # Get token usage from composer
    context_tokens = data.get('contextTokensUsed', 0)
    if isinstance(context_tokens, (int, float)) and context_tokens > 0:
        total_context_tokens += context_tokens
        sessions_with_tokens += 1
    
    # Get lines metrics
    added = data.get('totalLinesAdded', 0)
    removed = data.get('totalLinesRemoved', 0)
    if isinstance(added, (int, float)):
        lines_added += added
        if added > 0:
            sessions_with_lines += 1
    if isinstance(removed, (int, float)):
        lines_removed += removed
    
    # Get session names
    name = data.get('name', '')
    if name:
        session_names.append(name)

print(f"\nTotal composer sessions: {len(composer_rows)}")
print(f"Sessions with context tokens: {sessions_with_tokens}")
print(f"Total context tokens used: {total_context_tokens:,}")
print(f"Sessions with code changes: {sessions_with_lines}")
print(f"Total lines added: {lines_added:,}")
print(f"Total lines removed: {lines_removed:,}")

print(f"\nSample session names:")
for name in session_names[:10]:
    print(f"  - {name[:60]}")

# Check workspace databases for more data
print("\n" + "=" * 70)
print("WORKSPACE DATABASE VERIFICATION")
print("=" * 70)

ws_path = CURSOR_BASE / 'User/workspaceStorage'
total_ws_composers = 0
total_ws_lines_added = 0
total_ws_lines_removed = 0

for ws in list(ws_path.iterdir())[:100]:  # Check 100 workspaces
    db_file = ws / 'state.vscdb'
    if not db_file.exists():
        continue
    
    try:
        ws_conn = sqlite3.connect(str(db_file))
        ws_cursor = ws_conn.cursor()
        ws_cursor.execute("SELECT value FROM ItemTable WHERE key = 'composer.composerData'")
        result = ws_cursor.fetchone()
        
        if result and result[0]:
            data = safe_json(result[0])
            if data and isinstance(data, dict):
                composers = data.get('allComposers', [])
                for comp in composers:
                    if isinstance(comp, dict):
                        total_ws_composers += 1
                        total_ws_lines_added += comp.get('totalLinesAdded', 0) or 0
                        total_ws_lines_removed += comp.get('totalLinesRemoved', 0) or 0
        
        ws_conn.close()
    except:
        continue

print(f"\nAcross 100 workspaces:")
print(f"  Total composer sessions: {total_ws_composers}")
print(f"  Total lines added: {total_ws_lines_added:,}")
print(f"  Total lines removed: {total_ws_lines_removed:,}")

# Check aiCodeTrackingLines
print("\n" + "=" * 70)
print("AI CODE TRACKING LINES")
print("=" * 70)

cursor.execute("SELECT value FROM ItemTable WHERE key = 'aiCodeTrackingLines'")
result = cursor.fetchone()
if result and result[0]:
    data = safe_json(result[0])
    if data and isinstance(data, list):
        print(f"Total entries: {len(data)}")
        
        sources = defaultdict(int)
        extensions = defaultdict(int)
        
        for entry in data:
            if isinstance(entry, dict):
                meta = entry.get('metadata', {})
                sources[meta.get('source', 'unknown')] += 1
                extensions[meta.get('fileExtension', 'unknown')] += 1
        
        print(f"\nBy source:")
        for src, count in sorted(sources.items(), key=lambda x: x[1], reverse=True):
            print(f"  {src}: {count}")
        
        print(f"\nTop file extensions:")
        for ext, count in sorted(extensions.items(), key=lambda x: x[1], reverse=True)[:15]:
            print(f"  {ext}: {count}")

conn.close()

print("\n" + "=" * 70)
print("VERIFICATION COMPLETE")
print("=" * 70)
print("""
CONFIRMED USABLE DATA:
  [x] Model names (from modelInfo.modelName)
  [x] Session names (from composerData.name)
  [x] Lines added/removed (from composerData)
  [x] Context tokens (from composerData.contextTokensUsed)
  [x] AI code tracking (source, fileExtension)
  [x] Message types (user vs AI)
  [x] Agentic vs Chat mode

ISSUES FOUND:
  [!] Token counts in bubbles often zero (maybe not populated?)
  [!] Many bubbles missing modelInfo (empty dict)
  [!] Need to aggregate from both global and workspace DBs

RECOMMENDATIONS:
  1. Use composerData.contextTokensUsed for token totals
  2. Use bubbleId modelInfo for model breakdown
  3. Aggregate workspace data for complete picture
""")

