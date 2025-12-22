"""
Modular session statistics calculators.

This package contains session stats organized into focused modules:
- counts: Session counts (stats 67-70)
- duration_outcomes: Duration and outcomes (stats 71-76)
- files_context: Files and context (stats 77-84)
- conversation_config: Conversation structure and config (stats 85-91)
- naming: Session naming (stats 92-93)
"""

from typing import Dict, Any, List
import logging

from stats.models.session import Session
from stats.models.message import Message
from stats.calculators.base_calculator import BaseCalculator

# Import all stat modules
from .counts import SessionCountStats
from .duration_outcomes import SessionDurationOutcomesStats
from .files_context import SessionFilesContextStats
from .conversation_config import SessionConversationConfigStats
from .naming import SessionNamingStats

logger = logging.getLogger(__name__)


class SessionCalculator(BaseCalculator):
    """
    Main session calculator that orchestrates all session stat modules.
    
    This calculator delegates to specialized modules for maintainability.
    """
    
    def __init__(self, sessions: List[Session], messages: List[Message] = None):
        """
        Initialize calculator.
        
        Args:
            sessions: List of Session objects
            messages: Optional list of Message objects for cross-referencing
        """
        super().__init__(sessions)
        self.sessions = sessions
        self.messages = messages or []
        
        # Initialize sub-calculators
        self.counts = SessionCountStats(sessions, messages)
        self.duration_outcomes = SessionDurationOutcomesStats(sessions, messages)
        self.files_context = SessionFilesContextStats(sessions, messages)
        self.conversation_config = SessionConversationConfigStats(sessions, messages)
        self.naming = SessionNamingStats(sessions, messages)
        
    def calculate_all(self) -> Dict[str, Any]:
        """
        Calculate all session stats by delegating to sub-calculators.
        
        Returns:
            Dictionary of all calculated stats
        """
        logger.info(f"Calculating session stats for {len(self.sessions)} sessions...")
        
        stats = {}
        
        # Collect stats from each module
        stats.update(self.counts.calculate())
        stats.update(self.duration_outcomes.calculate())
        stats.update(self.files_context.calculate())
        stats.update(self.conversation_config.calculate())
        stats.update(self.naming.calculate())
        
        logger.info(f"Calculated {len(stats)} session stats")
        return stats


__all__ = ['SessionCalculator']

