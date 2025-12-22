"""MessageRequestContext data model."""

from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional
from datetime import datetime


@dataclass
class MessageRequestContext:
    """
    Represents context data for a message request.
    
    Contains linter errors, git status, file context, todos, and more.
    """
    
    # ==================== REQUIRED FIELDS ====================
    
    context_id: str
    """Full key from database (messageRequestContext:composerId:type)"""
    
    composer_id: str
    """Composer session ID"""
    
    context_type: str
    """Context type (WARM_SUBMIT, etc.)"""
    
    # ==================== LINTER ERRORS ====================
    
    multi_file_linter_errors: List[Dict[str, Any]] = field(default_factory=list)
    """Linter errors across files"""
    
    # ==================== FILE CONTEXT ====================
    
    current_file_location_data: Optional[str] = None
    """Current file and cursor location"""
    
    ide_editors_state: Optional[str] = None
    """State of open editors"""
    
    attached_file_code_chunks: List[Dict[str, Any]] = field(default_factory=list)
    """Attached file code chunks"""
    
    # ==================== GIT & CHANGES ====================
    
    git_status_raw: str = ""
    """Raw git status output"""
    
    diffs_since_last_apply: List[Dict[str, Any]] = field(default_factory=list)
    """Code diffs since last apply"""
    
    deleted_files: List[str] = field(default_factory=list)
    """Deleted files"""
    
    # ==================== TODOS & KNOWLEDGE ====================
    
    todos: List[str] = field(default_factory=list)
    """TODO items (JSON strings)"""
    
    knowledge_items: List[str] = field(default_factory=list)
    """Cursor rules/knowledge (JSON strings)"""
    
    cursor_rules: List[str] = field(default_factory=list)
    """Cursor rules"""
    
    # ==================== TERMINAL & FOLDERS ====================
    
    terminal_files: List[Dict[str, Any]] = field(default_factory=list)
    """Terminal file context"""
    
    attached_folders_list_dir_results: List[Dict[str, Any]] = field(default_factory=list)
    """Folder listing results"""
    
    # ==================== OTHER ====================
    
    summarized_composers: List[Dict[str, Any]] = field(default_factory=list)
    """Summarized composer sessions"""
    
    project_layouts: List[Dict[str, Any]] = field(default_factory=list)
    """Project layout information"""
    
    raw_data: Optional[Dict[str, Any]] = None
    """Raw JSON data for future-proofing"""
    
    # ==================== CLASS METHODS ====================
    
    @classmethod
    def from_dict(cls, key: str, data: Dict[str, Any]) -> 'MessageRequestContext':
        """
        Create MessageRequestContext from dictionary.
        
        Args:
            key: The messageRequestContext key (format: "messageRequestContext:composerId:type")
            data: The JSON data
            
        Returns:
            MessageRequestContext object
        """
        # Parse key
        parts = key.split(':')
        composer_id = parts[1] if len(parts) > 1 else ''
        context_type = parts[2] if len(parts) > 2 else 'UNKNOWN'
        
        # Handle multiFileLinterErrors - might be string or list
        multi_file_linter_errors = data.get('multiFileLinterErrors', [])
        if isinstance(multi_file_linter_errors, str):
            try:
                multi_file_linter_errors = json.loads(multi_file_linter_errors)
            except json.JSONDecodeError:
                multi_file_linter_errors = []
        
        # Handle todos - might be string or list
        todos_raw = data.get('todos', [])
        if isinstance(todos_raw, str):
            try:
                todos_raw = json.loads(todos_raw)
            except json.JSONDecodeError:
                todos_raw = []
        
        # Handle knowledge_items - might be string or list
        knowledge_items_raw = data.get('knowledgeItems', [])
        if isinstance(knowledge_items_raw, str):
            try:
                knowledge_items_raw = json.loads(knowledge_items_raw)
            except json.JSONDecodeError:
                knowledge_items_raw = []
        
        return cls(
            context_id=key,
            composer_id=composer_id,
            context_type=context_type,
            multi_file_linter_errors=multi_file_linter_errors,
            current_file_location_data=data.get('currentFileLocationData'),
            ide_editors_state=data.get('ideEditorsState'),
            attached_file_code_chunks=data.get('attachedFileCodeChunksMetadataOnly', []),
            git_status_raw=data.get('gitStatusRaw', ''),
            diffs_since_last_apply=data.get('diffsSinceLastApply', []),
            deleted_files=data.get('deletedFiles', []),
            todos=todos_raw,
            knowledge_items=knowledge_items_raw,
            cursor_rules=data.get('cursorRules', []),
            terminal_files=data.get('terminalFiles', []),
            attached_folders_list_dir_results=data.get('attachedFoldersListDirResults', []),
            summarized_composers=data.get('summarizedComposers', []),
            project_layouts=data.get('projectLayouts', []),
            raw_data=data
        )
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for serialization."""
        return {
            'context_id': self.context_id,
            'composer_id': self.composer_id,
            'context_type': self.context_type,
            'multi_file_linter_errors': self.multi_file_linter_errors,
            'current_file_location_data': self.current_file_location_data,
            'git_status_raw': self.git_status_raw,
            'has_linter_errors': self.has_linter_errors,
            'linter_error_count': self.linter_error_count,
            'has_git_changes': self.has_git_changes,
            'has_todos': self.has_todos,
        }
    
    # ==================== COMPUTED PROPERTIES ====================
    
    @property
    def has_linter_errors(self) -> bool:
        """Whether this context has linter errors."""
        return len(self.multi_file_linter_errors) > 0
    
    @property
    def linter_error_count(self) -> int:
        """Total number of linter errors."""
        return len(self.multi_file_linter_errors)
    
    @property
    def has_git_changes(self) -> bool:
        """Whether this context has git changes."""
        return bool(self.git_status_raw and self.git_status_raw.strip())
    
    @property
    def has_todos(self) -> bool:
        """Whether this context has todos."""
        return len(self.todos) > 0
    
    @property
    def has_file_context(self) -> bool:
        """Whether this context has file location data."""
        return self.current_file_location_data is not None

