"""Cursor Stats Dashboard - Main Application

A comprehensive dashboard for analyzing Cursor IDE usage data.
"""

import streamlit as st
import sys
from pathlib import Path

# Add paths
STREAMLIT_APP_DIR = Path(__file__).parent
PROJECT_ROOT = STREAMLIT_APP_DIR.parent

sys.path.insert(0, str(PROJECT_ROOT))
sys.path.insert(0, str(STREAMLIT_APP_DIR))

# Now import from streamlit_app modules
import config
from utils.data_loader import get_summary_stats, clear_cache

# Page config
st.set_page_config(
    page_title=config.APP_TITLE,
    page_icon=config.APP_ICON,
    layout=config.LAYOUT,
    initial_sidebar_state=config.INITIAL_SIDEBAR_STATE
)

# Custom CSS for better UI/UX
st.markdown("""
<style>
    /* Main content area */
    .main {
        padding-top: 2rem;
    }
    
    /* Metric cards */
    [data-testid="stMetricValue"] {
        font-size: 2rem;
        font-weight: 600;
    }
    
    [data-testid="stMetricLabel"] {
        font-size: 0.9rem;
        font-weight: 500;
        color: #6B7280;
    }
    
    /* Headers */
    h1 {
        color: #1F2937;
        font-weight: 700;
    }
    
    h2 {
        color: #374151;
        font-weight: 600;
        margin-top: 2rem;
    }
    
    h3 {
        color: #4B5563;
        font-weight: 600;
    }
    
    /* Cards */
    .stat-card {
        background: white;
        border-radius: 0.5rem;
        padding: 1.5rem;
        box-shadow: 0 1px 3px 0 rgba(0, 0, 0, 0.1);
        margin-bottom: 1rem;
    }
    
    /* Tables */
    .dataframe {
        font-size: 0.9rem;
    }
    
    /* Sidebar */
    [data-testid="stSidebar"] {
        background-color: #F9FAFB;
    }
    
    /* Buttons */
    .stButton>button {
        border-radius: 0.375rem;
        font-weight: 500;
    }
    
    /* Expanders */
    .streamlit-expanderHeader {
        font-weight: 600;
        color: #374151;
    }
</style>
""", unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.title(f"{config.APP_ICON} {config.APP_TITLE}")
    st.markdown("---")
    
    # Database info
    st.subheader("📁 Database")
    if config.DB_PATH.exists():
        st.success("✓ Connected")
        db_size_mb = config.DB_PATH.stat().st_size / (1024**2)
        st.caption(f"Size: {db_size_mb:.0f} MB")
    else:
        st.error("✗ Not found")
        st.caption(f"Path: {config.DB_PATH}")
    
    st.markdown("---")
    
    # Quick stats
    st.subheader("📊 Quick Stats")
    with st.spinner("Loading..."):
        try:
            summary = get_summary_stats()
            
            st.metric("Messages", f"{summary['total_messages']:,}")
            st.metric("Sessions", f"{summary['total_sessions']:,}")
            st.metric("Tool Calls", f"{int(summary['total_tools']):,}")
            st.metric("Success Rate", f"{summary['tool_success_rate']:.1f}%")
            
        except Exception as e:
            st.error(f"Error loading stats: {str(e)}")
    
    st.markdown("---")
    
    # Actions
    st.subheader("⚙️ Actions")
    if st.button("🔄 Refresh Data", use_container_width=True):
        clear_cache()
        st.rerun()
    
    if st.button("ℹ️ About", use_container_width=True):
        st.info("""
        **Cursor Stats Dashboard**
        
        Analyze your Cursor IDE usage with comprehensive statistics and visualizations.
        
        **Features:**
        - 139 calculated statistics
        - Interactive charts
        - Search & filter
        - Export capabilities
        
        **Data Sources:**
        - Messages & sessions
        - Tool usage
        - Code changes
        - Context data
        """)

# Main content
def main():
    """Main application content."""
    st.title(f"{config.APP_ICON} Welcome to Cursor Stats Dashboard")
    
    st.markdown("""
    ### Analyze your Cursor IDE usage with detailed insights
    
    This dashboard provides comprehensive analytics across 6 major categories:
    """)
    
    # Feature cards
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        #### 📊 Overview
        High-level summary and key metrics at a glance.
        """)
    
    with col2:
        st.markdown("""
        #### 🔍 Browse
        Search and filter through all your messages and sessions.
        """)
    
    with col3:
        st.markdown("""
        #### 📈 Stats
        Explore all 139 calculated statistics in detail.
        """)
    
    col4, col5, col6 = st.columns(3)
    
    with col4:
        st.markdown("""
        #### 📉 Analytics
        Interactive charts and visualizations of your data.
        """)
    
    with col5:
        st.markdown("""
        #### 📅 Calendar
        Timeline view of your activity patterns.
        """)
    
    with col6:
        st.markdown("""
        #### 🧠 Intelligence
        Actionable insights and recommendations.
        """)
    
    st.markdown("---")
    
    # Getting started
    st.subheader("🚀 Getting Started")
    st.markdown("""
    1. **Navigate** using the sidebar menu or the pages above
    2. **Explore** your stats across different categories
    3. **Filter** and search to find specific insights
    4. **Export** your data in multiple formats
    
    👈 **Start exploring from the sidebar!**
    """)
    
    # Quick preview
    st.markdown("---")
    st.subheader("📊 Quick Preview")
    
    try:
        with st.spinner("Loading preview..."):
            summary = get_summary_stats()
            
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.metric(
                    "Total Messages",
                    f"{summary['total_messages']:,}",
                    help="Total number of messages extracted"
                )
            
            with col2:
                st.metric(
                    "Sessions",
                    f"{summary['total_sessions']:,}",
                    help="Total number of conversation sessions"
                )
            
            with col3:
                st.metric(
                    "Tool Invocations",
                    f"{int(summary['total_tools']):,}",
                    help="Total times tools were used"
                )
            
            with col4:
                success_rate = summary['tool_success_rate']
                st.metric(
                    "Tool Success Rate",
                    f"{success_rate:.1f}%",
                    help="Percentage of successful tool calls"
                )
        
        st.success("✓ Data loaded successfully! Ready to explore.")
        
    except Exception as e:
        st.error(f"⚠️ Error loading preview: {str(e)}")
        st.info("Please check your database connection and try refreshing.")


if __name__ == "__main__":
    main()

