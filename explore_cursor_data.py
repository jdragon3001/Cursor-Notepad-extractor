#!/usr/bin/env python3
"""
Cursor Data Explorer - Discover all available data sources in Cursor IDE.
This script exhaustively maps out all data stored by Cursor.
"""

import sqlite3
from pathlib import Path
import json
import os
from collections import defaultdict

def explore_global_storage():
    """Explore the global state database."""
    print("\n" + "="*80)
    print("GLOBAL STATE DATABASE")
    print("="*80)
    
    db_path = Path.home() / 'AppData/Roaming/Cursor/User/globalStorage/state.vscdb'
    if not db_path.exists():
        print(f"NOT FOUND: {db_path}")
        return
        
    print(f"Path: {db_path}")
    print(f"Size: {db_path.stat().st_size:,} bytes")
    
    try:
        conn = sqlite3.connect(str(db_path))
        cursor = conn.cursor()
        
        # Get tables
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = cursor.fetchall()
        print(f"Tables: {[t[0] for t in tables]}")
        
        # Get all keys and their value sizes
        cursor.execute('SELECT key, length(value) as size FROM ItemTable ORDER BY size DESC')
        all_keys = cursor.fetchall()
        print(f"\nTotal keys: {len(all_keys)}")
        
        print("\n--- Top 50 Keys by Value Size ---")
        for key, size in all_keys[:50]:
            print(f"  [{size:>10,} bytes] {key[:80]}{'...' if len(key) > 80 else ''}")
        
        # Categorize keys by patterns
        patterns = defaultdict(list)
        for key, size in all_keys:
            if 'chat' in key.lower():
                patterns['CHAT'].append((key, size))
            elif 'composer' in key.lower():
                patterns['COMPOSER/AGENT'].append((key, size))
            elif 'notepad' in key.lower():
                patterns['NOTEPAD'].append((key, size))
            elif 'workbench' in key.lower():
                patterns['WORKBENCH'].append((key, size))
            elif 'terminal' in key.lower():
                patterns['TERMINAL'].append((key, size))
            elif 'history' in key.lower():
                patterns['HISTORY'].append((key, size))
            elif 'ai' in key.lower() or 'cursor' in key.lower():
                patterns['AI/CURSOR'].append((key, size))
            elif 'git' in key.lower():
                patterns['GIT'].append((key, size))
            elif 'edit' in key.lower():
                patterns['EDITS'].append((key, size))
                
        print("\n--- Keys by Category ---")
        for category, keys in sorted(patterns.items()):
            total_size = sum(s for _, s in keys)
            print(f"\n{category}: {len(keys)} keys, {total_size:,} bytes total")
            for key, size in keys[:5]:
                print(f"  [{size:>10,} bytes] {key[:70]}{'...' if len(key) > 70 else ''}")
            if len(keys) > 5:
                print(f"  ... and {len(keys) - 5} more")
        
        conn.close()
    except Exception as e:
        print(f"Error: {e}")


def explore_workspace_storage():
    """Explore workspace storage databases."""
    print("\n" + "="*80)
    print("WORKSPACE STORAGE DATABASES")
    print("="*80)
    
    workspace_path = Path.home() / 'AppData/Roaming/Cursor/User/workspaceStorage'
    if not workspace_path.exists():
        print(f"NOT FOUND: {workspace_path}")
        return
        
    workspaces = list(workspace_path.iterdir())
    print(f"Total workspaces: {len(workspaces)}")
    
    # Explore one workspace in detail
    key_patterns = defaultdict(int)
    total_keys = 0
    
    for ws in workspaces[:10]:  # Sample 10 workspaces
        db_file = ws / 'state.vscdb'
        if not db_file.exists():
            continue
            
        try:
            conn = sqlite3.connect(str(db_file))
            cursor = conn.cursor()
            cursor.execute('SELECT key FROM ItemTable')
            keys = cursor.fetchall()
            total_keys += len(keys)
            
            for (key,) in keys:
                key_patterns[key] += 1
                
            conn.close()
        except:
            continue
    
    print(f"\nSampled 10 workspaces, found {total_keys} total keys")
    print("\n--- Most Common Keys Across Workspaces ---")
    sorted_patterns = sorted(key_patterns.items(), key=lambda x: x[1], reverse=True)
    for key, count in sorted_patterns[:30]:
        print(f"  [{count:>3}x] {key[:80]}{'...' if len(key) > 80 else ''}")
    
    # Explore anysphere folder (Cursor-specific)
    print("\n--- Anysphere (Cursor AI) Folders ---")
    for ws in workspaces[:5]:
        anysphere = ws / 'anysphere.cursor-retrieval'
        if anysphere.exists():
            print(f"\n{ws.name}:")
            for f in anysphere.iterdir():
                print(f"  - {f.name} ({f.stat().st_size:,} bytes)")


