"""Message code suggestions and diffs statistics (Stats 31-41)."""

from typing import Dict, Any, List
from stats.models.message import Message
from .base import MessageStatsBase


class MessageSuggestionsStats(MessageStatsBase):
    """Calculate code suggestions and diff statistics."""
    
    def __init__(self, messages: List[Message]):
        """Initialize with messages."""
        super().__init__(messages)
    
    def calculate(self) -> Dict[str, Any]:
        """Calculate all suggestion stats."""
        return {
            'suggested_code_blocks': self.stat_031_suggested_code_blocks(),
            'suggestion_action_types': self.stat_032_suggestion_action_types(),
            'assistant_suggested_diffs': self.stat_033_assistant_suggested_diffs(),
            'accepted_suggestions': self.stat_034_accepted_suggestions(),
            'rejected_suggestions': self.stat_035_rejected_suggestions(),
            'modified_suggestions': self.stat_036_modified_suggestions(),
            'acceptance_rate': self.stat_037_acceptance_rate(),
            # response_time_to_suggestions removed - timing data not available
            'messages_with_git_diffs': self.stat_039_messages_with_git_diffs(),
            'messages_with_diff_histories': self.stat_040_messages_with_diff_histories(),
            'messages_with_human_changes': self.stat_041_messages_with_human_changes(),
        }
    
    def stat_031_suggested_code_blocks(self) -> Dict[str, Any]:
        """Stat #31: Assistant messages with code blocks."""
        # Assistant messages (type=2) with code blocks are suggestions
        assistant_msgs = [m for m in self.messages if m.message_type == 2]
        with_code = [m for m in assistant_msgs if m.code_blocks]
        
        total_blocks = sum(len(m.code_blocks) for m in with_code)
        
        return self.create_stat_result(
            value=total_blocks,
            label='Suggested code blocks',
            category='Messages',
            data_source='bubbleId',
            stat_type='count',
            messages_with_suggestions=len(with_code),
            percentage=self.percentage(len(with_code), len(self.messages))
        )
    
    def stat_032_suggestion_action_types(self) -> Dict[str, Any]:
        """Stat #32: Code modification tool types."""
        modification_tools = ['search_replace', 'apply_patch', 'edit_file', 'edit_file_v2', 'write', 'delete_file']
        tool_counts = {}
        
        for m in self.messages:
            if isinstance(m.tool_former_data, dict):
                tool_name = m.tool_former_data.get('name', '')
                if tool_name in modification_tools:
                    tool_counts[tool_name] = tool_counts.get(tool_name, 0) + 1
        
        top_tools = sorted(tool_counts.items(), key=lambda x: x[1], reverse=True)
        
        return self.create_stat_result(
            value=len(tool_counts),
            label='Unique suggestion action types',
            category='Messages',
            data_source='toolFormerData',
            stat_type='count',
            tool_distribution=top_tools,
            total_suggestions=sum(tool_counts.values())
        )
    
    def stat_033_assistant_suggested_diffs(self) -> Dict[str, Any]:
        """Stat #33: Total code modification suggestions."""
        modification_tools = ['search_replace', 'apply_patch', 'edit_file', 'edit_file_v2']
        suggestion_count = 0
        
        for m in self.messages:
            if isinstance(m.tool_former_data, dict):
                tool_name = m.tool_former_data.get('name', '')
                if tool_name in modification_tools:
                    suggestion_count += 1
        
        return self.create_stat_result(
            value=suggestion_count,
            label='Assistant suggested diffs',
            category='Messages',
            data_source='toolFormerData',
            stat_type='count'
        )
    
    def stat_034_accepted_suggestions(self) -> Dict[str, Any]:
        """Stat #34: Accepted suggestions (userDecision=accepted)."""
        accepted_count = 0
        accepted_by_tool = {}
        
        for m in self.messages:
            if isinstance(m.tool_former_data, dict):
                decision = m.tool_former_data.get('userDecision')
                if decision == 'accepted':
                    accepted_count += 1
                    tool_name = m.tool_former_data.get('name', 'unknown')
                    accepted_by_tool[tool_name] = accepted_by_tool.get(tool_name, 0) + 1
        
        top_accepted = sorted(accepted_by_tool.items(), key=lambda x: x[1], reverse=True)[:10]
        
        return self.create_stat_result(
            value=accepted_count,
            label='Accepted suggestions',
            category='Messages',
            data_source='toolFormerData',
            stat_type='count',
            by_tool=top_accepted
        )
    
    def stat_035_rejected_suggestions(self) -> Dict[str, Any]:
        """Stat #35: Rejected suggestions (userDecision=rejected)."""
        rejected_count = 0
        rejected_by_tool = {}
        
        for m in self.messages:
            if isinstance(m.tool_former_data, dict):
                decision = m.tool_former_data.get('userDecision')
                if decision == 'rejected':
                    rejected_count += 1
                    tool_name = m.tool_former_data.get('name', 'unknown')
                    rejected_by_tool[tool_name] = rejected_by_tool.get(tool_name, 0) + 1
        
        top_rejected = sorted(rejected_by_tool.items(), key=lambda x: x[1], reverse=True)[:10]
        
        return self.create_stat_result(
            value=rejected_count,
            label='Rejected suggestions',
            category='Messages',
            data_source='toolFormerData',
            stat_type='count',
            by_tool=top_rejected
        )
    
    def stat_036_modified_suggestions(self) -> Dict[str, Any]:
        """Stat #36: Modified suggestions (userDecision=modified)."""
        modified_count = 0
        modified_by_tool = {}
        
        for m in self.messages:
            if isinstance(m.tool_former_data, dict):
                decision = m.tool_former_data.get('userDecision')
                if decision == 'modified':
                    modified_count += 1
                    tool_name = m.tool_former_data.get('name', 'unknown')
                    modified_by_tool[tool_name] = modified_by_tool.get(tool_name, 0) + 1
        
        return self.create_stat_result(
            value=modified_count,
            label='Modified suggestions',
            category='Messages',
            data_source='toolFormerData',
            stat_type='count',
            by_tool=list(modified_by_tool.items())
        )
    
    def stat_037_acceptance_rate(self) -> Dict[str, Any]:
        """Stat #37: Suggestion acceptance rate."""
        accepted = 0
        rejected = 0
        modified = 0
        
        for m in self.messages:
            if isinstance(m.tool_former_data, dict):
                decision = m.tool_former_data.get('userDecision')
                if decision == 'accepted':
                    accepted += 1
                elif decision == 'rejected':
                    rejected += 1
                elif decision == 'modified':
                    modified += 1
        
        total = accepted + rejected + modified
        acceptance_rate = (accepted / total * 100) if total > 0 else 0
        
        return self.create_stat_result(
            value=round(acceptance_rate, 2),
            label='Suggestion acceptance rate (%)',
            category='Messages',
            data_source='toolFormerData',
            stat_type='percentage',
            accepted=accepted,
            rejected=rejected,
            modified=modified,
            total_decided=total
        )
    
    def stat_038_response_time_to_suggestions(self) -> Dict[str, Any]:
        """Stat #38: Response time to suggestions."""
        # This would require timing data between suggestion and acceptance
        # Not available in current data structure
        return self.create_stat_result(
            value=0,
            label='Response time to suggestions (seconds)',
            category='Messages',
            data_source='bubbleId',
            stat_type='numeric',
            note='Timing data not available in current schema'
        )
    
    def stat_039_messages_with_git_diffs(self) -> Dict[str, Any]:
        """Stat #39: Messages with git diffs."""
        with_diffs = 0
        for m in self.messages:
            if m.raw_data and 'gitDiffs' in m.raw_data and m.raw_data['gitDiffs']:
                with_diffs += 1
        
        return self.create_stat_result(
            value=with_diffs,
            label='Messages with git diffs',
            category='Messages',
            data_source='bubbleId',
            stat_type='count',
            percentage=self.percentage(with_diffs, len(self.messages))
        )
    
    def stat_040_messages_with_diff_histories(self) -> Dict[str, Any]:
        """Stat #40: Messages with diff histories."""
        with_histories = 0
        for m in self.messages:
            if m.raw_data and 'diffHistories' in m.raw_data and m.raw_data['diffHistories']:
                with_histories += 1
        
        return self.create_stat_result(
            value=with_histories,
            label='Messages with diff histories',
            category='Messages',
            data_source='bubbleId',
            stat_type='count',
            percentage=self.percentage(with_histories, len(self.messages))
        )
    
    def stat_041_messages_with_human_changes(self) -> Dict[str, Any]:
        """Stat #41: Messages with human changes."""
        with_changes = 0
        for m in self.messages:
            if m.raw_data and 'humanChanges' in m.raw_data and m.raw_data['humanChanges']:
                with_changes += 1
        
        return self.create_stat_result(
            value=with_changes,
            label='Messages with human changes',
            category='Messages',
            data_source='bubbleId',
            stat_type='count',
            percentage=self.percentage(with_changes, len(self.messages))
        )
