import sys
sys.path.insert(0, '.')

from stats.extractors.request_context_extractor import MessageRequestContextExtractor
from pathlib import Path

print("Checking MessageRequestContext for actual file/context data...")

db_path = Path.home() / 'AppData' / 'Roaming' / 'Cursor' / 'User' / 'globalStorage' / 'state.vscdb'

with MessageRequestContextExtractor(db_path) as extractor:
    contexts = extractor.extract()
    
    print(f"\nTotal contexts: {len(contexts)}")
    
    # Check attached_file_code_chunks
    with_attached = [c for c in contexts if c.attached_file_code_chunks]
    print(f"\nContexts with attached_file_code_chunks: {len(with_attached)}")
    if with_attached:
        sample = with_attached[0].attached_file_code_chunks
        print(f"  Sample: {sample[0] if sample else 'empty'}")
    
    # Check for file-related data in raw_data
    fields_in_raw = [
        'attachedFileCodeChunksMetadataOnly',
        'ideEditorsState',
        'currentFileLocationData',
    ]
    
    for field in fields_in_raw:
        with_field = [c for c in contexts if field in c.raw_data and c.raw_data[field]]
        print(f"\n{field}: {len(with_field)} contexts")
        if with_field:
            sample = with_field[0].raw_data[field]
            if isinstance(sample, list):
                print(f"  Type: list of {len(sample)} items")
                if sample:
                    print(f"  First item keys: {list(sample[0].keys()) if isinstance(sample[0], dict) else type(sample[0])}")
            elif isinstance(sample, dict):
                print(f"  Keys: {list(sample.keys())}")
            else:
                print(f"  Type: {type(sample)}")

