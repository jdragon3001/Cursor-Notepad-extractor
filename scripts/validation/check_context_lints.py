import sqlite3, json
from pathlib import Path

conn = sqlite3.connect(str(Path.home()/'AppData/Roaming/Cursor/User/globalStorage/state.vscdb'))
cursor = conn.cursor()

cursor.execute('SELECT COUNT(*) FROM cursorDiskKV WHERE key LIKE "messageRequestContext:%"')
total = cursor.fetchone()[0]
print(f'Total messageRequestContext entries: {total}')

cursor.execute('SELECT value FROM cursorDiskKV WHERE key LIKE "messageRequestContext:%"')

found_multi_file = 0
found_empty_multi_file = 0
found_with_errors = 0

for (v,) in cursor.fetchall():
    if v is None:
        continue
    data = json.loads(v.decode('utf-8') if isinstance(v, bytes) else v)
    if 'multiFileLinterErrors' in data:
        found_multi_file += 1
        errors = data['multiFileLinterErrors']
        if errors and len(errors) > 0:
            found_with_errors += 1
        else:
            found_empty_multi_file += 1

print(f'\nEntries with multiFileLinterErrors field: {found_multi_file}')
print(f'  With actual error data: {found_with_errors}')
print(f'  With empty array: {found_empty_multi_file}')

conn.close()

