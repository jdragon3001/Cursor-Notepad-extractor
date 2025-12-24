import sys
sys.path.insert(0, '.')

from stats.extractors.message_extractor import MessageExtractor
from pathlib import Path

print("Checking code block and file reference fields...")

db_path = Path.home() / 'AppData' / 'Roaming' / 'Cursor' / 'User' / 'globalStorage' / 'state.vscdb'

with MessageExtractor(db_path) as extractor:
    messages = extractor.extract()
    
    print(f"\nTotal messages: {len(messages)}")
    
    # Check code_blocks field
    has_code_blocks = [m for m in messages if m.code_blocks]
    print(f"\nMessages with code_blocks: {len(has_code_blocks)}")
    if has_code_blocks:
        print(f"  Example: {has_code_blocks[0].code_blocks[:2]}")
    
    # Check suggested_code_blocks field
    has_suggested = [m for m in messages if m.suggested_code_blocks]
    print(f"\nMessages with suggested_code_blocks: {len(has_suggested)}")
    if has_suggested:
        print(f"  Example: {has_suggested[0].suggested_code_blocks[:2]}")
    
    # Check raw_data for code-related fields
    print("\n\nChecking raw_data for code-related fields...")
    sample_msg = messages[0]
    code_fields = [k for k in sample_msg.raw_data.keys() if 'code' in k.lower() or 'block' in k.lower() or 'lang' in k.lower()]
    print(f"Fields with 'code', 'block', or 'lang' in name: {code_fields}")
    
    # Check for codeblock or code field
    msgs_with_code_field = []
    for msg in messages[:100]:
        if 'code' in msg.raw_data or 'codeBlocks' in msg.raw_data or 'codeblock' in msg.raw_data:
            msgs_with_code_field.append(msg)
            if len(msgs_with_code_field) == 1:
                print(f"\nFound message with code field!")
                print(f"  Keys: {list(msg.raw_data.keys())}")
                for k in ['code', 'codeBlocks', 'codeblock']:
                    if k in msg.raw_data:
                        print(f"  {k}: {msg.raw_data[k][:200] if isinstance(msg.raw_data[k], str) else msg.raw_data[k]}")
    
    print(f"\nMessages with code-related fields (first 100): {len(msgs_with_code_field)}")

