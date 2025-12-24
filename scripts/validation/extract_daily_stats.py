#!/usr/bin/env python3
"""
EXTRACT ALL DAILY USAGE STATISTICS
This is the data we were missing!
"""

import sqlite3
from pathlib import Path
import json
from datetime import datetime
from collections import defaultdict

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
print("EXTRACTING ALL DAILY USAGE STATISTICS")
print("=" * 70)

db_path = CURSOR_BASE / 'User/globalStorage/state.vscdb'
conn = sqlite3.connect(str(db_path))
cursor = conn.cursor()

# Get ALL daily stats
cursor.execute("SELECT key, value FROM ItemTable WHERE key LIKE 'aiCodeTracking.dailyStats%' ORDER BY key")
daily_stats = cursor.fetchall()

print(f"\nFound {len(daily_stats)} days of usage data!\n")

# Parse and aggregate
all_days = []
totals = {
    'tabSuggestedLines': 0,
    'tabAcceptedLines': 0,
    'composerSuggestedLines': 0,
    'composerAcceptedLines': 0
}

for key, value in daily_stats:
    data = safe_json(value)
    if data:
        all_days.append(data)
        for field in totals.keys():
            totals[field] += data.get(field, 0)

# Sort by date
all_days.sort(key=lambda x: x.get('date', ''))

print("Daily Statistics (Oldest to Newest):")
print("-" * 70)
print(f"{'Date':<12} {'Tab Sugg':>10} {'Tab Acc':>10} {'Comp Sugg':>12} {'Comp Acc':>12}")
print("-" * 70)

for day in all_days:
    date = day.get('date', 'unknown')
    tab_sugg = day.get('tabSuggestedLines', 0)
    tab_acc = day.get('tabAcceptedLines', 0)
    comp_sugg = day.get('composerSuggestedLines', 0)
    comp_acc = day.get('composerAcceptedLines', 0)
    print(f"{date:<12} {tab_sugg:>10,} {tab_acc:>10,} {comp_sugg:>12,} {comp_acc:>12,}")

print("-" * 70)
print(f"{'TOTAL':<12} {totals['tabSuggestedLines']:>10,} {totals['tabAcceptedLines']:>10,} {totals['composerSuggestedLines']:>12,} {totals['composerAcceptedLines']:>12,}")

# Other important stats
print("\n" + "=" * 70)
print("OTHER KEY STATISTICS")
print("=" * 70)

# Prompt count
cursor.execute("SELECT value FROM ItemTable WHERE key = 'freeBestOfN.promptCount'")
result = cursor.fetchone()
if result:
    print(f"\nTotal prompts used: {safe_json(result[0])}")

# AI tracking start time
cursor.execute("SELECT value FROM ItemTable WHERE key = 'aiCodeTrackingStartTime'")
result = cursor.fetchone()
if result:
    data = safe_json(result[0])
    if data and 'timestamp' in data:
        start_date = datetime.fromtimestamp(data['timestamp'] / 1000)
        print(f"Tracking started: {start_date}")

# Subscription status
cursor.execute("SELECT value FROM ItemTable WHERE key = 'cursorAuth/stripeSubscriptionStatus'")
result = cursor.fetchone()
if result:
    print(f"Subscription status: {result[0]}")

# Recent commit stats
cursor.execute("SELECT value FROM ItemTable WHERE key = 'aiCodeTracking.recentCommit'")
result = cursor.fetchone()
if result:
    data = safe_json(result[0])
    if data:
        print(f"\nMost recent commit tracked:")
        print(f"  Repo: {data.get('repoName')}")
        print(f"  Branch: {data.get('branchName')}")
        print(f"  AI percentage: {data.get('aiPercentage')}%")
        print(f"  Lines added: {data.get('linesAdded')}")
        print(f"  Composer lines: {data.get('composerLinesAdded')}")

# Get scored commits
cursor.execute("SELECT value FROM ItemTable WHERE key = 'aiCodeTrackingScoredCommits'")
result = cursor.fetchone()
if result:
    data = safe_json(result[0])
    if data and isinstance(data, list):
        print(f"\nTotal scored commits: {len(data)}")

conn.close()

# SUMMARY
print("\n" + "=" * 70)
print("SUMMARY: LINES OF CODE DATA")
print("=" * 70)
print(f"""
FROM DAILY STATS:
  - Date range: {all_days[0]['date'] if all_days else 'N/A'} to {all_days[-1]['date'] if all_days else 'N/A'}
  - Days tracked: {len(all_days)}
  
TAB COMPLETIONS:
  - Suggested: {totals['tabSuggestedLines']:,} lines
  - Accepted: {totals['tabAcceptedLines']:,} lines
  - Acceptance rate: {totals['tabAcceptedLines']/max(totals['tabSuggestedLines'],1)*100:.1f}%

COMPOSER (AGENT/CHAT):
  - Suggested: {totals['composerSuggestedLines']:,} lines
  - Accepted: {totals['composerAcceptedLines']:,} lines
  - Acceptance rate: {totals['composerAcceptedLines']/max(totals['composerSuggestedLines'],1)*100:.1f}%

TOTAL LINES:
  - Suggested: {totals['tabSuggestedLines'] + totals['composerSuggestedLines']:,}
  - Accepted: {totals['tabAcceptedLines'] + totals['composerAcceptedLines']:,}
""")

# Save to file
output_file = Path("cursor-data-docs/11-DAILY-USAGE-STATS.md")
output_file.parent.mkdir(exist_ok=True)

with open(output_file, 'w', encoding='utf-8') as f:
    f.write("# Daily Usage Statistics\n\n")
    f.write(f"**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
    
    f.write("## Summary\n\n")
    f.write(f"- **Date Range:** {all_days[0]['date'] if all_days else 'N/A'} to {all_days[-1]['date'] if all_days else 'N/A'}\n")
    f.write(f"- **Days Tracked:** {len(all_days)}\n\n")
    
    f.write("### Composer (Agent/Chat)\n")
    f.write(f"- Lines Suggested: **{totals['composerSuggestedLines']:,}**\n")
    f.write(f"- Lines Accepted: **{totals['composerAcceptedLines']:,}**\n")
    f.write(f"- Acceptance Rate: {totals['composerAcceptedLines']/max(totals['composerSuggestedLines'],1)*100:.1f}%\n\n")
    
    f.write("### Tab Completions\n")
    f.write(f"- Lines Suggested: {totals['tabSuggestedLines']:,}\n")
    f.write(f"- Lines Accepted: {totals['tabAcceptedLines']:,}\n\n")
    
    f.write("## Daily Breakdown\n\n")
    f.write("| Date | Tab Sugg | Tab Acc | Comp Sugg | Comp Acc |\n")
    f.write("|------|----------|---------|-----------|----------|\n")
    for day in all_days:
        f.write(f"| {day.get('date')} | {day.get('tabSuggestedLines', 0):,} | {day.get('tabAcceptedLines', 0):,} | {day.get('composerSuggestedLines', 0):,} | {day.get('composerAcceptedLines', 0):,} |\n")
    f.write(f"| **TOTAL** | **{totals['tabSuggestedLines']:,}** | **{totals['tabAcceptedLines']:,}** | **{totals['composerSuggestedLines']:,}** | **{totals['composerAcceptedLines']:,}** |\n")

print(f"\nSaved to: {output_file}")

