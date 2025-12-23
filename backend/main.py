"""FastAPI backend server for Cursor Stats Dashboard."""

import sys
import logging
from pathlib import Path
from typing import Dict, Any, List, Optional

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

# Add parent directory to path to import stats modules
sys.path.insert(0, str(Path(__file__).parent.parent))

from stats import StatsOrchestrator
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
            # Get global database path
            user_home = Path.home()
            db_path = user_home / "AppData" / "Roaming" / "Cursor" / "User" / "globalStorage" / Config.DB_FILENAME
            
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
async def get_all_stats() -> Dict[str, Any]:
    """Get all calculated statistics."""
    try:
        orchestrator = get_orchestrator()
        stats = orchestrator.calculate_all_stats()
        return stats
    except Exception as e:
        logger.error(f"Error calculating stats: {e}")
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


if __name__ == "__main__":
    import uvicorn
    
    logger.info("Starting Cursor Stats API server...")
    uvicorn.run(
        app,
        host="127.0.0.1",
        port=8000,
        log_level="info"
    )

