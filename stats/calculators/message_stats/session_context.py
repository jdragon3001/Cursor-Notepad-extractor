"""Message session context statistics (Stats 50-52)."""

from typing import Dict, Any, List
from stats.models.message import Message
from .base import MessageStatsBase


class MessageSessionContextStats(MessageStatsBase):
    """Calculate session context statistics."""
    
    def __init__(self, messages: List[Message]):
        """Initialize with messages."""
        super().__init__(messages)
    
    def calculate(self) -> Dict[str, Any]:
        """Calculate all session context stats."""
        return {
            'agentic_messages': self.stat_050_agentic_messages(),
            'chat_messages': self.stat_051_chat_messages(),
            'messages_with_checkpoints': self.stat_052_messages_with_checkpoints(),
        }
    
    def stat_050_agentic_messages(self) -> Dict[str, Any]:
        """Stat #50: Agentic messages (agent mode)."""
        agentic = self.filter_by(self.messages, lambda m: m.is_agentic)
        total = len(self.messages)
        
        return self.create_stat_result(
            value=len(agentic),
            label='Agentic messages (agent mode)',
            category='Messages',
            data_source='bubbleId',
            stat_type='count',
            percentage=self.percentage(len(agentic), total),
            breakdown={
                'agentic': len(agentic),
                'chat': total - len(agentic)
            }
        )
    
    def stat_051_chat_messages(self) -> Dict[str, Any]:
        """Stat #51: Chat messages (non-agent mode)."""
        chat = self.filter_by(self.messages, lambda m: not m.is_agentic)
        total = len(self.messages)
        
        return self.create_stat_result(
            value=len(chat),
            label='Chat messages (non-agent mode)',
            category='Messages',
            data_source='bubbleId',
            stat_type='count',
            percentage=self.percentage(len(chat), total),
            breakdown={
                'chat': len(chat),
                'agentic': total - len(chat)
            }
        )
    
    def stat_052_messages_with_checkpoints(self) -> Dict[str, Any]:
        """Stat #52: Messages with checkpoints."""
        # Check if messages have checkpoint references in raw_data
        with_checkpoints = 0
        for m in self.messages:
            if m.raw_data:
                if 'checkpointId' in m.raw_data or 'checkpoint' in m.raw_data:
                    with_checkpoints += 1
        
        return self.create_stat_result(
            value=with_checkpoints,
            label='Messages with checkpoints',
            category='Messages',
            data_source='bubbleId',
            stat_type='count',
            percentage=self.percentage(with_checkpoints, len(self.messages))
        )

