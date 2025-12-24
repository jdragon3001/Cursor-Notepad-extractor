import sys
sys.path.insert(0, '.')

from stats.orchestrator import StatsOrchestrator
from pathlib import Path
import json

print("Recalculating stats after removing duplicate tool stats...")
db_path = Path.home() / '.cursor-tutor'
o = StatsOrchestrator(db_path)
stats = o.calculate_all_stats(force=True)

# Save to file
with open('stats_output.json', 'w') as f:
    json.dump(stats, f, indent=2)

# Check for duplicate tool stats
msgs = stats.get('messages', {})
tools = stats.get('tools', {})

print("\nMESSAGE category tool-related stats:")
msg_tool_stats = [k for k in msgs.keys() if 'tool' in k.lower()]
print(f"  Found {len(msg_tool_stats)} stats: {msg_tool_stats}")

print("\nTOOLS category stats:")
tool_stats = list(tools.keys())
print(f"  Found {len(tool_stats)} stats: {tool_stats}")

print("\nVerifying no duplicates...")
for stat_name in tool_stats:
    if stat_name in msgs:
        print(f"  WARNING: '{stat_name}' exists in both MESSAGE and TOOLS!")
    else:
        print(f"  ✓ '{stat_name}' unique to TOOLS")

print("\nStats saved to stats_output.json!")

