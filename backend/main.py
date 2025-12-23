"""FastAPI backend server for Cursor Stats Dashboard."""

import sys
import logging
from pathlib import Path
from typing import Dict, Any, List, Optional
from datetime import datetime

from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

# Add parent directory to path to import stats modules
sys.path.insert(0, str(Path(__file__).parent.parent))

from stats import StatsOrchestrator
from stats.models.time_range import TimeRange
from stats.consolidator import MessageConsolidator
from utils.config import Config

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title="Cursor Stats API",
    description="Backend API for Cursor IDE usage statistics",
    version="1.0.0"
)

# Configure CORS for React frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:5174", "http://localhost:3000"],  # Allow multiple Vite ports
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize stats orchestrator (lazy loading)
_orchestrator: Optional[StatsOrchestrator] = None


def get_orchestrator() -> StatsOrchestrator:
    """Get or initialize the stats orchestrator."""
    global _orchestrator
    if _orchestrator is None:
        try:
            # Get global database path (cross-platform)
            db_path = Config.get_global_db_path()
            
            if not db_path.exists():
                raise FileNotFoundError(f"Database not found at {db_path}")
            
            logger.info(f"Initializing orchestrator with DB: {db_path}")
            _orchestrator = StatsOrchestrator(db_path)  # Pass Path object, not string
            
            # Load data on initialization
            _orchestrator.extract_all_data()
            logger.info("Data extraction complete")
            
        except Exception as e:
            logger.error(f"Failed to initialize orchestrator: {e}")
            raise
    
    return _orchestrator


# Response models
class HealthResponse(BaseModel):
    status: str
    message: str


class SummaryResponse(BaseModel):
    total_messages: int
    total_sessions: int
    total_code_diffs: int
    total_tracking_lines: int
    total_daily_stats: int
    total_request_contexts: int
    total_workspaces: int
    database_path: str
    cache_enabled: bool


class StatResponse(BaseModel):
    id: str
    value: Any
    label: str
    category: str
    data_source: str
    type: str


# API Routes

@app.get("/", response_model=HealthResponse)
async def root():
    """Health check endpoint."""
    return HealthResponse(
        status="ok",
        message="Cursor Stats API is running"
    )


@app.get("/api/health", response_model=HealthResponse)
async def health_check():
    """Detailed health check."""
    try:
        orchestrator = get_orchestrator()
        return HealthResponse(
            status="ok",
            message=f"Connected to database with {len(orchestrator.messages):,} messages"
        )
    except Exception as e:
        return HealthResponse(
            status="error",
            message=str(e)
        )


@app.get("/api/summary", response_model=SummaryResponse)
async def get_summary():
    """Get summary of all extracted data."""
    try:
        orchestrator = get_orchestrator()
        summary = orchestrator.get_summary()
        return SummaryResponse(**summary)
    except Exception as e:
        logger.error(f"Error getting summary: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/stats/all")
