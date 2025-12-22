#!/usr/bin/env python3
"""
COMPREHENSIVE CHAT DATA RECOVERY
=================================
Goal: Find ALL chat/conversation data across ALL sources including:
- Global cursorDiskKV table (Oct 2025+)
- Workspace databases (Nov 2024+)
- Backup folder
- Any other potential sources

This is critical for building the complete data extraction app.
"""

import sqlite3
from pathlib import Path
import json
from datetime import datetime
from collections import defaultdict
import os

CURSOR_BASE = Path.home() / 'AppData/Roaming/Cursor'
OUTPUT_DIR = Path("cursor-data-docs")

def safe_json(val):
    """Safely parse JSON from string or bytes."""
    if val is None: return None
    if isinstance(val, bytes):
        try: return json.loads(val.decode('utf-8'))
        except: return None
    if isinstance(val, str):
        try: return json.loads(val)
        except: return val
    return val

def ts_to_date(ts):
    """Convert Unix milliseconds to datetime."""
    if ts is None or ts == 0:
        return None
    try:
        if isinstance(ts, str):
            ts = int(ts)
        if ts > 1e12:  # Milliseconds
            return datetime.fromtimestamp(ts / 1000)
        else:  # Seconds
            return datetime.fromtimestamp(ts)
    except:
        return None

def scan_sqlite_for_chat_data(db_path, source_name):
    """Scan a SQLite database for any chat-related data."""
    results = {
        'source': source_name,
        'path': str(db_path),
        'tables': [],
        'chat_keys': [],
        'composer_data': [],
        'earliest_timestamp': None,
        'latest_timestamp': None,
        'total_sessions': 0,
        'total_messages': 0,
        'errors': []
    }
    
    try:
        conn = sqlite3.connect(str(db_path))
        cursor = conn.cursor()
        
        # Get all tables
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = [t[0] for t in cursor.fetchall()]
        results['tables'] = tables
        
        # Check ItemTable for chat data
        if 'ItemTable' in tables:
            cursor.execute("SELECT key, value FROM ItemTable WHERE key LIKE '%composer%' OR key LIKE '%chat%' OR key LIKE '%bubble%' OR key LIKE '%conversation%'")
            for key, value in cursor.fetchall():
                data = safe_json(value)
                if data:
                    results['chat_keys'].append({
                        'key': key,
                        'type': type(data).__name__,
                        'size': len(value) if value else 0
                    })
                    
                    # Extract composer data
                    if 'composerData' in key or 'composer.composerData' == key:
                        if isinstance(data, dict):
                            composers = data.get('allComposers', [data])
                            for comp in composers:
                                if isinstance(comp, dict):
                                    created = comp.get('createdAt')
                                    if created:
                                        results['composer_data'].append({
                                            'composerId': comp.get('composerId', comp.get('id', 'unknown')),
                                            'createdAt': created,
                                            'date': str(ts_to_date(created)),
                                            'name': comp.get('name', ''),
                                            'unifiedMode': comp.get('unifiedMode', ''),
                                            'totalLinesAdded': comp.get('totalLinesAdded', 0),
                                            'totalLinesRemoved': comp.get('totalLinesRemoved', 0),
                                            'hasMessages': bool(comp.get('conversation') or comp.get('bubbles') or comp.get('fullConversationHeadersOnly'))
                                        })
                                        results['total_sessions'] += 1
        
        # Check cursorDiskKV if exists
        if 'cursorDiskKV' in tables:
            # Count entries
            cursor.execute("SELECT COUNT(*) FROM cursorDiskKV WHERE key LIKE 'composerData:%'")
            composer_count = cursor.fetchone()[0]
            results['total_sessions'] += composer_count
            
            cursor.execute("SELECT COUNT(*) FROM cursorDiskKV WHERE key LIKE 'bubbleId:%'")
            results['total_messages'] = cursor.fetchone()[0]
            
            # Get timestamp range from composerData
            cursor.execute("SELECT value FROM cursorDiskKV WHERE key LIKE 'composerData:%'")
            for (value,) in cursor.fetchall():
                data = safe_json(value)
                if data and isinstance(data, dict):
                    created = data.get('createdAt')
                    if created:
                        try:
                            created = int(created) if isinstance(created, str) else created
                            if results['earliest_timestamp'] is None or created < results['earliest_timestamp']:
                                results['earliest_timestamp'] = created
                            if results['latest_timestamp'] is None or created > results['latest_timestamp']:
                                results['latest_timestamp'] = created
                        except:
                            pass
        
        # Calculate timestamp range from composer_data
        for comp in results['composer_data']:
            created = comp.get('createdAt')
            if created:
                try:
                    created = int(created) if isinstance(created, str) else created
                    if results['earliest_timestamp'] is None or created < results['earliest_timestamp']:
                        results['earliest_timestamp'] = created
                    if results['latest_timestamp'] is None or created > results['latest_timestamp']:
                        results['latest_timestamp'] = created
                except:
                    pass
        
        conn.close()
        
    except Exception as e:
        results['errors'].append(str(e))
    
    return results

