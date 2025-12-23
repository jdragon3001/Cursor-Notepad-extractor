"""
Check how many messages actually have these fields with non-empty values.
"""

import sys
import os
from pathlib import Path

# Fix Windows console encoding
if sys.platform == 'win32':
    os.environ['PYTHONIOENCODING'] = 'utf-8'
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

from stats.extractors.message_extractor import MessageExtractor
from collections import Counter

def analyze_extracted_messages():
    """Analyze what actually got extracted."""
    print("="*80)
    print("ANALYZING EXTRACTED MESSAGE DATA")
    print("="*80)
    
    user_home = Path.home()
    db_path = user_home / "AppData" / "Roaming" / "Cursor" / "User" / "globalStorage" / "state.vscdb"
    
    print("\nExtracting messages...")
    with MessageExtractor(db_path) as extractor:
        messages = extractor.extract()
    
    print(f"Extracted {len(messages)} messages\n")
    
    # Count messages with various fields
    stats = {
        'lints': 0,
        'lints_non_empty': 0,
        'console_logs': 0,
        'console_logs_non_empty': 0,
        'tool_results': 0,
        'tool_results_non_empty': 0,
        'tool_former_data': 0,
        'tool_former_data_non_empty': 0,
    }
    
    # Sample some data
    sample_with_lints = []
    sample_with_logs = []
    sample_with_tools = []
    
    for msg in messages:
        # Lints
        if hasattr(msg, 'lints'):
            stats['lints'] += 1
            if msg.lints and len(msg.lints) > 0:
                stats['lints_non_empty'] += 1
                if len(sample_with_lints) < 3:
                    sample_with_lints.append(msg)
        
        # Console logs
        if hasattr(msg, 'console_logs'):
            stats['console_logs'] += 1
            if msg.console_logs and len(msg.console_logs) > 0:
                stats['console_logs_non_empty'] += 1
                if len(sample_with_logs) < 3:
                    sample_with_logs.append(msg)
        
        # Tool results
        if hasattr(msg, 'tool_results'):
            stats['tool_results'] += 1
            if msg.tool_results and len(msg.tool_results) > 0:
                stats['tool_results_non_empty'] += 1
                if len(sample_with_tools) < 3:
                    sample_with_tools.append(msg)
        
        # Tool former data
        if hasattr(msg, 'tool_former_data'):
            stats['tool_former_data'] += 1
            if msg.tool_former_data and isinstance(msg.tool_former_data, dict) and len(msg.tool_former_data) > 0:
                stats['tool_former_data_non_empty'] += 1
    
    print("📊 EXTRACTED MESSAGE FIELD STATISTICS:\n")
    for field, count in stats.items():
        percentage = (count / len(messages)) * 100
        print(f"  {field:30} {count:>8} ({percentage:>5.1f}%)")
    
    # Show samples
    if sample_with_lints:
        print("\n📝 SAMPLE MESSAGE WITH LINTS:\n")
        msg = sample_with_lints[0]
        print(f"  Message ID: {msg.bubble_id[:50]}...")
        print(f"  Lints: {msg.lints[:500] if msg.lints else 'None'}...")
    
    if sample_with_logs:
        print("\n📝 SAMPLE MESSAGE WITH CONSOLE LOGS:\n")
        msg = sample_with_logs[0]
        print(f"  Message ID: {msg.bubble_id[:50]}...")
        print(f"  Console Logs: {msg.console_logs[:500] if msg.console_logs else 'None'}...")
    
    if sample_with_tools:
        print("\n📝 SAMPLE MESSAGE WITH TOOL RESULTS:\n")
        msg = sample_with_tools[0]
        print(f"  Message ID: {msg.bubble_id[:50]}...")
        print(f"  Tool Results: {str(msg.tool_results)[:500] if msg.tool_results else 'None'}...")
    
    # Check raw_data
    print("\n🔍 CHECKING RAW DATA FOR SAMPLE MESSAGES:\n")
    for i, msg in enumerate(messages[:10]):
        if hasattr(msg, 'raw_data') and msg.raw_data:
            has_lints = 'lints' in msg.raw_data
            has_logs = 'consoleLogs' in msg.raw_data
            has_tools = 'toolResults' in msg.raw_data or 'toolFormerData' in msg.raw_data
            
            lints_val = msg.raw_data.get('lints', [])
            logs_val = msg.raw_data.get('consoleLogs', [])
            tools_val = msg.raw_data.get('toolResults', [])
            tool_former = msg.raw_data.get('toolFormerData')
            
            if has_lints or has_logs or has_tools:
                print(f"  Message {i+1}:")
                if has_lints:
                    print(f"    lints in raw_data: {len(lints_val) if isinstance(lints_val, list) else 'not a list'}")
                if has_logs:
                    print(f"    consoleLogs in raw_data: {len(logs_val) if isinstance(logs_val, list) else 'not a list'}")
                if has_tools:
                    print(f"    toolResults in raw_data: {len(tools_val) if isinstance(tools_val, list) else 'not a list'}")
                    if tool_former:
                        print(f"    toolFormerData in raw_data: {type(tool_former).__name__}")

if __name__ == '__main__':
    analyze_extracted_messages()

