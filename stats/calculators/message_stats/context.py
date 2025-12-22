"""Message context statistics (Stats 21-26)."""

from typing import Dict, Any, List
from stats.models.message import Message
from .base import MessageStatsBase


class MessageContextStats(MessageStatsBase):
    """Calculate context provided statistics."""
    
    def __init__(self, messages: List[Message]):
        """Initialize with messages."""
        super().__init__(messages)
    
    def calculate(self) -> Dict[str, Any]:
        """Calculate all context stats."""
        return {
            'attached_code_chunks': self.stat_021_attached_code_chunks(),
            'codebase_context_chunks': self.stat_022_codebase_context_chunks(),
            'lines_in_attached_chunks': self.stat_023_lines_in_attached_chunks(),
            'relevant_files': self.stat_024_relevant_files(),
            'recently_viewed_files': self.stat_025_recently_viewed_files(),
            'unique_files_in_context': self.stat_026_unique_files_in_context(),
        }
    
    def stat_021_attached_code_chunks(self) -> Dict[str, Any]:
        """Stat #21: Attached code chunks."""
        total_chunks = sum(len(m.attached_code_chunks) for m in self.messages)
        messages_with_chunks = len([m for m in self.messages if len(m.attached_code_chunks) > 0])
        
        return self.create_stat_result(
            value=total_chunks,
            label='Attached code chunks',
            category='Messages',
            data_source='bubbleId',
            stat_type='count',
            messages_with_chunks=messages_with_chunks,
            percentage=self.percentage(messages_with_chunks, len(self.messages))
        )
    
    def stat_022_codebase_context_chunks(self) -> Dict[str, Any]:
        """Stat #22: Codebase context chunks (auto-retrieved)."""
        total_chunks = sum(len(m.codebase_context_chunks) for m in self.messages)
        messages_with_chunks = len([m for m in self.messages if len(m.codebase_context_chunks) > 0])
        
        return self.create_stat_result(
            value=total_chunks,
            label='Codebase context chunks (auto-retrieved)',
            category='Messages',
            data_source='bubbleId',
            stat_type='count',
            messages_with_chunks=messages_with_chunks,
            percentage=self.percentage(messages_with_chunks, len(self.messages))
        )
    
    def stat_023_lines_in_attached_chunks(self) -> Dict[str, Any]:
        """Stat #23: Lines in attached chunks."""
        line_counts = []
        for m in self.messages:
            for chunk in m.attached_code_chunks:
                if isinstance(chunk, dict):
                    code = chunk.get('code', '') or chunk.get('content', '')
                    if code:
                        line_counts.append(len(code.split('\n')))
        
        if not line_counts:
            return self.create_stat_result(
                value=0,
                label='Lines in attached chunks',
                category='Messages',
                data_source='bubbleId',
                stat_type='numeric',
                sample_size=0
            )
        
        return self.create_stat_result(
            value=self.average(line_counts),
            label='Lines in attached chunks (per chunk)',
            category='Messages',
            data_source='bubbleId',
            stat_type='numeric',
            total_lines=sum(line_counts),
            median=self.median(line_counts),
            min=self.min_val(line_counts),
            max=self.max_val(line_counts),
            p95=self.percentile(line_counts, 95),
            sample_size=len(line_counts)
        )
    
    def stat_024_relevant_files(self) -> Dict[str, Any]:
        """Stat #24: Relevant files (from context)."""
        files = []
        for m in self.messages:
            # Check attached chunks
            for chunk in m.attached_code_chunks:
                if isinstance(chunk, dict):
                    file_path = chunk.get('filePath') or chunk.get('file') or chunk.get('path')
                    if file_path:
                        files.append(file_path)
            # Check codebase chunks
            for chunk in m.codebase_context_chunks:
                if isinstance(chunk, dict):
                    file_path = chunk.get('filePath') or chunk.get('file') or chunk.get('path')
                    if file_path:
                        files.append(file_path)
        
        unique_files = len(set(files))
        top_files = self.most_common(files, n=20) if files else []
        
        return self.create_stat_result(
            value=unique_files,
            label='Unique relevant files',
            category='Messages',
            data_source='bubbleId',
            stat_type='count',
            top_files=top_files,
            total_references=len(files)
        )
    
    def stat_025_recently_viewed_files(self) -> Dict[str, Any]:
        """Stat #25: Recently viewed files."""
        # This data might be in raw_data or a specific field
        viewed_files = []
        for m in self.messages:
            if m.raw_data and 'recentlyViewedFiles' in m.raw_data:
                files = m.raw_data.get('recentlyViewedFiles', [])
                viewed_files.extend(files)
            elif m.raw_data and 'recentFiles' in m.raw_data:
                files = m.raw_data.get('recentFiles', [])
                viewed_files.extend(files)
        
        unique_files = len(set(viewed_files))
        top_files = self.most_common(viewed_files, n=20) if viewed_files else []
        
        return self.create_stat_result(
            value=unique_files,
            label='Unique recently viewed files',
            category='Messages',
            data_source='bubbleId',
            stat_type='count',
            top_files=top_files,
            total_references=len(viewed_files)
        )
    
    def stat_026_unique_files_in_context(self) -> Dict[str, Any]:
        """Stat #26: Unique files in context (deduplicated)."""
        all_files = set()
        
        for m in self.messages:
            # From attached chunks
            for chunk in m.attached_code_chunks:
                if isinstance(chunk, dict):
                    file_path = chunk.get('filePath') or chunk.get('file') or chunk.get('path')
                    if file_path:
                        all_files.add(file_path)
            
            # From codebase chunks
            for chunk in m.codebase_context_chunks:
                if isinstance(chunk, dict):
                    file_path = chunk.get('filePath') or chunk.get('file') or chunk.get('path')
                    if file_path:
                        all_files.add(file_path)
            
            # From recently viewed
            if m.raw_data:
                for key in ['recentlyViewedFiles', 'recentFiles']:
                    if key in m.raw_data:
                        files = m.raw_data.get(key, [])
                        for f in files:
                            if isinstance(f, str):
                                all_files.add(f)
                            elif isinstance(f, dict):
                                path = f.get('path') or f.get('filePath')
                                if path:
                                    all_files.add(path)
        
        return self.create_stat_result(
            value=len(all_files),
            label='Unique files in context (all sources)',
            category='Messages',
            data_source='bubbleId',
            stat_type='count'
        )

