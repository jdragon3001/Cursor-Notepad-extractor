import sys
sys.path.insert(0, '.')

from stats.extractors.message_extractor import MessageExtractor
from pathlib import Path
import json

print("Checking toolFormerData dict structure for web/browser tools...")

db_path = Path.home() / 'AppData' / 'Roaming' / 'Cursor' / 'User' / 'globalStorage' / 'state.vscdb'

with MessageExtractor(db_path) as extractor:
    messages = extractor.extract()
    
    msgs_with_tfd = [m for m in messages if m.tool_former_data]
    print(f"\nMessages with toolFormerData: {len(msgs_with_tfd)}")
    
    # Collect all unique keys in toolFormerData
    all_keys = set()
    for msg in msgs_with_tfd[:1000]:  # Sample 1000
        if isinstance(msg.tool_former_data, dict):
            all_keys.update(msg.tool_former_data.keys())
    
    print(f"\nUnique keys in toolFormerData (first 1000 messages): {sorted(all_keys)}")
    
    # Look for samples with different keys
    for key in all_keys:
        for msg in msgs_with_tfd:
            if isinstance(msg.tool_former_data, dict) and key in msg.tool_former_data:
                val = msg.tool_former_data[key]
                print(f"\n{key}:")
                print(f"  Type: {type(val)}")
                if isinstance(val, list) and val:
                    print(f"  List length: {len(val)}")
                    if isinstance(val[0], dict):
                        print(f"  First item keys: {list(val[0].keys())[:10]}")
                        # Check for tool names
                        if 'tool' in val[0]:
                            print(f"  Tool name: {val[0]['tool']}")
                elif isinstance(val, dict):
                    print(f"  Dict keys: {list(val.keys())[:10]}")
                else:
                    print(f"  Value: {str(val)[:200]}")
                break  # One sample per key

