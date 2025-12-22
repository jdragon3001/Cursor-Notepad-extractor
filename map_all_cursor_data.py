#!/usr/bin/env python3
"""
Phase 1: Complete Cursor Data Source Discovery

Maps EVERY file and folder in Cursor's data directory to ensure
we don't miss any potential data sources.
"""

from pathlib import Path
from datetime import datetime
import os

CURSOR_BASE = Path.home() / 'AppData/Roaming/Cursor'

def get_size_str(size):
    """Convert bytes to human readable."""
    for unit in ['B', 'KB', 'MB', 'GB']:
        if size < 1024:
            return f"{size:.1f} {unit}"
        size /= 1024
    return f"{size:.1f} TB"

def get_folder_size(path):
    """Get total size of a folder."""
    total = 0
    try:
        for item in path.rglob('*'):
            if item.is_file():
                total += item.stat().st_size
    except:
        pass
    return total

def count_items(path):
    """Count files and folders."""
    files = 0
    folders = 0
    try:
        for item in path.rglob('*'):
            if item.is_file():
                files += 1
            else:
                folders += 1
    except:
        pass
    return files, folders

def identify_data_type(path):
    """Try to identify what type of data a folder contains."""
    if not path.is_dir():
        ext = path.suffix.lower()
        type_map = {
            '.vscdb': 'SQLite Database',
            '.json': 'JSON File',
            '.log': 'Log File',
            '.txt': 'Text File',
            '.db': 'Database',
            '.sqlite': 'SQLite Database',
        }
        return type_map.get(ext, f'File ({ext})')
    
    # Check folder contents
    children = list(path.iterdir()) if path.exists() else []
    child_names = [c.name for c in children]
    
    if 'CURRENT' in child_names and 'MANIFEST-000001' in child_names:
        return 'LevelDB Database'
    if any(c.suffix == '.vscdb' for c in children):
        return 'Contains SQLite DBs'
    if any(c.suffix == '.json' for c in children):
        return 'Contains JSON Files'
    if any(c.suffix == '.log' for c in children):
        return 'Contains Log Files'
    
    return 'Folder'


