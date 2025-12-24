"""Message count statistics (Stats 1-4)."""

from typing import Dict, Any, List
from stats.models.message import Message
from .base import MessageStatsBase


class MessageCountStats(MessageStatsBase):
    """Calculate message count statistics."""
    
    def calculate(self) -> Dict[str, Any]:
        """Calculate all count stats."""
        return {
            'total_messages': self.stat_001_total_messages(),
            'user_messages': self.stat_002_user_messages(),
            'ai_messages': self.stat_003_ai_messages(),
            'messages_per_session': self.stat_004_messages_per_session(),
        }
    
    def stat_001_total_messages(self) -> Dict[str, Any]:
        """Stat #1: Total messages."""
        return self.create_stat_result(
            value=self.count(self.messages),
            label='Total messages',
            category='Messages',
            data_source='bubbleId',
            stat_type='count'
        )
    
    def stat_002_user_messages(self) -> Dict[str, Any]:
        """Stat #2: User messages."""
        user_msgs = self.filter_by(self.messages, lambda m: m.is_user_message)
        total = len(self.messages)
        
        return self.create_stat_result(
            value=len(user_msgs),
            label='User messages',
            category='Messages',
            data_source='bubbleId',
            stat_type='count',
            percentage=self.percentage(len(user_msgs), total),
            breakdown={
                'total': total,
                'user': len(user_msgs),
                'ai': total - len(user_msgs)
            }
        )
    
    def stat_003_ai_messages(self) -> Dict[str, Any]:
        """Stat #3: AI messages."""
        ai_msgs = self.filter_by(self.messages, lambda m: m.is_ai_message)
        total = len(self.messages)
        
        return self.create_stat_result(
            value=len(ai_msgs),
            label='AI messages',
            category='Messages',
            data_source='bubbleId',
            stat_type='count',
            percentage=self.percentage(len(ai_msgs), total),
            breakdown={
                'total': total,
                'user': total - len(ai_msgs),
                'ai': len(ai_msgs)
            }
        )
    
    def stat_004_messages_per_session(self) -> Dict[str, Any]:
        """Stat #4: Messages per session."""
        sessions = self.group_by(self.messages, lambda m: m.composer_id)
        message_counts = [len(msgs) for msgs in sessions.values()]
        
        return self.create_stat_result(
            value=self.average(message_counts),
            label='Messages per session',
            category='Messages',
            data_source='bubbleId',
            stat_type='numeric',
            median=self.median(message_counts),
            min=self.min_val(message_counts),
            max=self.max_val(message_counts),
            p95=self.percentile(message_counts, 95),
            std_dev=self.std_dev(message_counts),
            distribution=self.distribution(message_counts, bins=20),
            sample_size=len(sessions)
        )
