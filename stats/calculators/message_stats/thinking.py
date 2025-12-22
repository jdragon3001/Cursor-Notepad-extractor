"""Message thinking statistics (Stats 12-15)."""

from typing import Dict, Any, List
from stats.models.message import Message
from .base import MessageStatsBase


class MessageThinkingStats(MessageStatsBase):
    """Calculate thinking and reasoning statistics."""
    
    def __init__(self, messages: List[Message]):
        """Initialize with messages."""
        super().__init__(messages)
    
    def calculate(self) -> Dict[str, Any]:
        """Calculate all thinking stats."""
        return {
            'messages_with_thinking': self.stat_012_messages_with_thinking(),
            'thinking_text_length': self.stat_013_thinking_text_length(),
            'thinking_duration': self.stat_014_thinking_duration(),
            'thinking_blocks_per_message': self.stat_015_thinking_blocks_per_message(),
        }
    
    def stat_012_messages_with_thinking(self) -> Dict[str, Any]:
        """Stat #12: Messages with thinking."""
        with_thinking = self.filter_by(self.messages, lambda m: m.has_thinking)
        total = len(self.messages)
        
        return self.create_stat_result(
            value=len(with_thinking),
            label='Messages with thinking',
            category='Messages',
            data_source='bubbleId',
            stat_type='count',
            percentage=self.percentage(len(with_thinking), total),
            breakdown={
                'with_thinking': len(with_thinking),
                'without_thinking': total - len(with_thinking)
            }
        )
    
    def stat_013_thinking_text_length(self) -> Dict[str, Any]:
        """Stat #13: Thinking text length."""
        lengths = []
        for m in self.messages:
            if m.has_thinking:
                # Handle both string and dict formats
                if isinstance(m.thinking, str):
                    lengths.append(len(m.thinking))
                elif isinstance(m.thinking, dict):
                    text = m.thinking.get('text', '') or m.thinking.get('content', '')
                    lengths.append(len(str(text)))
        
        return self.create_stat_result(
            value=self.average(lengths),
            label='Thinking text length (characters)',
            category='Messages',
            data_source='bubbleId',
            stat_type='numeric',
            median=self.median(lengths),
            min=self.min_val(lengths),
            max=self.max_val(lengths),
            p95=self.percentile(lengths, 95),
            std_dev=self.std_dev(lengths),
            distribution=self.distribution(lengths, bins=20),
            sample_size=len(lengths)
        )
    
    def stat_014_thinking_duration(self) -> Dict[str, Any]:
        """Stat #14: Thinking duration."""
        durations = [
            m.thinking_duration_ms for m in self.messages 
            if m.thinking_duration_ms
        ]
        
        # Convert to seconds for readability
        durations_sec = [d / 1000 for d in durations]
        
        return self.create_stat_result(
            value=self.average(durations_sec),
            label='Thinking duration (seconds)',
            category='Messages',
            data_source='bubbleId',
            stat_type='numeric',
            median=self.median(durations_sec),
            min=self.min_val(durations_sec),
            max=self.max_val(durations_sec),
            p95=self.percentile(durations_sec, 95),
            std_dev=self.std_dev(durations_sec),
            distribution=self.distribution(durations_sec, bins=20),
            sample_size=len(durations_sec)
        )
    
    def stat_015_thinking_blocks_per_message(self) -> Dict[str, Any]:
        """Stat #15: Thinking blocks per message."""
        # Count thinking blocks (thinking field can be string, dict, or list)
        block_counts = []
        for m in self.messages:
            if m.thinking:
                if isinstance(m.thinking, list):
                    block_counts.append(len(m.thinking))
                else:
                    # Single thinking block
                    block_counts.append(1)
        
        if not block_counts:
            return self.create_stat_result(
                value=0,
                label='Thinking blocks per message',
                category='Messages',
                data_source='bubbleId',
                stat_type='numeric',
                sample_size=0
            )
        
        return self.create_stat_result(
            value=self.average(block_counts),
            label='Thinking blocks per message',
            category='Messages',
            data_source='bubbleId',
            stat_type='numeric',
            median=self.median(block_counts),
            min=self.min_val(block_counts),
            max=self.max_val(block_counts),
            p95=self.percentile(block_counts, 95),
            std_dev=self.std_dev(block_counts),
            distribution=self.distribution(block_counts, bins=10),
            sample_size=len(block_counts)
        )

