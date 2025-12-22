"""Base extractor class for all data extractors."""

from abc import ABC, abstractmethod
from typing import Any, List, Optional
from pathlib import Path
import sqlite3
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class BaseExtractor(ABC):
    """Base class for all data extractors."""
    
    def __init__(self, db_path: Path):
        """
        Initialize extractor.
        
        Args:
            db_path: Path to the database file
        """
        self.db_path = Path(db_path)
        self.conn: Optional[sqlite3.Connection] = None
        self.cursor: Optional[sqlite3.Cursor] = None
        
        if not self.db_path.exists():
            raise FileNotFoundError(f"Database not found: {self.db_path}")
    
    def connect(self):
        """Connect to the database."""
        try:
            self.conn = sqlite3.connect(str(self.db_path))
            self.cursor = self.conn.cursor()
            logger.info(f"Connected to database: {self.db_path.name}")
        except Exception as e:
            logger.error(f"Failed to connect to database: {e}")
            raise
    
    def disconnect(self):
        """Disconnect from the database."""
        if self.cursor:
            self.cursor.close()
        if self.conn:
            self.conn.close()
        logger.info(f"Disconnected from database: {self.db_path.name}")
    
    @abstractmethod
    def extract(self) -> List[Any]:
        """
        Extract and return data from the database.
        
        Returns:
            List of extracted data objects
        """
        pass
    
    def __enter__(self):
        """Context manager entry."""
        self.connect()
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit."""
        self.disconnect()
        return False
    
    def _execute_query(self, query: str, params: tuple = ()) -> List[tuple]:
        """
        Execute a query and return results.
        
        Args:
            query: SQL query string
            params: Query parameters
            
        Returns:
            List of result tuples
        """
        if not self.cursor:
            raise RuntimeError("Database not connected. Use context manager or call connect().")
        
        try:
            self.cursor.execute(query, params)
            return self.cursor.fetchall()
        except Exception as e:
            logger.error(f"Query failed: {e}")
            logger.error(f"Query: {query}")
            raise

