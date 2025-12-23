import sys
sys.path.insert(0, '.')

from stats.extractors.message_extractor import MessageExtractor
from pathlib import Path
import json

print("Checking for web browsing in tool usage...")

db_path = Path.home() / 'AppData' / 'Roaming' / 'Cursor' / 'User' / 'globalStorage' / 'state.vscdb'

with MessageExtractor(db_path) as extractor:
    messages = extractor.extract()
    
    print(f"\nTotal messages: {len(messages)}")
    
    # Check toolFormerData for web/browser tools
    web_tools_found = []
    web_search_found = []
    browser_found = []
    
    for msg in messages:
        if msg.tool_former_data:
            tfd = msg.tool_former_data
            if isinstance(tfd, list):
                for tool in tfd:
                    if isinstance(tool, dict):
                        tool_name = tool.get('tool', '')
                        if 'web' in tool_name.lower() or 'browser' in tool_name.lower() or 'search' in tool_name.lower():
                            if 'browser' in tool_name.lower():
                                browser_found.append(tool_name)
                            elif 'search' in tool_name.lower():
                                web_search_found.append(tool_name)
                            else:
                                web_tools_found.append(tool_name)
    
    print(f"\nMessages with browser tools: {len(set(browser_found))}")
    if browser_found:
        print(f"  Browser tools used: {set(browser_found)}")
        print(f"  Total browser tool invocations: {len(browser_found)}")
    
    print(f"\nMessages with web search tools: {len(set(web_search_found))}")
    if web_search_found:
        print(f"  Search tools used: {set(web_search_found)}")
        print(f"  Total search tool invocations: {len(web_search_found)}")
    
    print(f"\nMessages with other web tools: {len(set(web_tools_found))}")
    if web_tools_found:
        print(f"  Other web tools: {set(web_tools_found)}")
    
    # Also check for web-related capabilities
    web_capabilities = []
    for msg in messages:
        for cap in msg.capabilities:
            if 'web' in cap.lower() or 'browser' in cap.lower():
                web_capabilities.append(cap)
    
    if web_capabilities:
        print(f"\nWeb-related capabilities found: {set(web_capabilities)}")
        print(f"  Total messages with web capabilities: {len(web_capabilities)}")
    
    # Check if there's a useWeb field
    msgs_with_useweb = [m for m in messages if m.raw_data.get('useWeb')]
    print(f"\nMessages with useWeb=true: {len(msgs_with_useweb)}")

