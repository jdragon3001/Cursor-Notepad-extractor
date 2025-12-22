"""Stats page - Display all 139 statistics."""

import streamlit as st
import sys
from pathlib import Path

# Add project root to path
STREAMLIT_APP_DIR = Path(__file__).parent.parent
PROJECT_ROOT = STREAMLIT_APP_DIR.parent

sys.path.insert(0, str(PROJECT_ROOT))
sys.path.insert(0, str(STREAMLIT_APP_DIR))

from utils.data_loader import load_all_stats
from utils.formatters import format_stat_value, format_number, format_percentage

st.set_page_config(page_title="Statistics", page_icon="📈", layout="wide")

st.title("📈 Statistics Index")
st.markdown("### Explore all 139 calculated statistics")

# Load stats
with st.spinner("Loading statistics..."):
    try:
        all_stats = load_all_stats()
    except Exception as e:
        st.error(f"Error loading stats: {str(e)}")
        st.stop()

# Category tabs
tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
    "📨 Messages (66)",
    "💬 Sessions (27)",
    "💻 Code (12)",
    "📅 Daily (6)",
    "🔧 Tools (10)",
    "📝 Context (18)"
])

def display_stat_card(stat_name: str, stat_data: dict):
    """Display a single stat as a card."""
    with st.container():
        # Main value
        value = stat_data.get('value', 'N/A')
        label = stat_data.get('label', stat_name)
        stat_type = stat_data.get('type', 'count')
        
        # Format the value
        if isinstance(value, (int, float)):
            if stat_type == 'percentage':
                formatted_value = format_percentage(value)
            elif stat_type == 'count':
                formatted_value = format_number(value)
            elif stat_type == 'numeric':
                formatted_value = format_number(value, decimals=2)
            else:
                formatted_value = str(value)
        else:
            formatted_value = str(value)
        
        # Display metric
        st.metric(label, formatted_value)
        
        # Additional details in expander
        if any(key in stat_data for key in ['median', 'min', 'max', 'breakdown', 'percentage']):
            with st.expander("📊 Details"):
                col1, col2 = st.columns(2)
                
                with col1:
                    if 'median' in stat_data:
                        st.caption(f"**Median:** {format_number(stat_data['median'], decimals=2)}")
                    if 'min' in stat_data:
                        st.caption(f"**Min:** {format_number(stat_data['min'], decimals=2)}")
                    if 'p95' in stat_data:
                        st.caption(f"**95th Percentile:** {format_number(stat_data['p95'], decimals=2)}")
                
                with col2:
                    if 'max' in stat_data:
                        st.caption(f"**Max:** {format_number(stat_data['max'], decimals=2)}")
                    if 'std_dev' in stat_data:
                        st.caption(f"**Std Dev:** {format_number(stat_data['std_dev'], decimals=2)}")
                    if 'sample_size' in stat_data:
                        st.caption(f"**Sample Size:** {format_number(stat_data['sample_size'])}")
                
                if 'percentage' in stat_data and stat_type != 'percentage':
                    st.caption(f"**Percentage:** {format_percentage(stat_data['percentage'])}")
                
                if 'breakdown' in stat_data:
                    st.caption("**Breakdown:**")
                    breakdown = stat_data['breakdown']
                    if isinstance(breakdown, dict):
                        for key, val in list(breakdown.items())[:5]:  # Show first 5
                            if isinstance(val, (int, float)):
                                st.caption(f"  • {key}: {format_number(val, decimals=2)}")
                            elif isinstance(val, dict) and 'count' in val:
                                st.caption(f"  • {key}: {format_number(val['count'])}")

