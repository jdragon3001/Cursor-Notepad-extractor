"""Test workspace extraction."""

import sys
sys.path.insert(0, r'C:\notepad extractor\Cursor-Notepad-extractor')

from stats.extractors.workspace_extractor import WorkspaceExtractor

print("=" * 60)
print("WORKSPACE EXTRACTION TEST")
print("=" * 60)

extractor = WorkspaceExtractor()
workspaces = extractor.extract()

print(f"\nTotal workspaces extracted: {len(workspaces):,}")

if workspaces:
    # Analysis
    with_data = [w for w in workspaces if w.has_data]
    with_composer = [w for w in workspaces if w.has_composer_data]
    with_notepad = [w for w in workspaces if w.has_notepad_data]
    
    total_size_mb = sum(w.size_mb for w in workspaces)
    
    print(f"\n{'='*60}")
    print("ANALYSIS")
    print(f"{'='*60}")
    print(f"Workspaces with data: {len(with_data):,}")
    print(f"Workspaces with composer data: {len(with_composer):,}")
    print(f"Workspaces with notepad data: {len(with_notepad):,}")
    print(f"Total size: {total_size_mb:.2f} MB")
    print(f"Average size: {total_size_mb/len(workspaces):.2f} MB")
    
    # Top 5 largest
    workspaces.sort(key=lambda w: w.size_mb, reverse=True)
    print(f"\n{'='*60}")
    print("TOP 5 LARGEST WORKSPACES")
    print(f"{'='*60}")
    for i, ws in enumerate(workspaces[:5], 1):
        print(f"{i}. {ws.workspace_id}")
        print(f"   Size: {ws.size_mb:.2f} MB")
        print(f"   Keys: {ws.total_keys:,}")
        print(f"   Composer keys: {ws.composer_count}")
        print(f"   Notepad keys: {ws.notepad_count}")

print(f"\n{'='*60}")
print("TEST COMPLETE")
print(f"{'='*60}")

