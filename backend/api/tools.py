"""Tools endpoints for the API."""

from fastapi import APIRouter, HTTPException, Query
from typing import Dict, Any, Optional, List
import logging

logger = logging.getLogger(__name__)

router = APIRouter()


@router.get("/tools")
async def get_tool_calls(
    orchestrator,
    page: int = Query(1, ge=1, description="Page number"),
    limit: int = Query(20, ge=1, le=100, description="Items per page"),
    tool_type: Optional[str] = Query(None, description="Filter by tool type"),
    session_id: Optional[str] = Query(None, description="Filter by session ID"),
    search: Optional[str] = Query(None, description="Search in parameters or results"),
) -> Dict[str, Any]:
    """Get paginated list of tool calls extracted from messages."""
    try:
        # Get all messages
        messages = orchestrator.messages
        
        # Extract tool calls from messages
        tool_calls = []
        for message in messages:
            if message.tool_results and len(message.tool_results) > 0:
                for idx, tool in enumerate(message.tool_results):
                    tool_call = {
                        'id': f"{message.bubble_id}_{idx}",
                        'message_id': message.bubble_id,
                        'session_id': message.composer_id,
                        'created_at': message.created_at.isoformat(),
                        'tool_type': tool.get('type', 'unknown'),
                        'tool_name': tool.get('name', tool.get('type', 'unknown')),
                        'parameters': tool.get('parameters', {}),
                        'result': tool.get('result', None),
                        'success': tool.get('success', True),
                        'error': tool.get('error', None),
                    }
                    tool_calls.append(tool_call)
        
        # Filter by tool type
        if tool_type:
            tool_calls = [t for t in tool_calls if t['tool_type'] == tool_type]
        
        # Filter by session
        if session_id:
            tool_calls = [t for t in tool_calls if t['session_id'] == session_id]
        
        # Search in parameters or results
        if search:
            search_lower = search.lower()
            tool_calls = [
                t for t in tool_calls
                if search_lower in str(t['parameters']).lower() or
                   search_lower in str(t['result']).lower() or
                   search_lower in t['tool_name'].lower()
            ]
        
        # Sort by date (most recent first)
        tool_calls.sort(key=lambda t: t['created_at'], reverse=True)
        
        # Pagination
        total_count = len(tool_calls)
        start_idx = (page - 1) * limit
        end_idx = start_idx + limit
        page_tools = tool_calls[start_idx:end_idx]
        
        # Get unique tool types for statistics
        tool_types = {}
        for tool in tool_calls:
            tool_type = tool['tool_type']
            if tool_type not in tool_types:
                tool_types[tool_type] = 0
            tool_types[tool_type] += 1
        
        return {
            'tools': page_tools,
            'pagination': {
                'page': page,
                'limit': limit,
                'total_count': total_count,
                'total_pages': (total_count + limit - 1) // limit,
                'has_next': end_idx < total_count,
                'has_prev': page > 1
            },
            'stats': {
                'tool_types': tool_types,
                'total_calls': total_count,
                'success_count': sum(1 for t in tool_calls if t['success']),
            }
        }
    except Exception as e:
        logger.error(f"Error getting tool calls: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/tools/{tool_id}")
async def get_tool_detail(orchestrator, tool_id: str) -> Dict[str, Any]:
    """Get detailed information about a specific tool call."""
    try:
        # Parse tool_id (format: messageId_idx)
        parts = tool_id.rsplit('_', 1)
        if len(parts) != 2:
            raise HTTPException(status_code=400, detail="Invalid tool ID format")
        
        message_id, idx_str = parts
        try:
            idx = int(idx_str)
        except ValueError:
            raise HTTPException(status_code=400, detail="Invalid tool ID format")
        
        # Get all messages
        messages = orchestrator.messages
        
        # Find the message
        message = next((m for m in messages if m.bubble_id == message_id), None)
        
        if not message:
            raise HTTPException(status_code=404, detail=f"Message {message_id} not found")
        
        if not message.tool_results or len(message.tool_results) <= idx:
            raise HTTPException(status_code=404, detail=f"Tool call {tool_id} not found")
        
        tool = message.tool_results[idx]
        
        # Get session info
        sessions = orchestrator.sessions
        session = next((s for s in sessions if s.composer_id == message.composer_id), None)
        
        return {
            'id': tool_id,
            'message_id': message.bubble_id,
            'session_id': message.composer_id,
            'session_name': session.name if session else None,
            'created_at': message.created_at.isoformat(),
            'tool_type': tool.get('type', 'unknown'),
            'tool_name': tool.get('name', tool.get('type', 'unknown')),
            'parameters': tool.get('parameters', {}),
            'result': tool.get('result', None),
            'success': tool.get('success', True),
            'error': tool.get('error', None),
            'message_context': {
                'text_preview': message.text[:200] if message.text else None,
                'is_user_message': message.is_user_message,
                'has_code': message.has_code,
                'has_thinking': message.has_thinking,
            }
        }
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting tool detail: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))

