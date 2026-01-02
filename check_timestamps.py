"""Check for messages with weird timestamps."""
from stats import StatsOrchestrator
from utils.config import Config
from datetime import datetime

o = StatsOrchestrator(Config.get_global_db_path())
o.extract_all_data()
messages = o.messages

now = datetime.now()
year_2020 = datetime(2020, 1, 1)

future = [m for m in messages if m.created_at > now]
before_2020 = [m for m in messages if m.created_at < year_2020]

print(f"Total messages: {len(messages)}")
print(f"Messages with future timestamps: {len(future)}")
print(f"Messages before 2020: {len(before_2020)}")

if future:
    print(f"\nExample future dates:")
    for m in future[:5]:
        print(f"  {m.created_at.isoformat()} - {m.text[:50] if m.text else 'No text'}")

if before_2020:
    print(f"\nExample dates before 2020:")
    for m in before_2020[:5]:
        print(f"  {m.created_at.isoformat()} - {m.text[:50] if m.text else 'No text'}")

# Check date range
dates = sorted([m.created_at for m in messages])
print(f"\nDate range:")
print(f"  Earliest: {dates[0].isoformat()}")
print(f"  Latest: {dates[-1].isoformat()}")
print(f"  Span: {(dates[-1] - dates[0]).days} days")

