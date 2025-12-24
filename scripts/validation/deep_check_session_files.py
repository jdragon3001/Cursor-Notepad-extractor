import sys
sys.path.insert(0, '.')

from stats.extractors.session_extractor import SessionExtractor
from pathlib import Path
import json

print("Deep check: Are addedFiles/removedFiles populated in raw data?")

db_path = Path.home() / 'AppData' / 'Roaming' / 'Cursor' / 'User' / 'globalStorage' / 'state.vscdb'

with SessionExtractor(db_path) as extractor:
    sessions = extractor.extract()
    
    print(f"\nTotal sessions: {len(sessions)}")
    
    # Check raw_data directly
    count_added = 0
    count_removed = 0
    sample_added = None
    sample_removed = None
    
    for session in sessions:
        if 'addedFiles' in session.raw_data and session.raw_data['addedFiles']:
            if isinstance(session.raw_data['addedFiles'], list) and len(session.raw_data['addedFiles']) > 0:
                count_added += 1
                if sample_added is None:
                    sample_added = session.raw_data['addedFiles'][:3]
        
        if 'removedFiles' in session.raw_data and session.raw_data['removedFiles']:
            if isinstance(session.raw_data['removedFiles'], list) and len(session.raw_data['removedFiles']) > 0:
                count_removed += 1
                if sample_removed is None:
                    sample_removed = session.raw_data['removedFiles'][:3]
    
    print(f"\nSessions with non-empty addedFiles in raw_data: {count_added}")
    if sample_added:
        print(f"  Sample: {sample_added}")
    
    print(f"\nSessions with non-empty removedFiles in raw_data: {count_removed}")
    if sample_removed:
        print(f"  Sample: {sample_removed}")
    
    # Also check model fields
    print("\n\nChecking model attributes after extraction:")
    for session in sessions[:10]:
        if session.added_files:
            print(f"  Session with added_files: {session.added_files[:3]}")
            break
    else:
        print("  No sessions with populated added_files attribute found in first 10")

