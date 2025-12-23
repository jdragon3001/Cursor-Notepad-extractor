"""Message error statistics (Stats 53-56)."""

from typing import Dict, Any, List
from stats.models.message import Message
from .base import MessageStatsBase


class MessageErrorsStats(MessageStatsBase):
    """Calculate error-related statistics."""
    
    def __init__(self, messages: List[Message]):
        """Initialize with messages."""
        super().__init__(messages)
    
    def calculate(self) -> Dict[str, Any]:
        """
        Calculate all error stats.
        
        NOTE: Stats 53-55 removed - Cursor doesn't populate lints/consoleLogs arrays in message data.
        Linter errors ARE tracked in messageRequestContext (see context_stats), not in bubbleId messages.
        Terminal interactions stat remains but uses different fields (toolFormerData, lastTerminalCwd).
        """
        return {
            # Removed: messages_with_lints (always 0 - field not used)
            # Removed: linter_errors (always 0 - field not used)
            # Removed: messages_with_console_logs (always 0 - field not used)
            'terminal_interactions': self.stat_056_terminal_interactions(),
        }
    
    # REMOVED STAT #53 - Messages with lints
    # This stat always returned 0 because Cursor doesn't populate the m.lints array in bubbleId messages.
    # Linter error data IS available in messageRequestContext (see context_stats module).
    
    # REMOVED STAT #54 - Total linter errors  
    # This stat always returned 0 because Cursor doesn't populate the m.lints array in bubbleId messages.
    # Real linter errors: 174 contexts with 1,206 errors (see context_stats.total_linter_errors).
    
    # REMOVED STAT #55 - Messages with console logs
    # This stat always returned 0 because Cursor doesn't populate the m.console_logs array in bubbleId messages.
    
    def stat_056_terminal_interactions(self) -> Dict[str, Any]:
        """
        Stat #56: Terminal interactions around messages.
        
        Checks for terminal-related data in messages.
        Note: Only ~3% of messages have terminal context (lastTerminalCwd).
        """
        # Check for terminal-related data
        with_terminal_cwd = 0
        with_terminal_capability = 0
        
        for m in self.messages:
            if m.raw_data:
                # Check for lastTerminalCwd field (actually exists in ~3% of messages)
                if 'lastTerminalCwd' in m.raw_data and m.raw_data['lastTerminalCwd']:
                    with_terminal_cwd += 1
                
                # Check if terminal capability was available
                if 'terminal' in m.capabilities:
                    with_terminal_capability += 1
        
        total = len(self.messages)
        
        return self.create_stat_result(
            value=with_terminal_cwd,
            label='Messages with terminal context',
            category='Messages',
            data_source='bubbleId',
            stat_type='count',
            percentage=self.percentage(with_terminal_cwd, total),
            breakdown={
                'with_terminal_cwd': with_terminal_cwd,
                'with_terminal_capability': with_terminal_capability,
                'total_messages': total
            }
        )

