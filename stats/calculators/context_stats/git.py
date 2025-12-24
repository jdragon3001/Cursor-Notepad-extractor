"""Git context statistics from RequestContext."""

import logging
from typing import Dict, Any, List

from stats.models.request_context import MessageRequestContext
from .base import ContextStatsBase

logger = logging.getLogger(__name__)


class GitContextStats(ContextStatsBase):
    """Calculate git context-related stats."""
    
    def calculate_all(self) -> Dict[str, Any]:
        """Calculate all stats in this module."""
        return {
            'contexts_with_git_changes': self.stat_contexts_with_git_changes(),
            'git_status_length': self.stat_git_status_length(),
            'contexts_with_diffs': self.stat_contexts_with_diffs(),
        }
    
    def _get_contexts_with_git(self) -> List[MessageRequestContext]:
        """Get contexts that have git status."""
        return [rc for rc in self.request_contexts if rc.has_git_changes]
    
    def stat_contexts_with_git_changes(self) -> Dict[str, Any]:
        """Contexts with git status information."""
        contexts_with_git = self._get_contexts_with_git()
        total = len(self.request_contexts)
        
        return self.create_stat_result(
            value=len(contexts_with_git),
            label='Contexts with git changes',
            category='Context',
            data_source='messageRequestContext',
            stat_type='count',
            percentage=self.percentage(len(contexts_with_git), total),
            breakdown={
                'with_git': len(contexts_with_git),
                'total_contexts': total
            }
        )
    
    def stat_git_status_length(self) -> Dict[str, Any]:
        """Average length of git status output."""
        contexts_with_git = self._get_contexts_with_git()
        git_lengths = [len(rc.git_status_raw) for rc in contexts_with_git if rc.git_status_raw]
        
        return self.create_stat_result(
            value=self.average(git_lengths) if git_lengths else 0.0,
            label='Git status length (characters)',
            category='Context',
            data_source='messageRequestContext',
            stat_type='numeric',
            median=self.median(git_lengths) if git_lengths else 0.0,
            min=self.min_val(git_lengths) if git_lengths else 0.0,
            max=self.max_val(git_lengths) if git_lengths else 0.0,
            sample_size=len(git_lengths)
        )
    
    def stat_contexts_with_diffs(self) -> Dict[str, Any]:
        """Contexts with diffs since last apply."""
        contexts_with_diffs = [rc for rc in self.request_contexts if rc.diffs_since_last_apply]
        total = len(self.request_contexts)
        
        return self.create_stat_result(
            value=len(contexts_with_diffs),
            label='Contexts with diffs since last apply',
            category='Context',
            data_source='messageRequestContext',
            stat_type='count',
            percentage=self.percentage(len(contexts_with_diffs), total),
            breakdown={
                'with_diffs': len(contexts_with_diffs),
                'total_contexts': total
            }
        )

