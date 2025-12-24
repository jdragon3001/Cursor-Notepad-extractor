import sys
sys.path.insert(0, '.')

from stats.extractors.message_extractor import MessageExtractor
from pathlib import Path

print("Checking git diffs, diff histories, and human changes fields...")

db_path = Path.home() / 'AppData' / 'Roaming' / 'Cursor' / 'User' / 'globalStorage' / 'state.vscdb'

with MessageExtractor(db_path) as extractor:
    messages = extractor.extract()
    
    print(f"\nTotal messages: {len(messages)}")
    
    fields_to_check = {
        'gitDiffs': 'gitDiffs',
        'diffHistories': 'diffHistories',
        'humanChanges': 'humanChanges',
        'attachedHumanChanges': 'attachedHumanChanges',
        'gitStatusRaw': 'gitStatusRaw',
        'diffsSinceLastApply': 'diffsSinceLastApply',
    }
    
    for field_name, raw_key in fields_to_check.items():
        count = 0
        for msg in messages:
            if msg.raw_data and raw_key in msg.raw_data:
                val = msg.raw_data[raw_key]
                # Check if it's non-empty
                if val:
                    if isinstance(val, list) and len(val) > 0:
                        count += 1
                    elif isinstance(val, dict) and len(val) > 0:
                        count += 1
                    elif isinstance(val, str) and len(val) > 0:
                        count += 1
                    elif isinstance(val, (int, float)) and val != 0:
                        count += 1
        
        print(f"\n{field_name}: {count} messages with data")
        
        # Show a sample if found
        if count > 0:
            for msg in messages:
                if msg.raw_data and raw_key in msg.raw_data and msg.raw_data[raw_key]:
                    sample = msg.raw_data[raw_key]
                    if isinstance(sample, str):
                        print(f"  Sample: {sample[:200]}")
                    elif isinstance(sample, list):
                        print(f"  Sample (list of {len(sample)} items)")
                    elif isinstance(sample, dict):
                        print(f"  Sample keys: {list(sample.keys())[:10]}")
                    break