def main():
    print("="*80)
    print("CURSOR DATA SOURCE COMPLETE MAP")
    print("="*80)
    print(f"\nBase Path: {CURSOR_BASE}")
    print(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
    
    if not CURSOR_BASE.exists():
        print("ERROR: Cursor data folder not found!")
        return
    
    # Get top-level overview
    print("\n" + "="*80)
    print("TOP-LEVEL FOLDERS OVERVIEW")
    print("="*80)
    
    top_level = []
    for item in sorted(CURSOR_BASE.iterdir()):
        size = get_folder_size(item) if item.is_dir() else item.stat().st_size
        files, folders = count_items(item) if item.is_dir() else (1, 0)
        dtype = identify_data_type(item)
        
        top_level.append({
            'name': item.name,
            'size': size,
            'files': files,
            'folders': folders,
            'type': dtype,
            'path': item
        })
    
    # Sort by size
    top_level.sort(key=lambda x: x['size'], reverse=True)
    
    print(f"\n{'Folder/File':<35} {'Size':>12} {'Files':>8} {'Type':<25}")
    print("-"*80)
    
    for item in top_level:
        print(f"{item['name']:<35} {get_size_str(item['size']):>12} {item['files']:>8} {item['type']:<25}")
    
    # Deep dive into each significant folder
    print("\n" + "="*80)
    print("DETAILED BREAKDOWN OF EACH DATA SOURCE")
    print("="*80)
    
    for item in top_level:
        print(f"\n{'='*80}")
        print(f"[FOLDER] {item['name']}")
        print(f"{'='*80}")
        print(f"Path: {item['path']}")
        print(f"Total Size: {get_size_str(item['size'])}")
        print(f"Files: {item['files']}, Folders: {item['folders']}")
        print(f"Type: {item['type']}")
        
        if not item['path'].is_dir():
            print("\n  [Single file - see type above]")
            continue
        
        # Show contents
        print("\nContents (first 2 levels):")
        
        try:
            for child in sorted(item['path'].iterdir())[:30]:
                child_size = get_folder_size(child) if child.is_dir() else child.stat().st_size
                child_type = identify_data_type(child)
                print(f"  {'[D]' if child.is_dir() else '[F]'} {child.name:<40} {get_size_str(child_size):>10} [{child_type}]")
                
                # One more level for folders
                if child.is_dir():
                    try:
                        subchildren = list(child.iterdir())[:10]
                        for subchild in subchildren:
                            sub_size = subchild.stat().st_size if subchild.is_file() else 0
                            print(f"      {'[D]' if subchild.is_dir() else '[F]'} {subchild.name:<36} {get_size_str(sub_size):>10}")
                        if len(list(child.iterdir())) > 10:
                            print(f"      ... and {len(list(child.iterdir())) - 10} more items")
                    except:
                        pass
            
            if len(list(item['path'].iterdir())) > 30:
                print(f"  ... and {len(list(item['path'].iterdir())) - 30} more items")
                
        except Exception as e:
            print(f"  Error reading: {e}")
    
    # Summary of data types found
    print("\n" + "="*80)
    print("SUMMARY: ALL DATA SOURCES BY TYPE")
    print("="*80)
    
    sqlite_dbs = []
    leveldb_dbs = []
    json_files = []
    log_files = []
    other = []
    
    for item in CURSOR_BASE.rglob('*'):
        if item.is_file():
            if item.suffix == '.vscdb' or item.suffix == '.db':
                sqlite_dbs.append(item)
            elif item.suffix == '.json':
                json_files.append(item)
            elif item.suffix == '.log':
                log_files.append(item)
        elif item.is_dir():
            children = [c.name for c in item.iterdir()] if item.exists() else []
            if 'CURRENT' in children and 'MANIFEST-000001' in children:
                leveldb_dbs.append(item)
    
    print(f"\n[DB] SQLite Databases: {len(sqlite_dbs)}")
    for db in sqlite_dbs[:10]:
        print(f"   - {db.relative_to(CURSOR_BASE)} ({get_size_str(db.stat().st_size)})")
    if len(sqlite_dbs) > 10:
        print(f"   ... and {len(sqlite_dbs) - 10} more")
    
    print(f"\n[DB] LevelDB Databases: {len(leveldb_dbs)}")
    for db in leveldb_dbs[:10]:
        print(f"   - {db.relative_to(CURSOR_BASE)}")
    
    print(f"\n[JSON] JSON Files: {len(json_files)}")
    for jf in sorted(json_files, key=lambda x: x.stat().st_size, reverse=True)[:10]:
        print(f"   - {jf.relative_to(CURSOR_BASE)} ({get_size_str(jf.stat().st_size)})")
    if len(json_files) > 10:
        print(f"   ... and {len(json_files) - 10} more")
    
    print(f"\n[LOG] Log Files: {len(log_files)}")
    
    print("\n" + "="*80)
    print("NEXT STEPS")
    print("="*80)
    print("""
Now that we have mapped all data sources, we should:

1. EXPLORE SQLITE DATABASES - These are the richest data sources
   - Global state.vscdb (2.6GB) 
   - Workspace state.vscdb files (245 of them)
   
2. DECODE LEVELDB DATABASES - May contain chat history
   - Local Storage/leveldb
   - Session Storage
   
3. PARSE JSON FILES - Configuration and metadata
   - storage.json, settings.json, etc.
   
4. ANALYZE LOGS - Usage patterns and timing
   
5. CHECK UNEXPLORED FOLDERS:
   - Backups/
   - CachedData/
   - Partitions/
   - Service Worker/
   - Network/
""")


if __name__ == "__main__":
    main()

