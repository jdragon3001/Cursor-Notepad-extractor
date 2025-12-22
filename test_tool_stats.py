"""Test tool stats calculation."""

import sys
sys.stdout.reconfigure(encoding='utf-8')
sys.stderr.reconfigure(encoding='utf-8')

from pathlib import Path
import json

from stats.orchestrator import StatsOrchestrator
from utils.config import Config

user_home = Path.home()
global_db_path = user_home / "AppData" / "Roaming" / "Cursor" / "User" / "globalStorage" / Config.DB_FILENAME

print("=" * 60)
print("TOOL STATS TEST")
print("=" * 60)

orchestrator = StatsOrchestrator(global_db_path)
orchestrator.extract_all_data()

print(f"\nTotal messages: {len(orchestrator._messages):,}")

# Calculate tool stats
all_stats = orchestrator.calculate_all_stats(force=True)
tool_stats = all_stats.get('tools', {})

print(f"\n{'='*60}")
print("TOOL STATS")
print(f"{'='*60}")

if tool_stats:
    print(f"\n1. Total tool invocations:")
    print(f"   {tool_stats.get('total_tool_invocations', {}).get('value', 0):,}")
    
    print(f"\n2. Tool success rate:")
    success = tool_stats.get('tool_success_rate', {})
    print(f"   {success.get('value', 0):.1f}%")
    print(f"   Breakdown: {json.dumps(success.get('breakdown', {}), indent=4)}")
    
    print(f"\n3. Tool error rate:")
    error = tool_stats.get('tool_error_rate', {})
    print(f"   {error.get('value', 0):.1f}%")
    
    print(f"\n4. Tool cancellation rate:")
    cancelled = tool_stats.get('tool_cancellation_rate', {})
    print(f"   {cancelled.get('value', 0):.1f}%")
    
    print(f"\n5. Messages with tools:")
    with_tools = tool_stats.get('messages_with_tools', {})
    print(f"   {with_tools.get('value', 0):,} ({with_tools.get('percentage', 0):.1f}%)")
    
    print(f"\n6. Most used tools:")
    most_used = tool_stats.get('most_used_tools', {})
    if most_used.get('breakdown', {}).get('top_10'):
        for item in most_used['breakdown']['top_10'][:5]:
            print(f"   {item['tool']}: {item['count']:,}")
    
    print(f"\n7. Tool status distribution:")
    status_dist = tool_stats.get('tool_status_distribution', {})
    for status, data in status_dist.get('breakdown', {}).items():
        print(f"   {status}: {data['count']:,} ({data['percentage']:.1f}%)")
    
    print(f"\n8. Tools per message:")
    tools_per_msg = tool_stats.get('tools_per_message', {})
    print(f"   Average: {tools_per_msg.get('value', 0):.2f}")
    print(f"   Median: {tools_per_msg.get('median', 0):.2f}")
    
    print(f"\n9. Tool argument length:")
    arg_length = tool_stats.get('tool_arg_length', {})
    print(f"   Average: {arg_length.get('value', 0):.0f} characters")
    print(f"   Median: {arg_length.get('median', 0):.0f} characters")
    
    print(f"\n10. Unique tool types:")
    unique_tools = tool_stats.get('unique_tool_types', {})
    print(f"   {unique_tools.get('value', 0)} unique tools")
    if unique_tools.get('breakdown', {}).get('tool_list'):
        print(f"   Tools: {', '.join(unique_tools['breakdown']['tool_list'][:10])}")
else:
    print("No tool stats calculated.")

print(f"\n{'='*60}")
print("TEST COMPLETE")
print(f"{'='*60}")

