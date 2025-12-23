"""Quick script to check the actual format of timestamps in the database."""

import sys
import os
from pathlib import Path

# Fix Windows console encoding
if sys.platform == 'win32':
    os.environ['PYTHONIOENCODING'] = 'utf-8'
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')

import sqlite3
import json
from datetime import datetime

# Get database path
user_home = Path.home()
db_path = user_home / "AppData" / "Roaming" / "Cursor" / "User" / "globalStorage" / "state.vscdb"

print(f"Checking database: {db_path}\n")

conn = sqlite3.connect(str(db_path))
cursor = conn.cursor()

# Get some sample messages
cursor.execute("SELECT key, value FROM cursorDiskKV WHERE key LIKE 'bubbleId:%' LIMIT 10")
rows = cursor.fetchall()

print("="*80)
print("SAMPLE MESSAGE TIMESTAMPS")
print("="*80)

for key, value in rows:
    try:
        if isinstance(value, bytes):
            data = json.loads(value.decode('utf-8'))
        elif isinstance(value, str):
            data = json.loads(value)
        else:
            continue
        
        created_at = data.get('createdAt')
        
        print(f"\nKey: {key[:50]}...")
        print(f"  createdAt (raw): {created_at}")
        print(f"  createdAt (type): {type(created_at)}")
        
        # Try different parsing methods
        if created_at:
            if isinstance(created_at, str):
                # Try ISO format
                try:
                    dt = datetime.fromisoformat(created_at.replace('Z', '+00:00'))
                    print(f"  Parsed (ISO): {dt}")
                except:
                    print(f"  Failed to parse as ISO")
                
                # Try as timestamp string
                try:
                    dt = datetime.fromtimestamp(int(created_at) / 1000)
                    print(f"  Parsed (timestamp): {dt}")
                except:
                    print(f"  Failed to parse as timestamp")
            
            elif isinstance(created_at, (int, float)):
                # Try as milliseconds
                try:
                    dt = datetime.fromtimestamp(created_at / 1000)
                    print(f"  Parsed (ms): {dt}")
                except:
                    print(f"  Failed to parse as ms")
                
                # Try as seconds
                try:
                    dt = datetime.fromtimestamp(created_at)
                    print(f"  Parsed (s): {dt}")
                except:
                    print(f"  Failed to parse as seconds")
        
        # Check other timestamp fields
        for field in ['updatedAt', 'timestamp', 'time', 'date']:
            if field in data:
                print(f"  {field}: {data[field]} (type: {type(data[field])})")
        
    except Exception as e:
        print(f"Error: {e}")

conn.close()

print("\n" + "="*80)
print("Check complete!")

