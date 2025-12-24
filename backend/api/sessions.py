"""Session/Conversation endpoints for the API."""

from fastapi import APIRouter, HTTPException, Query
from typing import Dict, Any, Optional
import logging

from stats.consolidator import MessageConsolidator

logger = logging.getLogger(__name__)

router = APIRouter()


@router.get("/sessions")
async def get_sessions(
    orchestrator,
    page: int = Query(1, ge=1, description="Page number"),
    limit: int = Query(20, ge=1, le=100, description="Items per page"),
    sort: str = Query("recent", description="Sort: recent, oldest, longest, shortest"),
    search: Optional[str] = Query(None, description="Search in session names"),
) -> Dict[str, Any]:
    """Get paginated list of sessions (conversations)."""
    try:
        sessions = orchestrator.sessions
        
        # Filter by search
        filtered_sessions = sessions
        if search:
            search_lower = search.lower()
            filtered_sessions = [
                s for s in filtered_sessions
                if s.name and search_lower in s.name.lower()
            ]
        
        # Sort
        if sort == "recent":
            # Sort by last_updated_at (most recently active)
            filtered_sessions.sort(key=lambda s: s.last_updated_at, reverse=True)
        elif sort == "oldest":
            # Sort by created_at (oldest first)
            filtered_sessions.sort(key=lambda s: s.created_at)
        elif sort == "longest":
            filtered_sessions.sort(key=lambda s: s.duration_minutes, reverse=True)
        elif sort == "shortest":
            filtered_sessions.sort(key=lambda s: s.duration_minutes)
        
        # Pagination
        total_count = len(filtered_sessions)
        start_idx = (page - 1) * limit
        end_idx = start_idx + limit
        page_sessions = filtered_sessions[start_idx:end_idx]
        
        # Convert to dict
        sessions_data = []
        for session in page_sessions:
            # Calculate files modified count
            files_modified = len(session.added_files) + len(session.removed_files)
            
            sessions_data.append({
                'id': session.composer_id,
                'name': session.name,
                'created_at': session.created_at.isoformat(),
                'last_updated_at': session.last_updated_at.isoformat() if session.last_updated_at else None,
                'duration_minutes': round(session.duration_minutes, 1),
                'message_count': 0,  # Will be calculated on detail view
                'total_lines_added': session.total_lines_added,
                'total_lines_removed': session.total_lines_removed,
                'files_modified_count': files_modified,
            })
        
        return {
            'sessions': sessions_data,
            'pagination': {
                'page': page,
                'limit': limit,
                'total_count': total_count,
                'total_pages': (total_count + limit - 1) // limit,
                'has_next': end_idx < total_count,
                'has_prev': page > 1
            }
        }
    except Exception as e:
        logger.error(f"Error getting sessions: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/sessions/{session_id}")
async def get_session_detail(orchestrator, session_id: str) -> Dict[str, Any]:
    """Get full conversation details for a session including all messages."""
    try:
        # Find session
        sessions = orchestrator.sessions
        session = next((s for s in sessions if s.composer_id == session_id), None)
        
        if not session:
            raise HTTPException(status_code=404, detail=f"Session {session_id} not found")
        
        # Get ALL messages for this session
        all_messages = orchestrator.messages
        session_messages = [m for m in all_messages if m.composer_id == session_id]
        
        # Consolidate just this session's messages
        try:
            consolidated_session_messages = MessageConsolidator.consolidate(session_messages)
        except Exception as e:
            logger.error(f"Consolidation failed for session {session_id}: {e}")
            consolidated_session_messages = session_messages
        
        # Sort by timestamp - NEWEST FIRST for conversation view
        consolidated_session_messages.sort(key=lambda m: m.created_at, reverse=True)
        
        # Get file changes for this session from code tracking lines
        file_changes = []
        try:
            from stats.extractors.code_tracking_extractor import CodeTrackingExtractor
            tracking_extractor = CodeTrackingExtractor(orchestrator.db_path)
            all_tracking_lines = tracking_extractor.extract()
            
            # Filter for this session and group by file
            session_tracking = [t for t in all_tracking_lines if t.composer_id == session_id]
            
            # Group by file name
            files_dict = {}
            for tracking in session_tracking:
                if tracking.file_name not in files_dict:
                    files_dict[tracking.file_name] = {
                        'file_name': tracking.file_name,
                        'file_extension': tracking.file_extension,
                        'line_count': 0,
                        'first_edit': tracking.timestamp,
                        'last_edit': tracking.timestamp
                    }
                files_dict[tracking.file_name]['line_count'] += 1
                if tracking.timestamp < files_dict[tracking.file_name]['first_edit']:
                    files_dict[tracking.file_name]['first_edit'] = tracking.timestamp
                if tracking.timestamp > files_dict[tracking.file_name]['last_edit']:
                    files_dict[tracking.file_name]['last_edit'] = tracking.timestamp
            
            file_changes = list(files_dict.values())
            file_changes.sort(key=lambda f: f['last_edit'], reverse=True)
            
        except Exception as e:
            logger.error(f"Error getting file changes: {e}")
        
        # Convert messages to detailed format
        messages_data = []
        for msg in consolidated_session_messages:
            messages_data.append({
                'id': msg.bubble_id,
                'type': 'user' if msg.is_user_message else 'ai',
                'created_at': msg.created_at.isoformat(),
                'text': msg.text,
                'word_count': msg.get_text_word_count(),
                'code_blocks': msg.code_blocks,
                'suggested_code_blocks': msg.suggested_code_blocks,
                'thinking': msg.thinking,
                'thinking_duration_ms': msg.thinking_duration_ms,
                'tool_results': msg.tool_results,
                'tool_count': msg.get_tool_count(),
                'tool_types': msg.get_tool_types(),
                'attached_code_chunks': msg.attached_code_chunks,
                'codebase_context_chunks': msg.codebase_context_chunks,
                'web_references': msg.web_references,
                'docs_references': msg.docs_references,
                'model_info': msg.model_info,
                'model_name': msg.get_model_name(),
                'is_agentic': msg.is_agentic,
                'is_consolidated': msg.raw_data and msg.raw_data.get('consolidated', False),
                'fragment_count': msg.raw_data.get('fragment_count', 1) if msg.raw_data else 1,
            })
        
        # Calculate files modified count
        files_modified = len(session.added_files) + len(session.removed_files)
        
        return {
            'session': {
                'id': session.composer_id,
                'name': session.name,
                'created_at': session.created_at.isoformat(),
                'last_updated_at': session.last_updated_at.isoformat() if session.last_updated_at else None,
                'duration_minutes': round(session.duration_minutes, 1),
                'message_count': len(consolidated_session_messages),
                'total_lines_added': session.total_lines_added,
                'total_lines_removed': session.total_lines_removed,
                'files_modified_count': files_modified,
            },
            'messages': messages_data,
            'file_changes': file_changes
        }
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting session detail: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))

