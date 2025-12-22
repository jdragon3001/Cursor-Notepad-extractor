"""Message tool usage statistics (Stats 16-20)."""

from typing import Dict, Any, List
from stats.models.message import Message
from .base import MessageStatsBase


class MessageToolStats(MessageStatsBase):
    """Calculate tool usage statistics."""
    
    def __init__(self, messages: List[Message]):
        """Initialize with messages."""
        super().__init__(messages)
    
    def calculate(self) -> Dict[str, Any]:
        """Calculate all tool stats."""
        return {
            'messages_with_tools': self.stat_016_messages_with_tools(),
            'tool_invocations': self.stat_017_tool_invocations(),
            'tools_per_message': self.stat_018_tools_per_message(),
            'tool_usage_by_type': self.stat_019_tool_usage_by_type(),
            'tool_success_failure': self.stat_020_tool_success_failure(),
        }
    
    def stat_016_messages_with_tools(self) -> Dict[str, Any]:
        """Stat #16: Messages with tools."""
        with_tools = self.filter_by(self.messages, lambda m: m.has_tools)
        total = len(self.messages)
        
        return self.create_stat_result(
            value=len(with_tools),
            label='Messages with tools',
            category='Messages',
            data_source='bubbleId',
            stat_type='count',
            percentage=self.percentage(len(with_tools), total),
            breakdown={
                'with_tools': len(with_tools),
                'without_tools': total - len(with_tools)
            }
        )
    
    def stat_017_tool_invocations(self) -> Dict[str, Any]:
        """Stat #17: Tool invocations."""
        total_tools = sum(m.get_tool_count() for m in self.messages)
        
        return self.create_stat_result(
            value=total_tools,
            label='Tool invocations',
            category='Messages',
            data_source='bubbleId',
            stat_type='count'
        )
    
    def stat_018_tools_per_message(self) -> Dict[str, Any]:
        """Stat #18: Tools per message."""
        tool_counts = [m.get_tool_count() for m in self.messages if m.has_tools]
        
        if not tool_counts:
            return self.create_stat_result(
                value=0,
                label='Tools per message',
                category='Messages',
                data_source='bubbleId',
                stat_type='numeric',
                sample_size=0
            )
        
        return self.create_stat_result(
            value=self.average(tool_counts),
            label='Tools per message',
            category='Messages',
            data_source='bubbleId',
            stat_type='numeric',
            median=self.median(tool_counts),
            min=self.min_val(tool_counts),
            max=self.max_val(tool_counts),
            p95=self.percentile(tool_counts, 95),
            std_dev=self.std_dev(tool_counts),
            distribution=self.distribution(tool_counts, bins=10),
            sample_size=len(tool_counts)
        )
    
    def stat_019_tool_usage_by_type(self) -> Dict[str, Any]:
        """Stat #19: Tool usage by type."""
        tool_types = []
        for msg in self.messages:
            tool_types.extend(msg.get_tool_types())
        
        if not tool_types:
            return self.create_stat_result(
                value=0,
                label='Unique tool types',
                category='Messages',
                data_source='bubbleId',
                stat_type='count',
                top_tools=[],
                total_invocations=0
            )
        
        top_tools = self.most_common(tool_types, n=20)
        
        return self.create_stat_result(
            value=len(set(tool_types)),
            label='Unique tool types',
            category='Messages',
            data_source='bubbleId',
            stat_type='count',
            top_tools=top_tools,
            total_invocations=len(tool_types)
        )
    
    def stat_020_tool_success_failure(self) -> Dict[str, Any]:
        """Stat #20: Tool success/failure."""
        successes = 0
        failures = 0
        
        for msg in self.messages:
            for tool in msg.tool_results:
                # Check for success/failure indicators
                if isinstance(tool, dict):
                    if tool.get('success') or tool.get('status') == 'success':
                        successes += 1
                    elif tool.get('error') or tool.get('status') == 'error' or tool.get('status') == 'failure':
                        failures += 1
                    elif 'result' in tool and tool['result'] is not None:
                        # If there's a result, assume success
                        successes += 1
        
        total = successes + failures
        
        return self.create_stat_result(
            value=successes,
            label='Successful tool invocations',
            category='Messages',
            data_source='bubbleId',
            stat_type='count',
            failures=failures,
            total=total,
            success_rate=self.percentage(successes, total) if total > 0 else 0,
            breakdown={
                'successes': successes,
                'failures': failures,
                'total': total
            }
        )

