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
        """Calculate all error stats."""
        return {
            'messages_with_lints': self.stat_053_messages_with_lints(),
            'linter_errors': self.stat_054_linter_errors(),
            'messages_with_console_logs': self.stat_055_messages_with_console_logs(),
            'terminal_interactions': self.stat_056_terminal_interactions(),
        }
    
    def stat_053_messages_with_lints(self) -> Dict[str, Any]:
        """Stat #53: Messages with lints."""
        with_lints = self.filter_by(self.messages, lambda m: m.has_errors and len(m.lints) > 0)
        total = len(self.messages)
        
        return self.create_stat_result(
            value=len(with_lints),
            label='Messages with linter errors',
            category='Messages',
            data_source='bubbleId',
            stat_type='count',
            percentage=self.percentage(len(with_lints), total)
        )
    
    def stat_054_linter_errors(self) -> Dict[str, Any]:
        """Stat #54: Total linter errors."""
        total_lints = sum(len(m.lints) for m in self.messages)
        messages_with_lints = len([m for m in self.messages if len(m.lints) > 0])
        
        # Extract error types
        error_types = []
        for m in self.messages:
            for lint in m.lints:
                if isinstance(lint, dict):
                    error_type = lint.get('type') or lint.get('severity') or lint.get('rule')
                    if error_type:
                        error_types.append(error_type)
        
        top_errors = self.most_common(error_types, n=20) if error_types else []
        
        return self.create_stat_result(
            value=total_lints,
            label='Total linter errors',
            category='Messages',
            data_source='bubbleId',
            stat_type='count',
            messages_with_lints=messages_with_lints,
            average_per_message=total_lints / messages_with_lints if messages_with_lints > 0 else 0,
            top_error_types=top_errors
        )
    
    def stat_055_messages_with_console_logs(self) -> Dict[str, Any]:
        """Stat #55: Messages with console logs."""
        with_logs = self.filter_by(self.messages, lambda m: len(m.console_logs) > 0)
        total = len(self.messages)
        
        return self.create_stat_result(
            value=len(with_logs),
            label='Messages with console logs',
            category='Messages',
            data_source='bubbleId',
            stat_type='count',
            percentage=self.percentage(len(with_logs), total)
        )
    
    def stat_056_terminal_interactions(self) -> Dict[str, Any]:
        """Stat #56: Terminal interactions around messages."""
        # Check for terminal-related data in raw_data
        with_terminal = 0
        for m in self.messages:
            if m.raw_data:
                if 'terminalOutput' in m.raw_data or 'terminalCommand' in m.raw_data:
                    with_terminal += 1
                elif 'terminal' in m.capabilities:
                    with_terminal += 1
        
        return self.create_stat_result(
            value=with_terminal,
            label='Messages with terminal interactions',
            category='Messages',
            data_source='bubbleId',
            stat_type='count',
            percentage=self.percentage(with_terminal, len(self.messages))
        )

