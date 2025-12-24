"""Session extractor for composerData."""

from typing import List
import json
import logging

from .base_extractor import BaseExtractor
from stats.models.session import Session

logger = logging.getLogger(__name__)


class SessionExtractor(BaseExtractor):
    """Extract sessions (composerData entries) from the database."""
    
    def extract(self) -> List[Session]:
        """
        Extract all sessions from cursorDiskKV table.
        
        Returns:
            List of Session objects
        """
        logger.info("Extracting sessions from cursorDiskKV...")
        
        # Query all composerData entries
        query = "SELECT key, value FROM cursorDiskKV WHERE key LIKE 'composerData:%'"
        rows = self._execute_query(query)
        
        sessions = []
        errors = 0
        
        for key, value in rows:
            try:
                # Skip None values
                if value is None:
                    continue
                    
                # Parse JSON value
                if isinstance(value, bytes):
                    data = json.loads(value.decode('utf-8'))
                elif isinstance(value, str):
                    data = json.loads(value)
                else:
                    logger.warning(f"Unexpected value type for {key}: {type(value)}")
                    continue
                
                # Create Session object
                session = Session.from_dict(key, data)
                sessions.append(session)
                
            except json.JSONDecodeError as e:
                logger.error(f"JSON decode error for {key}: {e}")
                errors += 1
            except Exception as e:
                logger.error(f"Error parsing session {key}: {e}")
                errors += 1
        
        logger.info(f"Extracted {len(sessions)} sessions ({errors} errors)")
        return sessions
    
    def extract_date_range(self, start_date, end_date) -> List[Session]:
        """
        Extract sessions within a date range.
        
        Args:
            start_date: Start datetime
            end_date: End datetime
            
        Returns:
            List of Session objects in date range
        """
        # Extract all sessions first
        all_sessions = self.extract()
        
        # Filter by date
        filtered = [
            session for session in all_sessions
            if start_date <= session.created_at <= end_date
        ]
        
        logger.info(f"Filtered to {len(filtered)} sessions in date range")
        return filtered
    
    def extract_agentic_sessions(self) -> List[Session]:
        """
        Extract only agentic (agent mode) sessions.
        
        Returns:
            List of agentic Session objects
        """
        all_sessions = self.extract()
        agentic = [s for s in all_sessions if s.is_agentic]
        
        logger.info(f"Filtered to {len(agentic)} agentic sessions")
        return agentic
    
    def extract_archived_sessions(self) -> List[Session]:
        """
        Extract only archived sessions.
        
        Returns:
            List of archived Session objects
        """
        all_sessions = self.extract()
        archived = [s for s in all_sessions if s.is_archived]
        
        logger.info(f"Filtered to {len(archived)} archived sessions")
        return archived
    
    def extract_sessions_with_code_changes(self) -> List[Session]:
        """
        Extract sessions that have code changes.
        
        Returns:
            List of Session objects with code changes
        """
        all_sessions = self.extract()
        with_changes = [s for s in all_sessions if s.has_code_changes]
        
        logger.info(f"Filtered to {len(with_changes)} sessions with code changes")
        return with_changes

