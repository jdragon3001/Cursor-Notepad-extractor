"""DailyStat data model representing daily usage statistics."""

from dataclasses import dataclass
from typing import Dict, Any
from datetime import datetime, date


@dataclass
class DailyStat:
    """Represents daily usage statistics from aiCodeTracking.dailyStats."""
    
    # ==================== REQUIRED FIELDS ====================
    
    date: date
    """The date for these stats"""
    
    # ==================== COMPOSER STATS ====================
    
    composer_suggested_lines: int = 0
    """Lines suggested by composer"""
    
    composer_accepted_lines: int = 0
    """Lines accepted by composer"""
    
    # ==================== TAB STATS ====================
    
    tab_suggested_lines: int = 0
    """Lines suggested by tab completion"""
    
    tab_accepted_lines: int = 0
    """Lines accepted by tab completion"""
    
    # ==================== CLASS METHODS ====================
    
    @classmethod
    def from_dict(cls, key: str, data: Dict[str, Any]) -> 'DailyStat':
        """
        Create DailyStat from dictionary (JSON data).
        
        Args:
            key: The ItemTable key (format: "aiCodeTracking.dailyStats.v1.5.YYYY-MM-DD")
            data: The JSON data
            
        Returns:
            DailyStat object
        """
        # Parse date from key or data
        date_str = data.get('date')
        if not date_str:
            # Extract from key: aiCodeTracking.dailyStats.v1.5.2025-11-20
            parts = key.split('.')
            if len(parts) >= 4:
                date_str = parts[-1]
        
        # Parse date string
        stat_date = datetime.strptime(date_str, '%Y-%m-%d').date()
        
        return cls(
            date=stat_date,
            composer_suggested_lines=data.get('composerSuggestedLines', 0),
            composer_accepted_lines=data.get('composerAcceptedLines', 0),
            tab_suggested_lines=data.get('tabSuggestedLines', 0),
            tab_accepted_lines=data.get('tabAcceptedLines', 0)
        )
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for serialization."""
        return {
            'date': self.date.isoformat(),
            'composer_suggested_lines': self.composer_suggested_lines,
            'composer_accepted_lines': self.composer_accepted_lines,
            'tab_suggested_lines': self.tab_suggested_lines,
            'tab_accepted_lines': self.tab_accepted_lines,
        }
    
    # ==================== COMPUTED PROPERTIES ====================
    
    @property
    def composer_acceptance_rate(self) -> float:
        """Calculate composer acceptance rate (0-100)."""
        if self.composer_suggested_lines == 0:
            return 0.0
        return (self.composer_accepted_lines / self.composer_suggested_lines) * 100
    
    @property
    def tab_acceptance_rate(self) -> float:
        """Calculate tab acceptance rate (0-100)."""
        if self.tab_suggested_lines == 0:
            return 0.0
        return (self.tab_accepted_lines / self.tab_suggested_lines) * 100
    
    @property
    def total_suggested_lines(self) -> int:
        """Total lines suggested (composer + tab)."""
        return self.composer_suggested_lines + self.tab_suggested_lines
    
    @property
    def total_accepted_lines(self) -> int:
        """Total lines accepted (composer + tab)."""
        return self.composer_accepted_lines + self.tab_accepted_lines
    
    @property
    def overall_acceptance_rate(self) -> float:
        """Calculate overall acceptance rate (0-100)."""
        total_suggested = self.total_suggested_lines
        if total_suggested == 0:
            return 0.0
        return (self.total_accepted_lines / total_suggested) * 100
    
    @property
    def composer_net_lines(self) -> int:
        """Net lines from composer (could be negative if more accepted than suggested)."""
        return self.composer_accepted_lines - self.composer_suggested_lines
    
    @property
    def has_composer_activity(self) -> bool:
        """Whether there was composer activity this day."""
        return self.composer_suggested_lines > 0 or self.composer_accepted_lines > 0
    
    @property
    def has_tab_activity(self) -> bool:
        """Whether there was tab activity this day."""
        return self.tab_suggested_lines > 0 or self.tab_accepted_lines > 0

