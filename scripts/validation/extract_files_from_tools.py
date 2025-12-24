import sys
sys.path.insert(0, '.')

from stats.extractors.message_extractor import MessageExtractor
from pathlib import Path
import json

print("Extracting file modifications from tool usage...")

db_path = Path.home() / 'AppData' / 'Roaming' / 'Cursor' / 'User' / 'globalStorage' / 'state.vscdb'

with MessageExtractor(db_path) as extractor:
    messages = extractor.extract()
    
    # Track file operations
    files_written = set()
    files_deleted = set()
    files_modified = set()
    
    write_count = 0
    delete_count = 0
    modify_count = 0
    
    for msg in messages:
        if isinstance(msg.tool_former_data, dict):
            tool_name = msg.tool_former_data.get('name', '')
            
            # Get file path from rawArgs or result
            file_path = None
            raw_args = msg.tool_former_data.get('rawArgs')
            
            if raw_args:
                try:
                    if isinstance(raw_args, str):
                        args = json.loads(raw_args)
                    else:
                        args = raw_args
                    
                    # Different tools store file path differently
                    file_path = args.get('file_path') or args.get('target_file') or args.get('filepath')
                except:
                    pass
            
            # Count operations
            if tool_name == 'write':
                write_count += 1
                if file_path:
                    files_written.add(file_path)
            elif tool_name == 'delete_file':
                delete_count += 1
                if file_path:
                    files_deleted.add(file_path)
            elif tool_name in ['search_replace', 'apply_patch', 'edit_file', 'edit_file_v2']:
                modify_count += 1
                if file_path:
                    files_modified.add(file_path)
    
    print(f"\nFile operations from tool usage:")
    print(f"  write tool: {write_count} invocations, {len(files_written)} unique files")
    print(f"  delete_file tool: {delete_count} invocations, {len(files_deleted)} unique files")
    print(f"  modification tools: {modify_count} invocations, {len(files_modified)} unique files")
    print(f"\nTotal unique files touched: {len(files_written | files_deleted | files_modified)}")
    
    if files_written:
        print(f"\nSample written files: {list(files_written)[:5]}")
    if files_deleted:
        print(f"Sample deleted files: {list(files_deleted)[:5]}")
    if files_modified:
        print(f"Sample modified files: {list(files_modified)[:5]}")