async def get_all_stats(
    start_date: Optional[str] = Query(None, description="Start date (ISO format or preset)"),
    end_date: Optional[str] = Query(None, description="End date (ISO format)"),
    preset: Optional[str] = Query(None, description="Preset time range (last_7_days, last_30_days, etc.)")
) -> Dict[str, Any]:
    """Get all calculated statistics, optionally filtered by time range."""
    try:
        orchestrator = get_orchestrator()
        
        # Parse time range if provided
        time_range = None
        if preset:
            # Use preset
            time_range = TimeRange.from_preset(preset)
            logger.info(f"Using preset time range: {preset}")
        elif start_date and end_date:
            # Use custom range
            time_range = TimeRange.from_iso_strings(start_date, end_date)
            logger.info(f"Using custom time range: {start_date} to {end_date}")
        
        stats = orchestrator.calculate_all_stats(time_range=time_range)
        
        # Add metadata about the time range
        response = {
            'stats': stats,
            'time_range': time_range.to_dict() if time_range else None
        }
        
        return response
    except ValueError as e:
        logger.error(f"Invalid time range: {e}")
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"Error calculating stats: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/stats/time-series/{stat_id}")
async def get_time_series(
    stat_id: str,
    start_date: Optional[str] = Query(None, description="Start date (ISO format)"),
    end_date: Optional[str] = Query(None, description="End date (ISO format)"),
    preset: Optional[str] = Query("last_30_days", description="Preset time range"),
    granularity: Optional[str] = Query("day", description="Time granularity (day, week, month)")
) -> Dict[str, Any]:
    """Get time series data for a specific stat."""
    try:
        orchestrator = get_orchestrator()
        
        # Parse time range
        if preset:
            time_range = TimeRange.from_preset(preset)
        elif start_date and end_date:
            time_range = TimeRange.from_iso_strings(start_date, end_date)
        else:
            # Default to last 30 days
            time_range = TimeRange.from_preset("last_30_days")
        
        logger.info(f"Getting time series for stat_id='{stat_id}', preset='{preset}', granularity='{granularity}'")
        
        time_series = orchestrator.get_time_series(stat_id, time_range, granularity)
        
        logger.info(f"Time series has {len(time_series.get('series', {}))} data points")
        
        return time_series
    except ValueError as e:
        logger.error(f"Invalid parameters: {e}")
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"Error getting time series: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/stats/{category}")
async def get_stats_by_category(category: str) -> Dict[str, Any]:
    """Get statistics for a specific category."""
    try:
        orchestrator = get_orchestrator()
        all_stats = orchestrator.calculate_all_stats()
        
        if category not in all_stats:
            raise HTTPException(
                status_code=404,
                detail=f"Category '{category}' not found. Available: {list(all_stats.keys())}"
            )
        
        return all_stats[category]
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting stats for category {category}: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/stats/{category}/{stat_id}")
async def get_single_stat(category: str, stat_id: str) -> Dict[str, Any]:
    """Get a single statistic by category and ID."""
    try:
        orchestrator = get_orchestrator()
        all_stats = orchestrator.calculate_all_stats()
        
        if category not in all_stats:
            raise HTTPException(status_code=404, detail=f"Category '{category}' not found")
        
        category_stats = all_stats[category]
        if stat_id not in category_stats:
            raise HTTPException(status_code=404, detail=f"Stat '{stat_id}' not found in category '{category}'")
        
        return category_stats[stat_id]
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting stat {category}/{stat_id}: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/cache/clear")
async def clear_cache():
    """Clear the stats cache and force refresh."""
    try:
        orchestrator = get_orchestrator()
        orchestrator.invalidate_cache()
        return {"status": "ok", "message": "Cache cleared successfully"}
    except Exception as e:
        logger.error(f"Error clearing cache: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/time-range/presets")
async def get_time_range_presets() -> Dict[str, Any]:
    """Get available time range presets."""
    return {
        "presets": [
            {"id": "today", "label": "Today"},
            {"id": "yesterday", "label": "Yesterday"},
            {"id": "last_7_days", "label": "Last 7 Days"},
            {"id": "last_30_days", "label": "Last 30 Days"},
            {"id": "last_90_days", "label": "Last 90 Days"},
            {"id": "this_week", "label": "This Week"},
            {"id": "this_month", "label": "This Month"},
            {"id": "last_month", "label": "Last Month"},
            {"id": "this_quarter", "label": "This Quarter"},
            {"id": "this_year", "label": "This Year"},
            {"id": "all_time", "label": "All Time"}
        ]
    }


