#!/usr/bin/env python3
"""
Deep Analysis of Cursor Data Keys

This script decodes and analyzes the actual content of key values
to understand what data is available for analytics.
"""

import sqlite3
from pathlib import Path
import json
from datetime import datetime
from collections import defaultdict

CURSOR_BASE = Path.home() / 'AppData/Roaming/Cursor'

def decode_value(value):
    """Decode a database value."""
    if value is None:
        return None
    if isinstance(value, bytes):
        try:
            return json.loads(value.decode('utf-8'))
        except:
            try:
                return value.decode('utf-8')
            except:
                return f"<binary: {len(value)} bytes>"
    return value

def analyze_global_database():
    """Deep dive into global database keys."""
    print("=" * 80)
    print("DEEP ANALYSIS OF GLOBAL DATABASE KEYS")
    print("=" * 80)
    
    db_path = CURSOR_BASE / 'User/globalStorage/state.vscdb'
    conn = sqlite3.connect(str(db_path))
    cursor = conn.cursor()
    
    # 1. ANALYZE aiCodeTrackingLines (2.8MB - the biggest!)
    print("\n" + "=" * 80)
    print("1. aiCodeTrackingLines (2.8MB) - AI Code Generation Tracking")
    print("=" * 80)
    
    cursor.execute("SELECT value FROM ItemTable WHERE key = 'aiCodeTrackingLines'")
    result = cursor.fetchone()
    if result:
        data = decode_value(result[0])
        if isinstance(data, dict):
            print(f"Type: dict with {len(data)} keys")
            print(f"Top-level keys: {list(data.keys())[:20]}")
            
            # Sample some entries
            for i, (k, v) in enumerate(list(data.items())[:3]):
                print(f"\nSample entry {i+1}:")
                print(f"  Key: {k[:80]}...")
                if isinstance(v, dict):
                    print(f"  Value type: dict with keys {list(v.keys())}")
                elif isinstance(v, list):
                    print(f"  Value type: list with {len(v)} items")
                    if v:
                        print(f"  First item: {str(v[0])[:200]}")
                else:
                    print(f"  Value: {str(v)[:200]}")
        elif isinstance(data, list):
            print(f"Type: list with {len(data)} items")
            if data:
                print(f"First item structure: {data[0] if isinstance(data[0], dict) else type(data[0])}")
        else:
            print(f"Type: {type(data)}")
            print(f"Preview: {str(data)[:500]}")
    
    # 2. ANALYZE aiCodeTrackingScoredCommits
    print("\n" + "=" * 80)
    print("2. aiCodeTrackingScoredCommits - AI Contribution Scoring")
    print("=" * 80)
    
    cursor.execute("SELECT value FROM ItemTable WHERE key = 'aiCodeTrackingScoredCommits'")
    result = cursor.fetchone()
    if result:
        data = decode_value(result[0])
        if isinstance(data, dict):
            print(f"Type: dict with {len(data)} keys")
            print(f"Keys: {list(data.keys())[:20]}")
            for k, v in list(data.items())[:2]:
                print(f"\n  {k}: {str(v)[:300]}")
        else:
            print(f"Content: {str(data)[:500]}")
    
    # 3. ANALYZE terminal.history.entries.commands
    print("\n" + "=" * 80)
    print("3. terminal.history.entries.commands - Command History")
    print("=" * 80)
    
    cursor.execute("SELECT value FROM ItemTable WHERE key = 'terminal.history.entries.commands'")
    result = cursor.fetchone()
    if result:
        data = decode_value(result[0])
        if isinstance(data, list):
            print(f"Total commands: {len(data)}")
            print("\nLast 10 commands:")
            for cmd in data[-10:]:
                if isinstance(cmd, dict):
                    print(f"  - {cmd}")
                else:
                    print(f"  - {cmd[:80]}")
        elif isinstance(data, dict):
            print(f"Structure: {list(data.keys())}")
    
    # 4. ANALYZE history.recentlyOpenedPathsList
    print("\n" + "=" * 80)
    print("4. history.recentlyOpenedPathsList - Recent Projects/Files")
    print("=" * 80)
    
    cursor.execute("SELECT value FROM ItemTable WHERE key = 'history.recentlyOpenedPathsList'")
    result = cursor.fetchone()
    if result:
        data = decode_value(result[0])
        if isinstance(data, dict):
            print(f"Keys: {list(data.keys())}")
            entries = data.get('entries', [])
            print(f"Total entries: {len(entries)}")
            print("\nRecent 5:")
            for entry in entries[:5]:
                if 'folderUri' in entry:
                    print(f"  Folder: {entry['folderUri'][:70]}...")
                elif 'fileUri' in entry:
                    print(f"  File: {entry['fileUri'][:70]}...")
    
    # 5. ANALYZE cursorai/serverConfig
    print("\n" + "=" * 80)
    print("5. cursorai/serverConfig - AI Server Configuration")
    print("=" * 80)
    
    cursor.execute("SELECT value FROM ItemTable WHERE key = 'cursorai/serverConfig'")
    result = cursor.fetchone()
    if result:
        data = decode_value(result[0])
        if isinstance(data, dict):
            print(f"Keys: {list(data.keys())}")
            # Look for model info
            for k in ['models', 'model', 'defaultModel', 'availableModels']:
                if k in data:
                    print(f"\n{k}: {data[k]}")
    
    # 6. CHECK cursorDiskKV table
    print("\n" + "=" * 80)
    print("6. cursorDiskKV Table - Additional Cursor Storage")
    print("=" * 80)
    
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
    tables = [t[0] for t in cursor.fetchall()]
    print(f"Tables in database: {tables}")
    
    if 'cursorDiskKV' in tables:
        cursor.execute("SELECT * FROM cursorDiskKV LIMIT 20")
        rows = cursor.fetchall()
        print(f"\ncursorDiskKV rows (first 20):")
        for row in rows:
            print(f"  {row}")
    
    # 7. LOOK FOR CHAT/MODEL USAGE DATA
    print("\n" + "=" * 80)
    print("7. Searching for Chat/Model Usage Data")
    print("=" * 80)
    
    # Search for keys that might have chat/model data
    interesting_patterns = ['chat', 'model', 'token', 'usage', 'composer', 'agent', 'message', 'conversation']
    
    for pattern in interesting_patterns:
        cursor.execute("SELECT key, length(value) FROM ItemTable WHERE key LIKE ? ORDER BY length(value) DESC LIMIT 5", (f'%{pattern}%',))
        results = cursor.fetchall()
        if results:
            print(f"\nKeys matching '{pattern}':")
            for key, size in results:
                print(f"  [{size:>8} bytes] {key[:70]}")
    
    conn.close()


