"""Message metadata statistics (Stats 57-59)."""

from typing import Dict, Any, List
from stats.models.message import Message
from .base import MessageStatsBase


class MessageMetadataStats(MessageStatsBase):
    """Calculate message metadata statistics."""
    
    def __init__(self, messages: List[Message]):
        """Initialize with messages."""
        super().__init__(messages)
    
    def calculate(self) -> Dict[str, Any]:
        """Calculate all metadata stats."""
        return {
            'refunded_messages': self.stat_057_refunded_messages(),
            'nudge_messages': self.stat_058_nudge_messages(),
            'messages_with_server_references': self.stat_059_messages_with_server_references(),
        }
    
    def stat_057_refunded_messages(self) -> Dict[str, Any]:
        """Stat #57: Refunded messages."""
        refunded = 0
        for m in self.messages:
            if m.raw_data:
                if m.raw_data.get('refunded') or m.raw_data.get('isRefunded'):
                    refunded += 1
        
        return self.create_stat_result(
            value=refunded,
            label='Refunded messages',
            category='Messages',
            data_source='bubbleId',
            stat_type='count',
            percentage=self.percentage(refunded, len(self.messages))
        )
    
    def stat_058_nudge_messages(self) -> Dict[str, Any]:
        """Stat #58: Nudge messages."""
        nudges = 0
        for m in self.messages:
            if m.raw_data:
                if m.raw_data.get('isNudge') or m.raw_data.get('nudge'):
                    nudges += 1
        
        return self.create_stat_result(
            value=nudges,
            label='Nudge messages',
            category='Messages',
            data_source='bubbleId',
            stat_type='count',
            percentage=self.percentage(nudges, len(self.messages))
        )
    
    def stat_059_messages_with_server_references(self) -> Dict[str, Any]:
        """Stat #59: Messages with server references (serverBubbleId)."""
        with_server_ref = 0
        for m in self.messages:
            if m.raw_data:
                if 'serverBubbleId' in m.raw_data or 'serverId' in m.raw_data:
                    with_server_ref += 1
        
        return self.create_stat_result(
            value=with_server_ref,
            label='Messages with server references',
            category='Messages',
            data_source='bubbleId',
            stat_type='count',
            percentage=self.percentage(with_server_ref, len(self.messages))
        )

