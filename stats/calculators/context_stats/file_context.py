"""File context statistics from RequestContext."""

import logging
from typing import Dict, Any, List

from stats.models.request_context import MessageRequestContext
from .base import ContextStatsBase

logger = logging.getLogger(__name__)


class FileContextStats(ContextStatsBase):
    """Calculate file context-related stats."""
    
    def calculate_all(self) -> Dict[str, Any]:
        """Calculate all stats in this module."""
        return {
            'contexts_with_file_context': self.stat_contexts_with_file_context(),
            'contexts_with_current_file': self.stat_contexts_with_current_file(),
            'contexts_with_attached_chunks': self.stat_contexts_with_attached_chunks(),
            'attached_chunks_per_context': self.stat_attached_chunks_per_context(),
            'contexts_with_editor_state': self.stat_contexts_with_editor_state(),
        }
    
    def stat_contexts_with_file_context(self) -> Dict[str, Any]:
        """Contexts with any file context information."""
        contexts_with_context = [rc for rc in self.request_contexts if rc.has_file_context]
        total = len(self.request_contexts)
        
        return self.create_stat_result(
            value=len(contexts_with_context),
            label='Contexts with file context',
            category='Context',
            data_source='messageRequestContext',
            stat_type='count',
            percentage=self.percentage(len(contexts_with_context), total),
            breakdown={
                'with_context': len(contexts_with_context),
                'total_contexts': total
            }
        )
    
    def stat_contexts_with_current_file(self) -> Dict[str, Any]:
        """Contexts with current file location data."""
        contexts_with_current = [rc for rc in self.request_contexts if rc.current_file_location_data]
        total = len(self.request_contexts)
        
        return self.create_stat_result(
            value=len(contexts_with_current),
            label='Contexts with current file location',
            category='Context',
            data_source='messageRequestContext',
            stat_type='count',
            percentage=self.percentage(len(contexts_with_current), total),
            breakdown={
                'with_current_file': len(contexts_with_current),
                'total_contexts': total
            }
        )
    
    def stat_contexts_with_attached_chunks(self) -> Dict[str, Any]:
        """Contexts with attached code chunks."""
        contexts_with_chunks = [rc for rc in self.request_contexts 
                                if rc.attached_file_code_chunks]
        total = len(self.request_contexts)
        
        return self.create_stat_result(
            value=len(contexts_with_chunks),
            label='Contexts with attached code chunks',
            category='Context',
            data_source='messageRequestContext',
            stat_type='count',
            percentage=self.percentage(len(contexts_with_chunks), total),
            breakdown={
                'with_chunks': len(contexts_with_chunks),
                'total_contexts': total
            }
        )
    
    def stat_attached_chunks_per_context(self) -> Dict[str, Any]:
        """Average attached code chunks per context with chunks."""
        contexts_with_chunks = [rc for rc in self.request_contexts 
                                if rc.attached_file_code_chunks]
        chunk_counts = [len(rc.attached_file_code_chunks) for rc in contexts_with_chunks]
        
        return self.create_stat_result(
            value=self.average(chunk_counts) if chunk_counts else 0.0,
            label='Attached chunks per context (with chunks)',
            category='Context',
            data_source='messageRequestContext',
            stat_type='numeric',
            median=self.median(chunk_counts) if chunk_counts else 0.0,
            min=self.min_val(chunk_counts) if chunk_counts else 0.0,
            max=self.max_val(chunk_counts) if chunk_counts else 0.0,
            sample_size=len(chunk_counts)
        )
    
    def stat_contexts_with_editor_state(self) -> Dict[str, Any]:
        """Contexts with IDE editor state information."""
        contexts_with_state = [rc for rc in self.request_contexts if rc.ide_editors_state]
        total = len(self.request_contexts)
        
        return self.create_stat_result(
            value=len(contexts_with_state),
            label='Contexts with editor state',
            category='Context',
            data_source='messageRequestContext',
            stat_type='count',
            percentage=self.percentage(len(contexts_with_state), total),
            breakdown={
                'with_editor_state': len(contexts_with_state),
                'total_contexts': total
            }
        )

