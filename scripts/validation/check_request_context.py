import sys
sys.path.insert(0, '.')

from stats.extractors.request_context_extractor import MessageRequestContextExtractor
from pathlib import Path

print("Checking MessageRequestContext for context fields...")

db_path = Path.home() / 'AppData' / 'Roaming' / 'Cursor' / 'User' / 'globalStorage' / 'state.vscdb'

with MessageRequestContextExtractor(db_path) as extractor:
    contexts = extractor.extract()
    
    print(f"\nTotal contexts: {len(contexts)}")
    
    # Check what fields exist
    if contexts:
        sample = contexts[0]
        print(f"\nSample context attributes: {[attr for attr in dir(sample) if not attr.startswith('_')]}")
        print(f"\nSample raw_data keys: {list(sample.raw_data.keys())[:20]}")
        
        # Check for file/chunk related data
        fields_to_check = [
            'codebase_chunks',
            'attached_chunks', 
            'relevant_files',
            'recently_viewed_files',
        ]
        
        for field in fields_to_check:
            if hasattr(sample, field):
                val = getattr(sample, field)
                print(f"\n{field}: {type(val)} = {val if not isinstance(val, list) else f'list of {len(val)} items'}")

