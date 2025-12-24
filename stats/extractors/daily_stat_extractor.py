"""Extractor for daily usage statistics."""

import logging
import json
from typing import List
from .base_extractor import BaseExtractor
from stats.models.daily_stat import DailyStat

logger = logging.getLogger(__name__)


class DailyStatExtractor(BaseExtractor):
    """
    Extracts daily usage statistics from the ItemTable.
    """
    
    def extract(self) -> List[DailyStat]:
        """
        Extracts aiCodeTracking.dailyStats entries from ItemTable.
        """
        logger.info("Extracting daily stats from ItemTable...")
        
        try:
            # Query ItemTable for dailyStats entries
            query = "SELECT key, value FROM ItemTable WHERE key LIKE 'aiCodeTracking.dailyStats%' ORDER BY key"
            results = self._execute_query(query)
            
            if not results:
                logger.warning("No daily stats found in ItemTable")
                return []
            
            # Convert to DailyStat objects
            daily_stats = []
            errors = 0
            
            for key, value in results:
                try:
                    # Parse JSON
                    data = json.loads(value) if isinstance(value, str) else value
                    
                    daily_stat = DailyStat.from_dict(key, data)
                    daily_stats.append(daily_stat)
                except Exception as e:
                    errors += 1
                    if errors <= 5:  # Only log first 5 errors
                        logger.error(f"Error parsing daily stat {key}: {e}")
            
            logger.info(f"Extracted {len(daily_stats)} daily stats ({errors} errors)")
            return daily_stats
            
        except Exception as e:
            logger.error(f"Error extracting daily stats: {e}")
            return []

