"""Linter error statistics from RequestContext."""

import logging
from typing import Dict, Any, List
from collections import Counter

from stats.models.request_context import MessageRequestContext
from .base import ContextStatsBase

logger = logging.getLogger(__name__)


class LinterErrorStats(ContextStatsBase):
    """Calculate linter error-related stats."""
    
    def _parse_file_errors(self, file_errors: Any) -> Dict[str, Any]:
        """Parse file_errors which might be a string (JSON) or dict."""
        if isinstance(file_errors, str):
            try:
                import json
                return json.loads(file_errors)
            except json.JSONDecodeError:
                return {}
        elif isinstance(file_errors, dict):
            return file_errors
        return {}
    
    def calculate_all(self) -> Dict[str, Any]:
        """Calculate all stats in this module."""
        return {
            'contexts_with_linter_errors': self.stat_contexts_with_linter_errors(),
            'total_linter_errors': self.stat_total_linter_errors(),
            'errors_per_context': self.stat_errors_per_context(),
            'linter_errors_by_file_type': self.stat_errors_by_file_type(),
            'linter_errors_by_source': self.stat_errors_by_source(),
            'files_with_linter_errors': self.stat_files_with_linter_errors(),
        }
    
    def _get_contexts_with_errors(self) -> List[MessageRequestContext]:
        """Get contexts that have linter errors."""
        return [rc for rc in self.request_contexts if rc.has_linter_errors]
    
    def _extract_all_errors(self) -> List[Dict[str, Any]]:
        """Extract all individual linter errors from all contexts."""
        all_errors = []
        for rc in self._get_contexts_with_errors():
            for file_errors_raw in rc.multi_file_linter_errors:
                file_errors = self._parse_file_errors(file_errors_raw)
                if not file_errors:
                    continue
                
                errors = file_errors.get('errors', [])
                file_path = file_errors.get('relativeWorkspacePath', 'unknown')
                for error in errors:
                    error_with_file = error.copy() if isinstance(error, dict) else {}
                    error_with_file['file'] = file_path
                    all_errors.append(error_with_file)
        return all_errors
    
    def stat_contexts_with_linter_errors(self) -> Dict[str, Any]:
        """Contexts containing linter errors."""
        contexts_with_errors = self._get_contexts_with_errors()
        total = len(self.request_contexts)
        
        return self.create_stat_result(
            value=len(contexts_with_errors),
            label='Contexts with linter errors',
            category='Context',
            data_source='messageRequestContext',
            stat_type='count',
            percentage=self.percentage(len(contexts_with_errors), total),
            breakdown={
                'with_errors': len(contexts_with_errors),
                'total_contexts': total
            }
        )
    
    def stat_total_linter_errors(self) -> Dict[str, Any]:
        """Total number of linter errors."""
        all_errors = self._extract_all_errors()
        
        return self.create_stat_result(
            value=len(all_errors),
            label='Total linter errors',
            category='Context',
            data_source='messageRequestContext',
            stat_type='count',
            breakdown={
                'total_errors': len(all_errors),
                'contexts_with_errors': len(self._get_contexts_with_errors())
            }
        )
    
    def stat_errors_per_context(self) -> Dict[str, Any]:
        """Average errors per context with errors."""
        contexts_with_errors = self._get_contexts_with_errors()
        error_counts = []
        
        for rc in contexts_with_errors:
            error_count = 0
            for file_errors_raw in rc.multi_file_linter_errors:
                file_errors = self._parse_file_errors(file_errors_raw)
                error_count += len(file_errors.get('errors', []))
            error_counts.append(error_count)
        
        return self.create_stat_result(
            value=self.average(error_counts) if error_counts else 0.0,
            label='Errors per context (with errors)',
            category='Context',
            data_source='messageRequestContext',
            stat_type='numeric',
            median=self.median(error_counts) if error_counts else 0.0,
            min=self.min_val(error_counts) if error_counts else 0.0,
            max=self.max_val(error_counts) if error_counts else 0.0,
            sample_size=len(error_counts)
        )
    
    def stat_errors_by_file_type(self) -> Dict[str, Any]:
        """Distribution of linter errors by file extension."""
        all_errors = self._extract_all_errors()
        
        file_extensions = []
        for error in all_errors:
            file_path = error.get('file', '')
            if '.' in file_path:
                ext = file_path.split('.')[-1]
                file_extensions.append(ext)
            else:
                file_extensions.append('no_extension')
        
        extension_counts = Counter(file_extensions)
        
        return self.create_stat_result(
            value=dict(extension_counts.most_common(10)),
            label='Linter errors by file type',
            category='Context',
            data_source='messageRequestContext',
            stat_type='distribution',
            breakdown={
                'top_10': [{'extension': ext, 'count': count} for ext, count in extension_counts.most_common(10)],
                'unique_extensions': len(extension_counts)
            }
        )
    
    def stat_errors_by_source(self) -> Dict[str, Any]:
        """Distribution of linter errors by source (css, ts, etc.)."""
        all_errors = self._extract_all_errors()
        
        sources = [error.get('source', 'unknown') for error in all_errors]
        source_counts = Counter(sources)
        
        return self.create_stat_result(
            value=dict(source_counts),
            label='Linter errors by source',
            category='Context',
            data_source='messageRequestContext',
            stat_type='distribution',
            breakdown={
                source: {
                    'count': count,
                    'percentage': self.percentage(count, len(sources))
                }
                for source, count in source_counts.items()
            }
        )
    
    def stat_files_with_linter_errors(self) -> Dict[str, Any]:
        """Number of unique files with linter errors."""
        all_files = set()
        
        for rc in self._get_contexts_with_errors():
            for file_errors_raw in rc.multi_file_linter_errors:
                file_errors = self._parse_file_errors(file_errors_raw)
                file_path = file_errors.get('relativeWorkspacePath')
                if file_path:
                    all_files.add(file_path)
        
        return self.create_stat_result(
            value=len(all_files),
            label='Files with linter errors',
            category='Context',
            data_source='messageRequestContext',
            stat_type='count',
            breakdown={
                'unique_files': len(all_files),
                'contexts_with_errors': len(self._get_contexts_with_errors())
            }
        )

