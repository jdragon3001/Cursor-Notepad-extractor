import sys
sys.path.insert(0, '.')

from stats.extractors.message_extractor import MessageExtractor
from pathlib import Path

print("Checking references and suggestions fields...")

db_path = Path.home() / 'AppData' / 'Roaming' / 'Cursor' / 'User' / 'globalStorage' / 'state.vscdb'

with MessageExtractor(db_path) as extractor:
    messages = extractor.extract()
    
    print(f"\nTotal messages: {len(messages)}")
    
    # Check references
    print("\n=== REFERENCES ===")
    fields = {
        'web_references': 'webReferences',
        'docs_references': 'docsReferences',
        'ai_web_search_results': 'aiWebSearchResults',
    }
    
    for attr, raw_key in fields.items():
        msgs_with_data = [m for m in messages if getattr(m, attr, None)]
        print(f"{attr}: {len(msgs_with_data)} messages")
        if msgs_with_data:
            sample = getattr(msgs_with_data[0], attr)
            print(f"  Sample: {sample[0] if isinstance(sample, list) and sample else sample}")
    
    # Check web capability
    msgs_with_web = [m for m in messages if 'web' in m.capabilities]
    print(f"\nmessages with 'web' in capabilities: {len(msgs_with_web)}")
    
    # Check suggestions
    print("\n=== SUGGESTIONS ===")
    sugg_fields = {
        'suggested_code_blocks': 'suggestedCodeBlocks',
        'assistant_suggested_diffs': 'assistantSuggestedDiffs',
        'user_responses_to_suggested_code_blocks': 'userResponsesToSuggestedCodeBlocks',
    }
    
    for attr, raw_key in sugg_fields.items():
        msgs_with_data = [m for m in messages if raw_key in m.raw_data and m.raw_data[raw_key]]
        print(f"{raw_key}: {len(msgs_with_data)} messages")
        if msgs_with_data:
            sample = msgs_with_data[0].raw_data[raw_key]
            if isinstance(sample, list) and sample:
                print(f"  Sample type: list of {len(sample)} items")
                print(f"  First item keys: {list(sample[0].keys()) if isinstance(sample[0], dict) else type(sample[0])}")
            else:
                print(f"  Type: {type(sample)}")

