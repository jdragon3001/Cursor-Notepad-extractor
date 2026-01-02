"""Stats orchestrator for coordinating extraction and calculation."""

from pathlib import Path
from typing import Dict, Any, Optional
import logging

from stats.extractors.message_extractor import MessageExtractor
from stats.extractors.session_extractor import SessionExtractor
from stats.extractors.code_diff_extractor import CodeDiffExtractor
from stats.extractors.code_tracking_extractor import CodeTrackingExtractor
from stats.extractors.daily_stat_extractor import DailyStatExtractor
from stats.extractors.request_context_extractor import MessageRequestContextExtractor
from stats.extractors.workspace_extractor import WorkspaceExtractor
from stats.models.code_diff import CodeDiff, CodeTrackingLine
from stats.models.daily_stat import DailyStat
from stats.models.request_context import MessageRequestContext
from stats.models.workspace import Workspace
from stats.models.time_range import TimeRange
from stats.calculators.message_stats import MessageCalculator
from stats.calculators.session_stats import SessionCalculator
from stats.calculators.code_stats import CodeCalculator
from stats.calculators.daily_stats import DailyUsageCalculator
from stats.calculators.tool_stats import ToolCalculator
from stats.calculators.context_stats import ContextCalculator
from stats.filters.temporal_filter import TemporalFilter
from stats.cache import StatsCache
from stats.consolidator import MessageConsolidator

logger = logging.getLogger(__name__)


