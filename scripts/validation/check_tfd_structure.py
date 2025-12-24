import sys
sys.path.insert(0, '.')

from stats.extractors.message_extractor import MessageExtractor
from pathlib import Path
import json

print("Checking toolFormerData structure...")

db_path = Path.home() / 'AppData' / 'Roaming' / 'Cursor' / 'User' / 'globalStorage' / 'state.vscdb'

with MessageExtractor(db_path) as extractor:
    messages = extractor.extract()
    
    # Find messages with toolFormerData
    msgs_with_tfd = [m for m in messages if m.tool_former_data]
    print(f"\nMessages with toolFormerData: {len(msgs_with_tfd)}")
    
    if msgs_with_tfd:
        sample = msgs_with_tfd[0]
        print(f"\nSample toolFormerData:")
        print(f"  Type: {type(sample.tool_former_data)}")
        print(f"  Value: {json.dumps(sample.tool_former_data, indent=2)[:500]}")
        
        # Check if it's a list
        if isinstance(sample.tool_former_data, list) and sample.tool_former_data:
            first_item = sample.tool_former_data[0]
            print(f"\n  First item type: {type(first_item)}")
            if isinstance(first_item, dict):
                print(f"  First item keys: {list(first_item.keys())}")
                print(f"  First item: {json.dumps(first_item, indent=2)[:500]}")
        elif isinstance(sample.tool_former_data, dict):
            print(f"  Keys: {list(sample.tool_former_data.keys())}")