def explore_history():
    """Explore file history."""
    print("\n" + "="*80)
    print("FILE HISTORY")
    print("="*80)
    
    history_path = Path.home() / 'AppData/Roaming/Cursor/User/History'
    if not history_path.exists():
        print(f"NOT FOUND: {history_path}")
        return
        
    entries = list(history_path.iterdir())
    print(f"Total history entries: {len(entries)}")
    
    # Sample some entries
    print("\n--- Sample History Entries ---")
    for entry in entries[:5]:
        entries_json = entry / 'entries.json'
        if entries_json.exists():
            try:
                with open(entries_json, 'r') as f:
                    data = json.load(f)
                resource = data.get('resource', 'Unknown')
                num_entries = len(data.get('entries', []))
                print(f"  {resource[:80]}...")
                print(f"    Versions: {num_entries}")
            except:
                continue


def explore_logs():
    """Explore log files for usage data."""
    print("\n" + "="*80)
    print("LOG FILES")
    print("="*80)
    
    logs_path = Path.home() / 'AppData/Roaming/Cursor/logs'
    if not logs_path.exists():
        print(f"NOT FOUND: {logs_path}")
        return
        
    sessions = sorted(logs_path.iterdir(), reverse=True)
    print(f"Total log sessions: {len(sessions)}")
    
    print("\n--- Log Types in Latest Session ---")
    latest = sessions[0] if sessions else None
    if latest:
        print(f"Session: {latest.name}")
        for item in latest.iterdir():
            if item.is_file():
                print(f"  - {item.name} ({item.stat().st_size:,} bytes)")
            elif item.is_dir():
                print(f"  - {item.name}/ (folder)")


def explore_single_workspace_deep(workspace_id=None):
    """Deep dive into a single workspace database."""
    print("\n" + "="*80)
    print("DEEP DIVE: SINGLE WORKSPACE")
    print("="*80)
    
    workspace_path = Path.home() / 'AppData/Roaming/Cursor/User/workspaceStorage'
    
    # Find a workspace with chat data
    for ws in workspace_path.iterdir():
        db_file = ws / 'state.vscdb'
        if not db_file.exists():
            continue
            
        try:
            conn = sqlite3.connect(str(db_file))
            cursor = conn.cursor()
            
            # Check for AI-related keys
            cursor.execute("SELECT key, length(value) FROM ItemTable WHERE key LIKE '%composer%' OR key LIKE '%chat%' OR key LIKE '%aiChat%'")
            ai_keys = cursor.fetchall()
            
            if ai_keys:
                print(f"\nWorkspace: {ws.name}")
                print(f"Database size: {db_file.stat().st_size:,} bytes")
                
                # Get workspace.json to see what project this is
                ws_json = ws / 'workspace.json'
                if ws_json.exists():
                    with open(ws_json) as f:
                        ws_data = json.load(f)
                    print(f"Folder: {ws_data.get('folder', 'Unknown')}")
                
                print(f"\nAI-related keys: {len(ai_keys)}")
                for key, size in ai_keys:
                    print(f"  [{size:>10,} bytes] {key}")
                    
                    # Try to peek at the content
                    if size > 0 and size < 100000:
                        cursor.execute("SELECT value FROM ItemTable WHERE key = ?", (key,))
                        value = cursor.fetchone()
                        if value:
                            try:
                                text = value[0].decode('utf-8') if isinstance(value[0], bytes) else value[0]
                                # Show structure if JSON
                                data = json.loads(text)
                                if isinstance(data, dict):
                                    print(f"    JSON keys: {list(data.keys())[:10]}")
                            except:
                                pass
                
                conn.close()
                break
                
        except Exception as e:
            continue


def main():
    print("="*80)
    print("CURSOR IDE DATA EXPLORATION")
    print("="*80)
    print("\nThis script maps all data sources available in Cursor IDE.")
    
    explore_global_storage()
    explore_workspace_storage()
    explore_history()
    explore_logs()
    explore_single_workspace_deep()
    
    print("\n" + "="*80)
    print("EXPLORATION COMPLETE")
    print("="*80)


if __name__ == "__main__":
    main()

