"""Base class for tool stats calculators."""

from typing import List
from stats.models.message import Message
from stats.calculators.base_calculator import BaseCalculator


class ToolStatsBase(BaseCalculator):
    """Base class for modular tool stat calculators."""
    def __init__(self, messages: List[Message]):
        super().__init__(messages)
        self.messages = messages

