"""Session data model representing a composerData entry."""

from dataclasses import dataclass, field
from typing import Optional, List, Dict, Any
from datetime import datetime


@dataclass
class Session:
    """Represents a chat session (composerData entry) from Cursor."""
    
    # ==================== REQUIRED FIELDS ====================
    
    composer_id: str
    """Unique session ID"""
    
    created_at: datetime
    """When the session was created"""
    
    last_updated_at: datetime
    """When the session was last updated"""
    
    # ==================== SESSION INFO ====================
    
    name: Optional[str] = None
    """Session name/title"""
    
    text: Optional[str] = None
    """Current input text"""
    
    status: str = 'idle'
    """Session status (idle, processing, etc.)"""
    
    is_archived: bool = False
    """Whether session is archived"""
    
    has_unread_messages: bool = False
    """Whether session has unread messages"""
    
    # ==================== TOKEN USAGE ====================
    
    context_tokens_used: int = 0
    """Number of context tokens used"""
    
    context_token_limit: int = 128000
    """Context token limit"""
    
    context_usage_percent: float = 0.0
    """Percentage of context used"""
    
    # ==================== CODE METRICS ====================
    
    total_lines_added: int = 0
    """Total lines of code added in this session"""
    
    total_lines_removed: int = 0
    """Total lines of code removed in this session"""
    
    added_files: List[str] = field(default_factory=list)
    """List of files added in this session"""
    
    removed_files: List[str] = field(default_factory=list)
    """List of files removed in this session"""
    
    # ==================== MODE FIELDS ====================
    
    is_agentic: bool = False
    """Whether session is in agent mode"""
    
    capabilities: List[str] = field(default_factory=list)
    """Available capabilities (codebase, web, terminal, etc.)"""
    
    # ==================== MODEL CONFIG ====================
    
    model_config: Optional[Dict[str, Any]] = None
    """Model configuration"""
    
    # ==================== USAGE DATA ====================
    
    usage_data: Optional[Dict[str, Any]] = None
    """Usage/billing data"""
    
    # ==================== META FIELDS ====================
    
    version: int = 10
    """Schema version"""
    
    raw_data: Optional[Dict[str, Any]] = None
    """Raw JSON data for future-proofing"""
    
    # ==================== CLASS METHODS ====================
    
    @classmethod
    def from_dict(cls, key: str, data: Dict[str, Any]) -> 'Session':
        """
        Create Session from dictionary (JSON data).
        
        Args:
            key: The composerData key (format: "composerData:{uuid}")
            data: The JSON data
            
        Returns:
            Session object
        """
        # Parse key to extract ID
        parts = key.split(':')
        composer_id = parts[1] if len(parts) > 1 else data.get('composerId', '')
        
        # Parse timestamps - handle both ISO string and numeric formats
        created_at_raw = data.get('createdAt', None)
        created_at = None
        
        if created_at_raw:
            if isinstance(created_at_raw, str):
                try:
                    created_at = datetime.fromisoformat(created_at_raw.replace('Z', '+00:00'))
                    created_at = created_at.replace(tzinfo=None)
                except (ValueError, TypeError):
                    try:
                        created_at = datetime.fromtimestamp(int(created_at_raw) / 1000)
                    except (ValueError, TypeError):
                        pass
            elif isinstance(created_at_raw, (int, float)):
                try:
                    created_at = datetime.fromtimestamp(created_at_raw / 1000)
                except (ValueError, TypeError, OSError):
                    pass
        
        if created_at is None:
            created_at = datetime.now()
        
        # Parse lastUpdatedAt similarly
        last_updated_raw = data.get('lastUpdatedAt', None)
        last_updated_at = None
        
        if last_updated_raw:
            if isinstance(last_updated_raw, str):
                try:
                    last_updated_at = datetime.fromisoformat(last_updated_raw.replace('Z', '+00:00'))
                    last_updated_at = last_updated_at.replace(tzinfo=None)
                except (ValueError, TypeError):
                    try:
                        last_updated_at = datetime.fromtimestamp(int(last_updated_raw) / 1000)
                    except (ValueError, TypeError):
                        pass
            elif isinstance(last_updated_raw, (int, float)):
                try:
                    last_updated_at = datetime.fromtimestamp(last_updated_raw / 1000)
                except (ValueError, TypeError, OSError):
                    pass
        
        if last_updated_at is None:
            last_updated_at = created_at
        
        return cls(
            composer_id=composer_id,
            created_at=created_at,
            last_updated_at=last_updated_at,
            name=data.get('name'),
            text=data.get('text'),
            status=data.get('status', 'idle'),
            is_archived=data.get('isArchived', False),
            has_unread_messages=data.get('hasUnreadMessages', False),
            context_tokens_used=data.get('contextTokensUsed', 0),
            context_token_limit=data.get('contextTokenLimit', 128000),
            context_usage_percent=data.get('contextUsagePercent', 0.0),
            total_lines_added=data.get('totalLinesAdded', 0),
            total_lines_removed=data.get('totalLinesRemoved', 0),
            added_files=data.get('addedFiles', []) if isinstance(data.get('addedFiles'), list) else [],
            removed_files=data.get('removedFiles', []) if isinstance(data.get('removedFiles'), list) else [],
            is_agentic=data.get('isAgentic', False),
            capabilities=data.get('capabilities', []),
            model_config=data.get('modelConfig'),
            usage_data=data.get('usageData'),
            version=data.get('_v', 10),
            raw_data=data
        )
    
    # ==================== HELPER PROPERTIES ====================
    
    @property
    def has_name(self) -> bool:
        """Check if session has a name."""
        return self.name is not None and len(self.name.strip()) > 0
    
    @property
    def has_code_changes(self) -> bool:
        """Check if session has code changes."""
        return self.total_lines_added > 0 or self.total_lines_removed > 0
    
    @property
    def has_file_changes(self) -> bool:
        """Check if session has file changes."""
        return len(self.added_files) > 0 or len(self.removed_files) > 0
    
    @property
    def net_lines_changed(self) -> int:
        """Get net lines changed (added - removed)."""
        return self.total_lines_added - self.total_lines_removed
    
    @property
    def total_lines_changed(self) -> int:
        """Get total lines changed (added + removed)."""
        return self.total_lines_added + self.total_lines_removed
    
    @property
    def duration_seconds(self) -> float:
        """Get session duration in seconds."""
        return (self.last_updated_at - self.created_at).total_seconds()
    
    @property
    def duration_minutes(self) -> float:
        """Get session duration in minutes."""
        return self.duration_seconds / 60
    
    @property
    def duration_hours(self) -> float:
        """Get session duration in hours."""
        return self.duration_seconds / 3600
    
    @property
    def is_long_session(self) -> bool:
        """Check if session is longer than 1 hour."""
        return self.duration_hours > 1.0
    
    @property
    def context_usage_level(self) -> str:
        """Get context usage level (low, medium, high, very high)."""
        if self.context_usage_percent < 25:
            return 'low'
        elif self.context_usage_percent < 50:
            return 'medium'
        elif self.context_usage_percent < 75:
            return 'high'
        else:
            return 'very high'
    
    # ==================== HELPER METHODS ====================
    
    def get_added_file_count(self) -> int:
        """Get number of files added."""
        return len(self.added_files)
    
    def get_removed_file_count(self) -> int:
        """Get number of files removed."""
        return len(self.removed_files)
    
    def get_net_file_count(self) -> int:
        """Get net file count (added - removed)."""
        return len(self.added_files) - len(self.removed_files)
    
    def get_model_name(self) -> Optional[str]:
        """Get model name from config."""
        if not self.model_config:
            return None
        return self.model_config.get('modelName') or self.model_config.get('model')
    
    def get_capability_count(self) -> int:
        """Get number of capabilities."""
        return len(self.capabilities)
    
    def has_capability(self, capability: str) -> bool:
        """Check if session has specific capability."""
        return capability in self.capabilities
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert Session to dictionary."""
        return {
            'composer_id': self.composer_id,
            'created_at': self.created_at.isoformat(),
            'last_updated_at': self.last_updated_at.isoformat(),
            'name': self.name,
            'text': self.text,
            'status': self.status,
            'is_archived': self.is_archived,
            'has_unread_messages': self.has_unread_messages,
            'context_tokens_used': self.context_tokens_used,
            'context_token_limit': self.context_token_limit,
            'context_usage_percent': self.context_usage_percent,
            'total_lines_added': self.total_lines_added,
            'total_lines_removed': self.total_lines_removed,
            'added_files': self.added_files,
            'removed_files': self.removed_files,
            'is_agentic': self.is_agentic,
            'capabilities': self.capabilities,
            'model_config': self.model_config,
            'usage_data': self.usage_data,
            'version': self.version
        }

