"""Base class for context stats calculators."""

from typing import List
from stats.models.request_context import MessageRequestContext
from stats.calculators.base_calculator import BaseCalculator


class ContextStatsBase(BaseCalculator):
    """Base class for modular context stat calculators."""
    def __init__(self, request_contexts: List[MessageRequestContext]):
        super().__init__(request_contexts)
        self.request_contexts = request_contexts

