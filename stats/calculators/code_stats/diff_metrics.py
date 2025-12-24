"""Code diff counts and metrics (Stats 94-100)."""

from typing import Dict, Any
from .base import CodeStatsBase


class DiffMetricsStats(CodeStatsBase):
    """Calculate diff metrics statistics."""
    
    def calculate(self) -> Dict[str, Any]:
        """Calculate all diff metrics stats."""
        return {
            'code_diffs_total': self.stat_094_code_diffs_total(),
            'diffs_per_session': self.stat_095_diffs_per_session(),
            'lines_changed_per_diff': self.stat_096_lines_changed_per_diff(),
            'diff_line_spans': self.stat_097_diff_line_spans(),
            'edit_distance': self.stat_098_edit_distance(),
            'similarity_ratio': self.stat_099_similarity_ratio(),
            'character_changes': self.stat_100_character_changes(),
        }
    
    def stat_094_code_diffs_total(self) -> Dict[str, Any]:
        """Stat #94: Code diffs total."""
        return self.create_stat_result(
            value=self.count(self.code_diffs),
            label='Total code diffs',
            category='Code & Diffs',
            data_source='codeBlockDiff',
            stat_type='count'
        )
    
    def stat_095_diffs_per_session(self) -> Dict[str, Any]:
        """Stat #95: Diffs per session."""
        # Group by composer_id
        sessions = self.group_by(self.code_diffs, lambda d: d.composer_id)
        diff_counts = [len(diffs) for diffs in sessions.values()]
        
        return self.create_stat_result(
            value=self.average(diff_counts) if diff_counts else 0,
            label='Diffs per session',
            category='Code & Diffs',
            data_source='codeBlockDiff',
            stat_type='numeric',
            median=self.median(diff_counts) if diff_counts else 0,
            min=self.min_val(diff_counts) if diff_counts else 0,
            max=self.max_val(diff_counts) if diff_counts else 0,
            p95=self.percentile(diff_counts, 95) if diff_counts else 0,
            sample_size=len(sessions)
        )
    
    def stat_096_lines_changed_per_diff(self) -> Dict[str, Any]:
        """Stat #96: Lines changed per diff."""
        line_counts = [d.get_total_lines_changed() for d in self.code_diffs]
        
        return self.create_stat_result(
            value=self.average(line_counts) if line_counts else 0,
            label='Lines changed per diff',
            category='Code & Diffs',
            data_source='codeBlockDiff',
            stat_type='numeric',
            median=self.median(line_counts) if line_counts else 0,
            min=self.min_val(line_counts) if line_counts else 0,
            max=self.max_val(line_counts) if line_counts else 0,
            p95=self.percentile(line_counts, 95) if line_counts else 0,
            total_lines=self.sum_val(line_counts)
        )
    
    def stat_097_diff_line_spans(self) -> Dict[str, Any]:
        """Stat #97: Diff line spans."""
        spans = [d.get_diff_span() for d in self.code_diffs if d.get_diff_span() > 0]
        
        return self.create_stat_result(
            value=self.average(spans) if spans else 0,
            label='Diff line spans',
            category='Code & Diffs',
            data_source='codeBlockDiff',
            stat_type='numeric',
            median=self.median(spans) if spans else 0,
            min=self.min_val(spans) if spans else 0,
            max=self.max_val(spans) if spans else 0,
            p95=self.percentile(spans, 95) if spans else 0,
            sample_size=len(spans)
        )
    
    def stat_098_edit_distance(self) -> Dict[str, Any]:
        """Stat #98: Edit distance (placeholder - requires text comparison)."""
        # This would require Levenshtein distance calculation between versions
        # For now, return placeholder
        return self.create_stat_result(
            value=0,
            label='Edit distance (Levenshtein)',
            category='Code & Diffs',
            data_source='codeBlockDiff',
            stat_type='numeric',
            note='Requires implementation of Levenshtein distance calculation'
        )
    
    def stat_099_similarity_ratio(self) -> Dict[str, Any]:
        """Stat #99: Similarity ratio (placeholder - requires text comparison)."""
        # This would require similarity calculation between original and modified
        # For now, return placeholder
        return self.create_stat_result(
            value=0,
            label='Similarity ratio',
            category='Code & Diffs',
            data_source='codeBlockDiff',
            stat_type='percentage',
            note='Requires implementation of similarity calculation'
        )
    
    def stat_100_character_changes(self) -> Dict[str, Any]:
        """Stat #100: Character changes."""
        char_changes = []
        for diff in self.code_diffs:
            for change in diff.new_changes + diff.original_changes:
                # Count characters in modified lines
                chars = sum(len(line) for line in change.modified_lines)
                char_changes.append(chars)
        
        return self.create_stat_result(
            value=self.sum_val(char_changes),
            label='Total character changes',
            category='Code & Diffs',
            data_source='codeBlockDiff',
            stat_type='count',
            average_per_change=self.average(char_changes) if char_changes else 0,
            median=self.median(char_changes) if char_changes else 0
        )

