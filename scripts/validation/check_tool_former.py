"""Check toolFormerData structure."""
import sys, os
from pathlib import Path
if sys.platform == 'win32':
    os.environ['PYTHONIOENCODING'] = 'utf-8'
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')

import sqlite3, json

conn = sqlite3.connect(str(Path.home() / 'AppData/Roaming/Cursor/User/globalStorage/state.vscdb'))
cursor = conn.cursor()
cursor.execute('SELECT value FROM cursorDiskKV WHERE key LIKE "bubbleId:%" LIMIT 10000')

found = 0
for (v,) in cursor.fetchall():
    data = json.loads(v.decode('utf-8') if isinstance(v, bytes) else v)
    if data.get('toolFormerData'):
        print(f"\ntoolFormerData sample:\n{json.dumps(data['toolFormerData'], indent=2)[:1500]}")
        found += 1
        if found >= 3:
            break

conn.close()

