"""
Modular message statistics calculators.

This package contains message stats organized into focused modules:
- counts: Message counts (stats 1-4)
- content: Content analysis (stats 5-11)
- thinking: Thinking/reasoning (stats 12-15)
- tools: Tool usage (stats 16-20)
- context: Context provided (stats 21-26)
- references: External references (stats 27-30)
- suggestions: Code suggestions & diffs (stats 31-41)
- models: Model information (stats 42-44)
- tokens: Token usage (stats 45-49)
- session_context: Session context (stats 50-52)
- errors: Errors in messages (stats 53-56)
- metadata: Message metadata (stats 57-59)
- timing: Activity timing (stats 60-66)
"""

from typing import Dict, Any, List
import logging

from stats.models.message import Message
from stats.calculators.base_calculator import BaseCalculator

# Import all stat modules
from .counts import MessageCountStats
from .content import MessageContentStats
from .thinking import MessageThinkingStats
from .tools import MessageToolStats
from .context import MessageContextStats
from .references import MessageReferencesStats
from .suggestions import MessageSuggestionsStats
from .models import MessageModelsStats
from .tokens import MessageTokensStats
from .session_context import MessageSessionContextStats
from .errors import MessageErrorsStats
from .metadata import MessageMetadataStats
from .timing import MessageTimingStats

logger = logging.getLogger(__name__)


class MessageCalculator(BaseCalculator):
    """
    Main message calculator that orchestrates all message stat modules.
    
    This calculator delegates to specialized modules for maintainability.
    """
    
    def __init__(self, messages: List[Message]):
        """
        Initialize calculator.
        
        Args:
            messages: List of Message objects
        """
        super().__init__(messages)
        self.messages = messages
        
        # Initialize sub-calculators
        self.counts = MessageCountStats(messages)
        self.content = MessageContentStats(messages)
        self.thinking = MessageThinkingStats(messages)
        self.tools = MessageToolStats(messages)
        self.context = MessageContextStats(messages)
        self.references = MessageReferencesStats(messages)
        self.suggestions = MessageSuggestionsStats(messages)
        self.models = MessageModelsStats(messages)
        self.tokens = MessageTokensStats(messages)
        self.session_context = MessageSessionContextStats(messages)
        self.errors = MessageErrorsStats(messages)
        self.metadata = MessageMetadataStats(messages)
        self.timing = MessageTimingStats(messages)
        
    def calculate_all(self) -> Dict[str, Any]:
        """
        Calculate all message stats by delegating to sub-calculators.
        
        Returns:
            Dictionary of all calculated stats
        """
        logger.info(f"Calculating message stats for {len(self.messages)} messages...")
        
        stats = {}
        
        # Collect stats from each module
        stats.update(self.counts.calculate())
        stats.update(self.content.calculate())
        stats.update(self.thinking.calculate())
        stats.update(self.tools.calculate())
        stats.update(self.context.calculate())
        stats.update(self.references.calculate())
        stats.update(self.suggestions.calculate())
        stats.update(self.models.calculate())
        stats.update(self.tokens.calculate())
        stats.update(self.session_context.calculate())
        stats.update(self.errors.calculate())
        stats.update(self.metadata.calculate())
        stats.update(self.timing.calculate())
        
        logger.info(f"Calculated {len(stats)} message stats")
        return stats


__all__ = ['MessageCalculator']

