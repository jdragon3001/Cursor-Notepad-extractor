"""Context endpoints for the API."""

from fastapi import APIRouter, HTTPException, Query
from typing import Dict, Any, Optional, List
import logging

logger = logging.getLogger(__name__)

router = APIRouter()


@router.get("/context")
async def get_context_items(
    orchestrator,
    page: int = Query(1, ge=1, description="Page number"),
    limit: int = Query(20, ge=1, le=100, description="Items per page"),
    context_type: Optional[str] = Query(None, description="Filter by context type"),
    session_id: Optional[str] = Query(None, description="Filter by session ID"),
    search: Optional[str] = Query(None, description="Search in context content"),
) -> Dict[str, Any]:
    """Get paginated list of context items."""
    try:
        # Get all request contexts
        request_contexts = orchestrator._request_contexts
        
        if not request_contexts:
            return {
                'contexts': [],
                'pagination': {
                    'page': 1,
                    'limit': limit,
                    'total_count': 0,
                    'total_pages': 0,
                    'has_next': False,
                    'has_prev': False
                },
                'stats': {
                    'context_types': {},
                    'total_items': 0
                }
            }
        
        # Convert to list of context items with details
        context_items = []
        for ctx in request_contexts:
            # Determine primary context type
            context_types = []
            
            if ctx.multi_file_linter_errors:
                context_types.append('linter')
            if ctx.git_status_raw:
                context_types.append('git')
            if ctx.current_file_location_data or ctx.ide_editors_state:
                context_types.append('file_context')
            if ctx.attached_file_code_chunks:
                context_types.append('code_chunks')
            if ctx.todos:
                context_types.append('todos')
            if ctx.terminal_files:
                context_types.append('terminal')
            if ctx.cursor_rules or ctx.knowledge_items:
                context_types.append('knowledge')
            
            primary_type = context_types[0] if context_types else 'unknown'
            
            # Create summary
            summary = []
            if ctx.multi_file_linter_errors:
                summary.append(f"{len(ctx.multi_file_linter_errors)} linter errors")
            if ctx.git_status_raw:
                summary.append("Git status")
            if ctx.attached_file_code_chunks:
                summary.append(f"{len(ctx.attached_file_code_chunks)} code chunks")
            if ctx.todos:
                summary.append(f"{len(ctx.todos)} TODOs")
            
            context_items.append({
                'id': ctx.context_id,
                'session_id': ctx.composer_id,
                'context_type': primary_type,
                'all_types': context_types,
                'summary': ', '.join(summary) if summary else 'Context data',
                'has_linter_errors': len(ctx.multi_file_linter_errors) > 0,
                'has_git_status': bool(ctx.git_status_raw),
                'has_file_context': bool(ctx.current_file_location_data or ctx.ide_editors_state),
                'has_code_chunks': len(ctx.attached_file_code_chunks) > 0,
                'has_todos': len(ctx.todos) > 0,
                'has_terminal': len(ctx.terminal_files) > 0,
                'has_knowledge': len(ctx.cursor_rules) > 0 or len(ctx.knowledge_items) > 0,
            })
        
        # Filter by context type
        if context_type:
            context_items = [c for c in context_items if context_type in c['all_types']]
        
        # Filter by session
        if session_id:
            context_items = [c for c in context_items if c['session_id'] == session_id]
        
        # Search in summary
        if search:
            search_lower = search.lower()
            context_items = [
                c for c in context_items
                if search_lower in c['summary'].lower() or
                   search_lower in c['context_type'].lower()
            ]
        
        # Sort by ID (most recent first)
        context_items.sort(key=lambda c: c['id'], reverse=True)
        
        # Pagination
        total_count = len(context_items)
        start_idx = (page - 1) * limit
        end_idx = start_idx + limit
        page_contexts = context_items[start_idx:end_idx]
        
        # Calculate statistics
        type_counts = {}
        for item in context_items:
            for ctx_type in item['all_types']:
                if ctx_type not in type_counts:
                    type_counts[ctx_type] = 0
                type_counts[ctx_type] += 1
        
        return {
            'contexts': page_contexts,
            'pagination': {
                'page': page,
                'limit': limit,
                'total_count': total_count,
                'total_pages': (total_count + limit - 1) // limit,
                'has_next': end_idx < total_count,
                'has_prev': page > 1
            },
            'stats': {
                'context_types': type_counts,
                'total_items': total_count
            }
        }
    except Exception as e:
        logger.error(f"Error getting context items: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/context/{context_id}")
async def get_context_detail(orchestrator, context_id: str) -> Dict[str, Any]:
    """Get detailed information about a specific context item."""
    try:
        # Get all request contexts
        request_contexts = orchestrator._request_contexts
        
        # Find the context
        ctx = next((c for c in request_contexts if c.context_id == context_id), None)
        
        if not ctx:
            raise HTTPException(status_code=404, detail=f"Context {context_id} not found")
        
        # Get session info
        sessions = orchestrator.sessions
        session = next((s for s in sessions if s.composer_id == ctx.composer_id), None)
        
        return {
            'id': ctx.context_id,
            'session_id': ctx.composer_id,
            'session_name': session.name if session else None,
            'context_type': ctx.context_type,
            
            # Linter errors
            'linter_errors': ctx.multi_file_linter_errors,
            'linter_error_count': len(ctx.multi_file_linter_errors),
            
            # Git status
            'git_status': ctx.git_status_raw,
            'deleted_files': ctx.deleted_files,
            'diffs_since_last_apply': ctx.diffs_since_last_apply,
            
            # File context
            'current_file_location': ctx.current_file_location_data,
            'ide_editors_state': ctx.ide_editors_state,
            'attached_file_chunks': ctx.attached_file_code_chunks,
            'attached_file_count': len(ctx.attached_file_code_chunks),
            
            # TODOs and knowledge
            'todos': ctx.todos,
            'todo_count': len(ctx.todos),
            'knowledge_items': ctx.knowledge_items,
            'cursor_rules': ctx.cursor_rules,
            
            # Terminal and folders
            'terminal_files': ctx.terminal_files,
            'terminal_count': len(ctx.terminal_files),
            'folder_listings': ctx.attached_folders_list_dir_results,
            
            # Other
            'summarized_composers': ctx.summarized_composers,
            'project_layouts': ctx.project_layouts,
            
            'session_info': {
                'name': session.name if session else None,
                'created_at': session.created_at.isoformat() if session else None,
            } if session else None,
        }
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting context detail: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))