@app.get("/api/messages")
async def get_messages(
    page: int = Query(1, ge=1, description="Page number (1-indexed)"),
    limit: int = Query(20, ge=1, le=100, description="Items per page"),
    sort: str = Query("recent", description="Sort order: recent, oldest, longest, shortest"),
    message_type: Optional[str] = Query(None, description="Filter by type: user, ai, all"),
    has_code: Optional[bool] = Query(None, description="Filter messages with code blocks"),
    has_thinking: Optional[bool] = Query(None, description="Filter messages with thinking"),
    has_tools: Optional[bool] = Query(None, description="Filter messages with tool usage"),
    session_id: Optional[str] = Query(None, description="Filter by session ID"),
    search: Optional[str] = Query(None, description="Search in message text"),
    start_date: Optional[str] = Query(None, description="Start date filter"),
    end_date: Optional[str] = Query(None, description="End date filter"),
) -> Dict[str, Any]:
    """Get paginated list of messages with filters and sorting."""
    try:
        orchestrator = get_orchestrator()
        
        # Get all messages
        messages = orchestrator.messages
        logger.info(f"Raw messages before consolidation: {len(messages)}")
        
        # Try to consolidate AI message fragments into logical conversation turns
        try:
            consolidated_messages = MessageConsolidator.consolidate(messages)
            logger.info(f"Consolidated messages: {len(consolidated_messages)}")
            messages_to_use = consolidated_messages if consolidated_messages else messages
        except Exception as e:
            logger.error(f"Consolidation failed, using raw messages: {e}", exc_info=True)
            messages_to_use = messages
        
        # Apply filters
        filtered_messages = messages_to_use
        
        # Filter by time range
        if start_date and end_date:
            time_range = TimeRange.from_iso_strings(start_date, end_date)
            from stats.filters.temporal_filter import TemporalFilter
            filtered_messages = TemporalFilter.filter_messages(filtered_messages, time_range)
        
        # Filter by type
        if message_type == "user":
            filtered_messages = [m for m in filtered_messages if m.is_user_message]
        elif message_type == "ai":
            filtered_messages = [m for m in filtered_messages if m.is_ai_message]
        
        # Filter by features
        if has_code is not None:
            filtered_messages = [m for m in filtered_messages if m.has_code == has_code]
        if has_thinking is not None:
            filtered_messages = [m for m in filtered_messages if m.has_thinking == has_thinking]
        if has_tools is not None:
            filtered_messages = [m for m in filtered_messages if m.has_tools == has_tools]
        
        # Filter by session
        if session_id:
            filtered_messages = [m for m in filtered_messages if m.composer_id == session_id]
        
        # Search in text
        if search:
            search_lower = search.lower()
            filtered_messages = [
                m for m in filtered_messages 
                if m.text and search_lower in m.text.lower()
            ]
        
        # Sort
        if sort == "recent":
            filtered_messages.sort(key=lambda m: m.created_at, reverse=True)
        elif sort == "oldest":
            filtered_messages.sort(key=lambda m: m.created_at)
        elif sort == "longest":
            filtered_messages.sort(key=lambda m: m.get_text_length(), reverse=True)
        elif sort == "shortest":
            filtered_messages.sort(key=lambda m: m.get_text_length())
        
        # Pagination
        total_count = len(filtered_messages)
        start_idx = (page - 1) * limit
        end_idx = start_idx + limit
        page_messages = filtered_messages[start_idx:end_idx]
        
        # Convert to dict for JSON serialization
        messages_data = []
        for msg in page_messages:
            messages_data.append({
                'id': msg.bubble_id,
                'session_id': msg.composer_id,
                'type': 'user' if msg.is_user_message else 'ai',
                'created_at': msg.created_at.isoformat(),
                'text': msg.text,
                'text_preview': msg.text[:200] if msg.text else None,
                'word_count': msg.get_text_word_count(),
                'has_code': msg.has_code,
                'has_thinking': msg.has_thinking,
                'has_tools': msg.has_tools,
                'code_block_count': msg.get_code_block_count(),
                'tool_count': msg.get_tool_count(),
                'token_count': msg.get_total_tokens(),
            })
        
        return {
            'messages': messages_data,
            'pagination': {
                'page': page,
                'limit': limit,
                'total_count': total_count,
                'total_pages': (total_count + limit - 1) // limit,
                'has_next': end_idx < total_count,
                'has_prev': page > 1
            },
            'filters': {
                'sort': sort,
                'message_type': message_type,
                'has_code': has_code,
                'has_thinking': has_thinking,
                'has_tools': has_tools,
                'session_id': session_id,
                'search': search
            }
        }
    except Exception as e:
        logger.error(f"Error getting messages: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/messages/{message_id}")
