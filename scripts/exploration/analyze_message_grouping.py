import sys
sys.path.append('.')

from stats.extractors.message_extractor import MessageExtractor
from utils.config import Config

extractor = MessageExtractor(Config.get_global_db_path())
messages = extractor.extract()

# Group by composer and timestamp
from collections import defaultdict

composer_messages = defaultdict(list)
for msg in messages[:100]:  # First 100 to see pattern
    composer_messages[msg.composer_id].append(msg)

# Show one session
first_composer = list(composer_messages.keys())[0] if composer_messages else None
if first_composer:
    session_msgs = sorted(composer_messages[first_composer], key=lambda m: m.created_at)
    print(f"Session: {first_composer}")
    print(f"Total messages: {len(session_msgs)}\n")
    
    for msg in session_msgs[:10]:
        print(f"Bubble ID: {msg.bubble_id}")
        print(f"  Type: {'USER' if msg.is_user_message else 'AI'}")
        print(f"  Created: {msg.created_at}")
        print(f"  Has text: {msg.has_text}")
        print(f"  Has thinking: {msg.has_thinking}")
        print(f"  Has tools: {msg.has_tools}")
        print(f"  Has code: {msg.has_code}")
        print()

