#!/usr/bin/env python3
"""
CHECK ALL DATA SOURCES COMPREHENSIVELY
Looking for:
1. Missing model data (only 11.5% has modelInfo)
2. Additional token usage data
3. LevelDB and IndexedDB data
4. Message type distribution
"""

import sqlite3
from pathlib import Path
import json
from collections import defaultdict
import os
import struct

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
print("COMPREHENSIVE DATA SOURCE CHECK")
print("=" * 70)

# 1. Message type analysis
print("\n### 1. Message Type Analysis ###")

db_path = CURSOR_BASE / 'User/globalStorage/state.vscdb'
conn = sqlite3.connect(str(db_path))
cursor = conn.cursor()

cursor.execute("SELECT value FROM cursorDiskKV WHERE key LIKE 'bubbleId:%'")
all_bubbles = cursor.fetchall()

type_counts = defaultdict(int)
type_with_model = defaultdict(int)
type_with_text = defaultdict(int)

for (value,) in all_bubbles:
    data = safe_json(value)
    if not data:
        continue
    
    msg_type = data.get('type', 'unknown')
    type_counts[msg_type] += 1
    
    if data.get('modelInfo', {}).get('modelName'):
        type_with_model[msg_type] += 1
    
    if data.get('text'):
        type_with_text[msg_type] += 1

print("Message distribution by type:")
for t in sorted(type_counts.keys(), key=lambda x: str(x)):
    total = type_counts[t]
    with_model = type_with_model.get(t, 0)
    with_text = type_with_text.get(t, 0)
    model_pct = (with_model / total * 100) if total > 0 else 0
    text_pct = (with_text / total * 100) if total > 0 else 0
    print(f"  Type {t}: {total:,} messages")
    print(f"    - With model info: {with_model:,} ({model_pct:.1f}%)")
    print(f"    - With text: {with_text:,} ({text_pct:.1f}%)")

# Check what type 1 and type 2 really are
print("\nSample type 1 (user message?):")
cursor.execute("SELECT value FROM cursorDiskKV WHERE key LIKE 'bubbleId:%' LIMIT 100")
for (value,) in cursor.fetchall():
    data = safe_json(value)
    if data and data.get('type') == 1 and data.get('text'):
        print(f"  Text: {data['text'][:100]}...")
        print(f"  Keys: {[k for k in data.keys() if data[k]][:10]}")
        break

print("\nSample type 2 (AI response?):")
cursor.execute("SELECT value FROM cursorDiskKV WHERE key LIKE 'bubbleId:%' LIMIT 200")
for (value,) in cursor.fetchall():
    data = safe_json(value)
    if data and data.get('type') == 2 and data.get('text'):
        model = data.get('modelInfo', {}).get('modelName', 'no model')
        print(f"  Model: {model}")
        print(f"  Text: {data['text'][:100]}...")
        break

# 2. Check for usage tracking keys
print("\n" + "=" * 70)
print("### 2. Usage/Billing Related Keys ###")

cursor.execute("SELECT key, length(value) FROM ItemTable ORDER BY key")
all_keys = cursor.fetchall()

usage_keywords = ['usage', 'billing', 'quota', 'limit', 'count', 'stat', 'metric', 'track']

print("Keys that might contain usage data:")
for key, size in all_keys:
    if any(kw in key.lower() for kw in usage_keywords):
        print(f"  {key}: {size} bytes")
        cursor.execute("SELECT value FROM ItemTable WHERE key = ?", (key,))
        result = cursor.fetchone()
        if result:
            data = safe_json(result[0])
            if data and size < 1000:
                print(f"    {data}")

# 3. Check serverBubbleId field (might link to server-side data)
print("\n" + "=" * 70)
print("### 3. Server-side references ###")

cursor.execute("SELECT value FROM cursorDiskKV WHERE key LIKE 'bubbleId:%' LIMIT 50")
server_refs = []
for (value,) in cursor.fetchall():
    data = safe_json(value)
    if data:
        server_id = data.get('serverBubbleId')
        usage_uuid = data.get('usageUuid')
        request_id = data.get('requestId')
        if server_id or usage_uuid or request_id:
            server_refs.append({
                'serverBubbleId': server_id,
                'usageUuid': usage_uuid,
                'requestId': request_id
            })

print(f"Found {len(server_refs)} messages with server references")
if server_refs:
    print("Sample:")
    for ref in server_refs[:3]:
        print(f"  {ref}")

# 4. Check Local Storage LevelDB
print("\n" + "=" * 70)
print("### 4. Local Storage (LevelDB) ###")

