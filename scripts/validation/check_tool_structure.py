import sys
sys.path.insert(0, '.')

from stats.extractors.message_extractor import MessageExtractor
from pathlib import Path
import json

db_path = Path.home() / 'AppData' / 'Roaming' / 'Cursor' / 'User' / 'globalStorage' / 'state.vscdb'

with MessageExtractor(db_path) as extractor:
    messages = extractor.extract()
    
    # Find a message with write tool
    for msg in messages:
        if isinstance(msg.tool_former_data, dict) and msg.tool_former_data.get('name') == 'write':
            print("Found write tool!")
            print(json.dumps(msg.tool_former_data, indent=2))
            break

