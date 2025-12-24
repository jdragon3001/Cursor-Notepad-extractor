"""Explore File History structure."""

from pathlib import Path
import json

history_path = Path.home() / "AppData" / "Roaming" / "Cursor" / "User" / "History"

print("=" * 60)
print("FILE HISTORY EXPLORATION")
print("=" * 60)

if not history_path.exists():
    print(f"\nHistory path not found: {history_path}")
else:
    # Count file hash directories
    file_dirs = list(history_path.glob("*/"))
    print(f"\nTotal file hash directories: {len(file_dirs)}")
    
    # Check structure
    if file_dirs:
        sample = file_dirs[0]
        print(f"\nSample directory: {sample.name}")
        files = list(sample.glob("*"))
        print(f"Files in directory: {[f.name for f in files]}")
        
        # Check entries.json
        entries_file = sample / "entries.json"
        if entries_file.exists():
            print(f"\nentries.json exists!")
            print(f"Size: {entries_file.stat().st_size} bytes")
            
            # Read and show structure
            try:
                with open(entries_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                print(f"\nData type: {type(data)}")
                if isinstance(data, dict):
                    print(f"Keys: {list(data.keys())}")
                elif isinstance(data, list):
                    print(f"List length: {len(data)}")
                    if data:
                        print(f"\nFirst entry:")
                        print(json.dumps(data[0], indent=2)[:500])
            except Exception as e:
                print(f"Error reading entries.json: {e}")
    
    # Count files with entries
    files_with_entries = 0
    total_entries = 0
    
    for file_dir in file_dirs[:100]:  # Sample first 100
        entries_file = file_dir / "entries.json"
        if entries_file.exists():
            files_with_entries += 1
            try:
                with open(entries_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    if isinstance(data, dict):
                        total_entries += len(data.get('entries', []))
                    elif isinstance(data, list):
                        total_entries += len(data)
            except:
                pass
    
    print(f"\n{'='*60}")
    print("SUMMARY (from 100 samples)")
    print(f"{'='*60}")
    print(f"Files with entries.json: {files_with_entries}")
    print(f"Total entries found: {total_entries}")

print(f"\n{'='*60}")
print("EXPLORATION COMPLETE")
print(f"{'='*60}")

