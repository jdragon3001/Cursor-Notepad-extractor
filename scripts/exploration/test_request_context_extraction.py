"""Test messageRequestContext extraction."""

import sys
sys.path.insert(0, r'C:\notepad extractor\Cursor-Notepad-extractor')

from pathlib import Path
from stats.extractors.request_context_extractor import MessageRequestContextExtractor

db_path = Path.home() / "AppData" / "Roaming" / "Cursor" / "User" / "globalStorage" / "state.vscdb"

print("=" * 60)
print("MESSAGE REQUEST CONTEXT EXTRACTION TEST")
print("=" * 60)

with MessageRequestContextExtractor(db_path) as extractor:
    contexts = extractor.extract()

print(f"\nTotal contexts extracted: {len(contexts):,}")

if contexts:
    # Analyze the data
    contexts_with_errors = [c for c in contexts if c.has_linter_errors]
    contexts_with_git = [c for c in contexts if c.has_git_changes]
    contexts_with_todos = [c for c in contexts if c.has_todos]
    
    total_linter_errors = sum(c.linter_error_count for c in contexts)
    
    print(f"\n{'='*60}")
    print("ANALYSIS")
    print(f"{'='*60}")
    print(f"Contexts with linter errors: {len(contexts_with_errors):,}")
    print(f"Total linter errors: {total_linter_errors:,}")
    print(f"Contexts with git changes: {len(contexts_with_git):,}")
    print(f"Contexts with TODOs: {len(contexts_with_todos):,}")
    
    # Show sample with linter errors if available
    if contexts_with_errors:
        sample = contexts_with_errors[0]
        print(f"\n{'='*60}")
        print("SAMPLE CONTEXT WITH LINTER ERRORS")
        print(f"{'='*60}")
        print(f"Composer ID: {sample.composer_id}")
        print(f"Error count: {sample.linter_error_count}")
        print(f"Sample error:")
        import json
        print(json.dumps(sample.multi_file_linter_errors[0], indent=2)[:500])

print(f"\n{'='*60}")
print("TEST COMPLETE")
print(f"{'='*60}")

