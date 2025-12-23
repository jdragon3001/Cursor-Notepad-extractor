import sys
sys.path.insert(0, '.')

from stats.extractors.message_extractor import MessageExtractor
from pathlib import Path

print("Checking context-related fields...")

db_path = Path.home() / 'AppData' / 'Roaming' / 'Cursor' / 'User' / 'globalStorage' / 'state.vscdb'

with MessageExtractor(db_path) as extractor:
    messages = extractor.extract()
    
    print(f"\nTotal messages: {len(messages)}")
    
    # Check each context field
    fields_to_check = {
        'attached_code_chunks': 'attachedCodeChunks',
        'codebase_context_chunks': 'codebaseContextChunks',
        'relevant_files': 'relevantFiles',
        'recently_viewed_files': 'recentlyViewedFiles',
        'web_references': 'webReferences',
    }
    
    for attr, raw_key in fields_to_check.items():
        # Check model attribute
        msgs_with_attr = [m for m in messages if getattr(m, attr, None)]
        print(f"\n{attr}:")
        print(f"  In model: {len(msgs_with_attr)} messages have data")
        if msgs_with_attr:
            sample = getattr(msgs_with_attr[0], attr)
            print(f"  Sample (first item): {sample[0] if isinstance(sample, list) and sample else sample}")
        
        # Check raw_data
        msgs_with_raw = [m for m in messages if raw_key in m.raw_data and m.raw_data[raw_key]]
        print(f"  In raw_data['{raw_key}']: {len(msgs_with_raw)} messages have data")
        if msgs_with_raw:
            sample = msgs_with_raw[0].raw_data[raw_key]
            if isinstance(sample, list) and sample:
                print(f"  Sample keys: {list(sample[0].keys()) if isinstance(sample[0], dict) else type(sample[0])}")