def explore_backup_folder():
    """Explore the Cursor Backup folder for any recoverable data."""
    backup_path = CURSOR_BASE / 'Backups'
    results = {
        'exists': backup_path.exists(),
        'contents': [],
        'databases_found': [],
        'total_size': 0
    }
    
    if not backup_path.exists():
        return results
    
    for item in backup_path.iterdir():
        item_info = {
            'name': item.name,
            'is_dir': item.is_dir(),
            'size': 0,
            'contents': []
        }
        
        if item.is_dir():
            for sub_item in item.rglob('*'):
                if sub_item.is_file():
                    item_info['size'] += sub_item.stat().st_size
                    item_info['contents'].append(str(sub_item.relative_to(item)))
                    
                    # Check if it's a database
                    if sub_item.suffix in ['.vscdb', '.db', '.sqlite']:
                        results['databases_found'].append(str(sub_item))
        else:
            item_info['size'] = item.stat().st_size
            if item.suffix in ['.vscdb', '.db', '.sqlite']:
                results['databases_found'].append(str(item))
        
        results['contents'].append(item_info)
        results['total_size'] += item_info['size']
    
    return results

def main():
    print("=" * 70)
    print("COMPREHENSIVE CHAT DATA RECOVERY")
    print("=" * 70)
    print(f"Cursor base path: {CURSOR_BASE}")
    print(f"Output directory: {OUTPUT_DIR}")
    print()
    
    all_results = {
        'scan_time': datetime.now().isoformat(),
        'global_db': None,
        'workspace_dbs': [],
        'backup_folder': None,
        'summary': {
            'total_sessions': 0,
            'total_messages': 0,
            'earliest_date': None,
            'latest_date': None,
            'data_sources': []
        }
    }
    
    # 1. Scan global database
    print("### 1. Scanning Global Database ###")
    global_db = CURSOR_BASE / 'User/globalStorage/state.vscdb'
    if global_db.exists():
        results = scan_sqlite_for_chat_data(global_db, "Global Database")
        all_results['global_db'] = results
        print(f"  Tables: {results['tables']}")
        print(f"  Sessions: {results['total_sessions']}")
        print(f"  Messages: {results['total_messages']}")
        if results['earliest_timestamp']:
            print(f"  Earliest: {ts_to_date(results['earliest_timestamp'])}")
            print(f"  Latest: {ts_to_date(results['latest_timestamp'])}")
        all_results['summary']['data_sources'].append({
            'name': 'Global Database (cursorDiskKV)',
            'sessions': results['total_sessions'],
            'messages': results['total_messages'],
            'earliest': str(ts_to_date(results['earliest_timestamp'])) if results['earliest_timestamp'] else None,
            'latest': str(ts_to_date(results['latest_timestamp'])) if results['latest_timestamp'] else None
        })
    else:
        print("  Global database not found!")
    
    # 2. Scan ALL workspace databases
    print("\n### 2. Scanning ALL Workspace Databases ###")
    ws_path = CURSOR_BASE / 'User/workspaceStorage'
    workspace_count = 0
    total_ws_sessions = 0
    ws_earliest = None
    ws_latest = None
    
    if ws_path.exists():
        workspaces = list(ws_path.iterdir())
        print(f"  Found {len(workspaces)} workspace folders")
        
        for ws in workspaces:
            db_file = ws / 'state.vscdb'
            if not db_file.exists():
                continue
            
            workspace_count += 1
            results = scan_sqlite_for_chat_data(db_file, f"Workspace: {ws.name}")
            
            if results['total_sessions'] > 0 or results['composer_data']:
                all_results['workspace_dbs'].append(results)
                session_count = len(results['composer_data']) if results['composer_data'] else results['total_sessions']
                total_ws_sessions += session_count
                
                if results['earliest_timestamp']:
                    if ws_earliest is None or results['earliest_timestamp'] < ws_earliest:
                        ws_earliest = results['earliest_timestamp']
                    if ws_latest is None or results['latest_timestamp'] > ws_latest:
                        ws_latest = results['latest_timestamp']
        
        print(f"  Workspaces with data: {len(all_results['workspace_dbs'])}")
        print(f"  Total sessions in workspaces: {total_ws_sessions}")
        if ws_earliest:
            print(f"  Earliest workspace data: {ts_to_date(ws_earliest)}")
            print(f"  Latest workspace data: {ts_to_date(ws_latest)}")
        
        all_results['summary']['data_sources'].append({
            'name': 'Workspace Databases',
            'sessions': total_ws_sessions,
            'database_count': len(all_results['workspace_dbs']),
            'earliest': str(ts_to_date(ws_earliest)) if ws_earliest else None,
            'latest': str(ts_to_date(ws_latest)) if ws_latest else None
        })
    
    # 3. Explore Backup folder
    print("\n### 3. Exploring Backup Folder ###")
    backup_results = explore_backup_folder()
    all_results['backup_folder'] = backup_results
    
    if backup_results['exists']:
        print(f"  Backup folder exists!")
        print(f"  Total size: {backup_results['total_size'] / 1024 / 1024:.1f} MB")
        print(f"  Contents: {len(backup_results['contents'])} items")
        print(f"  Databases found: {len(backup_results['databases_found'])}")
        
        for db_path in backup_results['databases_found']:
            print(f"    - {db_path}")
            # Scan each backup database
            backup_db_results = scan_sqlite_for_chat_data(Path(db_path), f"Backup: {Path(db_path).name}")
            if backup_db_results['total_sessions'] > 0 or backup_db_results['composer_data']:
                print(f"      Sessions: {backup_db_results['total_sessions']}, Chat keys: {len(backup_db_results['chat_keys'])}")
                all_results['summary']['data_sources'].append({
                    'name': f'Backup: {Path(db_path).name}',
                    'sessions': backup_db_results['total_sessions'],
                    'path': db_path
                })
    else:
        print("  No backup folder found")
    
    # 4. Check for other potential data sources
    print("\n### 4. Checking Other Potential Sources ###")
    
    # Check Local Storage
    local_storage = CURSOR_BASE / 'Local Storage/leveldb'
    if local_storage.exists():
        print(f"  Local Storage exists: {local_storage}")
        ls_size = sum(f.stat().st_size for f in local_storage.iterdir() if f.is_file())
        print(f"    Size: {ls_size / 1024:.1f} KB")
        all_results['summary']['data_sources'].append({
            'name': 'Local Storage (LevelDB)',
            'path': str(local_storage),
            'size_kb': ls_size / 1024
        })
    
    # Check Session Storage
    session_storage = CURSOR_BASE / 'Session Storage'
    if session_storage.exists():
        print(f"  Session Storage exists: {session_storage}")
    
    # Check IndexedDB in Partitions
    partitions = CURSOR_BASE / 'Partitions'
    if partitions.exists():
        for partition in partitions.iterdir():
            idb = partition / 'IndexedDB'
            if idb.exists():
                print(f"  IndexedDB in {partition.name}")
    
    # 5. Calculate overall summary
    print("\n" + "=" * 70)
    print("SUMMARY")
    print("=" * 70)
    
    # Aggregate all timestamps
    all_earliest = None
    all_latest = None
    
    if all_results['global_db'] and all_results['global_db']['earliest_timestamp']:
        all_earliest = all_results['global_db']['earliest_timestamp']
        all_latest = all_results['global_db']['latest_timestamp']
    
    if ws_earliest:
        if all_earliest is None or ws_earliest < all_earliest:
            all_earliest = ws_earliest
        if all_latest is None or ws_latest > all_latest:
            all_latest = ws_latest
    
    all_results['summary']['earliest_date'] = str(ts_to_date(all_earliest)) if all_earliest else None
    all_results['summary']['latest_date'] = str(ts_to_date(all_latest)) if all_latest else None
    all_results['summary']['total_sessions'] = (
        (all_results['global_db']['total_sessions'] if all_results['global_db'] else 0) +
        total_ws_sessions
    )
    all_results['summary']['total_messages'] = (
        all_results['global_db']['total_messages'] if all_results['global_db'] else 0
    )
    
    print(f"\nTotal chat sessions found: {all_results['summary']['total_sessions']}")
    print(f"Total messages found: {all_results['summary']['total_messages']}")
    print(f"Earliest data: {all_results['summary']['earliest_date']}")
    print(f"Latest data: {all_results['summary']['latest_date']}")
    
    if all_earliest and all_latest:
        days = (ts_to_date(all_latest) - ts_to_date(all_earliest)).days
        print(f"Data span: {days} days")
    
    print("\nData sources found:")
    for source in all_results['summary']['data_sources']:
        print(f"  - {source['name']}")
        if 'earliest' in source and source['earliest']:
            print(f"    Range: {source['earliest']} to {source['latest']}")
        if 'sessions' in source:
            print(f"    Sessions: {source['sessions']}")
    
    # 6. Save detailed results
    OUTPUT_DIR.mkdir(exist_ok=True)
    
    # Save summary
    summary_file = OUTPUT_DIR / '10-CHAT-DATA-RECOVERY-REPORT.md'
    with open(summary_file, 'w', encoding='utf-8') as f:
        f.write("# Chat Data Recovery Report\n\n")
        f.write(f"**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
        f.write("## Executive Summary\n\n")
        f.write(f"- **Total Chat Sessions:** {all_results['summary']['total_sessions']}\n")
        f.write(f"- **Total Messages:** {all_results['summary']['total_messages']}\n")
        f.write(f"- **Earliest Data:** {all_results['summary']['earliest_date']}\n")
        f.write(f"- **Latest Data:** {all_results['summary']['latest_date']}\n")
        if all_earliest and all_latest:
            days = (ts_to_date(all_latest) - ts_to_date(all_earliest)).days
            f.write(f"- **Data Span:** {days} days\n")
        
        f.write("\n## Data Sources\n\n")
        f.write("| Source | Sessions | Date Range |\n")
        f.write("|--------|----------|------------|\n")
        for source in all_results['summary']['data_sources']:
            sessions = source.get('sessions', 'N/A')
            date_range = f"{source.get('earliest', 'N/A')} to {source.get('latest', 'N/A')}" if source.get('earliest') else "N/A"
            f.write(f"| {source['name']} | {sessions} | {date_range} |\n")
        
        f.write("\n## Critical Finding: Data Gap\n\n")
        f.write("The `cursorDiskKV` table in the global database only contains data from **October 2025**.\n")
        f.write("However, **workspace databases contain data from November 2024**.\n\n")
        f.write("### Implication\n\n")
        f.write("To get complete chat history, the data extraction app MUST:\n")
        f.write("1. Read from `cursorDiskKV` for recent data (Oct 2025+)\n")
        f.write("2. Read from individual workspace `state.vscdb` files for older data (Nov 2024+)\n")
        f.write("3. Check backup folder for any additional data\n")
        f.write("4. Deduplicate sessions that may appear in multiple sources\n\n")
        
        f.write("## Workspace Database Details\n\n")
        f.write(f"Found **{len(all_results['workspace_dbs'])}** workspace databases with chat data.\n\n")
        
        # Sort by earliest timestamp
        ws_with_dates = [(ws, ws.get('earliest_timestamp', float('inf'))) for ws in all_results['workspace_dbs'] if ws.get('composer_data')]
        ws_with_dates.sort(key=lambda x: x[1])
        
        f.write("### Workspaces by Date (Oldest First)\n\n")
        f.write("| Workspace | Sessions | Earliest | Latest |\n")
        f.write("|-----------|----------|----------|--------|\n")
        for ws, _ in ws_with_dates[:30]:  # Top 30
            earliest = ts_to_date(ws.get('earliest_timestamp'))
            latest = ts_to_date(ws.get('latest_timestamp'))
            session_count = len(ws.get('composer_data', []))
            ws_name = ws['source'].replace('Workspace: ', '')[:20]
            f.write(f"| `{ws_name}` | {session_count} | {earliest.strftime('%Y-%m-%d') if earliest else 'N/A'} | {latest.strftime('%Y-%m-%d') if latest else 'N/A'} |\n")
        
        f.write("\n## Recovery Strategy\n\n")
        f.write("```python\n")
        f.write("# Pseudocode for complete data extraction\n")
        f.write("def extract_all_chat_data():\n")
        f.write("    all_sessions = {}\n")
        f.write("    \n")
        f.write("    # 1. Extract from global cursorDiskKV (recent data)\n")
        f.write("    global_sessions = extract_from_cursorDiskKV(global_db)\n")
        f.write("    for session in global_sessions:\n")
        f.write("        all_sessions[session.id] = session\n")
        f.write("    \n")
        f.write("    # 2. Extract from ALL workspace databases (older data)\n")
        f.write("    for workspace in get_all_workspaces():\n")
        f.write("        ws_sessions = extract_from_workspace(workspace)\n")
        f.write("        for session in ws_sessions:\n")
        f.write("            if session.id not in all_sessions:\n")
        f.write("                all_sessions[session.id] = session\n")
        f.write("            else:\n")
        f.write("                # Merge/deduplicate\n")
        f.write("                all_sessions[session.id].merge(session)\n")
        f.write("    \n")
        f.write("    return all_sessions\n")
        f.write("```\n")
        
        f.write("\n## Data Quality Notes\n\n")
        f.write("### Global Database (cursorDiskKV)\n")
        f.write("- Contains: Full message content, model info, token counts\n")
        f.write("- Date range: October 2025 onwards\n")
        f.write("- 68,000+ message entries\n\n")
        
        f.write("### Workspace Databases\n")
        f.write("- Contains: Session metadata, some message headers\n")
        f.write("- Date range: November 2024 onwards\n")
        f.write("- May not have full message content for all sessions\n")
        f.write("- Has: composerId, createdAt, name, unifiedMode, lines added/removed\n\n")
        
        f.write("## Files Generated\n\n")
        f.write("- `10-CHAT-DATA-RECOVERY-REPORT.md` - This file\n")
        f.write("- `workspace_chat_data.json` - Raw workspace chat data\n")
    
    # Save raw workspace data
    workspace_data_file = OUTPUT_DIR / 'workspace_chat_data.json'
    with open(workspace_data_file, 'w', encoding='utf-8') as f:
        json.dump({
            'scan_time': all_results['scan_time'],
            'summary': all_results['summary'],
            'workspace_count': len(all_results['workspace_dbs']),
            'workspaces': [
                {
                    'path': ws['path'],
                    'sessions': ws.get('composer_data', []),
                    'earliest': str(ts_to_date(ws.get('earliest_timestamp'))) if ws.get('earliest_timestamp') else None,
                    'latest': str(ts_to_date(ws.get('latest_timestamp'))) if ws.get('latest_timestamp') else None
                }
                for ws in all_results['workspace_dbs']
            ]
        }, f, indent=2, default=str)
    
    print(f"\n\nReports saved to:")
    print(f"  - {summary_file}")
    print(f"  - {workspace_data_file}")


if __name__ == "__main__":
    main()