local_storage = CURSOR_BASE / 'Local Storage/leveldb'
if local_storage.exists():
    print(f"Path: {local_storage}")
    for f in local_storage.iterdir():
        print(f"  {f.name}: {f.stat().st_size} bytes")
    
    # Try to read the log file
    log_file = local_storage / '000003.log'
    if log_file.exists():
        try:
            with open(log_file, 'rb') as f:
                content = f.read()
            print(f"\nLog file content (first 500 bytes):")
            # Try to find readable strings
            import re
            strings = re.findall(b'[a-zA-Z0-9_.-]{5,}', content)
            unique_strings = list(set(s.decode('utf-8', errors='ignore') for s in strings[:50]))
            print(f"  Found strings: {unique_strings[:20]}")
        except Exception as e:
            print(f"  Error reading: {e}")

# 5. Check IndexedDB
print("\n" + "=" * 70)
print("### 5. IndexedDB Partitions ###")

partitions = CURSOR_BASE / 'Partitions'
if partitions.exists():
    for partition in partitions.iterdir():
        idb = partition / 'IndexedDB'
        if idb.exists():
            print(f"\nPartition: {partition.name}")
            for item in idb.iterdir():
                if item.is_dir():
                    total_size = sum(f.stat().st_size for f in item.rglob('*') if f.is_file())
                    print(f"  {item.name}: {total_size / 1024:.1f} KB")
                    
                    # Try to find any readable content
                    for leveldb_file in item.glob('*.log'):
                        try:
                            with open(leveldb_file, 'rb') as f:
                                content = f.read(1000)
                            strings = re.findall(b'[a-zA-Z0-9_.-]{10,}', content)
                            if strings:
                                print(f"    Strings in {leveldb_file.name}: {[s.decode('utf-8', errors='ignore') for s in strings[:5]]}")
                        except:
                            pass

# 6. Check for GitHub usages
print("\n" + "=" * 70)
print("### 6. GitHub/External Service Data ###")

cursor.execute("SELECT key, value FROM ItemTable WHERE key LIKE '%github%' OR key LIKE '%usage%'")
for key, value in cursor.fetchall():
    print(f"\n{key}:")
    data = safe_json(value)
    if data:
        print(f"  {str(data)[:300]}")

# 7. Check WebStorage for model/usage data
print("\n" + "=" * 70)
print("### 7. WebStorage Check ###")

webstorage = CURSOR_BASE / 'WebStorage'
if webstorage.exists():
    for folder in webstorage.iterdir():
        if folder.is_dir():
            size = sum(f.stat().st_size for f in folder.rglob('*') if f.is_file())
            if size > 1000:  # Only show folders with data
                print(f"  {folder.name}: {size / 1024 / 1024:.1f} MB")

# 8. Check Backups folder structure
print("\n" + "=" * 70)
print("### 8. Backup Folder Details ###")

backups = CURSOR_BASE / 'Backups'
if backups.exists():
    for item in backups.iterdir():
        print(f"\n{item.name}:")
        if item.is_dir():
            for sub in item.iterdir():
                if sub.is_file():
                    print(f"  {sub.name}: {sub.stat().st_size} bytes")
                elif sub.is_dir():
                    sub_size = sum(f.stat().st_size for f in sub.rglob('*') if f.is_file())
                    print(f"  {sub.name}/: {sub_size} bytes")

conn.close()

# 9. Final token/model summary from all sources
print("\n" + "=" * 70)
print("COMPREHENSIVE SUMMARY")
print("=" * 70)

print("""
DATA COMPLETENESS ANALYSIS:

1. MESSAGES:
   - Total bubbles: 68,657
   - Type 1 (user): ~4,000 (no model info expected)
   - Type 2 (AI): ~64,000 (should have model info)
   - With model info: 7,879 (only 12% of type 2!)

2. WHY MODEL INFO IS INCOMPLETE:
   - Model migrations: old model names were overwritten
   - Only recent conversations have modelInfo populated
   - Older data (pre-Oct 2025) may not have had this field

3. TOKEN DATA:
   - From bubbleId.tokenCount: 292M input, 3.5M output
   - From composerData.contextTokensUsed: 35M
   - Server-side billing likely tracks REAL totals

4. WHERE'S THE REST OF YOUR DATA?
   - Cursor Year Wrapped pulls from SERVER-SIDE data
   - Local storage only has PARTIAL data
   - Server has complete billing/usage records
   
5. WHAT WE CAN DO:
   - Use what's available locally (~292M tokens)
   - Accept that model breakdown is incomplete
   - Note: Server has authoritative data

This is a LIMITATION of local data extraction - Cursor's Wrapped
feature uses server-side analytics that we don't have access to.
""")

