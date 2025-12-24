"""Analyze tool results structure from actual messages."""

import sys
import json
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from utils.config import Config
from database.cursor_db import CursorDatabase
from stats.extractors.message_extractor import MessageExtractor

def analyze_tool_results():
    """Examine actual tool results structure from messages."""
    
    db_path = Config.get_global_db_path()
    
    print("=== Analyzing Tool Results Structure ===\n")
    
    extractor = MessageExtractor(db_path)
    
    # Get first 1000 messages
    messages = extractor.extract()
    
    print(f"Loaded {len(messages)} messages\n")
    
    # Find messages with tool results
    messages_with_tools = [m for m in messages if m.tool_results and len(m.tool_results) > 0]
    
    print(f"Found {len(messages_with_tools)} messages with tool results\n")
    
    if messages_with_tools:
        # Show first 5 examples
        for i, msg in enumerate(messages_with_tools[:5]):
            print(f"\n{'='*60}")
            print(f"Message {i+1}: {msg.bubble_id}")
            print(f"Tool results count: {len(msg.tool_results)}")
            print(f"{'='*60}\n")
            
            for j, tool in enumerate(msg.tool_results):
                print(f"\n--- Tool {j+1} ---")
                print(f"Type: {type(tool)}")
                print(f"Keys: {list(tool.keys()) if isinstance(tool, dict) else 'Not a dict'}")
                print(f"\nFull structure:")
                print(json.dumps(tool, indent=2, default=str))
                print("\n")
                
                if j >= 2:  # Limit to 3 tools per message
                    break
            
            if i >= 4:  # Limit to 5 messages
                break
    else:
        print("No messages with tool results found!")

if __name__ == "__main__":
    analyze_tool_results()

