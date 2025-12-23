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


if __name__ == "__main__":
    import uvicorn
    
    logger.info("Starting Cursor Stats API server...")
    uvicorn.run(
        app,
        host="127.0.0.1",
        port=8000,
        log_level="info"
    )

