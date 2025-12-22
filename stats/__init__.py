"""
Cursor Data Stats Extraction and Calculation System

This package contains:
- extractors: Extract data from Cursor databases
- models: Data models for structured data
- calculators: Calculate stats from extracted data
- orchestrator: Coordinate extraction and calculation
- cache: Cache system for performance
"""

from .orchestrator import StatsOrchestrator
from .cache import StatsCache

__version__ = "1.0.0"
__all__ = ['StatsOrchestrator', 'StatsCache']

