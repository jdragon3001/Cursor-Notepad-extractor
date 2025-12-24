"""Message consolidator - merges fragmented AI messages into logical conversation turns."""

from typing import List
from datetime import datetime
from stats.models.message import Message
import logging

logger = logging.getLogger(__name__)


class MessageConsolidator:
    """Consolidates fragmented AI messages into logical conversation turns."""
    
    @staticmethod
    def consolidate(messages: List[Message]) -> List[Message]:
        """
        Consolidate messages based on conversation turn logic:
        - User messages stay as-is
        - All consecutive AI messages are merged into ONE AI response
        
        Args:
            messages: List of raw Message objects
            
        Returns:
            List of consolidated Message objects
        """
        if not messages:
            logger.info("No messages to consolidate")
            return []
        
        logger.info(f"Starting consolidation of {len(messages)} messages...")
        
        # Sort by session and timestamp
        try:
            sorted_messages = sorted(messages, key=lambda m: (m.composer_id, m.created_at))
        except Exception as e:
            logger.error(f"Error sorting messages: {e}")
            return messages  # Return original if sorting fails
        
        consolidated = []
        current_ai_group = []
        
        for msg in sorted_messages:
            try:
                if msg.is_user_message:
                    # Before starting a new user message, flush any pending AI group
                    if current_ai_group:
                        merged = MessageConsolidator._merge_ai_messages(current_ai_group)
                        consolidated.append(merged)
                        current_ai_group = []
                    
                    # Add user message as-is
                    consolidated.append(msg)
                    
                elif msg.is_ai_message:
                    # Add to current AI group
                    current_ai_group.append(msg)
            except Exception as e:
                logger.error(f"Error processing message {msg.bubble_id}: {e}")
                # Skip this message but continue
                continue
        
        # Flush any remaining AI group
        if current_ai_group:
            try:
                merged = MessageConsolidator._merge_ai_messages(current_ai_group)
                consolidated.append(merged)
            except Exception as e:
                logger.error(f"Error merging final AI group: {e}")
        
        logger.info(f"Consolidation complete: {len(messages)} -> {len(consolidated)} messages")
        return consolidated
    
    @staticmethod
    def _merge_ai_messages(ai_messages: List[Message]) -> Message:
        """
        Merge multiple AI message fragments into one consolidated message.
        
        Args:
            ai_messages: List of AI message fragments to merge
            
        Returns:
            Single consolidated Message object
        """
        if not ai_messages:
            raise ValueError("Cannot merge empty list of messages")
        
        if len(ai_messages) == 1:
            return ai_messages[0]
        
        # Use the earliest timestamp as the main timestamp
        first_msg = min(ai_messages, key=lambda m: m.created_at)
        
        # Collect all text fragments
        text_parts = [msg.text for msg in ai_messages if msg.text and msg.text.strip()]
        merged_text = '\n\n'.join(text_parts) if text_parts else None
        
        # Collect all thinking fragments
        thinking_parts = []
        total_thinking_duration = 0
        for msg in ai_messages:
            if msg.thinking:
                if isinstance(msg.thinking, str) and msg.thinking.strip():
                    thinking_parts.append(msg.thinking)
                elif isinstance(msg.thinking, dict):
                    think_text = msg.thinking.get('text') or msg.thinking.get('content')
                    if think_text:
                        thinking_parts.append(str(think_text))
            if msg.thinking_duration_ms:
                total_thinking_duration += msg.thinking_duration_ms
        
        merged_thinking = '\n\n---\n\n'.join(thinking_parts) if thinking_parts else None
        
        # Collect all code blocks
        code_blocks = []
        suggested_code_blocks = []
        for msg in ai_messages:
            code_blocks.extend(msg.code_blocks)
            suggested_code_blocks.extend(msg.suggested_code_blocks)
        
        # Collect all tool results
        tool_results = []
        for msg in ai_messages:
            tool_results.extend(msg.tool_results)
        
        # Collect all context chunks
        attached_code_chunks = []
        codebase_context_chunks = []
        for msg in ai_messages:
            attached_code_chunks.extend(msg.attached_code_chunks)
            codebase_context_chunks.extend(msg.codebase_context_chunks)
        
        # Collect references
        web_references = []
        docs_references = []
        for msg in ai_messages:
            web_references.extend(msg.web_references)
            docs_references.extend(msg.docs_references)
        
        # Get model info (prefer non-None)
        model_info = None
        for msg in ai_messages:
            if msg.model_info:
                model_info = msg.model_info
                break
        
        # Get token count (prefer non-None)
        token_count = None
        for msg in ai_messages:
            if msg.token_count:
                token_count = msg.token_count
                break
        
        # Collect lints and console logs
        lints = []
        console_logs = []
        for msg in ai_messages:
            lints.extend(msg.lints)
            console_logs.extend(msg.console_logs)
        
        # Get tool former data (prefer non-None)
        tool_former_data = None
        for msg in ai_messages:
            if msg.tool_former_data:
                tool_former_data = msg.tool_former_data
                break
        
        # Check if any message is agentic
        is_agentic = any(msg.is_agentic for msg in ai_messages)
        
        # Collect all capabilities
        capabilities = []
        for msg in ai_messages:
            capabilities.extend(msg.capabilities)
        capabilities = list(set(capabilities))  # Unique
        
        # Create consolidated message
        # Use the first message's IDs but mark as consolidated
        consolidated_bubble_id = f"{first_msg.bubble_id}_consolidated_{len(ai_messages)}"
        
        consolidated = Message(
            bubble_id=consolidated_bubble_id,
            composer_id=first_msg.composer_id,
            message_type=2,  # AI message
            created_at=first_msg.created_at,
            text=merged_text,
            code_blocks=code_blocks,
            suggested_code_blocks=suggested_code_blocks,
            thinking=merged_thinking,
            thinking_duration_ms=total_thinking_duration if total_thinking_duration > 0 else None,
            tool_results=tool_results,
            attached_code_chunks=attached_code_chunks,
            codebase_context_chunks=codebase_context_chunks,
            web_references=web_references,
            docs_references=docs_references,
            model_info=model_info,
            token_count=token_count,
            lints=lints,
            console_logs=console_logs,
            tool_former_data=tool_former_data,
            is_agentic=is_agentic,
            capabilities=capabilities,
            version=first_msg.version,
            raw_data={
                'consolidated': True,
                'fragment_count': len(ai_messages),
                'fragment_ids': [msg.bubble_id for msg in ai_messages]
            }
        )
        
        return consolidated

