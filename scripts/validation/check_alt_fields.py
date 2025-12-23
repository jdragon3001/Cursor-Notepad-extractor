"""Check alternative error/lint fields."""
import sys, os
from pathlib import Path
if sys.platform == 'win32':
    os.environ['PYTHONIOENCODING'] = 'utf-8'
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')

import sqlite3, json

conn = sqlite3.connect(str(Path.home() / 'AppData/Roaming/Cursor/User/globalStorage/state.vscdb'))
cursor = conn.cursor()

print("Checking 50,000 messages for alternative error/lint fields...")
cursor.execute('SELECT value FROM cursorDiskKV WHERE key LIKE "bubbleId:%" LIMIT 50000')

stats = {
    'approximateLintErrors': 0,
    'multiFileLinterErrors': 0,
    'errorDetails': 0,
    'lastTerminalCwd': 0,
    'existedPreviousTerminalCommand': 0,
}

for (v,) in cursor.fetchall():
    d = json.loads(v.decode('utf-8') if isinstance(v, bytes) else v)
    
    if d.get('approximateLintErrors'):
        stats['approximateLintErrors'] += 1
    if d.get('multiFileLinterErrors'):
        stats['multiFileLinterErrors'] += 1
    if d.get('errorDetails'):
        stats['errorDetails'] += 1
    if d.get('lastTerminalCwd'):
        stats['lastTerminalCwd'] += 1
    if d.get('existedPreviousTerminalCommand'):
        stats['existedPreviousTerminalCommand'] += 1

conn.close()

print(f"\nResults:")
for field, count in stats.items():
    percentage = (count / 50000) * 100
    print(f"  {field:35} {count:>6} ({percentage:>5.1f}%)")

