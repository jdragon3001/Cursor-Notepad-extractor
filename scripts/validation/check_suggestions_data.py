import sys
sys.path.insert(0, '.')

from stats.extractors.message_extractor import MessageExtractor
from pathlib import Path
import json

print("Checking for code suggestions and user responses...")

db_path = Path.home() / 'AppData' / 'Roaming' / 'Cursor' / 'User' / 'globalStorage' / 'state.vscdb'

with MessageExtractor(db_path) as extractor:
    messages = extractor.extract()
    
    print(f"\nTotal messages: {len(messages)}")
    
    # Check for assistant messages (AI responses)
    assistant_msgs = [m for m in messages if m.message_type == 2]
    user_msgs = [m for m in messages if m.message_type == 1]
    print(f"\nAssistant messages: {len(assistant_msgs)}")
    print(f"User messages: {len(user_msgs)}")
    
    # Check code blocks in assistant messages
    assistant_with_code = [m for m in assistant_msgs if m.code_blocks]
    print(f"Assistant messages with code blocks: {len(assistant_with_code)}")
    
    # Check for tool usage: apply_patch, edit_file, search_replace (these are suggestions)
    suggestion_tools = ['apply_patch', 'edit_file', 'edit_file_v2', 'search_replace']
    msgs_with_suggestions = {}
    
    for msg in messages:
        if isinstance(msg.tool_former_data, dict):
            tool_name = msg.tool_former_data.get('name', '')
            if tool_name in suggestion_tools:
                msgs_with_suggestions[tool_name] = msgs_with_suggestions.get(tool_name, 0) + 1
    
    print(f"\nCode modification tools (suggestions):")
    for tool, count in msgs_with_suggestions.items():
        print(f"  {tool}: {count}")
    
    # Check userDecision field in toolFormerData
    decisions = {}
    for msg in messages:
        if isinstance(msg.tool_former_data, dict):
            decision = msg.tool_former_data.get('userDecision')
            if decision:
                tool_name = msg.tool_former_data.get('name', 'unknown')
                key = f"{tool_name}_{decision}"
                decisions[key] = decisions.get(key, 0) + 1
    
    print(f"\nUser decisions on tool suggestions:")
    for decision, count in sorted(decisions.items()):
        print(f"  {decision}: {count}")

