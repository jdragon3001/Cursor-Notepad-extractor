import sys
sys.path.insert(0, '.')

from stats.extractors.message_extractor import MessageExtractor
from pathlib import Path

print("Checking code block structure...")

db_path = Path.home() / 'AppData' / 'Roaming' / 'Cursor' / 'User' / 'globalStorage' / 'state.vscdb'

with MessageExtractor(db_path) as extractor:
    messages = extractor.extract()
    
    # Find messages with code blocks
    msgs_with_code = [m for m in messages if m.code_blocks][:10]
    
    print(f"Analyzing {len(msgs_with_code)} messages with code blocks...")
    
    for i, msg in enumerate(msgs_with_code):
        print(f"\n=== Message {i+1} ===")
        print(f"Total code blocks: {len(msg.code_blocks)}")
        
        for j, block in enumerate(msg.code_blocks[:2]):  # First 2 blocks
            print(f"\n  Block {j+1} keys: {list(block.keys())}")
            
            # Check for language fields
            lang_fields = ['language', 'lang', 'languageId']
            for field in lang_fields:
                if field in block:
                    print(f"    {field}: {block[field]}")
            
            # Check for file path fields
            file_fields = ['filePath', 'file', 'uri', 'path']
            for field in file_fields:
                if field in block:
                    val = block[field]
                    if isinstance(val, dict):
                        print(f"    {field}: {val.get('path', val)}")
                    else:
                        print(f"    {field}: {val}")
        
        if i >= 2:  # Only show first 3 messages
            break

