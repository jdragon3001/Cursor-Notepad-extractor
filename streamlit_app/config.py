"""Streamlit app configuration."""

from pathlib import Path

# App metadata
APP_TITLE = "Cursor Stats Dashboard"
APP_ICON = "📊"
LAYOUT = "wide"
INITIAL_SIDEBAR_STATE = "expanded"

# Paths
PROJECT_ROOT = Path(__file__).parent.parent
DB_PATH = Path.home() / "AppData" / "Roaming" / "Cursor" / "User" / "globalStorage" / "state.vscdb"

# Theme colors
PRIMARY_COLOR = "#4F46E5"  # Indigo
SECONDARY_COLOR = "#10B981"  # Green
ACCENT_COLOR = "#F59E0B"  # Amber
ERROR_COLOR = "#EF4444"  # Red
TEXT_COLOR = "#1F2937"  # Gray-800

# Chart settings
CHART_HEIGHT = 400
CHART_HEIGHT_SMALL = 250
CHART_TEMPLATE = "plotly_white"

# Pagination
ITEMS_PER_PAGE = 50

# Cache TTL (seconds)
CACHE_TTL = 300  # 5 minutes

