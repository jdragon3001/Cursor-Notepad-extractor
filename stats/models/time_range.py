"""TimeRange data model for temporal filtering."""

from dataclasses import dataclass
from typing import Optional
from datetime import datetime, date, timedelta


@dataclass
class TimeRange:
    """
    Represents a time range for filtering statistics.
    
    Used for filtering messages, sessions, and other temporal data.
    """
    
    # ==================== REQUIRED FIELDS ====================
    
    start: datetime
    """Start of the time range (inclusive)"""
    
    end: datetime
    """End of the time range (inclusive)"""
    
    label: str
    """Human-readable label for this time range"""
    
    # ==================== OPTIONAL FIELDS ====================
    
    granularity: str = "day"
    """Time granularity: day, week, month, quarter, year"""
    
    # ==================== CLASS METHODS ====================
    
    @classmethod
    def from_dates(cls, start: date, end: date, label: str = None) -> 'TimeRange':
        """
        Create TimeRange from date objects.
        
        Args:
            start: Start date
            end: End date
            label: Optional label (auto-generated if not provided)
            
        Returns:
            TimeRange object
        """
        start_dt = datetime.combine(start, datetime.min.time())
        end_dt = datetime.combine(end, datetime.max.time())
        
        if label is None:
            label = f"{start.isoformat()} to {end.isoformat()}"
        
        return cls(start=start_dt, end=end_dt, label=label)
    
    @classmethod
    def from_preset(cls, preset: str) -> 'TimeRange':
        """
        Create TimeRange from preset.
        
        Args:
            preset: Preset name (last_7_days, last_30_days, this_month, etc.)
            
        Returns:
            TimeRange object
        """
        now = datetime.now()
        today = date.today()
        
        if preset == "today":
            start = datetime.combine(today, datetime.min.time())
            end = datetime.combine(today, datetime.max.time())
            label = "Today"
        
        elif preset == "yesterday":
            yesterday = today - timedelta(days=1)
            start = datetime.combine(yesterday, datetime.min.time())
            end = datetime.combine(yesterday, datetime.max.time())
            label = "Yesterday"
        
        elif preset == "last_7_days":
            start = datetime.combine(today - timedelta(days=6), datetime.min.time())
            end = datetime.combine(today, datetime.max.time())
            label = "Last 7 Days"
        
        elif preset == "last_30_days":
            start = datetime.combine(today - timedelta(days=29), datetime.min.time())
            end = datetime.combine(today, datetime.max.time())
            label = "Last 30 Days"
        
        elif preset == "last_90_days":
            start = datetime.combine(today - timedelta(days=89), datetime.min.time())
            end = datetime.combine(today, datetime.max.time())
            label = "Last 90 Days"
        
        elif preset == "this_week":
            # Start from Monday
            start_date = today - timedelta(days=today.weekday())
            start = datetime.combine(start_date, datetime.min.time())
            end = now
            label = "This Week"
        
        elif preset == "this_month":
            start = datetime(now.year, now.month, 1)
            end = now
            label = f"{now.strftime('%B %Y')}"
        
        elif preset == "last_month":
            # First day of last month
            first_this_month = date(now.year, now.month, 1)
            last_day_last_month = first_this_month - timedelta(days=1)
            first_last_month = date(last_day_last_month.year, last_day_last_month.month, 1)
            
            start = datetime.combine(first_last_month, datetime.min.time())
            end = datetime.combine(last_day_last_month, datetime.max.time())
            label = f"{last_day_last_month.strftime('%B %Y')}"
        
        elif preset == "this_quarter":
            quarter = (now.month - 1) // 3 + 1
            first_month = (quarter - 1) * 3 + 1
            start = datetime(now.year, first_month, 1)
            end = now
            label = f"Q{quarter} {now.year}"
        
        elif preset == "this_year":
            start = datetime(now.year, 1, 1)
            end = now
            label = str(now.year)
        
        elif preset == "all_time":
            # Use a very early date
            start = datetime(2020, 1, 1)
            end = now
            label = "All Time"
        
        else:
            raise ValueError(f"Unknown preset: {preset}")
        
        return cls(start=start, end=end, label=label)
    
    @classmethod
    def from_iso_strings(cls, start_str: str, end_str: str, label: str = None) -> 'TimeRange':
        """
        Create TimeRange from ISO format strings.
        
        Args:
            start_str: Start datetime in ISO format
            end_str: End datetime in ISO format
            label: Optional label
            
        Returns:
            TimeRange object
        """
        start = datetime.fromisoformat(start_str.replace('Z', '+00:00'))
        end = datetime.fromisoformat(end_str.replace('Z', '+00:00'))
        
        # Remove timezone info to keep naive datetimes
        start = start.replace(tzinfo=None)
        end = end.replace(tzinfo=None)
        
        if label is None:
            label = f"{start.date()} to {end.date()}"
        
        return cls(start=start, end=end, label=label)
    
    # ==================== HELPER PROPERTIES ====================
    
    @property
    def duration_days(self) -> int:
        """Get duration in days."""
        return (self.end - self.start).days
    
    @property
    def duration_hours(self) -> float:
        """Get duration in hours."""
        return (self.end - self.start).total_seconds() / 3600
    
    @property
    def is_single_day(self) -> bool:
        """Check if this is a single day range."""
        return self.start.date() == self.end.date()
    
    @property
    def start_date(self) -> date:
        """Get start as date object."""
        return self.start.date()
    
    @property
    def end_date(self) -> date:
        """Get end as date object."""
        return self.end.date()
    
    # ==================== HELPER METHODS ====================
    
    def contains(self, dt: datetime) -> bool:
        """
        Check if a datetime is within this range.
        
        Args:
            dt: Datetime to check
            
        Returns:
            True if datetime is within range
        """
        return self.start <= dt <= self.end
    
    def overlaps(self, other: 'TimeRange') -> bool:
        """
        Check if this range overlaps with another.
        
        Args:
            other: Another TimeRange
            
        Returns:
            True if ranges overlap
        """
        return self.start <= other.end and other.start <= self.end
    
    def to_dict(self) -> dict:
        """Convert to dictionary for JSON serialization."""
        return {
            'start': self.start.isoformat(),
            'end': self.end.isoformat(),
            'label': self.label,
            'granularity': self.granularity,
            'duration_days': self.duration_days
        }
    
    def __str__(self) -> str:
        """String representation."""
        return f"{self.label} ({self.start.date()} to {self.end.date()})"

