"""Message activity timing statistics (Stats 60-66)."""

from typing import Dict, Any, List
from datetime import datetime, timedelta
from collections import defaultdict
from stats.models.message import Message
from .base import MessageStatsBase


class MessageTimingStats(MessageStatsBase):
    """Calculate activity timing statistics."""
    
    def __init__(self, messages: List[Message]):
        """Initialize with messages."""
        super().__init__(messages)
    
    def calculate(self) -> Dict[str, Any]:
        """Calculate all timing stats."""
        return {
            'message_timestamps': self.stat_060_message_timestamps(),
            'time_between_messages': self.stat_061_time_between_messages(),
            'active_days': self.stat_062_active_days(),
            'inactive_days': self.stat_063_inactive_days(),
            'activity_streak': self.stat_064_activity_streak(),
            'peak_activity_hours': self.stat_065_peak_activity_hours(),
            'peak_activity_days': self.stat_066_peak_activity_days(),
        }
    
    def stat_060_message_timestamps(self) -> Dict[str, Any]:
        """Stat #60: Message timestamps distribution."""
        if not self.messages:
            return self.create_stat_result(
                value=0,
                label='Message timestamps',
                category='Messages',
                data_source='bubbleId',
                stat_type='count',
                sample_size=0
            )
        
        # Sort by timestamp
        sorted_msgs = sorted(self.messages, key=lambda m: m.created_at)
        first_msg = sorted_msgs[0].created_at
        last_msg = sorted_msgs[-1].created_at
        time_span_days = (last_msg - first_msg).days
        
        return self.create_stat_result(
            value=len(self.messages),
            label='Message timestamps',
            category='Messages',
            data_source='bubbleId',
            stat_type='count',
            first_message=first_msg.isoformat(),
            last_message=last_msg.isoformat(),
            time_span_days=time_span_days
        )
    
    def stat_061_time_between_messages(self) -> Dict[str, Any]:
        """Stat #61: Time between consecutive messages."""
        sorted_msgs = sorted(self.messages, key=lambda m: m.created_at)
        
        gaps = []
        for i in range(1, len(sorted_msgs)):
            gap = (sorted_msgs[i].created_at - sorted_msgs[i-1].created_at).total_seconds()
            gaps.append(gap)
        
        if not gaps:
            return self.create_stat_result(
                value=0,
                label='Time between messages (seconds)',
                category='Messages',
                data_source='bubbleId',
                stat_type='numeric',
                sample_size=0
            )
        
        return self.create_stat_result(
            value=self.average(gaps),
            label='Time between messages (seconds)',
            category='Messages',
            data_source='bubbleId',
            stat_type='numeric',
            median=self.median(gaps),
            min=self.min_val(gaps),
            max=self.max_val(gaps),
            p95=self.percentile(gaps, 95),
            std_dev=self.std_dev(gaps),
            sample_size=len(gaps)
        )
    
    def stat_062_active_days(self) -> Dict[str, Any]:
        """Stat #62: Active days (days with message activity)."""
        # Group messages by date
        dates = set()
        for m in self.messages:
            date = m.created_at.date()
            dates.add(date)
        
        active_days = len(dates)
        
        # Calculate date range
        if dates:
            min_date = min(dates)
            max_date = max(dates)
            total_days = (max_date - min_date).days + 1
        else:
            total_days = 0
        
        return self.create_stat_result(
            value=active_days,
            label='Active days',
            category='Messages',
            data_source='bubbleId',
            stat_type='count',
            total_days_in_range=total_days,
            percentage_active=self.percentage(active_days, total_days) if total_days > 0 else 0
        )
    
    def stat_063_inactive_days(self) -> Dict[str, Any]:
        """Stat #63: Inactive days (days without messages)."""
        # Group messages by date
        dates = set()
        for m in self.messages:
            date = m.created_at.date()
            dates.add(date)
        
        if dates:
            min_date = min(dates)
            max_date = max(dates)
            total_days = (max_date - min_date).days + 1
            inactive_days = total_days - len(dates)
        else:
            inactive_days = 0
            total_days = 0
        
        return self.create_stat_result(
            value=inactive_days,
            label='Inactive days',
            category='Messages',
            data_source='bubbleId',
            stat_type='count',
            total_days_in_range=total_days,
            active_days=len(dates),
            percentage_inactive=self.percentage(inactive_days, total_days) if total_days > 0 else 0
        )
    
    def stat_064_activity_streak(self) -> Dict[str, Any]:
        """Stat #64: Activity streak (consecutive days of activity)."""
        # Get all unique dates sorted
        dates = sorted(set(m.created_at.date() for m in self.messages))
        
        if not dates:
            return self.create_stat_result(
                value=0,
                label='Longest activity streak (days)',
                category='Messages',
                data_source='bubbleId',
                stat_type='count',
                current_streak=0
            )
        
        # Find longest streak
        longest_streak = 1
        current_streak = 1
        
        for i in range(1, len(dates)):
            if (dates[i] - dates[i-1]).days == 1:
                current_streak += 1
                longest_streak = max(longest_streak, current_streak)
            else:
                current_streak = 1
        
        # Calculate current streak from today
        today = datetime.now().date()
        streak_from_today = 0
        for i in range(len(dates) - 1, -1, -1):
            expected_date = today - timedelta(days=streak_from_today)
            if dates[i] == expected_date:
                streak_from_today += 1
            else:
                break
        
        return self.create_stat_result(
            value=longest_streak,
            label='Longest activity streak (days)',
            category='Messages',
            data_source='bubbleId',
            stat_type='count',
            current_streak=streak_from_today
        )
    
    def stat_065_peak_activity_hours(self) -> Dict[str, Any]:
        """Stat #65: Peak activity hours (hour of day breakdown)."""
        hours = defaultdict(int)
        
        for m in self.messages:
            hour = m.created_at.hour
            hours[hour] += 1
        
        # Sort by count
        sorted_hours = sorted(hours.items(), key=lambda x: x[1], reverse=True)
        
        peak_hour = sorted_hours[0][0] if sorted_hours else 0
        peak_count = sorted_hours[0][1] if sorted_hours else 0
        
        return self.create_stat_result(
            value=peak_hour,
            label='Peak activity hour',
            category='Messages',
            data_source='bubbleId',
            stat_type='count',
            peak_message_count=peak_count,
            hour_breakdown=sorted_hours[:24],  # All 24 hours
            percentage_in_peak_hour=self.percentage(peak_count, len(self.messages))
        )
    
    def stat_066_peak_activity_days(self) -> Dict[str, Any]:
        """Stat #66: Peak activity days (day of week breakdown)."""
        days = defaultdict(int)
        day_names = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
        
        for m in self.messages:
            day = m.created_at.weekday()  # 0=Monday, 6=Sunday
            days[day] += 1
        
        # Sort by count
        sorted_days = sorted(days.items(), key=lambda x: x[1], reverse=True)
        
        # Convert to day names
        day_breakdown = [(day_names[day], count) for day, count in sorted_days]
        
        peak_day = day_names[sorted_days[0][0]] if sorted_days else 'N/A'
        peak_count = sorted_days[0][1] if sorted_days else 0
        
        return self.create_stat_result(
            value=peak_day,
            label='Peak activity day',
            category='Messages',
            data_source='bubbleId',
            stat_type='text',
            peak_message_count=peak_count,
            day_breakdown=day_breakdown,
            percentage_on_peak_day=self.percentage(peak_count, len(self.messages))
        )

