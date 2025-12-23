"""Message data model representing a bubbleId entry."""

from dataclasses import dataclass, field
from typing import Optional, List, Dict, Any
from datetime import datetime


@dataclass
class Message:
    """Represents a single message (bubbleId entry) from Cursor chat."""
    
    # ==================== REQUIRED FIELDS ====================
    
    bubble_id: str
    """Unique message ID"""
    
    composer_id: str
    """Session/composer ID this message belongs to"""
    
    message_type: int
    """Message type: 1=user message, 2=AI response"""
    
    created_at: datetime
    """When the message was created"""
    
    # ==================== CONTENT FIELDS ====================
    
    text: Optional[str] = None
    """Message text content"""
    
    code_blocks: List[Dict[str, Any]] = field(default_factory=list)
    """Code blocks in the message"""
    
    suggested_code_blocks: List[Dict[str, Any]] = field(default_factory=list)
    """AI-suggested code blocks"""
    
    # ==================== THINKING FIELDS ====================
    
    thinking: Optional[str] = None
    """AI thinking process text"""
    
    thinking_duration_ms: Optional[int] = None
    """How long AI spent thinking (milliseconds)"""
    
    # ==================== TOOL USAGE FIELDS ====================
    
    tool_results: List[Dict[str, Any]] = field(default_factory=list)
    """Results from tool usage (read_file, grep, etc.)"""
    
    # ==================== CONTEXT FIELDS ====================
    
    attached_code_chunks: List[Dict[str, Any]] = field(default_factory=list)
    """User-attached code chunks"""
    
    codebase_context_chunks: List[Dict[str, Any]] = field(default_factory=list)
    """Auto-retrieved codebase context"""
    
    # ==================== REFERENCE FIELDS ====================
    
    web_references: List[Dict[str, Any]] = field(default_factory=list)
    """Web search references"""
    
    docs_references: List[Dict[str, Any]] = field(default_factory=list)
    """Documentation references"""
    
    # ==================== MODEL & TOKEN FIELDS ====================
    
    model_info: Optional[Dict[str, Any]] = None
    """Model information (name, provider, etc.)"""
    
    token_count: Optional[Dict[str, int]] = None
    """Token counts (input, output, total)"""
    
    # ==================== ERROR FIELDS ====================
    
    lints: List[Dict[str, Any]] = field(default_factory=list)
    """Linter errors"""
    
    console_logs: List[Dict[str, Any]] = field(default_factory=list)
    """Console logs"""
    
    # ==================== TOOL FIELDS ====================
    
    tool_former_data: Optional[Dict[str, Any]] = None
    """Tool former data (tool status, name, args, results)"""
    
    # ==================== MODE FIELDS ====================
    
    is_agentic: bool = False
    """Whether this is in agent mode"""
    
    capabilities: List[str] = field(default_factory=list)
    """Available capabilities (codebase, web, terminal, etc.)"""
    
    # ==================== META FIELDS ====================
    
    version: int = 10
    """Schema version"""
    
    raw_data: Optional[Dict[str, Any]] = None
    """Raw JSON data for future-proofing"""
    
    # ==================== CLASS METHODS ====================
    
    @classmethod
    def from_dict(cls, key: str, data: Dict[str, Any]) -> 'Message':
        """
        Create Message from dictionary (JSON data).
        
        Args:
            key: The bubbleId key (format: "bubbleId:{composerId}:{messageId}")
            data: The JSON data
            
        Returns:
            Message object
        """
        # Parse key to extract IDs
        parts = key.split(':')
        bubble_id = key
        composer_id = parts[1] if len(parts) > 1 else ''
        
        # Parse timestamp - handle both ISO string and numeric formats
        created_at_raw = data.get('createdAt', None)
        created_at = None
        
        if created_at_raw:
            if isinstance(created_at_raw, str):
                try:
                    # ISO format: "2025-10-08T04:07:43.744Z"
                    created_at = datetime.fromisoformat(created_at_raw.replace('Z', '+00:00'))
                    created_at = created_at.replace(tzinfo=None)  # Keep naive
                except (ValueError, TypeError):
                    try:
                        # Maybe it's a timestamp as string
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
        
        return cls(
            bubble_id=bubble_id,
            composer_id=composer_id,
            message_type=data.get('type', 0),
            created_at=created_at,
            text=data.get('text'),
            code_blocks=data.get('codeBlocks', []),
            suggested_code_blocks=data.get('suggestedCodeBlocks', []),
            thinking=data.get('thinking'),
            thinking_duration_ms=data.get('thinkingDurationMs'),
            tool_results=data.get('toolResults', []),
            attached_code_chunks=data.get('attachedCodeChunks', []),
            codebase_context_chunks=data.get('codebaseContextChunks', []),
            web_references=data.get('webReferences', []),
            docs_references=data.get('docsReferences', []),
            model_info=data.get('modelInfo'),
            token_count=data.get('tokenCount'),
            lints=data.get('lints', []),
            console_logs=data.get('consoleLogs', []),
            tool_former_data=data.get('toolFormerData'),
            is_agentic=data.get('isAgentic', False),
            capabilities=data.get('capabilities', []),
            version=data.get('_v', 10),
            raw_data=data
        )
    
    # ==================== HELPER PROPERTIES ====================
    
    @property
    def is_user_message(self) -> bool:
        """Check if this is a user message."""
        return self.message_type == 1
    
    @property
    def is_ai_message(self) -> bool:
        """Check if this is an AI response."""
        return self.message_type == 2
    
    @property
    def has_text(self) -> bool:
        """Check if message has text content."""
        return self.text is not None and len(self.text.strip()) > 0
    
    @property
    def has_code(self) -> bool:
        """Check if message has code blocks."""
        return len(self.code_blocks) > 0 or len(self.suggested_code_blocks) > 0
    
    @property
    def has_thinking(self) -> bool:
        """Check if message has thinking."""
        if self.thinking is None:
            return False
        # Handle both string and dict formats
        if isinstance(self.thinking, str):
            return len(self.thinking.strip()) > 0
        elif isinstance(self.thinking, dict):
            # If it's a dict, check if it has content
            text = self.thinking.get('text', '') or self.thinking.get('content', '')
            return len(str(text).strip()) > 0
        return False
    
    @property
    def has_tools(self) -> bool:
        """Check if message has tool results."""
        return len(self.tool_results) > 0
    
    @property
    def has_context(self) -> bool:
        """Check if message has context chunks."""
        return len(self.attached_code_chunks) > 0 or len(self.codebase_context_chunks) > 0
    
    @property
    def has_errors(self) -> bool:
        """Check if message has errors/lints."""
        return len(self.lints) > 0 or len(self.console_logs) > 0
    
    @property
    def has_model_info(self) -> bool:
        """Check if message has model info."""
        return self.model_info is not None
    
    @property
    def has_token_count(self) -> bool:
        """Check if message has token count."""
        return self.token_count is not None
    
    @property
    def has_tool_former_data(self) -> bool:
        """Check if message has tool former data."""
        return self.tool_former_data is not None and bool(self.tool_former_data)
    
    # ==================== HELPER METHODS ====================
    
    def get_text_length(self) -> int:
        """Get text length in characters."""
        return len(self.text) if self.text else 0
    
    def get_text_word_count(self) -> int:
        """Get text word count."""
        if not self.text:
            return 0
        return len(self.text.split())
    
    def get_code_block_count(self) -> int:
        """Get total number of code blocks."""
        return len(self.code_blocks) + len(self.suggested_code_blocks)
    
    def get_code_line_count(self) -> int:
        """Get total lines of code in code blocks."""
        total = 0
        
        for block in self.code_blocks:
            code = block.get('code', '')
            total += len(code.split('\n'))
        
        for block in self.suggested_code_blocks:
            code = block.get('code', '')
            total += len(code.split('\n'))
        
        return total
    
    def get_tool_count(self) -> int:
        """Get number of tools used."""
        return len(self.tool_results)
    
    def get_tool_types(self) -> List[str]:
        """Get list of tool types used."""
        return [tool.get('type', 'unknown') for tool in self.tool_results]
    
    def get_context_chunk_count(self) -> int:
        """Get total number of context chunks."""
        return len(self.attached_code_chunks) + len(self.codebase_context_chunks)
    
    def get_model_name(self) -> Optional[str]:
        """Get model name."""
        if not self.model_info:
            return None
        return self.model_info.get('modelName') or self.model_info.get('model')
    
    def get_input_tokens(self) -> int:
        """Get input token count."""
        if not self.token_count:
            return 0
        return self.token_count.get('input', 0) or self.token_count.get('inputTokens', 0)
    
    def get_output_tokens(self) -> int:
        """Get output token count."""
        if not self.token_count:
            return 0
        return self.token_count.get('output', 0) or self.token_count.get('outputTokens', 0)
    
    def get_total_tokens(self) -> int:
        """Get total token count."""
        if not self.token_count:
            return 0
        return self.token_count.get('total', 0) or (self.get_input_tokens() + self.get_output_tokens())
    
    def get_tool_former_status(self) -> Optional[str]:
        """Get tool former status (error, success, cancelled, etc.)."""
        if not self.tool_former_data:
            return None
        additional_data = self.tool_former_data.get('additionalData', {})
        return additional_data.get('status') or self.tool_former_data.get('status')
    
    def get_tool_former_name(self) -> Optional[str]:
        """Get tool former name (codebase_search, grep, etc.)."""
        if not self.tool_former_data:
            return None
        return self.tool_former_data.get('name')
    
    def get_tool_former_args(self) -> Optional[str]:
        """Get tool former raw arguments."""
        if not self.tool_former_data:
            return None
        return self.tool_former_data.get('rawArgs')
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert Message to dictionary."""
        return {
            'bubble_id': self.bubble_id,
            'composer_id': self.composer_id,
            'message_type': self.message_type,
            'created_at': self.created_at.isoformat(),
            'text': self.text,
            'code_blocks': self.code_blocks,
            'suggested_code_blocks': self.suggested_code_blocks,
            'thinking': self.thinking,
            'thinking_duration_ms': self.thinking_duration_ms,
            'tool_results': self.tool_results,
            'attached_code_chunks': self.attached_code_chunks,
            'codebase_context_chunks': self.codebase_context_chunks,
            'web_references': self.web_references,
            'docs_references': self.docs_references,
            'model_info': self.model_info,
            'token_count': self.token_count,
            'lints': self.lints,
            'console_logs': self.console_logs,
            'is_agentic': self.is_agentic,
            'capabilities': self.capabilities,
            'version': self.version
        }

