"""Explore aiCodeTracking.dailyStats structure."""

import sqlite3
import json
from pathlib import Path
from datetime import datetime

# Connect to database
db_path = Path.home() / "AppData" / "Roaming" / "Cursor" / "User" / "globalStorage" / "state.vscdb"
conn = sqlite3.connect(str(db_path))
cursor = conn.cursor()

print("=" * 60)
print("AICODE TRACKING DAILYSTATS STRUCTURE EXPLORATION")
print("=" * 60)

# Check ItemTable for aiCodeTracking.dailyStats
cursor.execute("SELECT COUNT(*) FROM ItemTable WHERE key LIKE 'aiCodeTracking.dailyStats%'")
count = cursor.fetchone()[0]
print(f"\nTotal aiCodeTracking.dailyStats entries: {count:,}\n")

# Get all keys
cursor.execute("SELECT key FROM ItemTable WHERE key LIKE 'aiCodeTracking.dailyStats%' ORDER BY key")
keys = cursor.fetchall()
print(f"Keys found ({len(keys)}):")
for key, in keys[:10]:  # Show first 10
    print(f"  - {key}")
if len(keys) > 10:
    print(f"  ... and {len(keys) - 10} more")

# Get samples
cursor.execute("SELECT key, value FROM ItemTable WHERE key LIKE 'aiCodeTracking.dailyStats%' LIMIT 3")
samples = cursor.fetchall()

for i, (key, value) in enumerate(samples, 1):
    print(f"\n{'='*60}")
    print(f"SAMPLE {i}: {key}")
    print(f"{'='*60}")
    
    try:
        data = json.loads(value)
        print(f"Data type: {type(data).__name__}")
        print(f"\nStructure:")
        print(json.dumps(data, indent=2))
        
        # Show field types
        print(f"\nField types:")
        for k, v in data.items():
            print(f"  {k}: {type(v).__name__} = {v}")
            
    except Exception as e:
        print(f"Error parsing: {e}")
        print(f"Raw value: {value[:500]}")

# Get date range
cursor.execute("""
    SELECT 
        MIN(key) as earliest,
        MAX(key) as latest,
        COUNT(*) as total
    FROM ItemTable 
    WHERE key LIKE 'aiCodeTracking.dailyStats%'
""")
earliest, latest, total = cursor.fetchone()
print(f"\n{'='*60}")
print(f"DATE RANGE SUMMARY")
print(f"{'='*60}")
print(f"Earliest: {earliest}")
print(f"Latest: {latest}")
print(f"Total days: {total}")

# Calculate totals
cursor.execute("SELECT key, value FROM ItemTable WHERE key LIKE 'aiCodeTracking.dailyStats%'")
all_stats = cursor.fetchall()

total_composer_suggested = 0
total_composer_accepted = 0
total_tab_suggested = 0
total_tab_accepted = 0

for key, value in all_stats:
    try:
        data = json.loads(value)
        total_composer_suggested += data.get('composerSuggestedLines', 0)
        total_composer_accepted += data.get('composerAcceptedLines', 0)
        total_tab_suggested += data.get('tabSuggestedLines', 0)
        total_tab_accepted += data.get('tabAcceptedLines', 0)
    except:
        pass

print(f"\n{'='*60}")
print(f"TOTALS ACROSS ALL DAYS")
print(f"{'='*60}")
print(f"Composer Suggested: {total_composer_suggested:,}")
print(f"Composer Accepted: {total_composer_accepted:,}")
print(f"Composer Acceptance Rate: {(total_composer_accepted/total_composer_suggested*100) if total_composer_suggested > 0 else 0:.1f}%")
print(f"\nTab Suggested: {total_tab_suggested:,}")
print(f"Tab Accepted: {total_tab_accepted:,}")
print(f"Tab Acceptance Rate: {(total_tab_accepted/total_tab_suggested*100) if total_tab_suggested > 0 else 0:.1f}%")

conn.close()
print(f"\n{'='*60}")
print("EXPLORATION COMPLETE")
print(f"{'='*60}")