async def get_message_detail(message_id: str) -> Dict[str, Any]:
    """Get detailed information about a specific message."""
    try:
        orchestrator = get_orchestrator()
        
        # Get and consolidate messages
        messages = orchestrator.messages
        
        try:
            consolidated_messages = MessageConsolidator.consolidate(messages)
            messages_to_search = consolidated_messages if consolidated_messages else messages
        except Exception as e:
            logger.error(f"Consolidation failed in detail endpoint: {e}")
            messages_to_search = messages
        
        # Find the message (could be consolidated, so check for fragment IDs too)
        message = None
        for msg in messages_to_search:
            if msg.bubble_id == message_id:
                message = msg
                break
            # Check if this message_id is one of the fragments
            if msg.raw_data and isinstance(msg.raw_data, dict):
                fragment_ids = msg.raw_data.get('fragment_ids', [])
                if message_id in fragment_ids:
                    message = msg
                    break
        
        if not message:
            raise HTTPException(status_code=404, detail=f"Message {message_id} not found")
        
        # Get session info
        sessions = orchestrator.sessions
        session = next((s for s in sessions if s.composer_id == message.composer_id), None)
        
        # Get workspace info (if available)
        workspaces = orchestrator._workspaces if orchestrator._workspaces else []
        
        # Build detailed response
        return {
            'id': message.bubble_id,
            'session_id': message.composer_id,
            'session_name': session.name if session else None,
            'type': 'user' if message.is_user_message else 'ai',
            'created_at': message.created_at.isoformat(),
            'text': message.text,
            'word_count': message.get_text_word_count(),
            'char_count': message.get_text_length(),
            
            # Code blocks
            'code_blocks': message.code_blocks,
            'suggested_code_blocks': message.suggested_code_blocks,
            'code_block_count': message.get_code_block_count(),
            'code_line_count': message.get_code_line_count(),
            
            # Thinking
            'thinking': message.thinking,
            'thinking_duration_ms': message.thinking_duration_ms,
            'has_thinking': message.has_thinking,
            
            # Tools
            'tool_results': message.tool_results,
            'tool_count': message.get_tool_count(),
            'tool_types': message.get_tool_types(),
            
            # Context
            'attached_code_chunks': message.attached_code_chunks,
            'codebase_context_chunks': message.codebase_context_chunks,
            'context_chunk_count': message.get_context_chunk_count(),
            
            # References
            'web_references': message.web_references,
            'docs_references': message.docs_references,
            
            # Model & Tokens
            'model_info': message.model_info,
            'model_name': message.get_model_name(),
            'token_count': message.token_count,
            'input_tokens': message.get_input_tokens(),
            'output_tokens': message.get_output_tokens(),
            'total_tokens': message.get_total_tokens(),
            
            # Mode
            'is_agentic': message.is_agentic,
            'capabilities': message.capabilities,
            
            # Session context
            'session_info': {
                'name': session.name if session else None,
                'created_at': session.created_at.isoformat() if session else None,
                'duration_minutes': round(session.duration_minutes, 1) if session else None,
                'total_lines_added': session.total_lines_added if session else 0,
                'total_lines_removed': session.total_lines_removed if session else 0,
            } if session else None,
            
            # Raw data (for toggle view)
            'raw_data': message.raw_data
        }
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting message detail: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    import uvicorn
    
    logger.info("Starting Cursor Stats API server...")
    uvicorn.run(
        app,
        host="127.0.0.1",
        port=8000,
        log_level="info"
    )

