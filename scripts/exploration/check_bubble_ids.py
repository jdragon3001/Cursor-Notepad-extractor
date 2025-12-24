from database.cursor_db import CursorDB
from utils.config import Config

db = CursorDB(Config.get_global_db_path())
rows = db.execute_query("SELECT key FROM cursorDiskKV WHERE key LIKE 'bubbleId:%' LIMIT 20")

print("Sample bubble IDs:")
for row in rows:
    print(row[0])

