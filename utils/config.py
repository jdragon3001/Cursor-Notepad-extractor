"""
Configuration management for Cursor Notepad Extractor.

This module handles application settings, default paths, and user preferences.
"""

import os
from pathlib import Path
from typing import Optional

class Config:
    """Application configuration management."""
    
    # Dynamic workspace storage path - works on any Windows user account
    @classmethod
    def get_default_workspace_path(cls) -> str:
        """Get the default Cursor workspace path for the current user."""
        # Use expanduser to get the current user's home directory
        user_home = Path.home()
        # Standard Cursor workspace path relative to user directory
        workspace_path = user_home / "AppData" / "Roaming" / "Cursor" / "User" / "workspaceStorage"
        return str(workspace_path)
    
    # Application settings
    APP_NAME = "Cursor Notepad Extractor"
    APP_VERSION = "1.0.0"
    
    # Database settings
    DB_FILENAME = "state.vscdb"
    
    # UI settings
    WINDOW_WIDTH = 1200
    WINDOW_HEIGHT = 800
    WINDOW_MIN_WIDTH = 800
    WINDOW_MIN_HEIGHT = 600
    
    @classmethod
    def get_workspace_path(cls) -> str:
        """Get the workspace storage path."""
        return cls.get_default_workspace_path()
    
    @classmethod
    def validate_workspace_path(cls, path: Optional[str] = None) -> bool:
        """
        Validate if the workspace path exists and is accessible.
        
        Args:
            path: Path to validate. If None, uses default path.
            
        Returns:
            True if path is valid and accessible, False otherwise.
        """
        if path is None:
            path = cls.get_workspace_path()
            
        try:
            workspace_path = Path(path)
            return workspace_path.exists() and workspace_path.is_dir()
        except (OSError, ValueError):
            return False
    
    @classmethod
    def get_database_files(cls, workspace_path: Optional[str] = None) -> list[Path]:
        """
        Get list of database files in the workspace path.
        
        Args:
            workspace_path: Path to search. If None, uses default path.
            
        Returns:
            List of Path objects pointing to database files.
        """
        if workspace_path is None:
            workspace_path = cls.get_workspace_path()
            
        database_files = []
        
        try:
            workspace_dir = Path(workspace_path)
            if not workspace_dir.exists():
                return database_files
                
            # Search for state.vscdb files in subdirectories
            for subdir in workspace_dir.iterdir():
                if subdir.is_dir():
                    db_file = subdir / cls.DB_FILENAME
                    if db_file.exists() and db_file.is_file():
                        database_files.append(db_file)
                        
        except (OSError, ValueError):
            pass
            
        return sorted(database_files)
    
    @classmethod
    def get_workspace_info(cls, workspace_path: Optional[str] = None) -> dict:
        """
        Get information about the workspace.
        
        Args:
            workspace_path: Path to analyze. If None, uses default path.
            
        Returns:
            Dictionary with workspace information.
        """
        if workspace_path is None:
            workspace_path = cls.get_workspace_path()
            
        info = {
            "path": workspace_path,
            "exists": False,
            "accessible": False,
            "database_count": 0,
            "subdirectories": []
        }
        
        try:
            workspace_dir = Path(workspace_path)
            info["exists"] = workspace_dir.exists()
            
            if info["exists"]:
                info["accessible"] = True
                database_files = cls.get_database_files(workspace_path)
                info["database_count"] = len(database_files)
                
                # Get subdirectory names
                subdirs = [d.name for d in workspace_dir.iterdir() if d.is_dir()]
                info["subdirectories"] = sorted(subdirs)
                
        except (OSError, ValueError, PermissionError):
            info["accessible"] = False
            
        return info 