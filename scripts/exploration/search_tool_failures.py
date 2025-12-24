"""Comprehensive search for tool failures."""

import sys
sys.stdout.reconfigure(encoding='utf-8')
sys.stderr.reconfigure(encoding='utf-8')

from pathlib import Path
import sqlite3
import json

print("=" * 60)
print("TOOL FAILURES SEARCH")
print("=" * 60)

db_path = Path.home() / "AppData" / "Roaming" / "Cursor" / "User" / "globalStorage" / "state.vscdb"
conn = sqlite3.connect(str(db_path))
cursor = conn.cursor()

# Check messages for tool results with errors/failures
cursor.execute("""
    SELECT COUNT(*) FROM cursorDiskKV 
    WHERE key LIKE 'bubbleId:%' 
    AND value LIKE '%toolResults%'
    AND value NOT LIKE '%"toolResults":[]%'
""")
count = cursor.fetchone()[0]
print(f"\nMessages with non-empty toolResults: {count}")

if count > 0:
    # Get a sample with toolResults
    cursor.execute("""
        SELECT key, value FROM cursorDiskKV 
        WHERE key LIKE 'bubbleId:%' 
        AND value LIKE '%toolResults%'
        AND value NOT LIKE '%"toolResults":[]%'
        LIMIT 5
    """)
    
    total_tools = 0
    failed_tools = 0
    error_samples = []
    
    for key, value_bytes in cursor.fetchall():
        data = json.loads(value_bytes)
        tool_results = data.get('toolResults', [])
        total_tools += len(tool_results)
        
        for tool in tool_results:
            # Check various fields that might indicate failure
            if tool.get('error') or tool.get('failed') or tool.get('isError'):
                failed_tools += 1
                error_samples.append({
                    'tool': tool.get('toolName', 'unknown'),
                    'error': tool.get('error'),
                    'failed': tool.get('failed'),
                    'isError': tool.get('isError')
                })
    
    print(f"\nTotal tool invocations sampled: {total_tools}")
    print(f"Failed tools sampled: {failed_tools}")
    
    if error_samples:
        print(f"\nSample error structures:")
        for sample in error_samples[:3]:
            print(json.dumps(sample, indent=2))
    
    # Get one full toolResults array for structure analysis
    cursor.execute("""
        SELECT value FROM cursorDiskKV 
        WHERE key LIKE 'bubbleId:%' 
        AND value LIKE '%toolResults%'
        AND value NOT LIKE '%"toolResults":[]%'
        LIMIT 1
    """)
    result = cursor.fetchone()
    if result:
        data = json.loads(result[0])
        tool_results = data.get('toolResults', [])
        print(f"\n{'='*60}")
        print("Sample toolResults structure:")
        print(f"{'='*60}")
        if tool_results:
            print(json.dumps(tool_results[0], indent=2)[:1000])

# Check all messages with toolResults to get accurate count
print(f"\n{'='*60}")
print("ANALYZING ALL TOOL RESULTS")
print(f"{'='*60}")

cursor.execute("""
    SELECT value FROM cursorDiskKV 
    WHERE key LIKE 'bubbleId:%' 
    AND value LIKE '%toolResults%'
    AND value NOT LIKE '%"toolResults":[]%'
""")

all_tools = []
all_failed = []
tool_types = set()

for (value_bytes,) in cursor.fetchall():
    try:
        data = json.loads(value_bytes)
        tool_results = data.get('toolResults', [])
        
        for tool in tool_results:
            all_tools.append(tool)
            tool_name = tool.get('toolName') or tool.get('name', 'unknown')
            tool_types.add(tool_name)
            
            # Check for failures
            if (tool.get('error') or 
                tool.get('failed') or 
                tool.get('isError') or
                tool.get('status') == 'failed' or
                'error' in str(tool).lower()):
                all_failed.append(tool)
    except json.JSONDecodeError:
        pass

print(f"\nTotal messages with toolResults: {count}")
print(f"Total tool invocations: {len(all_tools)}")
print(f"Failed tool invocations: {len(all_failed)}")
print(f"Unique tool types: {len(tool_types)}")
print(f"\nTool types: {', '.join(sorted(tool_types))}")

if all_failed:
    print(f"\n{'='*60}")
    print("Sample failures:")
    print(f"{'='*60}")
    for failure in all_failed[:3]:
        print(json.dumps(failure, indent=2)[:500])
        print("...")

conn.close()

print(f"\n{'='*60}")
print("SEARCH COMPLETE")
print(f"{'='*60}")

