#!/usr/bin/env python3
"""
Comprehensive Cursor Data Source Explorer

This script systematically explores EVERY data source in Cursor IDE,
documents what each contains, and evaluates its potential value for analytics.

Run this to generate a complete data catalog.
"""

import sqlite3
from pathlib import Path
import json
import os
from datetime import datetime
from collections import defaultdict
import struct

CURSOR_BASE = Path.home() / 'AppData/Roaming/Cursor'


def decode_value(value):
    """Try to decode a value into readable format."""
    if value is None:
        return None, "null"
    
    if isinstance(value, str):
        try:
            return json.loads(value), "json"
        except:
            return value, "string"
    
    if isinstance(value, bytes):
        # Try UTF-8
        try:
            text = value.decode('utf-8')
            try:
                return json.loads(text), "json"
            except:
                return text, "string"
        except:
            pass
        
        # Try UTF-16
        try:
            text = value.decode('utf-16')
            return text, "utf16-string"
        except:
            pass
        
        return f"<binary: {len(value)} bytes>", "binary"
    
    return value, type(value).__name__


def truncate(s, max_len=200):
    """Truncate string for display."""
    s = str(s)
    if len(s) > max_len:
        return s[:max_len] + "..."
    return s


def explore_sqlite_database(db_path, output_file):
    """Explore a SQLite database and document all its contents."""
    output_file.write(f"\n{'='*80}\n")
    output_file.write(f"DATABASE: {db_path}\n")
    output_file.write(f"{'='*80}\n")
    
    if not db_path.exists():
        output_file.write("NOT FOUND\n")
        return {}
    
    output_file.write(f"Size: {db_path.stat().st_size:,} bytes\n")
    output_file.write(f"Modified: {datetime.fromtimestamp(db_path.stat().st_mtime)}\n\n")
    
    results = {
        'path': str(db_path),
        'size': db_path.stat().st_size,
        'tables': {},
        'interesting_keys': []
    }
    
    try:
        conn = sqlite3.connect(str(db_path))
        cursor = conn.cursor()
        
        # Get all tables
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = [t[0] for t in cursor.fetchall()]
        output_file.write(f"Tables: {tables}\n\n")
        
        for table in tables:
            output_file.write(f"\n--- TABLE: {table} ---\n")
            
            # Get schema
            cursor.execute(f"PRAGMA table_info({table})")
            schema = cursor.fetchall()
            columns = [col[1] for col in schema]
            output_file.write(f"Columns: {columns}\n")
            
            # Get row count
            cursor.execute(f"SELECT COUNT(*) FROM {table}")
            count = cursor.fetchone()[0]
            output_file.write(f"Rows: {count}\n")
            
            results['tables'][table] = {
                'columns': columns,
                'row_count': count,
                'sample_keys': []
            }
            
            # If it's a key-value table, explore the keys
            if 'key' in columns and 'value' in columns:
                # Get all keys with their value sizes
                cursor.execute(f"SELECT key, length(value) as size FROM {table} ORDER BY size DESC")
                all_keys = cursor.fetchall()
                
                output_file.write(f"\nAll {len(all_keys)} keys (sorted by value size):\n")
                
                for key, size in all_keys:
                    output_file.write(f"\n  KEY: {key}\n")
                    output_file.write(f"  Size: {size:,} bytes\n")
                    
                    # Try to decode and show sample
                    cursor.execute(f"SELECT value FROM {table} WHERE key = ?", (key,))
                    raw_value = cursor.fetchone()[0]
                    decoded, dtype = decode_value(raw_value)
                    
                    output_file.write(f"  Type: {dtype}\n")
                    
                    # Show structure for JSON
                    if dtype == "json" and isinstance(decoded, dict):
                        output_file.write(f"  JSON Structure: {list(decoded.keys())[:15]}\n")
                        
                        # For important-looking keys, show more detail
                        interesting_patterns = ['chat', 'composer', 'ai', 'history', 'terminal', 
                                              'notepad', 'edit', 'prompt', 'message', 'code']
                        if any(p in key.lower() for p in interesting_patterns):
                            output_file.write(f"  *** POTENTIALLY VALUABLE DATA ***\n")
                            # Show nested structure
                            for k, v in decoded.items():
                                if isinstance(v, dict):
                                    output_file.write(f"    .{k}: dict with keys {list(v.keys())[:10]}\n")
                                elif isinstance(v, list):
                                    output_file.write(f"    .{k}: list with {len(v)} items\n")
                                    if v and isinstance(v[0], dict):
                                        output_file.write(f"      Item keys: {list(v[0].keys())[:10]}\n")
                                else:
                                    output_file.write(f"    .{k}: {truncate(str(v), 50)}\n")
                            
                            results['interesting_keys'].append({
                                'key': key,
                                'size': size,
                                'structure': str(list(decoded.keys())[:10])
                            })
                    
                    elif dtype == "string":
                        output_file.write(f"  Preview: {truncate(decoded, 150)}\n")
                    
                    elif dtype == "binary":
                        output_file.write(f"  Content: {decoded}\n")
            
            else:
                # For non-KV tables, show sample rows
                cursor.execute(f"SELECT * FROM {table} LIMIT 5")
                rows = cursor.fetchall()
                output_file.write(f"\nSample rows:\n")
                for row in rows:
                    output_file.write(f"  {truncate(str(row), 200)}\n")
        
        conn.close()
        
    except Exception as e:
        output_file.write(f"ERROR: {e}\n")
    
    return results


