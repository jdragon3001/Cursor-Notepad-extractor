"""TODO statistics from RequestContext."""

import logging
from typing import Dict, Any, List
from collections import Counter

from stats.models.request_context import MessageRequestContext
from .base import ContextStatsBase

logger = logging.getLogger(__name__)


class TodoStats(ContextStatsBase):
    """Calculate TODO-related stats."""
    
    def calculate_all(self) -> Dict[str, Any]:
        """Calculate all stats in this module."""
        return {
            'contexts_with_todos': self.stat_contexts_with_todos(),
            'total_todos': self.stat_total_todos(),
            'todos_per_context': self.stat_todos_per_context(),
            'todos_by_status': self.stat_todos_by_status(),
        }
    
    def _get_contexts_with_todos(self) -> List[MessageRequestContext]:
        """Get contexts that have TODOs."""
        return [rc for rc in self.request_contexts if rc.has_todos]
    
    def _extract_all_todos(self) -> List[Dict[str, Any]]:
        """Extract all individual TODOs from all contexts."""
        all_todos = []
        for rc in self._get_contexts_with_todos():
            all_todos.extend(rc.todos)
        return all_todos
    
    def stat_contexts_with_todos(self) -> Dict[str, Any]:
        """Contexts containing TODOs."""
        contexts_with_todos = self._get_contexts_with_todos()
        total = len(self.request_contexts)
        
        return self.create_stat_result(
            value=len(contexts_with_todos),
            label='Contexts with TODOs',
            category='Context',
            data_source='messageRequestContext',
            stat_type='count',
            percentage=self.percentage(len(contexts_with_todos), total),
            breakdown={
                'with_todos': len(contexts_with_todos),
                'total_contexts': total
            }
        )
    
    def stat_total_todos(self) -> Dict[str, Any]:
        """Total number of TODOs."""
        all_todos = self._extract_all_todos()
        
        return self.create_stat_result(
            value=len(all_todos),
            label='Total TODOs',
            category='Context',
            data_source='messageRequestContext',
            stat_type='count',
            breakdown={
                'total_todos': len(all_todos),
                'contexts_with_todos': len(self._get_contexts_with_todos())
            }
        )
    
    def stat_todos_per_context(self) -> Dict[str, Any]:
        """Average TODOs per context with TODOs."""
        contexts_with_todos = self._get_contexts_with_todos()
        todo_counts = [len(rc.todos) for rc in contexts_with_todos]
        
        return self.create_stat_result(
            value=self.average(todo_counts) if todo_counts else 0.0,
            label='TODOs per context (with TODOs)',
            category='Context',
            data_source='messageRequestContext',
            stat_type='numeric',
            median=self.median(todo_counts) if todo_counts else 0.0,
            min=self.min_val(todo_counts) if todo_counts else 0.0,
            max=self.max_val(todo_counts) if todo_counts else 0.0,
            sample_size=len(todo_counts)
        )
    
    def stat_todos_by_status(self) -> Dict[str, Any]:
        """Distribution of TODOs by status."""
        all_todos = self._extract_all_todos()
        
        statuses = [todo.status for todo in all_todos if hasattr(todo, 'status')]
        status_counts = Counter(statuses)
        
        return self.create_stat_result(
            value=dict(status_counts),
            label='TODOs by status',
            category='Context',
            data_source='messageRequestContext',
            stat_type='distribution',
            breakdown={
                status: {
                    'count': count,
                    'percentage': self.percentage(count, len(statuses))
                }
                for status, count in status_counts.items()
            }
        )

