"""Extractor for code tracking lines data."""

import logging
import json
from typing import List
from .base_extractor import BaseExtractor
from stats.models.code_diff import CodeTrackingLine

logger = logging.getLogger(__name__)


class CodeTrackingExtractor(BaseExtractor):
    """
    Extracts code tracking lines from the ItemTable.
    """
    
    def extract(self) -> List[CodeTrackingLine]:
        """
        Extracts aiCodeTrackingLines from ItemTable.
        """
        logger.info("Extracting code tracking lines from ItemTable...")
        
        try:
            # Query ItemTable for aiCodeTrackingLines
            query = "SELECT value FROM ItemTable WHERE key = 'aiCodeTrackingLines'"
            results = self._execute_query(query)
            
            if not results or not results[0] or not results[0][0]:
                logger.warning("No aiCodeTrackingLines found in ItemTable")
                return []
            
            # Parse the JSON data
            data = json.loads(results[0][0])
            
            if not isinstance(data, list):
                logger.error(f"aiCodeTrackingLines is not a list: {type(data)}")
                return []
            
            # Convert to CodeTrackingLine objects
            tracking_lines = []
            errors = 0
            
            for item in data:
                try:
                    tracking_line = CodeTrackingLine.from_dict(item)
                    tracking_lines.append(tracking_line)
                except Exception as e:
                    errors += 1
                    if errors <= 5:  # Only log first 5 errors
                        logger.error(f"Error parsing tracking line: {e}")
            
            logger.info(f"Extracted {len(tracking_lines)} code tracking lines ({errors} errors)")
            return tracking_lines
            
        except Exception as e:
            logger.error(f"Error extracting code tracking lines: {e}")
            return []

