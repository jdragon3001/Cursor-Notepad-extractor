#!/usr/bin/env python3
"""Final deep analysis - bubbleId messages and aggregate stats."""

import sqlite3
from pathlib import Path
import json
from collections import Counter

db_path = Path.home() / 'AppData/Roaming/Cursor/User/globalStorage/state.vscdb'
conn = sqlite3.connect(str(db_path))
cursor = conn.cursor()

print("=" * 70)
print("EXPLORING bubbleId ENTRIES (68,542 messages!)")
print("=" * 70)

# Get a sample bubbleId entry
cursor.execute("""
    SELECT key, value FROM cursorDiskKV 
    WHERE key LIKE 'bubbleId:%' AND value IS NOT NULL 
    AND length(value) > 100 LIMIT 5
""")
results = cursor.fetchall()

for key, val in results:
    print(f"\nKey: {key}")
    try:
        data = json.loads(val)
        print(f"  Keys: {list(data.keys())[:15]}")
        
        # Show important fields
        for k in ['type', 'role', 'modelUsed', 'model', 'rawModelName', 'text']:
            if k in data:
                v = data[k]
                if isinstance(v, str) and len(v) > 100:
                    print(f"  {k}: {v[:100]}...")
                elif v:
                    print(f"  {k}: {v}")
    except:
        pass

print("\n" + "=" * 70)
print("CHECKING modelConfig IN composerData")
print("=" * 70)

cursor.execute("""
    SELECT value FROM cursorDiskKV 
    WHERE key LIKE 'composerData:%' AND value IS NOT NULL LIMIT 50
""")

model_configs = set()
for (val,) in cursor.fetchall():
    try:
        data = json.loads(val)
        mc = data.get('modelConfig')
        if mc:
            if isinstance(mc, dict):
                model_configs.add(str(mc.get('model', mc)))
            else:
                model_configs.add(str(mc))
    except:
        continue

print(f"Unique modelConfig values found: {model_configs}")

print("\n" + "=" * 70)
print("AGGREGATE STATISTICS FROM ALL SESSIONS")
print("=" * 70)

cursor.execute("SELECT value FROM cursorDiskKV WHERE key LIKE 'composerData:%' AND value IS NOT NULL")

total_tokens = 0
total_lines_added = 0
total_lines_removed = 0
session_count = 0
modes = Counter()
agent_sessions = 0
chat_sessions = 0

for (val,) in cursor.fetchall():
    try:
        data = json.loads(val)
        session_count += 1
        
        # Token usage
        tokens = data.get('contextTokensUsed', 0)
        if tokens:
            total_tokens += int(tokens)
        
        # Lines changed
        total_lines_added += data.get('totalLinesAdded', 0) or 0
        total_lines_removed += data.get('totalLinesRemoved', 0) or 0
        
        # Mode
        mode = data.get('unifiedMode', data.get('forceMode', 'unknown'))
        modes[mode] += 1
        
        if data.get('isAgentic'):
            agent_sessions += 1
        else:
            chat_sessions += 1
            
    except Exception as e:
        continue

print(f"\nSessions analyzed: {session_count:,}")
print(f"Total tokens used: {total_tokens:,}")
print(f"Total lines added by AI: {total_lines_added:,}")
print(f"Total lines removed by AI: {total_lines_removed:,}")
print(f"\nSession modes: {dict(modes)}")
print(f"Agent sessions: {agent_sessions:,}")
print(f"Chat sessions: {chat_sessions:,}")

print("\n" + "=" * 70)
print("BUBBLE/MESSAGE ANALYSIS")
print("=" * 70)

# Count bubbles by type
cursor.execute("SELECT value FROM cursorDiskKV WHERE key LIKE 'bubbleId:%' AND value IS NOT NULL LIMIT 10000")

bubble_types = Counter()
models_in_bubbles = Counter()
roles = Counter()

for (val,) in cursor.fetchall():
    try:
        data = json.loads(val)
        
        btype = data.get('type', 'unknown')
        bubble_types[btype] += 1
        
        role = data.get('role', data.get('type', 'unknown'))
        roles[role] += 1
        
        model = data.get('rawModelName', data.get('modelUsed', data.get('model', '')))
        if model:
            models_in_bubbles[str(model)] += 1
    except:
        continue

print(f"\nBubble types (from 10k sample):")
for t, count in bubble_types.most_common(10):
    print(f"  {count:>5} x {t}")

print(f"\nRoles:")
for r, count in roles.most_common(10):
    print(f"  {count:>5} x {r}")

print(f"\nModels used in messages:")
for m, count in models_in_bubbles.most_common(10):
    print(f"  {count:>5} x {m}")

conn.close()

print("\n" + "=" * 70)
print("SUMMARY: ANALYTICS WE CAN BUILD")
print("=" * 70)
print("""
FROM LOCAL DATA, WE CAN CALCULATE:

1. TOKEN USAGE
   - Total tokens across all sessions
   - Tokens per session
   - Token usage over time

2. CODE GENERATION METRICS
   - Total lines added by AI
   - Total lines removed
   - Net code contribution

3. SESSION ANALYTICS
   - Total chat/agent sessions
   - Agent vs Chat mode breakdown
   - Session duration (from timestamps)

4. MODEL USAGE (if models appear in bubbles)
   - Which models were used
   - Model usage frequency

5. MESSAGE COUNTS
   - Total messages sent/received
   - Messages per session
   - User vs AI message ratio

6. ACTIVITY PATTERNS
   - Sessions over time
   - Most active days/hours
   - Streak calculations (from timestamps)

WHAT WE PROBABLY CAN'T GET:
   - Billing/cost data (server-side)
   - Comparison to other users (server-side)
   - Exact API call logs
""")