class StatsOrchestrator:
    """Coordinates data extraction and stat calculation."""
    
    def __init__(self, db_path: Path, cache_dir: Optional[Path] = None):
        """
        Initialize orchestrator.
        
        Args:
            db_path: Path to the main Cursor database
            cache_dir: Optional cache directory
        """
        self.db_path = Path(db_path)
        self.cache = StatsCache(cache_dir) if cache_dir else None
        
        # Extracted data (loaded once)
        self._messages = None
        self._sessions = None
        self._code_diffs = None
        self._tracking_lines = None
        self._daily_stats = None
        self._request_contexts = None
        self._workspaces = None
        
        logger.info(f"Initialized StatsOrchestrator with DB: {db_path.name}")
    
    def extract_all_data(self, force: bool = False):
        """
        Extract all data from databases.
        
        Args:
            force: Force re-extraction even if cached
        """
        # Check cache first
        if not force and self.cache:
            cached_data = self.cache.load_extracted_data()
            if cached_data:
                self._messages = cached_data.get('messages')
                self._sessions = cached_data.get('sessions')
                self._code_diffs = cached_data.get('code_diffs')
                self._tracking_lines = cached_data.get('tracking_lines')
                self._daily_stats = cached_data.get('daily_stats')
                self._request_contexts = cached_data.get('request_contexts')
                self._workspaces = cached_data.get('workspaces')
                logger.info("Loaded data from cache")
                return
        
        logger.info("Extracting data from databases...")
        
        # Extract messages
        with MessageExtractor(self.db_path) as extractor:
            self._messages = extractor.extract()
        logger.info(f"  Extracted {len(self._messages)} messages")
        
        # Extract sessions
        with SessionExtractor(self.db_path) as extractor:
            self._sessions = extractor.extract()
        logger.info(f"  Extracted {len(self._sessions)} sessions")
        
        # Extract code diffs
        with CodeDiffExtractor(self.db_path) as extractor:
            self._code_diffs = extractor.extract()
        logger.info(f"  Extracted {len(self._code_diffs)} code diffs")
        
        # Extract tracking lines
        with CodeTrackingExtractor(self.db_path) as extractor:
            self._tracking_lines = extractor.extract()
        logger.info(f"  Extracted {len(self._tracking_lines)} tracking lines")
        
        # Extract daily stats
        with DailyStatExtractor(self.db_path) as extractor:
            self._daily_stats = extractor.extract()
        logger.info(f"  Extracted {len(self._daily_stats)} daily stats")
        
        # Extract request contexts
        with MessageRequestContextExtractor(self.db_path) as extractor:
            self._request_contexts = extractor.extract()
        logger.info(f"  Extracted {len(self._request_contexts)} request contexts")
        
        # Extract workspaces
        workspace_extractor = WorkspaceExtractor()
        self._workspaces = workspace_extractor.extract()
        logger.info(f"  Extracted {len(self._workspaces)} workspaces")
        
        # Cache extracted data
        if self.cache:
            self.cache.save_extracted_data({
                'messages': self._messages,
                'sessions': self._sessions,
                'code_diffs': self._code_diffs,
                'tracking_lines': self._tracking_lines,
                'daily_stats': self._daily_stats,
                'request_contexts': self._request_contexts,
                'workspaces': self._workspaces
            })
    
    def calculate_all_stats(
        self, 
        force: bool = False,
        time_range: Optional[TimeRange] = None
    ) -> Dict[str, Any]:
        """
        Calculate all stats.
        
        Args:
            force: Force recalculation even if cached
            time_range: Optional TimeRange to filter data by
            
        Returns:
            Dictionary of all stats organized by category
        """
        # Check cache (only for unfiltered queries)
        if not force and self.cache and time_range is None:
            cached_stats = self.cache.load_stats()
            if cached_stats:
                logger.info("Loaded stats from cache")
                return cached_stats
        
        # Ensure data is extracted
        if self._messages is None:
            self.extract_all_data()
        
        # Apply time filtering if requested
        if time_range:
            logger.info(f"Applying time filter: {time_range}")
            filtered_messages = TemporalFilter.filter_messages(self._messages, time_range)
            filtered_sessions = TemporalFilter.filter_sessions(self._sessions, time_range)
            filtered_code_diffs = TemporalFilter.filter_code_diffs(
                self._code_diffs, filtered_sessions, time_range
            )
            filtered_tracking_lines = TemporalFilter.filter_tracking_lines(
                self._tracking_lines, time_range
            )
            filtered_daily_stats = TemporalFilter.filter_daily_stats(
                self._daily_stats, time_range
            )
            filtered_request_contexts = TemporalFilter.filter_request_contexts(
                self._request_contexts, filtered_sessions, time_range
            )
        else:
            # No filtering - use all data
            filtered_messages = self._messages
            filtered_sessions = self._sessions
            filtered_code_diffs = self._code_diffs
            filtered_tracking_lines = self._tracking_lines
            filtered_daily_stats = self._daily_stats
            filtered_request_contexts = self._request_contexts
        
        # Consolidate messages (merge AI message fragments into logical turns)
        logger.info("Consolidating messages...")
        try:
            consolidated_messages = MessageConsolidator.consolidate(filtered_messages)
            logger.info(f"  Consolidated {len(filtered_messages)} raw messages into {len(consolidated_messages)} logical messages")
            messages_for_stats = consolidated_messages if consolidated_messages else filtered_messages
        except Exception as e:
            logger.error(f"  Consolidation failed, using raw messages: {e}")
            messages_for_stats = filtered_messages
        
        logger.info("Calculating stats...")
        all_stats = {}
        
        # Calculate message stats
        logger.info("  Calculating message stats...")
        message_calc = MessageCalculator(messages_for_stats)
        all_stats['messages'] = message_calc.calculate_all()
        
        # Calculate session stats
        logger.info("  Calculating session stats...")
        session_calc = SessionCalculator(filtered_sessions, messages_for_stats)
        all_stats['sessions'] = session_calc.calculate_all()
        
        # Calculate code & diffs stats
        logger.info("  Calculating code & diffs stats...")
        code_calc = CodeCalculator(filtered_code_diffs, filtered_tracking_lines)
        all_stats['code'] = code_calc.calculate_all()
        
        # Calculate daily usage stats
        logger.info("  Calculating daily usage stats...")
        daily_calc = DailyUsageCalculator(filtered_daily_stats)
        all_stats['daily'] = daily_calc.calculate_all()
        
        # Calculate tool usage stats
        logger.info("  Calculating tool usage stats...")
        tool_calc = ToolCalculator(messages_for_stats)
        all_stats['tools'] = tool_calc.calculate_all()
        
        # Calculate context stats
        logger.info("  Calculating context stats...")
        context_calc = ContextCalculator(filtered_request_contexts)
        all_stats['context'] = context_calc.calculate_all()
        
        # Cache results (only for unfiltered queries)
        if self.cache and time_range is None:
            self.cache.save_stats(all_stats)
        
        logger.info(f"Calculated stats for {len(all_stats)} categories")
        return all_stats
    
    def get_stat(self, stat_id: str, time_range: Optional[TimeRange] = None) -> Optional[Dict[str, Any]]:
        """
        Get a single stat by ID.
        
        Args:
            stat_id: The stat identifier
            time_range: Optional TimeRange to filter data by
            
        Returns:
            Stat data or None if not found
        """
        all_stats = self.calculate_all_stats(time_range=time_range)
        
        # Search through categories
        for category, stats in all_stats.items():
            if stat_id in stats:
                return stats[stat_id]
        
        return None
    
    def get_time_series(
        self,
        stat_id: str,
        time_range: TimeRange,
        granularity: str = "day"
    ) -> Dict[str, Any]:
        """
        Get time series data for a specific stat.
        
        Args:
            stat_id: The stat identifier
            time_range: TimeRange for the series
            granularity: Time granularity (day, week, month)
            
        Returns:
            Dictionary with time series data
        """
        # Ensure data is extracted
        if self._messages is None:
            self.extract_all_data()
        
        # Determine which category this stat belongs to
        all_stats = self.calculate_all_stats()
        stat_category = None
        for category, stats in all_stats.items():
            if stat_id in stats:
                stat_category = category
                break
        
        # Generate time series based on category
        series_data = {}
        
        if stat_category == 'messages' or stat_category == 'tools':
            # Message-based stats
            series_data = TemporalFilter.get_time_series_data(
                self._messages, time_range, granularity
            )
        elif stat_category == 'sessions':
            # Session-based stats
            series_data = TemporalFilter.get_session_time_series(
                self._sessions, time_range, granularity
            )
        elif stat_category == 'code':
            # Code diffs - use session timestamps
            series_data = TemporalFilter.get_session_time_series(
                self._sessions, time_range, granularity
            )
        elif stat_category == 'daily':
            # Daily stats already have dates
            from collections import defaultdict
            from datetime import timedelta
            
            counts = defaultdict(int)
            filtered_daily = TemporalFilter.filter_daily_stats(self._daily_stats, time_range)
            
            for stat in filtered_daily:
                if granularity == "day":
                    key = stat.date.isoformat()
                    counts[key] += 1
                elif granularity == "week":
                    start_of_week = stat.date - timedelta(days=stat.date.weekday())
                    key = start_of_week.isoformat()
                    counts[key] += 1
                elif granularity == "month":
                    key = f"{stat.date.year}-{stat.date.month:02d}"
                    counts[key] += 1
            
            series_data = dict(sorted(counts.items()))
        elif stat_category == 'context':
            # Context stats - use session timestamps
            series_data = TemporalFilter.get_session_time_series(
                self._sessions, time_range, granularity
            )
        else:
            # Default: use message time series
            series_data = TemporalFilter.get_time_series_data(
                self._messages, time_range, granularity
            )
        
        return {
            'stat_id': stat_id,
            'time_range': time_range.to_dict(),
            'granularity': granularity,
            'series': series_data,
            'category': stat_category
        }
    
    def invalidate_cache(self):
        """Clear cached data and stats."""
        if self.cache:
            self.cache.clear()
        self._messages = None
        self._sessions = None
        self._code_diffs = None
        self._tracking_lines = None
        self._daily_stats = None
        self._request_contexts = None
        self._workspaces = None
        logger.info("Invalidated cache")
    
    # ==================== DATA ACCESS ====================
    
    @property
    def messages(self):
        """Get extracted messages."""
        if self._messages is None:
            self.extract_all_data()
        return self._messages
    
    @property
    def sessions(self):
        """Get extracted sessions."""
        if self._sessions is None:
            self.extract_all_data()
        return self._sessions
    
    # ==================== UTILITY METHODS ====================
    
    def get_summary(self) -> Dict[str, Any]:
        """
        Get a quick summary of available data.
        
        Returns:
            Dictionary with data counts
        """
        # Ensure data is loaded
        if self._messages is None:
            self.extract_all_data()
        
        return {
            'total_messages': len(self._messages) if self._messages else 0,
            'total_sessions': len(self._sessions) if self._sessions else 0,
            'total_code_diffs': len(self._code_diffs) if self._code_diffs else 0,
            'total_tracking_lines': len(self._tracking_lines) if self._tracking_lines else 0,
            'total_daily_stats': len(self._daily_stats) if self._daily_stats else 0,
            'total_request_contexts': len(self._request_contexts) if self._request_contexts else 0,
            'total_workspaces': len(self._workspaces) if self._workspaces else 0,
            'database_path': str(self.db_path),
            'cache_enabled': self.cache is not None
        }

