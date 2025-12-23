import sys
sys.path.insert(0, '.')

from stats.extractors.message_extractor import MessageExtractor
from pathlib import Path
import json

print("Checking for MCP browser tool usage...")

db_path = Path.home() / 'AppData' / 'Roaming' / 'Cursor' / 'User' / 'globalStorage' / 'state.vscdb'

with MessageExtractor(db_path) as extractor:
    messages = extractor.extract()
    
    print(f"\nTotal messages: {len(messages)}")
    
    # Check ALL tool names in toolFormerData
    all_tool_names = set()
    for msg in messages:
        if msg.tool_former_data:
            tfd = msg.tool_former_data
            if isinstance(tfd, list):
                for tool in tfd:
                    if isinstance(tool, dict):
                        tool_name = tool.get('tool', '')
                        if tool_name:
                            all_tool_names.add(tool_name)
    
    print(f"\nAll unique tool names ({len(all_tool_names)}):")
    for name in sorted(all_tool_names):
        print(f"  - {name}")
    
    # Look for MCP-related tools
    mcp_tools = [name for name in all_tool_names if 'mcp' in name.lower() or 'browser' in name.lower() or 'cursor-ide' in name.lower()]
    
    if mcp_tools:
        print(f"\nMCP/Browser-related tools found:")
        for tool in mcp_tools:
            print(f"  - {tool}")
    else:
        print(f"\nNo MCP or browser-related tools found in tool usage data.")
    
    # Check for any messages that might have external links or URLs in text
    print("\nChecking for URL patterns in message text...")
    msgs_with_urls = 0
    for msg in messages[:1000]:  # Sample first 1000
        if msg.text and ('http://' in msg.text or 'https://' in msg.text):
            msgs_with_urls += 1
    
    print(f"  Messages with URLs in text (first 1000): {msgs_with_urls}")

