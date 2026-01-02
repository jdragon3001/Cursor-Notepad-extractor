"""Debug script to check activity streak calculation."""

from stats import StatsOrchestrator
from pathlib import Path
from datetime import datetime, timedelta
from collections import Counter

# Initialize orchestrator
db_path = Path.home() / "AppData" / "Roaming" / "Cursor" / "User" / "globalStorage" / "state.vscdb"
orchestrator = StatsOrchestrator(db_path)
orchestrator.extract_all_data()

# Get unique dates
messages = orchestrator.messages
dates = sorted(set(m.created_at.date() for m in messages if m.created_at))

print(f"Total messages: {len(messages)}")
print(f"Messages with dates: {len([m for m in messages if m.created_at])}")
print(f"Unique activity dates: {len(dates)}")
print(f"\nFirst 10 dates:")
for d in dates[:10]:
    print(f"  {d}")
print(f"\nLast 10 dates:")
for d in dates[-10:]:
    print(f"  {d}")

# Check streak manually
longest_streak = 1
current_streak = 1

for i in range(1, len(dates)):
    gap = (dates[i] - dates[i-1]).days
    if gap == 1:
        current_streak += 1
        longest_streak = max(longest_streak, current_streak)
    else:
        if current_streak > 1:
            print(f"\nFound streak of {current_streak} days ending on {dates[i-1]}")
        current_streak = 1

print(f"\n=== RESULTS ===")
print(f"Longest streak: {longest_streak} days")

# Calculate current streak from today
today = datetime.now().date()
print(f"Today: {today}")
print(f"Most recent activity: {dates[-1] if dates else 'None'}")
print(f"Days since last activity: {(today - dates[-1]).days if dates else 'N/A'}")

streak_from_today = 0
for i in range(len(dates) - 1, -1, -1):
    expected_date = today - timedelta(days=streak_from_today)
    if dates[i] == expected_date:
        streak_from_today += 1
        print(f"  Day {streak_from_today}: {dates[i]} matches {expected_date}")
    else:
        print(f"  Streak broken: {dates[i]} != {expected_date}")
        break

print(f"\nCurrent streak from today: {streak_from_today} days")










