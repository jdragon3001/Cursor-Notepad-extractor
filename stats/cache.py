"""Simple cache system for extracted data and calculated stats."""

from pathlib import Path
import pickle
import json
from datetime import datetime, timedelta
from typing import Any, Dict, Optional
import logging

logger = logging.getLogger(__name__)


class StatsCache:
    """Manage caching of extracted data and calculated stats."""
    
    def __init__(self, cache_dir: Path):
        """
        Initialize cache.
        
        Args:
            cache_dir: Directory to store cache files
        """
        self.cache_dir = Path(cache_dir)
        self.cache_dir.mkdir(parents=True, exist_ok=True)
        
        self.data_cache_file = self.cache_dir / "extracted_data.pkl"
        self.stats_cache_file = self.cache_dir / "calculated_stats.pkl"
        self.metadata_file = self.cache_dir / "cache_metadata.json"
    
    def save_extracted_data(self, data: Dict[str, Any]):
        """
        Save extracted data to cache.
        
        Args:
            data: Dictionary of extracted data
        """
        try:
            with open(self.data_cache_file, 'wb') as f:
                pickle.dump(data, f)
            
            self._update_metadata('data')
            logger.info("Saved extracted data to cache")
        except Exception as e:
            logger.error(f"Failed to save extracted data: {e}")
    
    def load_extracted_data(self) -> Optional[Dict[str, Any]]:
        """
        Load extracted data from cache.
        
        Returns:
            Cached data or None if not available/stale
        """
        if not self.data_cache_file.exists():
            logger.info("No cached data found")
            return None
        
        # Check if cache is stale (> 1 hour old)
        if self._is_stale('data', hours=1):
            logger.info("Cached data is stale")
            return None
        
        try:
            with open(self.data_cache_file, 'rb') as f:
                data = pickle.load(f)
            logger.info("Loaded extracted data from cache")
            return data
        except Exception as e:
            logger.error(f"Failed to load extracted data: {e}")
            return None
    
    def save_stats(self, stats: Dict[str, Any]):
        """
        Save calculated stats to cache.
        
        Args:
            stats: Dictionary of calculated stats
        """
        try:
            with open(self.stats_cache_file, 'wb') as f:
                pickle.dump(stats, f)
            
            self._update_metadata('stats')
            logger.info("Saved calculated stats to cache")
        except Exception as e:
            logger.error(f"Failed to save stats: {e}")
    
    def load_stats(self) -> Optional[Dict[str, Any]]:
        """
        Load calculated stats from cache.
        
        Returns:
            Cached stats or None if not available/stale
        """
        if not self.stats_cache_file.exists():
            logger.info("No cached stats found")
            return None
        
        # Check if cache is stale (> 5 minutes old)
        if self._is_stale('stats', minutes=5):
            logger.info("Cached stats are stale")
            return None
        
        try:
            with open(self.stats_cache_file, 'rb') as f:
                stats = pickle.load(f)
            logger.info("Loaded calculated stats from cache")
            return stats
        except Exception as e:
            logger.error(f"Failed to load stats: {e}")
            return None
    
    def clear(self):
        """Clear all cached data."""
        try:
            if self.data_cache_file.exists():
                self.data_cache_file.unlink()
            if self.stats_cache_file.exists():
                self.stats_cache_file.unlink()
            if self.metadata_file.exists():
                self.metadata_file.unlink()
            logger.info("Cleared all cache")
        except Exception as e:
            logger.error(f"Failed to clear cache: {e}")
    
    def _update_metadata(self, cache_type: str):
        """Update cache metadata."""
        try:
            metadata = {}
            if self.metadata_file.exists():
                with open(self.metadata_file, 'r') as f:
                    metadata = json.load(f)
            
            metadata[cache_type] = {
                'timestamp': datetime.now().isoformat(),
                'size': self._get_cache_size(cache_type)
            }
            
            with open(self.metadata_file, 'w') as f:
                json.dump(metadata, f, indent=2)
        except Exception as e:
            logger.error(f"Failed to update metadata: {e}")
    
    def _is_stale(self, cache_type: str, hours: int = 0, minutes: int = 0) -> bool:
        """Check if cache is stale."""
        try:
            if not self.metadata_file.exists():
                return True
            
            with open(self.metadata_file, 'r') as f:
                metadata = json.load(f)
            
            if cache_type not in metadata:
                return True
            
            timestamp = datetime.fromisoformat(metadata[cache_type]['timestamp'])
            age = datetime.now() - timestamp
            max_age = timedelta(hours=hours, minutes=minutes)
            
            return age > max_age
        except Exception as e:
            logger.error(f"Error checking cache staleness: {e}")
            return True
    
    def _get_cache_size(self, cache_type: str) -> int:
        """Get cache file size in bytes."""
        cache_file = self.data_cache_file if cache_type == 'data' else self.stats_cache_file
        return cache_file.stat().st_size if cache_file.exists() else 0

