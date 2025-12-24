#!/usr/bin/env python3
"""
Find the EARLIEST entry dates in Cursor's database.
This will tell us when the data starts from.
"""

import sqlite3
from pathlib import Path
import json
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

def ts_to_date(ts):
    """Convert Unix milliseconds to readable date."""
    if ts is None or ts == 0:
        return None
    try:
        # Handle both seconds and milliseconds
        if ts > 1e12:  # Milliseconds
            return datetime.fromtimestamp(ts / 1000)
        else:  # Seconds
            return datetime.fromtimestamp(ts)
    except:
        return None

print("=" * 70)
print("FINDING EARLIEST ENTRIES IN CURSOR DATABASE")
print("=" * 70)

db_path = CURSOR_BASE / 'User/globalStorage/state.vscdb'
conn = sqlite3.connect(str(db_path))
cursor = conn.cursor()

# Track all timestamps found
all_timestamps = []

# 1. Check composerData entries
print("\n### 1. Checking composerData timestamps ###")
cursor.execute("SELECT key, value FROM cursorDiskKV WHERE key LIKE 'composerData:%'")
composer_timestamps = []

for key, value in cursor.fetchall():
    if not value:
        continue
    data = safe_json(value)
    if data and isinstance(data, dict):
        created = data.get('createdAt')
        if created and created > 0:
            composer_timestamps.append(created)
            all_timestamps.append(('composerData', created))

if composer_timestamps:
    earliest = min(composer_timestamps)
    latest = max(composer_timestamps)
    print(f"Total sessions with timestamps: {len(composer_timestamps)}")
    print(f"Earliest: {ts_to_date(earliest)} (ts: {earliest})")
    print(f"Latest: {ts_to_date(latest)} (ts: {latest})")

# 2. Check bubbleId entries
print("\n### 2. Checking bubbleId (message) timestamps ###")
cursor.execute("SELECT key, value FROM cursorDiskKV WHERE key LIKE 'bubbleId:%'")
bubble_timestamps = []

for key, value in cursor.fetchall():
    if not value:
        continue
    data = safe_json(value)
    if data and isinstance(data, dict):
        created = data.get('createdAt')
        # Handle both int and string timestamps
        if created:
            try:
                created = int(created) if isinstance(created, str) else created
                if created > 0:
                    bubble_timestamps.append(created)
                    all_timestamps.append(('bubbleId', created))
            except (ValueError, TypeError):
                pass

if bubble_timestamps:
    earliest = min(bubble_timestamps)
    latest = max(bubble_timestamps)
    print(f"Total messages with timestamps: {len(bubble_timestamps)}")
    print(f"Earliest: {ts_to_date(earliest)} (ts: {earliest})")
    print(f"Latest: {ts_to_date(latest)} (ts: {latest})")

# 3. Check aiCodeTrackingLines
print("\n### 3. Checking aiCodeTrackingLines timestamps ###")
cursor.execute("SELECT value FROM ItemTable WHERE key = 'aiCodeTrackingLines'")
result = cursor.fetchone()
if result and result[0]:
    data = safe_json(result[0])
    if data and isinstance(data, list):
        tracking_timestamps = []
        for entry in data:
            if isinstance(entry, dict):
                meta = entry.get('metadata', {})
                # Look for any timestamp fields
                for ts_field in ['timestamp', 'createdAt', 'date', 'time']:
                    ts = meta.get(ts_field)
                    if ts and ts > 0:
                        tracking_timestamps.append(ts)
                        all_timestamps.append(('aiCodeTracking', ts))
        
        if tracking_timestamps:
            print(f"Found {len(tracking_timestamps)} timestamps")
            print(f"Earliest: {ts_to_date(min(tracking_timestamps))}")
        else:
            print("No timestamps found in aiCodeTrackingLines metadata")
            # Print what fields ARE in metadata
            if data:
                first = data[0]
                if isinstance(first, dict):
                    print(f"Available metadata fields: {list(first.get('metadata', {}).keys())}")

conn.close()

# 4. Check workspace databases
print("\n### 4. Checking workspace database timestamps ###")
ws_path = CURSOR_BASE / 'User/workspaceStorage'
ws_timestamps = []

for ws in list(ws_path.iterdir()):
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
                        created = comp.get('createdAt')
                        if created and created > 0:
                            ws_timestamps.append(created)
                            all_timestamps.append(('workspace', created))
        
        ws_conn.close()
    except:
        continue

