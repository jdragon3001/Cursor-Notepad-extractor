"""CodeDiff data model representing a codeBlockDiff entry."""

from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional
from datetime import datetime


@dataclass
class DiffChange:
    """Represents a single diff change (original vs modified)."""
    
    original_start_line: int
    """Starting line number in original"""
    
    original_end_line: int
    """Ending line number in original (exclusive)"""
    
    modified_lines: List[str]
    """Lines in the modified version"""
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'DiffChange':
        """Create DiffChange from dictionary."""
        original = data.get('original', {})
        return cls(
            original_start_line=original.get('startLineNumber', 0),
            original_end_line=original.get('endLineNumberExclusive', 0),
            modified_lines=data.get('modified', [])
        )
    
    @property
    def original_line_count(self) -> int:
        """Number of lines in original."""
        return max(0, self.original_end_line - self.original_start_line)
    
    @property
    def modified_line_count(self) -> int:
        """Number of lines in modified."""
        return len(self.modified_lines)
    
    @property
    def net_lines_changed(self) -> int:
        """Net change in line count."""
        return self.modified_line_count - self.original_line_count


@dataclass
class CodeDiff:
    """Represents a code diff from codeBlockDiff table."""
    
    # ==================== REQUIRED FIELDS ====================
    
    diff_id: str
    """Full key from database (codeBlockDiff:composerId:diffId)"""
    
    composer_id: str
    """Composer session ID"""
    
    block_id: str
    """Code block ID"""
    
    # ==================== DIFF DATA ====================
    
    new_changes: List[DiffChange] = field(default_factory=list)
    """Changes in new model"""
    
    original_changes: List[DiffChange] = field(default_factory=list)
    """Changes in original model"""
    
    raw_data: Optional[Dict[str, Any]] = None
    """Raw JSON data for future-proofing"""
    
    # ==================== CLASS METHODS ====================
    
    @classmethod
    def from_dict(cls, key: str, data: Dict[str, Any]) -> 'CodeDiff':
        """
        Create CodeDiff from dictionary (JSON data).
        
        Args:
            key: The codeBlockDiff key (format: "codeBlockDiff:composerId:blockId")
            data: The JSON data
            
        Returns:
            CodeDiff object
        """
        # Parse key to extract IDs
        parts = key.split(':')
        composer_id = parts[1] if len(parts) > 1 else ''
        block_id = parts[2] if len(parts) > 2 else ''
        
        # Parse changes
        new_changes = [
            DiffChange.from_dict(change) 
            for change in data.get('newModelDiffWrtV0', [])
        ]
        
        original_changes = [
            DiffChange.from_dict(change) 
            for change in data.get('originalModelDiffWrtV0', [])
        ]
        
        return cls(
            diff_id=key,
            composer_id=composer_id,
            block_id=block_id,
            new_changes=new_changes,
            original_changes=original_changes,
            raw_data=data
        )
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for serialization."""
        return {
            'diff_id': self.diff_id,
            'composer_id': self.composer_id,
            'block_id': self.block_id,
            'new_changes': [
                {
                    'original_start_line': c.original_start_line,
                    'original_end_line': c.original_end_line,
                    'modified_lines': c.modified_lines,
                }
                for c in self.new_changes
            ],
            'original_changes': [
                {
                    'original_start_line': c.original_start_line,
                    'original_end_line': c.original_end_line,
                    'modified_lines': c.modified_lines,
                }
                for c in self.original_changes
            ],
        }
    
    # ==================== COMPUTED PROPERTIES ====================
    
    @property
    def total_changes(self) -> int:
        """Total number of changes."""
        return len(self.new_changes) + len(self.original_changes)
    
    @property
    def has_changes(self) -> bool:
        """Whether this diff has any changes."""
        return len(self.new_changes) > 0 or len(self.original_changes) > 0
    
    def get_total_lines_changed(self) -> int:
        """Get total number of lines changed."""
        total = 0
        for change in self.new_changes + self.original_changes:
            total += change.modified_line_count
        return total
    
    def get_net_lines_changed(self) -> int:
        """Get net change in lines."""
        net = 0
        for change in self.new_changes + self.original_changes:
            net += change.net_lines_changed
        return net
    
    def get_diff_span(self) -> int:
        """Get the span of lines affected by this diff."""
        spans = []
        for change in self.new_changes + self.original_changes:
            if change.original_line_count > 0:
                spans.append(change.original_line_count)
        return sum(spans)


@dataclass
class CodeTrackingLine:
    """Represents a tracked code line from aiCodeTrackingLines."""
    
    hash: str
    """Hash of the line"""
    
    source: str
    """Source (composer, tab, etc.)"""
    
    composer_id: Optional[str] = None
    """Composer session ID if from composer"""
    
    file_extension: Optional[str] = None
    """File extension"""
    
    file_name: Optional[str] = None
    """Full file path"""
    
    timestamp: Optional[int] = None
    """Timestamp in milliseconds"""
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'CodeTrackingLine':
        """Create CodeTrackingLine from dictionary."""
        metadata = data.get('metadata', {})
        
        return cls(
            hash=data.get('hash', ''),
            source=metadata.get('source', 'unknown'),
            composer_id=metadata.get('composerId'),
            file_extension=metadata.get('fileExtension'),
            file_name=metadata.get('fileName'),
            timestamp=metadata.get('timestamp')
        )
    
    @property
    def created_at(self) -> Optional[datetime]:
        """Get datetime from timestamp."""
        if self.timestamp:
            return datetime.fromtimestamp(self.timestamp / 1000)
        return None

