"""Context statistics calculator."""

import logging
from typing import Dict, Any, List

from stats.models.request_context import MessageRequestContext
from stats.calculators.base_calculator import BaseCalculator
from .base import ContextStatsBase
from .linter import LinterErrorStats
from .todos import TodoStats
from .git import GitContextStats
from .file_context import FileContextStats

logger = logging.getLogger(__name__)


class ContextCalculator(BaseCalculator):
    """
    Calculates context statistics from MessageRequestContext data.
    Covers linter errors, TODOs, git status, and file context.
    """
    def __init__(self, request_contexts: List[MessageRequestContext]):
        super().__init__(request_contexts)
        self.request_contexts = request_contexts
        
        # Initialize modular calculators
        self.linter = LinterErrorStats(request_contexts)
        self.todos = TodoStats(request_contexts)
        self.git = GitContextStats(request_contexts)
        self.file_context = FileContextStats(request_contexts)
    
    def calculate_all(self) -> Dict[str, Any]:
        """Calculate all context stats."""
        logger.info(f"Calculating context stats for {len(self.request_contexts)} contexts...")
        
        stats = {}
        stats.update(self.linter.calculate_all())
        stats.update(self.todos.calculate_all())
        stats.update(self.git.calculate_all())
        stats.update(self.file_context.calculate_all())
        
        logger.info(f"Calculated {len(stats)} context stats")
        return stats