def explore_json_file(file_path, output_file):
    """Explore a JSON file and document its structure."""
    output_file.write(f"\n{'='*80}\n")
    output_file.write(f"JSON FILE: {file_path}\n")
    output_file.write(f"{'='*80}\n")
    
    if not file_path.exists():
        output_file.write("NOT FOUND\n")
        return {}
    
    output_file.write(f"Size: {file_path.stat().st_size:,} bytes\n")
    output_file.write(f"Modified: {datetime.fromtimestamp(file_path.stat().st_mtime)}\n\n")
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        if isinstance(data, dict):
            output_file.write(f"Structure: dict with {len(data)} keys\n")
            output_file.write(f"Top-level keys: {list(data.keys())[:20]}\n\n")
            
            for key, value in data.items():
                output_file.write(f"\n  {key}:\n")
                if isinstance(value, dict):
                    output_file.write(f"    Type: dict with {len(value)} keys\n")
                    output_file.write(f"    Keys: {list(value.keys())[:10]}\n")
                elif isinstance(value, list):
                    output_file.write(f"    Type: list with {len(value)} items\n")
                    if value and isinstance(value[0], dict):
                        output_file.write(f"    Item structure: {list(value[0].keys())[:10]}\n")
                else:
                    output_file.write(f"    Value: {truncate(str(value), 100)}\n")
                    
        elif isinstance(data, list):
            output_file.write(f"Structure: list with {len(data)} items\n")
            if data and isinstance(data[0], dict):
                output_file.write(f"Item keys: {list(data[0].keys())}\n")
                
        return {'structure': 'json', 'keys': list(data.keys()) if isinstance(data, dict) else None}
        
    except Exception as e:
        output_file.write(f"ERROR: {e}\n")
        return {}


def explore_directory(dir_path, output_file, depth=0):
    """Explore a directory and list its contents."""
    indent = "  " * depth
    
    if not dir_path.exists():
        return
    
    items = list(dir_path.iterdir())
    output_file.write(f"{indent}{dir_path.name}/ ({len(items)} items)\n")
    
    for item in sorted(items)[:20]:  # Limit to 20 items
        if item.is_file():
            output_file.write(f"{indent}  - {item.name} ({item.stat().st_size:,} bytes)\n")
        elif item.is_dir() and depth < 2:
            explore_directory(item, output_file, depth + 1)
    
    if len(items) > 20:
        output_file.write(f"{indent}  ... and {len(items) - 20} more items\n")


