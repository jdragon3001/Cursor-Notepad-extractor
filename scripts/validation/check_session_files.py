import sys
sys.path.insert(0, '.')

from stats.extractors.session_extractor import SessionExtractor
from pathlib import Path

print("Checking session file modification data...")

db_path = Path.home() / 'AppData' / 'Roaming' / 'Cursor' / 'User' / 'globalStorage' / 'state.vscdb'

with SessionExtractor(db_path) as extractor:
    sessions = extractor.extract()
    
    print(f"\nTotal sessions: {len(sessions)}")
    
    # Check added_files and removed_files
    sessions_with_added = [s for s in sessions if s.added_files]
    sessions_with_removed = [s for s in sessions if s.removed_files]
    
    print(f"\nSessions with added_files: {len(sessions_with_added)}")
    if sessions_with_added:
        print(f"  Sample: {sessions_with_added[0].added_files[:3]}")
    
    print(f"\nSessions with removed_files: {len(sessions_with_removed)}")
    if sessions_with_removed:
        print(f"  Sample: {sessions_with_removed[0].removed_files[:3]}")
    
    # Check raw_data for alternative fields
    print("\n\nChecking raw_data for file-related fields...")
    if sessions:
        sample = sessions[0]
        file_related = [k for k in sample.raw_data.keys() if 'file' in k.lower() or 'add' in k.lower() or 'remov' in k.lower() or 'modif' in k.lower()]
        print(f"File-related keys in raw_data: {file_related}")