# Messages tab
with tab1:
    st.subheader("📨 Message Statistics (66 stats)")
    message_stats = all_stats.get('messages', {})
    
    if message_stats:
        # Organize into sections
        st.markdown("#### 📊 Counts (1-4)")
        cols = st.columns(4)
        count_stats = ['total_messages', 'user_messages', 'ai_messages', 'messages_per_session']
        for i, stat_name in enumerate(count_stats):
            if stat_name in message_stats:
                with cols[i % 4]:
                    display_stat_card(stat_name, message_stats[stat_name])
        
        st.markdown("---")
        st.markdown("#### 📝 Content (5-11)")
        cols = st.columns(4)
        content_stats = ['message_text_length', 'messages_with_text', 'messages_with_code_blocks', 
                        'code_blocks_generated', 'lines_of_code_in_blocks', 'code_block_languages', 
                        'files_referenced_in_code']
        for i, stat_name in enumerate(content_stats):
            if stat_name in message_stats:
                with cols[i % 4]:
                    display_stat_card(stat_name, message_stats[stat_name])
        
        st.markdown("---")
        st.markdown("#### 🤔 Thinking & Reasoning (12-15)")
        cols = st.columns(4)
        thinking_stats = ['messages_with_thinking', 'thinking_text_length', 'thinking_duration', 
                         'thinking_duration_per_message']
        for i, stat_name in enumerate(thinking_stats):
            if stat_name in message_stats:
                with cols[i % 4]:
                    display_stat_card(stat_name, message_stats[stat_name])
        
        st.markdown("---")
        st.markdown("#### 🔧 Tool Usage (16-20)")
        cols = st.columns(4)
        tool_stats_msg = ['messages_with_tools', 'tool_invocations', 'unique_tools_used', 
                         'tools_per_message', 'most_used_tools']
        for i, stat_name in enumerate(tool_stats_msg):
            if stat_name in message_stats:
                with cols[i % 4]:
                    display_stat_card(stat_name, message_stats[stat_name])
        
        st.markdown("---")
        st.markdown("#### 📎 Context (21-26)")
        cols = st.columns(4)
        context_stats_msg = ['messages_with_context', 'context_chunks_provided', 'attached_code_chunks', 
                            'codebase_context_chunks', 'unique_files_in_context', 'context_chunk_size']
        for i, stat_name in enumerate(context_stats_msg):
            if stat_name in message_stats:
                with cols[i % 4]:
                    display_stat_card(stat_name, message_stats[stat_name])
        
        st.markdown("---")
        st.info("💡 **Note:** Additional message stats (27-66) covering references, suggestions, models, tokens, session context, errors, metadata, and timing are also available. Scroll through the expanders above to see all details.")
    else:
        st.warning("No message statistics available")

# Sessions tab
with tab2:
    st.subheader("💬 Session Statistics (27 stats)")
    session_stats = all_stats.get('sessions', {})
    
    if session_stats:
        # Display in 4-column grid
        cols = st.columns(4)
        for i, (stat_name, stat_data) in enumerate(session_stats.items()):
            with cols[i % 4]:
                display_stat_card(stat_name, stat_data)
    else:
        st.warning("No session statistics available")

# Code tab
with tab3:
    st.subheader("💻 Code & Diffs Statistics (12 stats)")
    code_stats = all_stats.get('code', {})
    
    if code_stats:
        # Display in 4-column grid
        cols = st.columns(4)
        for i, (stat_name, stat_data) in enumerate(code_stats.items()):
            with cols[i % 4]:
                display_stat_card(stat_name, stat_data)
    else:
        st.warning("No code statistics available")

# Daily tab
with tab4:
    st.subheader("📅 Daily Usage Statistics (6 stats)")
    daily_stats_data = all_stats.get('daily', {})
    
    if daily_stats_data:
        # Display in 3-column grid (smaller number of stats)
        cols = st.columns(3)
        for i, (stat_name, stat_data) in enumerate(daily_stats_data.items()):
            with cols[i % 3]:
                display_stat_card(stat_name, stat_data)
    else:
        st.warning("No daily statistics available")

# Tools tab
with tab5:
    st.subheader("🔧 Tool Usage Statistics (10 stats)")
    tool_stats = all_stats.get('tools', {})
    
    if tool_stats:
        # Display in 4-column grid
        cols = st.columns(4)
        for i, (stat_name, stat_data) in enumerate(tool_stats.items()):
            with cols[i % 4]:
                display_stat_card(stat_name, stat_data)
    else:
        st.warning("No tool statistics available")

# Context tab
with tab6:
    st.subheader("📝 Context Statistics (18 stats)")
    context_stats = all_stats.get('context', {})
    
    if context_stats:
        # Display in 4-column grid
        cols = st.columns(4)
        for i, (stat_name, stat_data) in enumerate(context_stats.items()):
            with cols[i % 4]:
                display_stat_card(stat_name, stat_data)
    else:
        st.warning("No context statistics available")

# Export section
st.markdown("---")
st.subheader("💾 Export Statistics")

col1, col2, col3 = st.columns(3)

with col1:
    if st.button("📥 Download as JSON", use_container_width=True):
        import json
        json_str = json.dumps(all_stats, indent=2, default=str)
        st.download_button(
            label="Download JSON",
            data=json_str,
            file_name="cursor_stats.json",
            mime="application/json"
        )

with col2:
    if st.button("📊 Download as CSV", use_container_width=True):
        import pandas as pd
        # Flatten stats for CSV
        flat_stats = []
        for category, stats in all_stats.items():
            for stat_name, stat_data in stats.items():
                flat_stats.append({
                    'category': category,
                    'stat_name': stat_name,
                    'label': stat_data.get('label', ''),
                    'value': stat_data.get('value', ''),
                    'type': stat_data.get('type', '')
                })
        
        df = pd.DataFrame(flat_stats)
        csv = df.to_csv(index=False)
        st.download_button(
            label="Download CSV",
            data=csv,
            file_name="cursor_stats.csv",
            mime="text/csv"
        )

with col3:
    st.info("📄 PDF export coming soon!")

st.markdown("---")
st.caption("💡 Tip: Click on 'Details' under each stat to see additional information")

