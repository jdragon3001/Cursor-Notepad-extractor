"""
Modular code & diffs statistics calculators.

This package contains code stats organized into focused modules:
- diff_metrics: Diff counts and metrics (stats 94-100)
- tracking_lines: Code tracking lines (stats 101-105)
"""

from typing import Dict, Any, List
import logging

from stats.models.code_diff import CodeDiff, CodeTrackingLine
from stats.calculators.base_calculator import BaseCalculator

# Import all stat modules
from .diff_metrics import DiffMetricsStats
from .tracking_lines import TrackingLinesStats

logger = logging.getLogger(__name__)


class CodeCalculator(BaseCalculator):
    """
    Main code calculator that orchestrates all code stat modules.
    
    This calculator delegates to specialized modules for maintainability.
    """
    
    def __init__(self, code_diffs: List[CodeDiff], tracking_lines: List[CodeTrackingLine] = None):
        """
        Initialize calculator.
        
        Args:
            code_diffs: List of CodeDiff objects
            tracking_lines: Optional list of CodeTrackingLine objects
        """
        super().__init__(code_diffs)
        self.code_diffs = code_diffs
        self.tracking_lines = tracking_lines or []
        
        # Initialize sub-calculators
        self.diff_metrics = DiffMetricsStats(code_diffs, tracking_lines)
        self.tracking_lines_stats = TrackingLinesStats(code_diffs, tracking_lines)
        
    def calculate_all(self) -> Dict[str, Any]:
        """
        Calculate all code stats by delegating to sub-calculators.
        
        Returns:
            Dictionary of all calculated stats
        """
        logger.info(f"Calculating code stats for {len(self.code_diffs)} diffs and {len(self.tracking_lines)} tracking lines...")
        
        stats = {}
        
        # Collect stats from each module
        stats.update(self.diff_metrics.calculate())
        stats.update(self.tracking_lines_stats.calculate())
        
        logger.info(f"Calculated {len(stats)} code stats")
        return stats


__all__ = ['CodeCalculator']

