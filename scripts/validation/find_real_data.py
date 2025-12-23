"""Find messages with substantial toolFormerData or actual errors/lints."""
import sys, os
from pathlib import Path
if sys.platform == 'win32':
    os.environ['PYTHONIOENCODING'] = 'utf-8'
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')

import sqlite3, json

conn = sqlite3.connect(str(Path.home() / 'AppData/Roaming/Cursor/User/globalStorage/state.vscdb'))
cursor = conn.cursor()

print("Searching 50,000 messages for non-empty data...")
cursor.execute('SELECT key, value FROM cursorDiskKV WHERE key LIKE "bubbleId:%" LIMIT 50000')

stats = {'with_lints': 0, 'with_logs': 0, 'with_tool_results': 0, 'with_tool_former': 0}
samples = {'lints': None, 'logs': None, 'tool_results': None, 'tool_former': None}

for key, v in cursor.fetchall():
    data = json.loads(v.decode('utf-8') if isinstance(v, bytes) else v)
    
    # Check lints
    lints = data.get('lints', [])
    if lints and len(lints) > 0:
        stats['with_lints'] += 1
        if not samples['lints']:
            samples['lints'] = (key, lints)
    
    # Check console logs
    logs = data.get('consoleLogs', [])
    if logs and len(logs) > 0:
        stats['with_logs'] += 1
        if not samples['logs']:
            samples['logs'] = (key, logs)
    
    # Check tool results
    tool_results = data.get('toolResults', [])
    if tool_results and len(tool_results) > 0:
        stats['with_tool_results'] += 1
        if not samples['tool_results']:
            samples['tool_results'] = (key, tool_results)
    
    # Check toolFormerData
    tfd = data.get('toolFormerData')
    if tfd and isinstance(tfd, dict) and len(tfd) > 1:  # More than just status
        stats['with_tool_former'] += 1
        if not samples['tool_former'] and len(str(tfd)) > 100:
            samples['tool_former'] = (key, tfd)

conn.close()

print(f"\nResults from 50,000 messages:")
print(f"  Messages with lints: {stats['with_lints']}")
print(f"  Messages with console logs: {stats['with_logs']}")
print(f"  Messages with toolResults: {stats['with_tool_results']}")
print(f"  Messages with toolFormerData: {stats['with_tool_former']}")

if samples['lints']:
    key, data = samples['lints']
    print(f"\nSample message with lints:")
    print(f"  Key: {key[:60]}...")
    print(f"  Lints: {json.dumps(data[:2], indent=2)[:500]}")

if samples['logs']:
    key, data = samples['logs']
    print(f"\nSample message with console logs:")
    print(f"  Key: {key[:60]}...")
    print(f"  Logs: {json.dumps(data[:2], indent=2)[:500]}")

if samples['tool_results']:
    key, data = samples['tool_results']
    print(f"\nSample message with toolResults:")
    print(f"  Key: {key[:60]}...")
    print(f"  Results: {json.dumps(data[:1], indent=2)[:1000]}")

if samples['tool_former']:
    key, data = samples['tool_former']
    print(f"\nSample message with toolFormerData:")
    print(f"  Key: {key[:60]}...")
    print(f"  Data: {json.dumps(data, indent=2)[:1500]}")

