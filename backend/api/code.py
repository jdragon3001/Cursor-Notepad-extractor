"""Code diffs endpoints for the API."""

from fastapi import APIRouter, HTTPException, Query
from typing import Dict, Any, Optional, List
import logging

logger = logging.getLogger(__name__)

router = APIRouter()


@router.get("/code-diffs")
async def get_code_diffs(
    orchestrator,
    page: int = Query(1, ge=1, description="Page number"),
    limit: int = Query(20, ge=1, le=100, description="Items per page"),
    sort: str = Query("recent", description="Sort: recent, oldest, most_changes"),
    session_id: Optional[str] = Query(None, description="Filter by session ID"),
    search: Optional[str] = Query(None, description="Search in file paths"),
) -> Dict[str, Any]:
    """Get paginated list of code diffs."""
    try:
        # Get all code diffs from orchestrator
        code_diffs = orchestrator._code_diffs
        
        if not code_diffs:
            return {
                'diffs': [],
                'pagination': {
                    'page': 1,
                    'limit': limit,
                    'total_count': 0,
                    'total_pages': 0,
                    'has_next': False,
                    'has_prev': False
                }
            }
        
        # Get sessions for lookup
        sessions = orchestrator.sessions
        session_map = {s.composer_id: s for s in sessions}
        
        # Filter by session
        filtered_diffs = code_diffs
        if session_id:
            filtered_diffs = [d for d in filtered_diffs if d.composer_id == session_id]
        
        # Search in raw data (since we don't have file paths directly)
        if search:
            search_lower = search.lower()
            filtered_diffs = [
                d for d in filtered_diffs
                if search_lower in str(d.raw_data).lower()
            ]
        
        # Sort
        # Note: CodeDiff doesn't have timestamps, so we can't sort by date directly
        # We'll sort by composer_id to group related diffs together
        if sort == "most_changes":
            filtered_diffs.sort(key=lambda d: d.get_total_lines_changed(), reverse=True)
        else:
            # Group by session (best we can do without timestamps)
            filtered_diffs.sort(key=lambda d: d.composer_id, reverse=True)
        
        # Pagination
        total_count = len(filtered_diffs)
        start_idx = (page - 1) * limit
        end_idx = start_idx + limit
        page_diffs = filtered_diffs[start_idx:end_idx]
        
        # Convert to dict for JSON serialization
        diffs_data = []
        for diff in page_diffs:
            session = session_map.get(diff.composer_id)
            
            # Calculate total lines added/removed
            lines_added = 0
            lines_removed = 0
            for change in diff.new_changes + diff.original_changes:
                if change.net_lines_changed > 0:
                    lines_added += change.net_lines_changed
                else:
                    lines_removed += abs(change.net_lines_changed)
            
            diffs_data.append({
                'id': diff.diff_id,
                'session_id': diff.composer_id,
                'session_name': session.name if session else None,
                'block_id': diff.block_id,
                'lines_added': lines_added,
                'lines_removed': lines_removed,
                'net_lines_changed': diff.get_net_lines_changed(),
                'total_changes': diff.total_changes,
                'has_changes': diff.has_changes,
                'created_at': session.created_at.isoformat() if session else None,
            })
        
        return {
            'diffs': diffs_data,
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
        logger.error(f"Error getting code diffs: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/code-diffs/{diff_id}")
async def get_code_diff_detail(orchestrator, diff_id: str) -> Dict[str, Any]:
    """Get detailed information about a specific code diff."""
    try:
        # Get all code diffs
        code_diffs = orchestrator._code_diffs
        
        # Find the diff
        diff = next((d for d in code_diffs if d.diff_id == diff_id), None)
        
        if not diff:
            raise HTTPException(status_code=404, detail=f"Code diff {diff_id} not found")
        
        # Get session info
        sessions = orchestrator.sessions
        session = next((s for s in sessions if s.composer_id == diff.composer_id), None)
        
        # Build detailed response
        return {
            'id': diff.diff_id,
            'session_id': diff.composer_id,
            'session_name': session.name if session else None,
            'block_id': diff.block_id,
            'new_changes': [
                {
                    'original_start_line': c.original_start_line,
                    'original_end_line': c.original_end_line,
                    'original_line_count': c.original_line_count,
                    'modified_lines': c.modified_lines,
                    'modified_line_count': c.modified_line_count,
                    'net_lines_changed': c.net_lines_changed,
                }
                for c in diff.new_changes
            ],
            'original_changes': [
                {
                    'original_start_line': c.original_start_line,
                    'original_end_line': c.original_end_line,
                    'original_line_count': c.original_line_count,
                    'modified_lines': c.modified_lines,
                    'modified_line_count': c.modified_line_count,
                    'net_lines_changed': c.net_lines_changed,
                }
                for c in diff.original_changes
            ],
            'total_changes': diff.total_changes,
            'total_lines_changed': diff.get_total_lines_changed(),
            'net_lines_changed': diff.get_net_lines_changed(),
            'diff_span': diff.get_diff_span(),
            'session_info': {
                'name': session.name if session else None,
                'created_at': session.created_at.isoformat() if session else None,
                'total_lines_added': session.total_lines_added if session else 0,
                'total_lines_removed': session.total_lines_removed if session else 0,
            } if session else None,
        }
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting code diff detail: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))

