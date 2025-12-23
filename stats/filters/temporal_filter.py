"""Temporal filtering for messages, sessions, and other time-based data."""

from typing import List, Dict, Any, Optional
from datetime import datetime
import logging

from stats.models.time_range import TimeRange
from stats.models.message import Message
from stats.models.session import Session
from stats.models.code_diff import CodeDiff, CodeTrackingLine
from stats.models.daily_stat import DailyStat

logger = logging.getLogger(__name__)


class TemporalFilter:
    """Filter data by time ranges."""
    
    @staticmethod
    def filter_messages(
        messages: List[Message],
        time_range: Optional[TimeRange]
    ) -> List[Message]:
        """
        Filter messages by time range.
        
        Args:
            messages: List of Message objects
            time_range: TimeRange to filter by (None = no filtering)
            
        Returns:
            Filtered list of messages
        """
        if time_range is None:
            return messages
        
        filtered = [
            msg for msg in messages
            if time_range.contains(msg.created_at)
        ]
        
        logger.info(
            f"Filtered messages: {len(messages)} -> {len(filtered)} "
            f"({time_range.label})"
        )
        return filtered
    
    @staticmethod
    def filter_sessions(
        sessions: List[Session],
        time_range: Optional[TimeRange]
    ) -> List[Session]:
        """
        Filter sessions by time range.
        
        Sessions are included if they were active during the time range.
        A session is "active" if it overlaps with the time range.
        
        Args:
            sessions: List of Session objects
            time_range: TimeRange to filter by (None = no filtering)
            
        Returns:
            Filtered list of sessions
        """
        if time_range is None:
            return sessions
        
        filtered = [
            session for session in sessions
            if (
                # Session started within range
                time_range.contains(session.created_at) or
                # Session ended within range
                time_range.contains(session.last_updated_at) or
                # Session spans the entire range
                (session.created_at <= time_range.start and 
                 session.last_updated_at >= time_range.end)
            )
        ]
        
        logger.info(
            f"Filtered sessions: {len(sessions)} -> {len(filtered)} "
            f"({time_range.label})"
        )
        return filtered
    
    @staticmethod
    def filter_code_diffs(
        code_diffs: List[CodeDiff],
        sessions: List[Session],
        time_range: Optional[TimeRange]
    ) -> List[CodeDiff]:
        """
        Filter code diffs by time range.
        
        Since CodeDiff doesn't have a timestamp, we use the associated session's
        timestamp.
        
        Args:
            code_diffs: List of CodeDiff objects
            sessions: List of Session objects (for timestamp lookup)
            time_range: TimeRange to filter by (None = no filtering)
            
        Returns:
            Filtered list of code diffs
        """
        if time_range is None:
            return code_diffs
        
        # Build session lookup by composer_id
        session_map = {session.composer_id: session for session in sessions}
        
        filtered = []
        for diff in code_diffs:
            session = session_map.get(diff.composer_id)
            if session and time_range.contains(session.created_at):
                filtered.append(diff)
        
        logger.info(
            f"Filtered code diffs: {len(code_diffs)} -> {len(filtered)} "
            f"({time_range.label})"
        )
        return filtered
    
    @staticmethod
    def filter_tracking_lines(
        tracking_lines: List[CodeTrackingLine],
        time_range: Optional[TimeRange]
    ) -> List[CodeTrackingLine]:
        """
        Filter code tracking lines by time range.
        
        Args:
            tracking_lines: List of CodeTrackingLine objects
            time_range: TimeRange to filter by (None = no filtering)
            
        Returns:
            Filtered list of tracking lines
        """
        if time_range is None:
            return tracking_lines
        
        filtered = []
        for line in tracking_lines:
            if line.created_at and time_range.contains(line.created_at):
                filtered.append(line)
        
        logger.info(
            f"Filtered tracking lines: {len(tracking_lines)} -> {len(filtered)} "
            f"({time_range.label})"
        )
        return filtered
    
    @staticmethod
    def filter_daily_stats(
        daily_stats: List[DailyStat],
        time_range: Optional[TimeRange]
    ) -> List[DailyStat]:
        """
        Filter daily stats by time range.
        
        Args:
            daily_stats: List of DailyStat objects
            time_range: TimeRange to filter by (None = no filtering)
            
        Returns:
            Filtered list of daily stats
        """
        if time_range is None:
            return daily_stats
        
        filtered = [
            stat for stat in daily_stats
            if time_range.start_date <= stat.date <= time_range.end_date
        ]
        
        logger.info(
            f"Filtered daily stats: {len(daily_stats)} -> {len(filtered)} "
            f"({time_range.label})"
        )
        return filtered
    
    @staticmethod
    def filter_request_contexts(
        request_contexts: List[Any],
        sessions: List[Session],
        time_range: Optional[TimeRange]
    ) -> List[Any]:
        """
        Filter request contexts by time range.
        
        Since request contexts don't have timestamps, we use the associated
        session's timestamp.
        
        Args:
            request_contexts: List of MessageRequestContext objects
            sessions: List of Session objects (for timestamp lookup)
            time_range: TimeRange to filter by (None = no filtering)
            
        Returns:
            Filtered list of request contexts
        """
        if time_range is None:
            return request_contexts
        
        # Build session lookup by composer_id
        session_map = {session.composer_id: session for session in sessions}
        
        filtered = []
        for context in request_contexts:
            session = session_map.get(context.composer_id)
            if session and time_range.contains(session.created_at):
                filtered.append(context)
        
        logger.info(
            f"Filtered request contexts: {len(request_contexts)} -> {len(filtered)} "
            f"({time_range.label})"
        )
        return filtered
    
    @staticmethod
    def get_time_series_data(
        messages: List[Message],
        time_range: TimeRange,
        granularity: str = "day"
    ) -> Dict[str, int]:
        """
        Get time series data for messages.
        
        Args:
            messages: List of Message objects
            time_range: TimeRange for grouping
            granularity: Time granularity (day, week, month)
            
        Returns:
            Dictionary mapping time label to count
        """
        from collections import defaultdict
        
        counts = defaultdict(int)
        
        for msg in messages:
            if time_range.contains(msg.created_at):
                if granularity == "day":
                    key = msg.created_at.date().isoformat()
                elif granularity == "week":
                    # Start of week (Monday)
                    start_of_week = msg.created_at.date()
                    start_of_week = start_of_week - timedelta(days=start_of_week.weekday())
                    key = start_of_week.isoformat()
                elif granularity == "month":
                    key = f"{msg.created_at.year}-{msg.created_at.month:02d}"
                else:
                    key = msg.created_at.date().isoformat()
                
                counts[key] += 1
        
        return dict(sorted(counts.items()))
    
    @staticmethod
    def get_session_time_series(
        sessions: List[Session],
        time_range: TimeRange,
        granularity: str = "day"
    ) -> Dict[str, int]:
        """
        Get time series data for sessions.
        
        Args:
            sessions: List of Session objects
            time_range: TimeRange for grouping
            granularity: Time granularity (day, week, month)
            
        Returns:
            Dictionary mapping time label to count
        """
        from collections import defaultdict
        
        counts = defaultdict(int)
        
        for session in sessions:
            if time_range.contains(session.created_at):
                if granularity == "day":
                    key = session.created_at.date().isoformat()
                elif granularity == "week":
                    # Start of week (Monday)
                    start_of_week = session.created_at.date()
                    start_of_week = start_of_week - timedelta(days=start_of_week.weekday())
                    key = start_of_week.isoformat()
                elif granularity == "month":
                    key = f"{session.created_at.year}-{session.created_at.month:02d}"
                else:
                    key = session.created_at.date().isoformat()
                
                counts[key] += 1
        
        return dict(sorted(counts.items()))


# Import timedelta for time series methods
from datetime import timedelta

