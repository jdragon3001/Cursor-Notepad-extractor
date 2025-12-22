"""Data loading utilities."""

import streamlit as st
from pathlib import Path
import sys

# Add project root to path
PROJECT_ROOT = Path(__file__).parent.parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from stats.orchestrator import StatsOrchestrator

# Import config from streamlit_app
sys.path.insert(0, str(Path(__file__).parent.parent))
from config import DB_PATH, CACHE_TTL


@st.cache_resource(ttl=CACHE_TTL)
def get_orchestrator():
    """Get cached orchestrator instance."""
    return StatsOrchestrator(DB_PATH)


@st.cache_data(ttl=CACHE_TTL)
def load_all_data():
    """Load and cache all extracted data."""
    orchestrator = get_orchestrator()
    orchestrator.extract_all_data()
    
    return {
        'messages': orchestrator._messages,
        'sessions': orchestrator._sessions,
        'code_diffs': orchestrator._code_diffs,
        'tracking_lines': orchestrator._tracking_lines,
        'daily_stats': orchestrator._daily_stats,
        'request_contexts': orchestrator._request_contexts,
        'workspaces': orchestrator._workspaces,
    }


@st.cache_data(ttl=CACHE_TTL)
def load_all_stats():
    """Load and cache all calculated stats."""
    orchestrator = get_orchestrator()
    return orchestrator.calculate_all_stats()


@st.cache_data(ttl=CACHE_TTL)
def get_summary_stats():
    """Get quick summary statistics."""
    data = load_all_data()
    stats = load_all_stats()
    
    return {
        'total_messages': len(data['messages']),
        'total_sessions': len(data['sessions']),
        'total_code_diffs': len(data['code_diffs']),
        'total_tools': stats.get('tools', {}).get('total_tool_invocations', {}).get('value', 0),
        'tool_success_rate': stats.get('tools', {}).get('tool_success_rate', {}).get('value', 0),
        'total_contexts': len(data['request_contexts']),
    }


def clear_cache():
    """Clear all cached data."""
    st.cache_data.clear()
    st.cache_resource.clear()

