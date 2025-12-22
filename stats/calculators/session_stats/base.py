"""Base class for session stat sub-modules."""

from typing import List, Dict, Any, Callable
import numpy as np
from collections import Counter
from stats.models.session import Session
from stats.models.message import Message


class SessionStatsBase:
    """
    Base class for session stat modules.
    
    Provides all utility functions for session stats calculations.
    """
    
    def __init__(self, sessions: List[Session], messages: List[Message] = None):
        """
        Initialize with sessions and optionally messages.
        
        Args:
            sessions: List of Session objects
            messages: Optional list of Message objects for cross-referencing
        """
        self.sessions = sessions
        self.messages = messages or []
        self._cache = {}
    
    # Utility methods (same as MessageStatsBase)
    
    def count(self, items: List[Any]) -> int:
        """Count items in a list."""
        return len(items)
    
    def percentage(self, part: int, total: int, decimals: int = 2) -> float:
        """Calculate percentage."""
        if total == 0:
            return 0.0
        return round((part / total * 100), decimals)
    
    def average(self, values: List[float]) -> float:
        """Calculate average (mean)."""
        if not values:
            return 0.0
        return float(np.mean(values))
    
    def median(self, values: List[float]) -> float:
        """Calculate median."""
        if not values:
            return 0.0
        return float(np.median(values))
    
    def percentile(self, values: List[float], p: int) -> float:
        """Calculate percentile."""
        if not values:
            return 0.0
        return float(np.percentile(values, p))
    
    def std_dev(self, values: List[float]) -> float:
        """Calculate standard deviation."""
        if not values:
            return 0.0
        return float(np.std(values))
    
    def min_val(self, values: List[float]) -> float:
        """Get minimum value."""
        if not values:
            return 0.0
        return float(min(values))
    
    def max_val(self, values: List[float]) -> float:
        """Get maximum value."""
        if not values:
            return 0.0
        return float(max(values))
    
    def sum_val(self, values: List[float]) -> float:
        """Get sum of values."""
        if not values:
            return 0.0
        return float(sum(values))
    
    def distribution(self, values: List[float], bins: int = 10) -> Dict[str, Any]:
        """Calculate distribution histogram."""
        if not values:
            return {'bins': [], 'counts': []}
        
        counts, bin_edges = np.histogram(values, bins=bins)
        return {
            'bins': bin_edges.tolist(),
            'counts': counts.tolist()
        }
    
    def most_common(self, items: List[Any], n: int = 10) -> List[tuple]:
        """Get most common items."""
        return Counter(items).most_common(n)
    
    def group_by(self, items: List[Any], key_func: Callable) -> Dict[Any, List[Any]]:
        """Group items by key function."""
        groups = {}
        for item in items:
            key = key_func(item)
            if key not in groups:
                groups[key] = []
            groups[key].append(item)
        return groups
    
    def filter_by(self, items: List[Any], predicate: Callable) -> List[Any]:
        """Filter items by predicate."""
        return [item for item in items if predicate(item)]
    
    def create_stat_result(
        self,
        value: Any,
        label: str,
        category: str,
        data_source: str,
        stat_type: str = 'count',
        **kwargs
    ) -> Dict[str, Any]:
        """Create a standardized stat result dictionary."""
        result = {
            'value': value,
            'label': label,
            'category': category,
            'data_source': data_source,
            'type': stat_type,
        }
        result.update(kwargs)
        return result

