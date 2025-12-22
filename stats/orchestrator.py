"""Stats orchestrator for coordinating extraction and calculation."""

from pathlib import Path
from typing import Dict, Any, Optional
import logging

from stats.extractors.message_extractor import MessageExtractor
from stats.extractors.session_extractor import SessionExtractor
from stats.extractors.code_diff_extractor import CodeDiffExtractor
from stats.extractors.code_tracking_extractor import CodeTrackingExtractor
from stats.extractors.daily_stat_extractor import DailyStatExtractor
from stats.models.code_diff import CodeDiff, CodeTrackingLine
from stats.models.daily_stat import DailyStat
from stats.calculators.message_stats import MessageCalculator
from stats.calculators.session_stats import SessionCalculator
from stats.calculators.code_stats import CodeCalculator
from stats.calculators.daily_stats import DailyUsageCalculator
from stats.cache import StatsCache

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
        
        # Cache extracted data
        if self.cache:
            self.cache.save_extracted_data({
                'messages': self._messages,
                'sessions': self._sessions,
                'code_diffs': self._code_diffs,
                'tracking_lines': self._tracking_lines,
                'daily_stats': self._daily_stats
            })
    
    def calculate_all_stats(self, force: bool = False) -> Dict[str, Any]:
        """
        Calculate all stats.
        
        Args:
            force: Force recalculation even if cached
            
        Returns:
            Dictionary of all stats organized by category
        """
        # Check cache
        if not force and self.cache:
            cached_stats = self.cache.load_stats()
            if cached_stats:
                logger.info("Loaded stats from cache")
                return cached_stats
        
        # Ensure data is extracted
        if self._messages is None:
            self.extract_all_data()
        
        logger.info("Calculating stats...")
        all_stats = {}
        
        # Calculate message stats
        logger.info("  Calculating message stats...")
        message_calc = MessageCalculator(self._messages)
        all_stats['messages'] = message_calc.calculate_all()
        
        # Calculate session stats
        logger.info("  Calculating session stats...")
        session_calc = SessionCalculator(self._sessions, self._messages)
        all_stats['sessions'] = session_calc.calculate_all()
        
        # Calculate code & diffs stats
        logger.info("  Calculating code & diffs stats...")
        code_calc = CodeCalculator(self._code_diffs, self._tracking_lines)
        all_stats['code'] = code_calc.calculate_all()
        
        # Calculate daily usage stats
        logger.info("  Calculating daily usage stats...")
        daily_calc = DailyUsageCalculator(self._daily_stats)
        all_stats['daily'] = daily_calc.calculate_all()
        
        # TODO: Add more calculators here as they're built
        # token_calc = TokenCalculator(...)
        # all_stats['tokens'] = token_calc.calculate_all()
        
        # Cache results
        if self.cache:
            self.cache.save_stats(all_stats)
        
        logger.info(f"Calculated stats for {len(all_stats)} categories")
        return all_stats
    
    def get_stat(self, stat_id: str) -> Optional[Dict[str, Any]]:
        """
        Get a single stat by ID.
        
        Args:
            stat_id: The stat identifier
            
        Returns:
            Stat data or None if not found
        """
        all_stats = self.calculate_all_stats()
        
        # Search through categories
        for category, stats in all_stats.items():
            if stat_id in stats:
                return stats[stat_id]
        
        return None
    
    def invalidate_cache(self):
        """Clear cached data and stats."""
        if self.cache:
            self.cache.clear()
        self._messages = None
        self._sessions = None
        self._code_diffs = None
        self._tracking_lines = None
        self._daily_stats = None
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
            'database_path': str(self.db_path),
            'cache_enabled': self.cache is not None
        }

