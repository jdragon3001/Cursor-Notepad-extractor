"""Workspace data model."""

from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional
from pathlib import Path


@dataclass
class Workspace:
    """
    Represents a workspace with its database and metadata.
    """
    
    # ==================== REQUIRED FIELDS ====================
    
    workspace_id: str
    """Unique workspace identifier (hash)"""
    
    db_path: Path
    """Path to workspace database"""
    
    size_bytes: int
    """Database file size in bytes"""
    
    # ==================== EXTRACTED DATA ====================
    
    has_composer_data: bool = False
    """Whether workspace has composer data"""
    
    composer_count: int = 0
    """Number of composer-related keys"""
    
    has_notepad_data: bool = False
    """Whether workspace has notepad data"""
    
    notepad_count: int = 0
    """Number of notepad-related keys"""
    
    total_keys: int = 0
    """Total keys in ItemTable"""
    
    # ==================== COMPOSER DATA ====================
    
    composer_data: Optional[Dict[str, Any]] = None
    """Extracted composer data if available"""
    
    # ==================== META ====================
    
    extraction_error: Optional[str] = None
    """Error message if extraction failed"""
    
    # ==================== COMPUTED PROPERTIES ====================
    
    @property
    def size_mb(self) -> float:
        """Size in megabytes."""
        return self.size_bytes / (1024 * 1024)
    
    @property
    def has_data(self) -> bool:
        """Whether workspace has meaningful data."""
        return self.has_composer_data or self.has_notepad_data
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for serialization."""
        return {
            'workspace_id': self.workspace_id,
            'db_path': str(self.db_path),
            'size_mb': self.size_mb,
            'has_composer_data': self.has_composer_data,
            'composer_count': self.composer_count,
            'has_notepad_data': self.has_notepad_data,
            'notepad_count': self.notepad_count,
            'total_keys': self.total_keys,
            'has_data': self.has_data,
        }

