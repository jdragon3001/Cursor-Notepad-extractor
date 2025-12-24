"""Extractor for message request context data."""

import logging
import json
from typing import List
from .base_extractor import BaseExtractor
from stats.models.request_context import MessageRequestContext

logger = logging.getLogger(__name__)


class MessageRequestContextExtractor(BaseExtractor):
    """
    Extracts message request context from the cursorDiskKV table.
    
    This data contains:
    - Linter errors
    - Git status
    - File context
    - TODOs
    - Cursor rules
    """
    
    def extract(self) -> List[MessageRequestContext]:
        """
        Extracts messageRequestContext entries.
        """
        logger.info("Extracting message request contexts from cursorDiskKV...")
        
        try:
            # Query for messageRequestContext entries
            query = "SELECT key, value FROM cursorDiskKV WHERE key LIKE 'messageRequestContext:%'"
            results = self._execute_query(query)
            
            if not results:
                logger.warning("No message request contexts found")
                return []
            
            # Convert to MessageRequestContext objects
            contexts = []
            errors = 0
            
            for key, value in results:
                try:
                    # Handle None values
                    if value is None:
                        errors += 1
                        continue
                    
                    # Parse JSON
                    data = json.loads(value) if isinstance(value, str) else value
                    
                    context = MessageRequestContext.from_dict(key, data)
                    contexts.append(context)
                except Exception as e:
                    errors += 1
                    if errors <= 5:  # Only log first 5 errors
                        logger.error(f"Error parsing context {key}: {e}")
            
            logger.info(f"Extracted {len(contexts)} message request contexts ({errors} errors)")
            return contexts
            
        except Exception as e:
            logger.error(f"Error extracting message request contexts: {e}")
            return []

