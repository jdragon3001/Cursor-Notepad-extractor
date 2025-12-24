"""Code tracking lines statistics (Stats 101-105)."""

from typing import Dict, Any
from .base import CodeStatsBase


class TrackingLinesStats(CodeStatsBase):
    """Calculate code tracking lines statistics."""
    
    def calculate(self) -> Dict[str, Any]:
        """Calculate all tracking lines stats."""
        return {
            'tracked_code_lines': self.stat_101_tracked_code_lines(),
            'code_by_source': self.stat_102_code_by_source(),
            'code_by_file_type': self.stat_103_code_by_file_type(),
            'code_by_file': self.stat_104_code_by_file(),
            'most_modified_files': self.stat_105_most_modified_files(),
        }
    
    def stat_101_tracked_code_lines(self) -> Dict[str, Any]:
        """Stat #101: Tracked code lines."""
        return self.create_stat_result(
            value=self.count(self.tracking_lines),
            label='Tracked code lines',
            category='Code & Diffs',
            data_source='aiCodeTrackingLines (ItemTable)',
            stat_type='count'
        )
    
    def stat_102_code_by_source(self) -> Dict[str, Any]:
        """Stat #102: Code by source."""
        sources = [line.source for line in self.tracking_lines if line.source]
        source_counts = self.most_common(sources, n=10)
        
        return self.create_stat_result(
            value=len(set(sources)),
            label='Unique code sources',
            category='Code & Diffs',
            data_source='aiCodeTrackingLines (ItemTable)',
            stat_type='count',
            source_breakdown=source_counts,
            total_lines=len(sources)
        )
    
    def stat_103_code_by_file_type(self) -> Dict[str, Any]:
        """Stat #103: Code by file type."""
        extensions = [line.file_extension for line in self.tracking_lines if line.file_extension]
        extension_counts = self.most_common(extensions, n=30)
        
        return self.create_stat_result(
            value=len(set(extensions)),
            label='Unique file types',
            category='Code & Diffs',
            data_source='aiCodeTrackingLines (ItemTable)',
            stat_type='count',
            file_type_breakdown=extension_counts,
            total_lines=len(extensions)
        )
    
    def stat_104_code_by_file(self) -> Dict[str, Any]:
        """Stat #104: Code by file."""
        files = [line.file_name for line in self.tracking_lines if line.file_name]
        unique_files = len(set(files))
        
        return self.create_stat_result(
            value=unique_files,
            label='Unique files modified',
            category='Code & Diffs',
            data_source='aiCodeTrackingLines (ItemTable)',
            stat_type='count',
            total_lines=len(files),
            average_lines_per_file=len(files) / unique_files if unique_files > 0 else 0
        )
    
    def stat_105_most_modified_files(self) -> Dict[str, Any]:
        """Stat #105: Most modified files."""
        files = [line.file_name for line in self.tracking_lines if line.file_name]
        most_modified = self.most_common(files, n=50)
        
        return self.create_stat_result(
            value=len(most_modified),
            label='Files with tracked lines',
            category='Code & Diffs',
            data_source='aiCodeTrackingLines (ItemTable)',
            stat_type='count',
            most_modified_files=most_modified
        )

