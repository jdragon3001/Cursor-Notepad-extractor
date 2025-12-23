import sys
sys.path.insert(0, '.')

from stats.extractors.message_extractor import MessageExtractor
from pathlib import Path

print("Checking for browser/web tools in toolFormerData...")

db_path = Path.home() / 'AppData' / 'Roaming' / 'Cursor' / 'User' / 'globalStorage' / 'state.vscdb'

with MessageExtractor(db_path) as extractor:
    messages = extractor.extract()
    
    msgs_with_tfd = [m for m in messages if m.tool_former_data]
    print(f"\nTotal messages with toolFormerData: {len(msgs_with_tfd)}")
    
    # Collect all tool names
    tool_names = {}
    for msg in msgs_with_tfd:
        if isinstance(msg.tool_former_data, dict) and 'name' in msg.tool_former_data:
            name = msg.tool_former_data['name']
            tool_names[name] = tool_names.get(name, 0) + 1
    
    print(f"\nAll unique tool names ({len(tool_names)}):")
    for name in sorted(tool_names.keys()):
        print(f"  - {name}: {tool_names[name]} times")
    
    # Filter for web/browser related
    web_related = [name for name in tool_names.keys() if 'web' in name.lower() or 'browser' in name.lower() or 'mcp' in name.lower() or 'search' in name.lower()]
    
    if web_related:
        print(f"\nWeb/Browser related tools:")
        for name in web_related:
            print(f"  - {name}: {tool_names[name]} times")
    else:
        print(f"\nNo web or browser-related tools found.")
        print(f"\nNote: 'codebase_search' is a code search tool, not web browsing.")

