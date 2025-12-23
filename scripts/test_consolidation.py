import sys
sys.path.append('.')

from stats.orchestrator import StatsOrchestrator
from stats.consolidator import MessageConsolidator
from utils.config import Config

# Load messages
orch = StatsOrchestrator(Config.get_global_db_path())
orch.extract_all_data()

print(f"Raw messages: {len(orch.messages)}")

# Consolidate
consolidated = MessageConsolidator.consolidate(orch.messages)
print(f"Consolidated messages: {len(consolidated)}")

# Show a sample
print("\n=== Sample Conversation (first 10 messages) ===\n")
for i, msg in enumerate(consolidated[:10], 1):
    msg_type = "USER" if msg.is_user_message else "AI"
    text_preview = (msg.text[:100] + "...") if msg.text and len(msg.text) > 100 else (msg.text or "(no text)")
    
    print(f"{i}. [{msg_type}] {msg.created_at}")
    print(f"   Text: {text_preview}")
    print(f"   Has thinking: {msg.has_thinking}")
    print(f"   Has code: {msg.has_code} ({msg.get_code_block_count()} blocks)")
    print(f"   Has tools: {msg.has_tools} ({msg.get_tool_count()} tools)")
    
    if msg.raw_data and msg.raw_data.get('consolidated'):
        print(f"   [CONSOLIDATED from {msg.raw_data.get('fragment_count')} fragments]")
    print()

