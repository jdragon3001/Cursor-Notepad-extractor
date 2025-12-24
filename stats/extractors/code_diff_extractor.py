"""Extractor for code diff data."""

import logging
import json
from typing import List

from .base_extractor import BaseExtractor
from stats.models.code_diff import CodeDiff

logger = logging.getLogger(__name__)


class CodeDiffExtractor(BaseExtractor):
    """
    Extracts code diff data from the cursorDiskKV table.
    """
    def extract(self) -> List[CodeDiff]:
        """
        Extracts raw code diff data and transforms it into CodeDiff objects.
        """
        logger.info("Extracting code diffs from cursorDiskKV...")
        
        # Query for codeBlockDiff entries
        query = "SELECT key, value FROM cursorDiskKV WHERE key LIKE 'codeBlockDiff:%'"
        raw_results = self._execute_query(query)
        
        diffs = []
        errors = 0
        for key, value in raw_results:
            try:
                # Handle cases where value might be None or empty
                if value is None:
                    logger.warning(f"Unexpected value type for {key}: {type(value)}")
                    errors += 1
                    continue
                
                # Parse JSON
                diff_data = json.loads(value) if isinstance(value, str) else value
                
                diff = CodeDiff.from_dict(key, diff_data)
                diffs.append(diff)
            except Exception as e:
                errors += 1
                if errors <= 5:  # Only log first 5 errors
                    logger.error(f"Error parsing code diff {key}: {e}")
        
        logger.info(f"Extracted {len(diffs)} code diffs ({errors} errors)")
        return diffs