if ws_timestamps:
    earliest = min(ws_timestamps)
    latest = max(ws_timestamps)
    print(f"Total workspace sessions with timestamps: {len(ws_timestamps)}")
    print(f"Earliest: {ts_to_date(earliest)} (ts: {earliest})")
    print(f"Latest: {ts_to_date(latest)} (ts: {latest})")

# 5. Check file history
print("\n### 5. Checking file history timestamps ###")
history_path = CURSOR_BASE / 'User/History'
history_timestamps = []

if history_path.exists():
    for entry_dir in list(history_path.iterdir())[:500]:  # Sample 500
        entries_json = entry_dir / 'entries.json'
        if entries_json.exists():
            try:
                with open(entries_json, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                for entry in data.get('entries', []):
                    ts = entry.get('timestamp')
                    if ts and ts > 0:
                        history_timestamps.append(ts)
                        all_timestamps.append(('fileHistory', ts))
            except:
                continue

if history_timestamps:
    earliest = min(history_timestamps)
    latest = max(history_timestamps)
    print(f"Total file history entries with timestamps: {len(history_timestamps)}")
    print(f"Earliest: {ts_to_date(earliest)} (ts: {earliest})")
    print(f"Latest: {ts_to_date(latest)} (ts: {latest})")

# 6. Check lastUpdatedAt in composerData
print("\n### 6. Checking lastUpdatedAt timestamps ###")
conn = sqlite3.connect(str(db_path))
cursor = conn.cursor()
cursor.execute("SELECT value FROM cursorDiskKV WHERE key LIKE 'composerData:%'")

last_updated_timestamps = []
for (value,) in cursor.fetchall():
    if not value:
        continue
    data = safe_json(value)
    if data and isinstance(data, dict):
        last_updated = data.get('lastUpdatedAt')
        if last_updated and last_updated > 0:
            last_updated_timestamps.append(last_updated)

if last_updated_timestamps:
    earliest = min(last_updated_timestamps)
    latest = max(last_updated_timestamps)
    print(f"Earliest lastUpdatedAt: {ts_to_date(earliest)}")
    print(f"Latest lastUpdatedAt: {ts_to_date(latest)}")

conn.close()

# FINAL SUMMARY
print("\n" + "=" * 70)
print("FINAL SUMMARY: EARLIEST DATA FOUND")
print("=" * 70)

if all_timestamps:
    # Group by source
    by_source = {}
    for source, ts in all_timestamps:
        if source not in by_source:
            by_source[source] = []
        by_source[source].append(ts)
    
    print("\nEarliest timestamp by source:")
    overall_earliest = None
    overall_earliest_source = None
    
    for source, timestamps in sorted(by_source.items()):
        earliest = min(timestamps)
        date = ts_to_date(earliest)
        print(f"  {source}: {date}")
        if overall_earliest is None or earliest < overall_earliest:
            overall_earliest = earliest
            overall_earliest_source = source
    
    print(f"\n>>> OVERALL EARLIEST: {ts_to_date(overall_earliest)}")
    print(f">>> Source: {overall_earliest_source}")
    print(f">>> Raw timestamp: {overall_earliest}")
    
    # Calculate date range
    overall_latest = max(ts for _, ts in all_timestamps)
    earliest_date = ts_to_date(overall_earliest)
    latest_date = ts_to_date(overall_latest)
    
    if earliest_date and latest_date:
        days = (latest_date - earliest_date).days
        print(f"\n>>> Data spans {days} days")
        print(f">>> From: {earliest_date.strftime('%Y-%m-%d %H:%M:%S')}")
        print(f">>> To: {latest_date.strftime('%Y-%m-%d %H:%M:%S')}")
else:
    print("No timestamps found!")

# Check if there might be older data we're missing
print("\n" + "=" * 70)
print("POTENTIAL MISSING DATA CHECK")
print("=" * 70)

# Check database file modification times
print("\nDatabase file dates:")
global_db = CURSOR_BASE / 'User/globalStorage/state.vscdb'
if global_db.exists():
    mtime = datetime.fromtimestamp(global_db.stat().st_mtime)
    ctime = datetime.fromtimestamp(global_db.stat().st_ctime)
    print(f"  Global DB created: {ctime}")
    print(f"  Global DB modified: {mtime}")

# Check if there are backup folders
backups = CURSOR_BASE / 'Backups'
if backups.exists():
    print(f"\nBackup folder exists: {backups}")
    for item in list(backups.iterdir())[:5]:
        print(f"  - {item.name}")