def explore_leveldb(db_path, output_file):
    """Document a LevelDB database (requires additional library)."""
    output_file.write(f"\n{'='*80}\n")
    output_file.write(f"LEVELDB: {db_path}\n")
    output_file.write(f"{'='*80}\n")
    
    if not db_path.exists():
        output_file.write("NOT FOUND\n")
        return
    
    output_file.write("Note: LevelDB exploration requires 'plyvel' library.\n")
    output_file.write("Contents:\n")
    explore_directory(db_path, output_file)


def main():
    output_path = Path("CURSOR_DATA_CATALOG.md")
    
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write("# Cursor IDE Complete Data Catalog\n")
        f.write(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
        f.write("This document catalogs ALL data sources found in Cursor IDE.\n")
        f.write("Each source is explored and documented for potential analytics value.\n\n")
        
        f.write("## Table of Contents\n")
        f.write("1. Global State Database\n")
        f.write("2. Workspace Storage Databases\n")
        f.write("3. Local Storage (LevelDB)\n")
        f.write("4. Session Storage\n")
        f.write("5. File History\n")
        f.write("6. Log Files\n")
        f.write("7. Configuration Files\n")
        f.write("8. Cursor-Specific Data (Anysphere)\n\n")
        
        # 1. GLOBAL STATE DATABASE
        f.write("\n# 1. GLOBAL STATE DATABASE\n")
        f.write("Primary storage for global Cursor state.\n")
        global_db = CURSOR_BASE / 'User/globalStorage/state.vscdb'
        explore_sqlite_database(global_db, f)
        
        # 2. WORKSPACE STORAGE - Sample a few
        f.write("\n\n# 2. WORKSPACE STORAGE DATABASES\n")
        f.write("Per-workspace databases with project-specific data.\n")
        ws_path = CURSOR_BASE / 'User/workspaceStorage'
        
        if ws_path.exists():
            workspaces = list(ws_path.iterdir())
            f.write(f"\nTotal workspaces: {len(workspaces)}\n")
            f.write("Sampling 3 workspaces in detail...\n")
            
            # Find workspaces with substantial data
            ws_sizes = []
            for ws in workspaces:
                db = ws / 'state.vscdb'
                if db.exists():
                    ws_sizes.append((ws, db.stat().st_size))
            
            ws_sizes.sort(key=lambda x: x[1], reverse=True)
            
            for ws, size in ws_sizes[:3]:
                # Get workspace info
                ws_json = ws / 'workspace.json'
                if ws_json.exists():
                    with open(ws_json) as wf:
                        ws_data = json.load(wf)
                    f.write(f"\nWorkspace: {ws_data.get('folder', 'Unknown')}\n")
                
                explore_sqlite_database(ws / 'state.vscdb', f)
        
        # 3. LOCAL STORAGE (LevelDB)
        f.write("\n\n# 3. LOCAL STORAGE (LevelDB)\n")
        explore_leveldb(CURSOR_BASE / 'Local Storage/leveldb', f)
        
        # 4. SESSION STORAGE
        f.write("\n\n# 4. SESSION STORAGE\n")
        explore_leveldb(CURSOR_BASE / 'Session Storage', f)
        
        # 5. FILE HISTORY
        f.write("\n\n# 5. FILE HISTORY\n")
        history_path = CURSOR_BASE / 'User/History'
        if history_path.exists():
            entries = list(history_path.iterdir())
            f.write(f"Total history entries: {len(entries)}\n\n")
            
            f.write("Sample entries:\n")
            for entry in entries[:5]:
                entries_json = entry / 'entries.json'
                if entries_json.exists():
                    explore_json_file(entries_json, f)
        
        # 6. LOG FILES
        f.write("\n\n# 6. LOG FILES\n")
        logs_path = CURSOR_BASE / 'logs'
        if logs_path.exists():
            sessions = sorted(logs_path.iterdir(), reverse=True)
            f.write(f"Total log sessions: {len(sessions)}\n\n")
            
            # Explore latest session
            if sessions:
                latest = sessions[0]
                f.write(f"Latest session: {latest.name}\n")
                explore_directory(latest, f)
                
                # Sample a few log files
                for log_file in ['main.log', 'telemetry.log', 'terminal.log']:
                    log_path = latest / log_file
                    if log_path.exists() and log_path.stat().st_size > 0:
                        f.write(f"\n--- {log_file} (first 50 lines) ---\n")
                        try:
                            with open(log_path, 'r', encoding='utf-8', errors='ignore') as lf:
                                for i, line in enumerate(lf):
                                    if i >= 50:
                                        break
                                    f.write(line)
                        except:
                            pass
        
        # 7. CONFIGURATION FILES
        f.write("\n\n# 7. CONFIGURATION FILES\n")
        config_files = [
            CURSOR_BASE / 'User/settings.json',
            CURSOR_BASE / 'User/keybindings.json',
            CURSOR_BASE / 'User/globalStorage/storage.json',
        ]
        
        for config in config_files:
            if config.exists():
                explore_json_file(config, f)
        
        # 8. CURSOR-SPECIFIC DATA
        f.write("\n\n# 8. CURSOR-SPECIFIC DATA (Anysphere)\n")
        f.write("Cursor's AI-specific data storage.\n\n")
        
        # Check a few workspaces for anysphere data
        if ws_path.exists():
            for ws in list(ws_path.iterdir())[:5]:
                anysphere = ws / 'anysphere.cursor-retrieval'
                if anysphere.exists():
                    f.write(f"\nWorkspace: {ws.name}\n")
                    for item in anysphere.iterdir():
                        f.write(f"  - {item.name} ({item.stat().st_size:,} bytes)\n")
                        if item.stat().st_size < 10000:
                            try:
                                with open(item, 'r', encoding='utf-8') as af:
                                    content = af.read()
                                f.write(f"    Content preview: {truncate(content, 500)}\n")
                            except:
                                pass
        
        # SUMMARY
        f.write("\n\n# SUMMARY: POTENTIALLY VALUABLE DATA SOURCES\n")
        f.write("="*80 + "\n\n")
        f.write("""
Based on exploration, the most valuable data sources for analytics are:

## HIGH VALUE:
1. **composer.composerData** - Chat/Agent conversation data
2. **aiCodeTrackingLines** - AI code edits tracking (2.8MB!)
3. **aiCodeTrackingScoredCommits** - AI contribution scoring
4. **terminal.history.entries.commands** - Command history
5. **notepadData** - Notepad content
6. **history.recentlyOpenedPathsList** - Project/file access patterns

## MEDIUM VALUE:
7. **aiService.prompts** - AI prompts used
8. **File History** - Edit history per file (2600+ entries)
9. **Log files** - Session timing, telemetry
10. **workbench.auxiliarybar** - UI state/usage patterns

## NEEDS MORE EXPLORATION:
11. **Local Storage (LevelDB)** - May contain additional chat data
12. **cursorai/serverConfig** - AI configuration
13. **Session Storage** - Real-time session data

## For Year Wrapped Style Analytics:
- Total AI chats/agents used
- Most common prompts/questions
- Code lines generated/modified
- Terminal commands used
- Projects worked on
- Time patterns (daily/weekly)
- Model usage (Claude, GPT, etc.)
""")
    
    print(f"\n{'='*80}")
    print(f"CATALOG GENERATED: {output_path.absolute()}")
    print(f"{'='*80}")
    print(f"\nOpen {output_path} to see the complete data catalog.")


if __name__ == "__main__":
    main()

