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
            'response_time_to_suggestions': self.stat_038_response_time_to_suggestions(),
            'messages_with_git_diffs': self.stat_039_messages_with_git_diffs(),
            'messages_with_diff_histories': self.stat_040_messages_with_diff_histories(),
            'messages_with_human_changes': self.stat_041_messages_with_human_changes(),
        }
    
    def stat_031_suggested_code_blocks(self) -> Dict[str, Any]:
        """Stat #31: Suggested code blocks."""
        total_blocks = sum(len(m.suggested_code_blocks) for m in self.messages)
        messages_with_suggestions = len([m for m in self.messages if len(m.suggested_code_blocks) > 0])
        
        return self.create_stat_result(
            value=total_blocks,
            label='Suggested code blocks',
            category='Messages',
            data_source='bubbleId',
            stat_type='count',
            messages_with_suggestions=messages_with_suggestions,
            percentage=self.percentage(messages_with_suggestions, len(self.messages))
        )
    
    def stat_032_suggestion_action_types(self) -> Dict[str, Any]:
        """Stat #32: Suggestion action types (replace/insert/delete)."""
        actions = []
        for m in self.messages:
            for block in m.suggested_code_blocks:
                if isinstance(block, dict):
                    action = block.get('action') or block.get('type')
                    if action:
                        actions.append(action)
        
        action_breakdown = self.most_common(actions, n=10) if actions else []
        
        return self.create_stat_result(
            value=len(set(actions)),
            label='Unique suggestion action types',
            category='Messages',
            data_source='bubbleId',
            stat_type='count',
            action_breakdown=action_breakdown,
            total_suggestions=len(actions)
        )
    
    def stat_033_assistant_suggested_diffs(self) -> Dict[str, Any]:
        """Stat #33: Assistant suggested diffs."""
        # Count diffs in raw_data
        diff_count = 0
        for m in self.messages:
            if m.raw_data:
                if 'diff' in m.raw_data or 'diffs' in m.raw_data:
                    diff_count += 1
                elif 'suggestedDiffs' in m.raw_data:
                    diffs = m.raw_data.get('suggestedDiffs', [])
                    diff_count += len(diffs) if isinstance(diffs, list) else 1
        
        return self.create_stat_result(
            value=diff_count,
            label='Assistant suggested diffs',
            category='Messages',
            data_source='bubbleId',
            stat_type='count'
        )
    
    def stat_034_accepted_suggestions(self) -> Dict[str, Any]:
        """Stat #34: Accepted suggestions."""
        accepted = 0
        for m in self.messages:
            for block in m.suggested_code_blocks:
                if isinstance(block, dict):
                    if block.get('accepted') or block.get('status') == 'accepted':
                        accepted += 1
        
        return self.create_stat_result(
            value=accepted,
            label='Accepted suggestions',
            category='Messages',
            data_source='bubbleId',
            stat_type='count',
            note='Limited data: acceptance tracking may be incomplete'
        )
    
    def stat_035_rejected_suggestions(self) -> Dict[str, Any]:
        """Stat #35: Rejected suggestions."""
        rejected = 0
        for m in self.messages:
            for block in m.suggested_code_blocks:
                if isinstance(block, dict):
                    if block.get('rejected') or block.get('status') == 'rejected':
                        rejected += 1
        
        return self.create_stat_result(
            value=rejected,
            label='Rejected suggestions',
            category='Messages',
            data_source='bubbleId',
            stat_type='count',
            note='Limited data: rejection tracking may be incomplete'
        )
    
    def stat_036_modified_suggestions(self) -> Dict[str, Any]:
        """Stat #36: Modified suggestions."""
        modified = 0
        for m in self.messages:
            for block in m.suggested_code_blocks:
                if isinstance(block, dict):
                    if block.get('modified') or block.get('status') == 'modified':
                        modified += 1
        
        return self.create_stat_result(
            value=modified,
            label='Modified suggestions',
            category='Messages',
            data_source='bubbleId',
            stat_type='count',
            note='Limited data: modification tracking may be incomplete'
        )
    
    def stat_037_acceptance_rate(self) -> Dict[str, Any]:
        """Stat #37: Acceptance rate."""
        accepted = 0
        rejected = 0
        total_with_status = 0
        
        for m in self.messages:
            for block in m.suggested_code_blocks:
                if isinstance(block, dict):
                    status = block.get('status')
                    if status in ['accepted', 'rejected', 'modified']:
                        total_with_status += 1
                        if status == 'accepted':
                            accepted += 1
                        elif status == 'rejected':
                            rejected += 1
        
        rate = self.percentage(accepted, total_with_status) if total_with_status > 0 else 0
        
        return self.create_stat_result(
            value=rate,
            label='Suggestion acceptance rate (%)',
            category='Messages',
            data_source='bubbleId',
            stat_type='percentage',
            accepted=accepted,
            rejected=rejected,
            total_tracked=total_with_status,
            note='Based on suggestions with status tracking'
        )
    
    def stat_038_response_time_to_suggestions(self) -> Dict[str, Any]:
        """Stat #38: Response time to suggestions."""
        # This would require tracking time between AI suggestion and user action
        # Limited data available in local storage
        return self.create_stat_result(
            value=0,
            label='Response time to suggestions (seconds)',
            category='Messages',
            data_source='bubbleId',
            stat_type='numeric',
            note='Insufficient data: response timing not tracked locally',
            sample_size=0
        )
    
    def stat_039_messages_with_git_diffs(self) -> Dict[str, Any]:
        """Stat #39: Messages with git diffs."""
        with_diffs = 0
        for m in self.messages:
            if m.raw_data:
                if 'gitDiff' in m.raw_data or 'gitDiffs' in m.raw_data:
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
        with_history = 0
        for m in self.messages:
            if m.raw_data:
                if 'diffHistory' in m.raw_data or 'historyDiffs' in m.raw_data:
                    with_history += 1
        
        return self.create_stat_result(
            value=with_history,
            label='Messages with diff histories',
            category='Messages',
            data_source='bubbleId',
            stat_type='count',
            percentage=self.percentage(with_history, len(self.messages))
        )
    
    def stat_041_messages_with_human_changes(self) -> Dict[str, Any]:
        """Stat #41: Messages with human changes (manual edits after AI)."""
        with_changes = 0
        for m in self.messages:
            if m.raw_data:
                if 'humanEdits' in m.raw_data or 'manualChanges' in m.raw_data:
                    with_changes += 1
                # Check for edited flag
                elif m.raw_data.get('edited') or m.raw_data.get('userModified'):
                    with_changes += 1
        
        return self.create_stat_result(
            value=with_changes,
            label='Messages with human changes',
            category='Messages',
            data_source='bubbleId',
            stat_type='count',
            percentage=self.percentage(with_changes, len(self.messages))
        )