def analyze_workspace_databases():
    """Analyze workspace databases for chat data."""
    print("\n" + "=" * 80)
    print("WORKSPACE DATABASE ANALYSIS - Looking for Chat Data")
    print("=" * 80)
    
    ws_path = CURSOR_BASE / 'User/workspaceStorage'
    
    # Find workspaces with the largest composer data
    composer_data_sizes = []
    
    for ws in ws_path.iterdir():
        db_file = ws / 'state.vscdb'
        if not db_file.exists():
            continue
        
        try:
            conn = sqlite3.connect(str(db_file))
            cursor = conn.cursor()
            cursor.execute("SELECT length(value) FROM ItemTable WHERE key = 'composer.composerData'")
            result = cursor.fetchone()
            if result and result[0]:
                composer_data_sizes.append((ws, result[0]))
            conn.close()
        except:
            continue
    
    composer_data_sizes.sort(key=lambda x: x[1], reverse=True)
    
    print(f"\nWorkspaces with largest composer.composerData:")
    for ws, size in composer_data_sizes[:10]:
        # Get project name
        ws_json = ws / 'workspace.json'
        project = "Unknown"
        if ws_json.exists():
            try:
                with open(ws_json) as f:
                    data = json.load(f)
                project = data.get('folder', 'Unknown')
            except:
                pass
        print(f"  [{size:>8} bytes] {project[:60]}")
    
    # Deep dive into the largest one
    if composer_data_sizes:
        largest_ws = composer_data_sizes[0][0]
        print(f"\n--- Deep dive into largest workspace: {largest_ws.name} ---")
        
        conn = sqlite3.connect(str(largest_ws / 'state.vscdb'))
        cursor = conn.cursor()
        
        cursor.execute("SELECT value FROM ItemTable WHERE key = 'composer.composerData'")
        result = cursor.fetchone()
        
        if result:
            data = decode_value(result[0])
            if isinstance(data, dict):
                print(f"\ncomposer.composerData structure:")
                print(f"Top-level keys: {list(data.keys())}")
                
                # Analyze composers
                composers = data.get('allComposers', [])
                print(f"\nTotal composers (chats/agents): {len(composers)}")
                
                if composers:
                    print("\nAnalyzing composer structure:")
                    sample = composers[0] if composers else {}
                    if isinstance(sample, dict):
                        print(f"Composer keys: {list(sample.keys())}")
                        
                        # Look for messages
                        if 'messages' in sample:
                            msgs = sample['messages']
                            print(f"Messages in first composer: {len(msgs)}")
                            if msgs:
                                print(f"Message structure: {list(msgs[0].keys()) if isinstance(msgs[0], dict) else type(msgs[0])}")
                        
                        # Look for model info
                        for key in ['model', 'modelId', 'modelName', 'selectedModel']:
                            if key in sample:
                                print(f"{key}: {sample[key]}")
                    
                    # Count total messages across all composers
                    total_messages = 0
                    models_used = defaultdict(int)
                    for comp in composers:
                        if isinstance(comp, dict):
                            msgs = comp.get('messages', comp.get('conversation', []))
                            if isinstance(msgs, list):
                                total_messages += len(msgs)
                            
                            model = comp.get('model', comp.get('modelId', comp.get('selectedModel', 'unknown')))
                            if model:
                                models_used[model] += 1
                    
                    print(f"\nTotal messages across all composers: {total_messages}")
                    if models_used:
                        print(f"Models used: {dict(models_used)}")
        
        conn.close()


