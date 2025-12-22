"""Workspace extractor for scanning all workspace databases."""

import logging
import sqlite3
import json
from typing import List
from pathlib import Path

from stats.models.workspace import Workspace

logger = logging.getLogger(__name__)


class WorkspaceExtractor:
    """
    Extracts metadata and data from all workspace databases.
    
    Does NOT inherit from BaseExtractor since it scans multiple databases.
    """
    
    def __init__(self, workspace_storage_path: Path = None):
        """
        Initialize workspace extractor.
        
        Args:
            workspace_storage_path: Path to workspaceStorage directory.
                                   If None, uses default Cursor location.
        """
        if workspace_storage_path is None:
            workspace_storage_path = (
                Path.home() / "AppData" / "Roaming" / "Cursor" / 
                "User" / "workspaceStorage"
            )
        
        self.workspace_storage_path = Path(workspace_storage_path)
        
        if not self.workspace_storage_path.exists():
            raise FileNotFoundError(
                f"Workspace storage not found: {self.workspace_storage_path}"
            )
    
    def extract(self) -> List[Workspace]:
        """
        Extract metadata from all workspace databases.
        
        Returns:
            List of Workspace objects
        """
        logger.info(f"Scanning workspace databases in {self.workspace_storage_path}...")
        
        # Find all workspace directories
        workspace_dirs = [d for d in self.workspace_storage_path.glob("*/") if d.is_dir()]
        logger.info(f"Found {len(workspace_dirs)} workspace directories")
        
        workspaces = []
        errors = 0
        
        for ws_dir in workspace_dirs:
            try:
                workspace = self._extract_workspace(ws_dir)
                if workspace:
                    workspaces.append(workspace)
            except Exception as e:
                errors += 1
                if errors <= 5:
                    logger.error(f"Error extracting workspace {ws_dir.name}: {e}")
        
        logger.info(f"Extracted {len(workspaces)} workspaces ({errors} errors)")
        return workspaces
    
    def _extract_workspace(self, ws_dir: Path) -> Workspace:
        """Extract data from a single workspace directory."""
        workspace_id = ws_dir.name
        db_path = ws_dir / "state.vscdb"
        
        # Check if database exists
        if not db_path.exists():
            return None
        
        size_bytes = db_path.stat().st_size
        
        # Create workspace object
        workspace = Workspace(
            workspace_id=workspace_id,
            db_path=db_path,
            size_bytes=size_bytes
        )
        
        # Try to extract metadata
        try:
            conn = sqlite3.connect(str(db_path))
            cursor = conn.cursor()
            
            # Check if ItemTable exists
            cursor.execute(
                "SELECT name FROM sqlite_master WHERE type='table' AND name='ItemTable'"
            )
            if not cursor.fetchone():
                conn.close()
                return workspace
            
            # Count total keys
            cursor.execute("SELECT COUNT(*) FROM ItemTable")
            workspace.total_keys = cursor.fetchone()[0]
            
            # Count composer keys
            cursor.execute("SELECT COUNT(*) FROM ItemTable WHERE key LIKE '%composer%'")
            workspace.composer_count = cursor.fetchone()[0]
            workspace.has_composer_data = workspace.composer_count > 0
            
            # Count notepad keys
            cursor.execute("SELECT COUNT(*) FROM ItemTable WHERE key LIKE '%notepad%'")
            workspace.notepad_count = cursor.fetchone()[0]
            workspace.has_notepad_data = workspace.notepad_count > 0
            
            # Try to extract actual composer data
            cursor.execute(
                "SELECT key, value FROM ItemTable WHERE key = 'composer.composerData' LIMIT 1"
            )
            result = cursor.fetchone()
            if result:
                key, value = result
                try:
                    workspace.composer_data = json.loads(value)
                except:
                    pass
            
            conn.close()
            
        except Exception as e:
            workspace.extraction_error = str(e)
            logger.warning(f"Error extracting metadata for {workspace_id}: {e}")
        
        return workspace

