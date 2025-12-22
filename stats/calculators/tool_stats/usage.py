"""Tool usage statistics."""

import logging
from typing import Dict, Any, List
from collections import Counter

from stats.models.message import Message
from .base import ToolStatsBase

logger = logging.getLogger(__name__)


class ToolUsageStats(ToolStatsBase):
    """Calculate tool usage-related stats."""
    
    def calculate_all(self) -> Dict[str, Any]:
        """Calculate all stats in this module."""
        return {
            'total_tool_invocations': self.stat_tool_invocations(),
            'tool_success_rate': self.stat_tool_success_rate(),
            'tool_error_rate': self.stat_tool_error_rate(),
            'tool_cancellation_rate': self.stat_tool_cancellation_rate(),
            'messages_with_tools': self.stat_messages_with_tools(),
            'most_used_tools': self.stat_most_used_tools(),
            'tool_status_distribution': self.stat_tool_status_distribution(),
            'tools_per_message': self.stat_tools_per_message(),
            'tool_arg_length': self.stat_tool_arg_length(),
            'unique_tool_types': self.stat_unique_tool_types(),
        }
    
    def _get_messages_with_tools(self) -> List[Message]:
        """Get messages that have tool former data."""
        return [m for m in self.messages if m.has_tool_former_data]
    
    def _get_all_tool_statuses(self) -> List[str]:
        """Extract all tool statuses from messages."""
        statuses = []
        for msg in self._get_messages_with_tools():
            status = msg.get_tool_former_status()
            if status:
                statuses.append(status)
        return statuses
    
    def _get_all_tool_names(self) -> List[str]:
        """Extract all tool names from messages."""
        names = []
        for msg in self._get_messages_with_tools():
            name = msg.get_tool_former_name()
            if name:
                names.append(name)
        return names
    
    def stat_tool_invocations(self) -> Dict[str, Any]:
        """Total tool invocations."""
        messages_with_tools = self._get_messages_with_tools()
        
        return self.create_stat_result(
            value=len(messages_with_tools),
            label='Total tool invocations',
            category='Tools',
            data_source='toolFormerData',
            stat_type='count',
            description='Total number of messages with tool former data'
        )
    
    def stat_tool_success_rate(self) -> Dict[str, Any]:
        """Tool success rate percentage."""
        statuses = self._get_all_tool_statuses()
        total = len(statuses)
        success_count = statuses.count('success') + statuses.count('completed')
        
        return self.create_stat_result(
            value=self.percentage(success_count, total) if total > 0 else 0.0,
            label='Tool success rate',
            category='Tools',
            data_source='toolFormerData',
            stat_type='percentage',
            breakdown={
                'total': total,
                'success': success_count,
                'percentage': self.percentage(success_count, total) if total > 0 else 0.0
            }
        )
    
    def stat_tool_error_rate(self) -> Dict[str, Any]:
        """Tool error rate percentage."""
        statuses = self._get_all_tool_statuses()
        total = len(statuses)
        error_count = statuses.count('error')
        
        return self.create_stat_result(
            value=self.percentage(error_count, total) if total > 0 else 0.0,
            label='Tool error rate',
            category='Tools',
            data_source='toolFormerData',
            stat_type='percentage',
            breakdown={
                'total': total,
                'errors': error_count,
                'percentage': self.percentage(error_count, total) if total > 0 else 0.0
            }
        )
    
    def stat_tool_cancellation_rate(self) -> Dict[str, Any]:
        """Tool cancellation rate percentage."""
        statuses = self._get_all_tool_statuses()
        total = len(statuses)
        cancelled_count = statuses.count('cancelled')
        
        return self.create_stat_result(
            value=self.percentage(cancelled_count, total) if total > 0 else 0.0,
            label='Tool cancellation rate',
            category='Tools',
            data_source='toolFormerData',
            stat_type='percentage',
            breakdown={
                'total': total,
                'cancelled': cancelled_count,
                'percentage': self.percentage(cancelled_count, total) if total > 0 else 0.0
            }
        )
    
    def stat_messages_with_tools(self) -> Dict[str, Any]:
        """Messages containing tool usage."""
        messages_with_tools = self._get_messages_with_tools()
        total = len(self.messages)
        
        return self.create_stat_result(
            value=len(messages_with_tools),
            label='Messages with tools',
            category='Tools',
            data_source='toolFormerData',
            stat_type='count',
            percentage=self.percentage(len(messages_with_tools), total),
            breakdown={
                'with_tools': len(messages_with_tools),
                'total_messages': total
            }
        )
    
    def stat_most_used_tools(self) -> Dict[str, Any]:
        """Most frequently used tools."""
        tool_names = self._get_all_tool_names()
        most_common = Counter(tool_names).most_common(10)
        
        return self.create_stat_result(
            value=most_common,
            label='Most used tools',
            category='Tools',
            data_source='toolFormerData',
            stat_type='distribution',
            breakdown={
                'top_10': [{'tool': tool, 'count': count} for tool, count in most_common],
                'unique_tools': len(set(tool_names))
            }
        )
    
    def stat_tool_status_distribution(self) -> Dict[str, Any]:
        """Distribution of tool statuses."""
        statuses = self._get_all_tool_statuses()
        distribution = Counter(statuses)
        
        return self.create_stat_result(
            value=dict(distribution),
            label='Tool status distribution',
            category='Tools',
            data_source='toolFormerData',
            stat_type='distribution',
            breakdown={
                status: {
                    'count': count,
                    'percentage': self.percentage(count, len(statuses))
                }
                for status, count in distribution.items()
            }
        )
    
    def stat_tools_per_message(self) -> Dict[str, Any]:
        """Average tools per message with tools."""
        messages_with_tools = self._get_messages_with_tools()
        
        # For now, each message has 1 tool former data entry
        # In the future, we might have multiple tool calls per message
        tools_per_msg = [1 for _ in messages_with_tools]
        
        return self.create_stat_result(
            value=self.average(tools_per_msg) if tools_per_msg else 0.0,
            label='Tools per message',
            category='Tools',
            data_source='toolFormerData',
            stat_type='numeric',
            median=self.median(tools_per_msg) if tools_per_msg else 0.0,
            min=self.min_val(tools_per_msg) if tools_per_msg else 0.0,
            max=self.max_val(tools_per_msg) if tools_per_msg else 0.0
        )
    
    def stat_tool_arg_length(self) -> Dict[str, Any]:
        """Average length of tool arguments."""
        arg_lengths = []
        for msg in self._get_messages_with_tools():
            args = msg.get_tool_former_args()
            if args:
                arg_lengths.append(len(args))
        
        return self.create_stat_result(
            value=self.average(arg_lengths) if arg_lengths else 0.0,
            label='Tool argument length (characters)',
            category='Tools',
            data_source='toolFormerData',
            stat_type='numeric',
            median=self.median(arg_lengths) if arg_lengths else 0.0,
            min=self.min_val(arg_lengths) if arg_lengths else 0.0,
            max=self.max_val(arg_lengths) if arg_lengths else 0.0,
            sample_size=len(arg_lengths)
        )
    
    def stat_unique_tool_types(self) -> Dict[str, Any]:
        """Number of unique tool types used."""
        tool_names = self._get_all_tool_names()
        unique_tools = set(tool_names)
        
        return self.create_stat_result(
            value=len(unique_tools),
            label='Unique tool types',
            category='Tools',
            data_source='toolFormerData',
            stat_type='count',
            breakdown={
                'unique_tools': len(unique_tools),
                'total_invocations': len(tool_names),
                'tool_list': sorted(list(unique_tools))
            }
        )

