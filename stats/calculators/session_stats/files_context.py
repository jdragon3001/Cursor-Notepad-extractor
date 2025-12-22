"""Session files and context statistics (Stats 77-84)."""

from typing import Dict, Any, List
from stats.models.session import Session
from stats.models.message import Message
from .base import SessionStatsBase


class SessionFilesContextStats(SessionStatsBase):
    """Calculate session files and context statistics."""
    
    def calculate(self) -> Dict[str, Any]:
        """Calculate all files and context stats."""
        return {
            'files_added': self.stat_077_files_added(),
            'files_removed': self.stat_078_files_removed(),
            'files_modified': self.stat_079_files_modified(),
            'most_modified_files': self.stat_080_most_modified_files(),
            'context_tokens_used': self.stat_081_context_tokens_used(),
            'context_token_limit': self.stat_082_context_token_limit(),
            'context_usage_percentage': self.stat_083_context_usage_percentage(),
            'sessions_near_context_limit': self.stat_084_sessions_near_context_limit(),
        }
    
    def stat_077_files_added(self) -> Dict[str, Any]:
        """Stat #77: Files added."""
        all_files = []
        for s in self.sessions:
            all_files.extend(s.added_files)
        
        total_files = len(all_files)
        unique_files = len(set(all_files))
        top_files = self.most_common(all_files, n=20) if all_files else []
        
        return self.create_stat_result(
            value=total_files,
            label='Files added',
            category='Sessions',
            data_source='composerData',
            stat_type='count',
            unique_files=unique_files,
            top_files=top_files
        )
    
    def stat_078_files_removed(self) -> Dict[str, Any]:
        """Stat #78: Files removed."""
        all_files = []
        for s in self.sessions:
            all_files.extend(s.removed_files)
        
        total_files = len(all_files)
        unique_files = len(set(all_files))
        top_files = self.most_common(all_files, n=20) if all_files else []
        
        return self.create_stat_result(
            value=total_files,
            label='Files removed',
            category='Sessions',
            data_source='composerData',
            stat_type='count',
            unique_files=unique_files,
            top_files=top_files
        )
    
    def stat_079_files_modified(self) -> Dict[str, Any]:
        """Stat #79: Files modified (union of added and removed)."""
        all_files = set()
        for s in self.sessions:
            all_files.update(s.added_files)
            all_files.update(s.removed_files)
        
        return self.create_stat_result(
            value=len(all_files),
            label='Unique files modified',
            category='Sessions',
            data_source='composerData',
            stat_type='count'
        )
    
    def stat_080_most_modified_files(self) -> Dict[str, Any]:
        """Stat #80: Most modified files."""
        file_counts = []
        for s in self.sessions:
            file_counts.extend(s.added_files)
            file_counts.extend(s.removed_files)
        
        top_files = self.most_common(file_counts, n=30) if file_counts else []
        
        return self.create_stat_result(
            value=len(top_files),
            label='Files with modification data',
            category='Sessions',
            data_source='composerData',
            stat_type='count',
            top_modified_files=top_files
        )
    
    def stat_081_context_tokens_used(self) -> Dict[str, Any]:
        """Stat #81: Context tokens used."""
        tokens_per_session = [s.context_tokens_used for s in self.sessions if s.context_tokens_used > 0]
        total_tokens = sum(s.context_tokens_used for s in self.sessions)
        
        return self.create_stat_result(
            value=total_tokens,
            label='Total context tokens used',
            category='Sessions',
            data_source='composerData',
            stat_type='count',
            average_per_session=self.average(tokens_per_session) if tokens_per_session else 0,
            median=self.median(tokens_per_session) if tokens_per_session else 0,
            max=self.max_val(tokens_per_session) if tokens_per_session else 0,
            sessions_tracked=len(tokens_per_session)
        )
    
    def stat_082_context_token_limit(self) -> Dict[str, Any]:
        """Stat #82: Context token limit."""
        limits = [s.context_token_limit for s in self.sessions if s.context_token_limit > 0]
        
        # Most common limit
        limit_counts = self.most_common(limits, n=5) if limits else []
        most_common_limit = limit_counts[0][0] if limit_counts else 128000
        
        return self.create_stat_result(
            value=most_common_limit,
            label='Most common context token limit',
            category='Sessions',
            data_source='composerData',
            stat_type='count',
            limit_distribution=limit_counts
        )
    
    def stat_083_context_usage_percentage(self) -> Dict[str, Any]:
        """Stat #83: Context usage percentage."""
        percentages = [s.context_usage_percent for s in self.sessions if s.context_usage_percent > 0]
        
        return self.create_stat_result(
            value=self.average(percentages) if percentages else 0,
            label='Average context usage (%)',
            category='Sessions',
            data_source='composerData',
            stat_type='percentage',
            median=self.median(percentages) if percentages else 0,
            min=self.min_val(percentages) if percentages else 0,
            max=self.max_val(percentages) if percentages else 0,
            p95=self.percentile(percentages, 95) if percentages else 0,
            sample_size=len(percentages)
        )
    
    def stat_084_sessions_near_context_limit(self) -> Dict[str, Any]:
        """Stat #84: Sessions near context limit (>80%)."""
        near_limit = self.filter_by(self.sessions, lambda s: s.context_usage_percent > 80)
        total = len(self.sessions)
        
        return self.create_stat_result(
            value=len(near_limit),
            label='Sessions near context limit (>80%)',
            category='Sessions',
            data_source='composerData',
            stat_type='count',
            percentage=self.percentage(len(near_limit), total)
        )

