"""Formatting utilities for display."""

from typing import Any, Optional
from datetime import datetime, timedelta


def format_number(value: float, decimals: int = 0) -> str:
    """Format number with commas and optional decimals."""
    if decimals > 0:
        return f"{value:,.{decimals}f}"
    return f"{int(value):,}"


def format_percentage(value: float, decimals: int = 1) -> str:
    """Format percentage with % sign."""
    return f"{value:.{decimals}f}%"


def format_duration(seconds: float) -> str:
    """Format duration in human-readable format."""
    if seconds < 60:
        return f"{seconds:.1f}s"
    elif seconds < 3600:
        minutes = seconds / 60
        return f"{minutes:.1f}m"
    else:
        hours = seconds / 3600
        return f"{hours:.1f}h"


def format_datetime(dt: datetime) -> str:
    """Format datetime for display."""
    return dt.strftime("%Y-%m-%d %H:%M:%S")


def format_date(dt: datetime) -> str:
    """Format date only."""
    return dt.strftime("%Y-%m-%d")


def format_time(dt: datetime) -> str:
    """Format time only."""
    return dt.strftime("%H:%M:%S")


def format_relative_time(dt: datetime) -> str:
    """Format relative time (e.g., '2 hours ago')."""
    now = datetime.now()
    diff = now - dt
    
    if diff < timedelta(minutes=1):
        return "Just now"
    elif diff < timedelta(hours=1):
        minutes = int(diff.total_seconds() / 60)
        return f"{minutes} minute{'s' if minutes != 1 else ''} ago"
    elif diff < timedelta(days=1):
        hours = int(diff.total_seconds() / 3600)
        return f"{hours} hour{'s' if hours != 1 else ''} ago"
    elif diff < timedelta(days=7):
        days = diff.days
        return f"{days} day{'s' if days != 1 else ''} ago"
    elif diff < timedelta(days=30):
        weeks = diff.days // 7
        return f"{weeks} week{'s' if weeks != 1 else ''} ago"
    else:
        months = diff.days // 30
        return f"{months} month{'s' if months != 1 else ''} ago"


def format_bytes(bytes_value: int) -> str:
    """Format bytes in human-readable format."""
    for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
        if bytes_value < 1024.0:
            return f"{bytes_value:.1f} {unit}"
        bytes_value /= 1024.0
    return f"{bytes_value:.1f} PB"


def truncate_text(text: str, max_length: int = 100, suffix: str = "...") -> str:
    """Truncate text to max length."""
    if len(text) <= max_length:
        return text
    return text[:max_length - len(suffix)] + suffix


def format_stat_value(value: Any, stat_type: str = 'count') -> str:
    """Format stat value based on type."""
    if stat_type == 'count':
        return format_number(value)
    elif stat_type == 'percentage':
        return format_percentage(value)
    elif stat_type == 'numeric':
        return format_number(value, decimals=2)
    elif stat_type == 'duration':
        return format_duration(value)
    else:
        return str(value)


def get_color_for_percentage(percentage: float) -> str:
    """Get color based on percentage value."""
    if percentage >= 80:
        return "#10B981"  # Green
    elif percentage >= 60:
        return "#F59E0B"  # Amber
    elif percentage >= 40:
        return "#EF4444"  # Red
    else:
        return "#6B7280"  # Gray

