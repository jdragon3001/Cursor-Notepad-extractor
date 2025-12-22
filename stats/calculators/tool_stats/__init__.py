"""Tool usage statistics calculator."""

import logging
from typing import Dict, Any, List

from stats.models.message import Message
from stats.calculators.base_calculator import BaseCalculator
from .base import ToolStatsBase
from .usage import ToolUsageStats

logger = logging.getLogger(__name__)


class ToolCalculator(BaseCalculator):
    """
    Calculates tool usage statistics from toolFormerData.
    Covers tool invocations, success rates, failures, and usage patterns.
    """
    def __init__(self, messages: List[Message]):
        super().__init__(messages)
        self.messages = messages
        
        # Initialize modular calculators
        self.usage = ToolUsageStats(messages)
    
    def calculate_all(self) -> Dict[str, Any]:
        """Calculate all tool stats."""
        logger.info(f"Calculating tool stats for {len(self.messages)} messages...")
        
        stats = {}
        stats.update(self.usage.calculate_all())
        
        logger.info(f"Calculated {len(stats)} tool stats")
        return stats