def analyze_for_year_wrapped():
    """Analyze what data we have for Year Wrapped style metrics."""
    print("\n" + "=" * 80)
    print("YEAR WRAPPED METRICS ANALYSIS")
    print("=" * 80)
    print("""
From the Cursor Year Wrapped image, we need:
1. Usage ranking (Top X%)
2. Models used (Claude 3.5 Sonnet, Auto, etc.)
3. Agent count (8K)
4. Tabs count (133)
5. Tokens used (3.99B)
6. Streak (20d consecutive)

Let's check what we can derive from local data:
""")
    
    db_path = CURSOR_BASE / 'User/globalStorage/state.vscdb'
    conn = sqlite3.connect(str(db_path))
    cursor = conn.cursor()
    
    # Check for usage/metrics keys
    print("\n1. Looking for usage/metrics data...")
    cursor.execute("SELECT key, length(value) FROM ItemTable WHERE key LIKE '%usage%' OR key LIKE '%metric%' OR key LIKE '%stat%' OR key LIKE '%count%'")
    for key, size in cursor.fetchall():
        print(f"  [{size:>8} bytes] {key}")
    
    # Check for token data
    print("\n2. Looking for token/billing data...")
    cursor.execute("SELECT key, length(value) FROM ItemTable WHERE key LIKE '%token%' OR key LIKE '%billing%' OR key LIKE '%credit%'")
    for key, size in cursor.fetchall():
        print(f"  [{size:>8} bytes] {key}")
    
    # Check for streak data
    print("\n3. Looking for streak/activity data...")
    cursor.execute("SELECT key, length(value) FROM ItemTable WHERE key LIKE '%streak%' OR key LIKE '%activity%' OR key LIKE '%daily%'")
    for key, size in cursor.fetchall():
        print(f"  [{size:>8} bytes] {key}")
    
    conn.close()
    
    print("""
\n--- ANALYSIS CONCLUSION ---

Based on exploration, here's what we CAN vs CANNOT get locally:

CAN GET (Local Data):
  [x] Chat/Agent history (composer.composerData per workspace)
  [x] AI code tracking (aiCodeTrackingLines - 2.8MB!)
  [x] Terminal command history
  [x] File edit history (2,600+ files)
  [x] Recently opened projects
  [x] Session logs (for activity patterns)

PROBABLY CAN'T GET (Server-side):
  [ ] Token usage (billing is server-side)
  [ ] Usage ranking (compared to other users)
  [ ] Exact model selection per request
  [ ] Streak data (may be server-calculated)

NEEDS MORE INVESTIGATION:
  [ ] Tab counts (might be in session data)
  [ ] Exact message counts with timestamps
  [ ] Model usage breakdown
""")


def main():
    analyze_global_database()
    analyze_workspace_databases()
    analyze_for_year_wrapped()
    
    print("\n" + "=" * 80)
    print("RECOMMENDATIONS FOR ANALYTICS")
    print("=" * 80)
    print("""
HIGH-VALUE ANALYTICS WE CAN BUILD:

1. CHAT ANALYTICS
   - Total chats/agents created
   - Messages per chat
   - Chat frequency over time
   - Longest conversations

2. CODE GENERATION ANALYTICS
   - Files modified by AI (from aiCodeTrackingLines)
   - Lines of code from AI
   - Most AI-edited file types

3. COMMAND LINE ANALYTICS
   - Most used commands
   - Command frequency
   - Common patterns

4. PROJECT ANALYTICS
   - Most active projects
   - Time spent per project (from logs)
   - Files edited per project

5. ACTIVITY PATTERNS
   - Active hours (from log timestamps)
   - Daily/weekly patterns
   - Session duration

6. FILE EDIT ANALYTICS
   - Most edited files
   - Edit frequency
   - File types worked on
""")


if __name__ == "__main__":
    main()

