"""
Cursor database handling module.

This module provides functionality to connect to and extract data from Cursor workspace databases.
"""

import sqlite3
import json
import logging
from pathlib import Path
from typing import Optional, List, Dict, Any, Tuple, Union

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class CursorDatabase:
    """Handler for Cursor workspace SQLite databases."""
    
    def __init__(self, db_path: Path):
        """
        Initialize database handler.
        
        Args:
            db_path: Path to the SQLite database file.
        """
        self.db_path = db_path
        self.connection: Optional[sqlite3.Connection] = None
        
    def connect(self) -> bool:
        """
        Connect to the database.
        
        Returns:
            True if connection successful, False otherwise.
        """
        try:
            self.connection = sqlite3.connect(str(self.db_path))
            self.connection.row_factory = sqlite3.Row  # Enable dict-like access
            return True
        except sqlite3.Error as e:
            logger.error(f"Error connecting to database {self.db_path}: {e}")
            return False
    
    def disconnect(self):
        """Close the database connection."""
        if self.connection:
            self.connection.close()
            self.connection = None
    
    def __enter__(self):
        """Context manager entry."""
        if self.connect():
            return self
        else:
            raise sqlite3.Error(f"Failed to connect to database: {self.db_path}")
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit."""
        self.disconnect()
    
    def get_tables(self) -> List[str]:
        """
        Get list of tables in the database.
        
        Returns:
            List of table names.
        """
        if not self.connection:
            return []
            
        try:
            cursor = self.connection.cursor()
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
            tables = [row[0] for row in cursor.fetchall()]
            return tables
        except sqlite3.Error as e:
            logger.error(f"Error getting tables: {e}")
            return []
    
    def get_table_info(self, table_name: str) -> List[Dict[str, Any]]:
        """
        Get information about table columns.
        
        Args:
            table_name: Name of the table.
            
        Returns:
            List of column information dictionaries.
        """
        if not self.connection:
            return []
            
        try:
            cursor = self.connection.cursor()
            cursor.execute(f"PRAGMA table_info({table_name})")
            columns = []
            for row in cursor.fetchall():
                columns.append({
                    'cid': row[0],
                    'name': row[1],
                    'type': row[2],
                    'notnull': row[3],
                    'dflt_value': row[4],
                    'pk': row[5]
                })
            return columns
        except sqlite3.Error as e:
            logger.error(f"Error getting table info for {table_name}: {e}")
            return []
    
    def get_all_keys(self, table_name: str = "ItemTable") -> List[str]:
        """
        Get all keys from a table.
        
        Args:
            table_name: Name of the table to query.
            
        Returns:
            List of keys.
        """
        if not self.connection:
            return []
            
        try:
            cursor = self.connection.cursor()
            cursor.execute(f"SELECT key FROM {table_name}")
            keys = [row[0] for row in cursor.fetchall()]
            return keys
        except sqlite3.Error as e:
            logger.error(f"Error getting keys from {table_name}: {e}")
            return []
    
    def get_value_by_key(self, key: str, table: str = None) -> Optional[bytes]:
        """Get value for a specific key."""
        if not self.connection:
            return None
        
        try:
            # Try all tables if none specified
            tables_to_search = [table] if table else self.get_tables()
            
            for search_table in tables_to_search:
                # Use parameterized query to avoid SQL injection and syntax errors
                cursor = self.connection.cursor()
                cursor.execute(f"SELECT value FROM {search_table} WHERE key = ?", (key,))
                result = cursor.fetchone()
                
                if result:
                    return result[0]
            
            return None
            
        except Exception as e:
            logger.error(f"Error getting value for key {key}: {e}")
            return None
    
    def get_all_data(self, table_name: str = "ItemTable", limit: Optional[int] = None) -> List[Tuple[str, Union[bytes, str]]]:
        """
        Get all key-value pairs from a table.
        
        Args:
            table_name: Name of the table to query.
            limit: Maximum number of rows to return.
            
        Returns:
            List of (key, value) tuples.
        """
        if not self.connection:
            return []
            
        try:
            cursor = self.connection.cursor()
            query = f"SELECT key, value FROM {table_name}"
            if limit:
                query += f" LIMIT {limit}"
                
            cursor.execute(query)
            return cursor.fetchall()
        except sqlite3.Error as e:
            logger.error(f"Error getting all data from {table_name}: {e}")
            return []
    
    def search_keys(self, pattern: str, table: str = None) -> List[str]:
        """Search for keys matching a pattern."""
        if not self.connection:
            return []
        
        try:
            # Try all tables if none specified
            tables_to_search = [table] if table else self.get_tables()
            matching_keys = []
            
            for search_table in tables_to_search:
                # Use parameterized query for pattern matching
                cursor = self.connection.cursor()
                cursor.execute(f"SELECT key FROM {search_table} WHERE key LIKE ?", (pattern,))
                results = cursor.fetchall()
                
                for result in results:
                    matching_keys.append(result[0])
            
            return matching_keys
            
        except Exception as e:
            logger.error(f"Error searching keys with pattern {pattern}: {e}")
            return []
    
    def get_debug_info(self) -> str:
        """Get detailed debug information about the database."""
        if not self.connection:
            return "No database connection"
        
        debug_info = []
        debug_info.append(f"Database: {self.db_path}")
        debug_info.append(f"File size: {self.db_path.stat().st_size:,} bytes")
        
        try:
            # Get all tables
            tables = self.get_tables()
            debug_info.append(f"Tables found: {len(tables)}")
            
            for table in tables:
                debug_info.append(f"\n[TABLE] {table}")
                
                # Get table schema
                cursor = self.connection.cursor()
                cursor.execute(f"PRAGMA table_info({table})")
                schema = cursor.fetchall()
                debug_info.append(f"  Columns: {[col[1] for col in schema]}")
                
                # Get row count
                cursor.execute(f"SELECT COUNT(*) FROM {table}")
                count = cursor.fetchone()[0]
                debug_info.append(f"  Rows: {count}")
                
                # Get sample keys (first 10)
                cursor.execute(f"SELECT key, LENGTH(value) as value_size FROM {table} ORDER BY value_size DESC LIMIT 10")
                samples = cursor.fetchall()
                
                debug_info.append("  Sample entries (largest first):")
                for key, size in samples:
                    debug_info.append(f"    {key[:50]}{'...' if len(key) > 50 else ''} ({size} bytes)")
                
                # Look for interesting patterns
                cursor.execute(f"SELECT key FROM {table} WHERE key LIKE '%note%' OR key LIKE '%text%' OR key LIKE '%draft%' LIMIT 5")
                interesting = cursor.fetchall()
                if interesting:
                    debug_info.append("  Potentially interesting keys:")
                    for (key,) in interesting:
                        debug_info.append(f"    {key}")
        
        except Exception as e:
            debug_info.append(f"Error getting debug info: {e}")
        
        return "\n".join(debug_info)

class DataDecoder:
    """Utility class for decoding BLOB data from Cursor databases."""
    
    @staticmethod
    def try_decode_as_text(data: Union[bytes, str]) -> Optional[str]:
        """
        Try to decode data as text using various encodings.
        
        Args:
            data: Data to decode (bytes or string).
            
        Returns:
            Decoded string or None if decoding fails.
        """
        # If already a string, return it
        if isinstance(data, str):
            return data
            
        # If bytes, try various encodings
        if isinstance(data, bytes):
            encodings = ['utf-8', 'utf-16', 'latin1', 'cp1252']
            
            for encoding in encodings:
                try:
                    return data.decode(encoding)
                except (UnicodeDecodeError, UnicodeError):
                    continue
        
        return None
    
    @staticmethod
    def try_decode_as_json(data: Union[bytes, str]) -> Optional[Dict[str, Any]]:
        """
        Try to decode data as JSON.
        
        Args:
            data: Data to decode (bytes or string).
            
        Returns:
            Parsed JSON object or None if decoding fails.
        """
        text = DataDecoder.try_decode_as_text(data)
        if not text:
            return None
            
        try:
            return json.loads(text)
        except (json.JSONDecodeError, ValueError):
            return None
    
    @staticmethod
    def analyze_data(data: Union[bytes, str]) -> Dict[str, Any]:
        """
        Analyze data and provide information about potential content.
        
        Args:
            data: Data to analyze (bytes or string).
            
        Returns:
            Dictionary with analysis results.
        """
        analysis = {
            'size': len(data) if data else 0,
            'type': type(data).__name__,
            'is_text': False,
            'is_json': False,
            'preview': None,
            'json_data': None
        }
        
        if not data:
            return analysis
        
        # Try to decode as text
        text = DataDecoder.try_decode_as_text(data)
        if text:
            analysis['is_text'] = True
            analysis['preview'] = text[:200] + "..." if len(text) > 200 else text
            
            # Try to parse as JSON
            json_data = DataDecoder.try_decode_as_json(data)
            if json_data:
                analysis['is_json'] = True
                analysis['json_data'] = json_data
        
        return analysis 