"""Explore workspace databases to understand structure."""

from pathlib import Path
import sqlite3
import json

workspace_storage = Path.home() / "AppData" / "Roaming" / "Cursor" / "User" / "workspaceStorage"

print("=" * 60)
print("WORKSPACE STORAGE EXPLORATION")
print("=" * 60)

# Find all workspace directories
workspaces = list(workspace_storage.glob("*/"))
print(f"\nTotal workspace directories: {len(workspaces)}")

# Check which have databases
workspaces_with_db = []
for ws in workspaces:
    db_path = ws / "state.vscdb"
    if db_path.exists():
        size_mb = db_path.stat().st_size / (1024 * 1024)
        workspaces_with_db.append({
            'path': ws,
            'name': ws.name,
            'db_path': db_path,
            'size_mb': size_mb
        })

print(f"Workspaces with databases: {len(workspaces_with_db)}")

# Sort by size
workspaces_with_db.sort(key=lambda x: x['size_mb'], reverse=True)

print(f"\n{'='*60}")
print("TOP 10 LARGEST WORKSPACE DATABASES")
print(f"{'='*60}")
for i, ws in enumerate(workspaces_with_db[:10], 1):
    print(f"{i}. {ws['name'][:50]}")
    print(f"   Size: {ws['size_mb']:.2f} MB")

# Explore a sample workspace database
print(f"\n{'='*60}")
print("SAMPLE WORKSPACE DATABASE STRUCTURE")
print(f"{'='*60}")

sample_ws = workspaces_with_db[0]
print(f"\nExamining: {sample_ws['name'][:60]}")
print(f"Size: {sample_ws['size_mb']:.2f} MB")

conn = sqlite3.connect(str(sample_ws['db_path']))
cursor = conn.cursor()

# Get tables
cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
tables = [row[0] for row in cursor.fetchall()]
print(f"\nTables: {tables}")

# Check ItemTable for interesting keys
if 'ItemTable' in tables:
    cursor.execute("SELECT key FROM ItemTable LIMIT 20")
    keys = [row[0] for row in cursor.fetchall()]
    print(f"\nSample ItemTable keys:")
    for key in keys[:15]:
        print(f"  - {key}")
    
    # Check for composer data
    cursor.execute("SELECT COUNT(*) FROM ItemTable WHERE key LIKE '%composer%'")
    composer_count = cursor.fetchone()[0]
    print(f"\nKeys with 'composer': {composer_count}")
    
    # Check for notepad data
    cursor.execute("SELECT COUNT(*) FROM ItemTable WHERE key LIKE '%notepad%'")
    notepad_count = cursor.fetchone()[0]
    print(f"Keys with 'notepad': {notepad_count}")
    
    # Get actual composer data
    cursor.execute("SELECT key, value FROM ItemTable WHERE key LIKE '%composer%' LIMIT 1")
    result = cursor.fetchone()
    if result:
        key, value = result
        print(f"\nSample composer key: {key}")
        try:
            data = json.loads(value)
            print(f"Data keys: {list(data.keys())[:10]}")
        except:
            print(f"Value preview: {str(value)[:200]}")

conn.close()

# Summary statistics
print(f"\n{'='*60}")
print("SUMMARY STATISTICS")
print(f"{'='*60}")
print(f"Total workspaces: {len(workspaces)}")
print(f"Workspaces with databases: {len(workspaces_with_db)}")
print(f"Total size: {sum(ws['size_mb'] for ws in workspaces_with_db):.2f} MB")
print(f"Average size: {sum(ws['size_mb'] for ws in workspaces_with_db) / len(workspaces_with_db):.2f} MB")

print(f"\n{'='*60}")
print("EXPLORATION COMPLETE")
print(f"{'='*60}")

