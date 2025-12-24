"""Explore tool results in messages to understand failure data."""

import sys
sys.path.insert(0, r'C:\notepad extractor\Cursor-Notepad-extractor')

from pathlib import Path
from stats import StatsOrchestrator

# Initialize orchestrator
db_path = Path.home() / "AppData" / "Roaming" / "Cursor" / "User" / "globalStorage" / "state.vscdb"
orchestrator = StatsOrchestrator(db_path)

# Load data
orchestrator.extract_all_data()
messages = orchestrator.messages

print("=" * 60)
print("TOOL RESULTS EXPLORATION")
print("=" * 60)

# Find messages with tool results
messages_with_tools = [m for m in messages if m.tool_results and len(m.tool_results) > 0]
print(f"\nMessages with tool results: {len(messages_with_tools):,}")
print(f"Total messages: {len(messages):,}")
print(f"Percentage: {len(messages_with_tools)/len(messages)*100:.2f}%\n")

if messages_with_tools:
    # Examine first few tool results
    print("=" * 60)
    print("SAMPLE TOOL RESULTS")
    print("=" * 60)
    
    for i, msg in enumerate(messages_with_tools[:3], 1):
        print(f"\nSample {i}:")
        print(f"Message ID: {msg.message_id}")
        print(f"Number of tool results: {len(msg.tool_results)}")
        
        for j, tool in enumerate(msg.tool_results[:2], 1):
            print(f"\n  Tool {j}:")
            print(f"  Keys: {list(tool.keys())}")
            
            # Show structure
            import json
            print(f"  Structure:")
            print("  " + json.dumps(tool, indent=4)[:500])
    
    # Analyze tool result structure
    print("\n" + "=" * 60)
    print("TOOL RESULT FIELD ANALYSIS")
    print("=" * 60)
    
    all_fields = set()
    field_counts = {}
    
    for msg in messages_with_tools:
        for tool in msg.tool_results:
            for field in tool.keys():
                all_fields.add(field)
                field_counts[field] = field_counts.get(field, 0) + 1
    
    print(f"\nUnique fields found: {len(all_fields)}")
    print("\nField frequency:")
    for field, count in sorted(field_counts.items(), key=lambda x: x[1], reverse=True):
        print(f"  {field}: {count:,}")
    
    # Check for error indicators
    print("\n" + "=" * 60)
    print("ERROR/FAILURE INDICATORS")
    print("=" * 60)
    
    tools_with_error = 0
    tools_with_success = 0
    tools_with_status = 0
    
    for msg in messages_with_tools:
        for tool in msg.tool_results:
            if 'error' in tool or 'failed' in str(tool).lower():
                tools_with_error += 1
            if 'success' in tool:
                tools_with_success += 1
            if 'status' in tool:
                tools_with_status += 1
    
    print(f"Tools with 'error' field: {tools_with_error}")
    print(f"Tools with 'success' field: {tools_with_success}")
    print(f"Tools with 'status' field: {tools_with_status}")

else:
    print("No messages with tool results found!")

print("\n" + "=" * 60)
print("EXPLORATION COMPLETE")
print("=" * 60)

