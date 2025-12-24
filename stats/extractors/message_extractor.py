"""Message extractor for bubbleId data."""

from typing import List
import json
import logging

from .base_extractor import BaseExtractor
from stats.models.message import Message

logger = logging.getLogger(__name__)


class MessageExtractor(BaseExtractor):
    """Extract messages (bubbleId entries) from the database."""
    
    def extract(self) -> List[Message]:
        """
        Extract all messages from cursorDiskKV table.
        
        Returns:
            List of Message objects
        """
        logger.info("Extracting messages from cursorDiskKV...")
        
        # Query all bubbleId entries
        query = "SELECT key, value FROM cursorDiskKV WHERE key LIKE 'bubbleId:%'"
        rows = self._execute_query(query)
        
        messages = []
        errors = 0
        
        for key, value in rows:
            try:
                # Parse JSON value
                if isinstance(value, bytes):
                    data = json.loads(value.decode('utf-8'))
                elif isinstance(value, str):
                    data = json.loads(value)
                else:
                    logger.warning(f"Unexpected value type for {key}: {type(value)}")
                    continue
                
                # Create Message object
                message = Message.from_dict(key, data)
                messages.append(message)
                
            except json.JSONDecodeError as e:
                logger.error(f"JSON decode error for {key}: {e}")
                errors += 1
            except Exception as e:
                logger.error(f"Error parsing message {key}: {e}")
                errors += 1
        
        logger.info(f"Extracted {len(messages)} messages ({errors} errors)")
        return messages
    
    def extract_by_session(self, composer_id: str) -> List[Message]:
        """
        Extract messages for a specific session.
        
        Args:
            composer_id: The session/composer ID
            
        Returns:
            List of Message objects for that session
        """
        logger.info(f"Extracting messages for session {composer_id}...")
        
        # Query bubbleId entries for specific composer
        query = "SELECT key, value FROM cursorDiskKV WHERE key LIKE ?"
        pattern = f"bubbleId:{composer_id}:%"
        rows = self._execute_query(query, (pattern,))
        
        messages = []
        errors = 0
        
        for key, value in rows:
            try:
                if isinstance(value, bytes):
                    data = json.loads(value.decode('utf-8'))
                elif isinstance(value, str):
                    data = json.loads(value)
                else:
                    continue
                
                message = Message.from_dict(key, data)
                messages.append(message)
                
            except Exception as e:
                logger.error(f"Error parsing message {key}: {e}")
                errors += 1
        
        logger.info(f"Extracted {len(messages)} messages for session ({errors} errors)")
        return messages
    
    def extract_date_range(self, start_date, end_date) -> List[Message]:
        """
        Extract messages within a date range.
        
        Args:
            start_date: Start datetime
            end_date: End datetime
            
        Returns:
            List of Message objects in date range
        """
        # Extract all messages first
        all_messages = self.extract()
        
        # Filter by date
        filtered = [
            msg for msg in all_messages
            if start_date <= msg.created_at <= end_date
        ]
        
        logger.info(f"Filtered to {len(filtered)} messages in date range")
        return filtered
    
    def extract_user_messages(self) -> List[Message]:
        """
        Extract only user messages.
        
        Returns:
            List of user Message objects
        """
        all_messages = self.extract()
        user_messages = [msg for msg in all_messages if msg.is_user_message]
        
        logger.info(f"Filtered to {len(user_messages)} user messages")
        return user_messages
    
    def extract_ai_messages(self) -> List[Message]:
        """
        Extract only AI messages.
        
        Returns:
            List of AI Message objects
        """
        all_messages = self.extract()
        ai_messages = [msg for msg in all_messages if msg.is_ai_message]
        
        logger.info(f"Filtered to {len(ai_messages)} AI messages")
        return ai_messages

