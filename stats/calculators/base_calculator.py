"""Base calculator class for all stat calculators."""

from abc import ABC, abstractmethod
from typing import Any, Dict, List, Callable
import numpy as np
from collections import Counter
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class BaseCalculator(ABC):
    """Base class for all stat calculators with common utilities."""
    
    def __init__(self, data: Any):
        """
        Initialize calculator.
        
        Args:
            data: The data to calculate stats from
        """
        self.data = data
        self._cache = {}
    
    @abstractmethod
    def calculate_all(self) -> Dict[str, Any]:
        """
        Calculate all stats for this category.
        
        Returns:
            Dictionary of stat_name: stat_data
        """
        pass
    
    # ==================== COUNT UTILITIES ====================
    
    def count(self, items: List[Any]) -> int:
        """Count items in a list."""
        return len(items)
    
    def percentage(self, part: int, total: int, decimals: int = 2) -> float:
        """
        Calculate percentage.
        
        Args:
            part: Part value
            total: Total value
            decimals: Number of decimal places
            
        Returns:
            Percentage value
        """
        if total == 0:
            return 0.0
        return round((part / total * 100), decimals)
    
    # ==================== STATISTICAL UTILITIES ====================
    
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
        """
        Calculate percentile.
        
        Args:
            values: List of values
            p: Percentile (0-100)
            
        Returns:
            Percentile value
        """
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
        """
        Calculate distribution histogram.
        
        Args:
            values: List of values
            bins: Number of bins
            
        Returns:
            Dictionary with 'bins' and 'counts' keys
        """
        if not values:
            return {'bins': [], 'counts': []}
        
        counts, bin_edges = np.histogram(values, bins=bins)
        return {
            'bins': bin_edges.tolist(),
            'counts': counts.tolist()
        }
    
    # ==================== AGGREGATION UTILITIES ====================
    
    def most_common(self, items: List[Any], n: int = 10) -> List[tuple]:
        """
        Get most common items.
        
        Args:
            items: List of items
            n: Number of top items to return
            
        Returns:
            List of (item, count) tuples
        """
        return Counter(items).most_common(n)
    
    def group_by(self, items: List[Any], key_func: Callable) -> Dict[Any, List[Any]]:
        """
        Group items by key function.
        
        Args:
            items: List of items
            key_func: Function to extract key from item
            
        Returns:
            Dictionary mapping key to list of items
        """
        groups = {}
        for item in items:
            key = key_func(item)
            if key not in groups:
                groups[key] = []
            groups[key].append(item)
        return groups
    
    def filter_by(self, items: List[Any], predicate: Callable) -> List[Any]:
        """
        Filter items by predicate.
        
        Args:
            items: List of items
            predicate: Function that returns True to keep item
            
        Returns:
            Filtered list of items
        """
        return [item for item in items if predicate(item)]
    
    # ==================== CACHING UTILITIES ====================
    
    def cached(self, key: str, calc_func: Callable) -> Any:
        """
        Cache calculation result.
        
        Args:
            key: Cache key
            calc_func: Function to calculate value if not cached
            
        Returns:
            Cached or calculated value
        """
        if key not in self._cache:
            self._cache[key] = calc_func()
        return self._cache[key]
    
    def clear_cache(self):
        """Clear all cached values."""
        self._cache = {}
    
    # ==================== STAT RESULT FORMATTING ====================
    
    def create_stat_result(
        self,
        value: Any,
        label: str,
        category: str,
        data_source: str,
        stat_type: str = 'count',
        **kwargs
    ) -> Dict[str, Any]:
        """
        Create a standardized stat result dictionary.
        
        Args:
            value: The primary stat value
            label: Human-readable label
            category: Category name (e.g., "Messages", "Sessions")
            data_source: Data source (e.g., "bubbleId", "composerData")
            stat_type: Type of stat (count, numeric, percentage, etc.)
            **kwargs: Additional stat-specific fields
            
        Returns:
            Standardized stat result dictionary
        """
        result = {
            'value': value,
            'label': label,
            'category': category,
            'data_source': data_source,
            'type': stat_type,
        }
        
        # Add any additional fields
        result.update(kwargs)
        
        return result

