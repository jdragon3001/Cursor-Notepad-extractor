"""Overview page - High-level summary and key metrics."""

import streamlit as st
import sys
from pathlib import Path
import pandas as pd
from datetime import datetime, timedelta

# Add project root to path
STREAMLIT_APP_DIR = Path(__file__).parent.parent
PROJECT_ROOT = STREAMLIT_APP_DIR.parent

sys.path.insert(0, str(PROJECT_ROOT))
sys.path.insert(0, str(STREAMLIT_APP_DIR))

from utils.data_loader import load_all_data, load_all_stats
from utils.formatters import format_number, format_percentage, format_duration
from utils.chart_builder import create_line_chart, create_bar_chart, create_pie_chart

st.set_page_config(page_title="Overview", page_icon="📊", layout="wide")

st.title("📊 Overview")
st.markdown("### High-level summary of your Cursor usage")

# Load data
with st.spinner("Loading data..."):
    try:
        data = load_all_data()
        stats = load_all_stats()
        
        messages = data['messages']
        sessions = data['sessions']
        
        # Extract stats
        message_stats = stats.get('messages', {})
        session_stats = stats.get('sessions', {})
        tool_stats = stats.get('tools', {})
        code_stats = stats.get('code', {})
        daily_stats = stats.get('daily', {})
        context_stats = stats.get('context', {})
        
    except Exception as e:
        st.error(f"Error loading data: {str(e)}")
        st.stop()

# Key metrics at the top
st.markdown("---")
st.subheader("🎯 Key Metrics")

col1, col2, col3, col4, col5 = st.columns(5)

with col1:
    total_msgs = message_stats.get('total_messages', {}).get('value', 0)
    st.metric(
        "Total Messages",
        format_number(total_msgs),
        help="All messages exchanged with Cursor AI"
    )

with col2:
    total_sessions = session_stats.get('total_sessions', {}).get('value', 0)
    st.metric(
        "Sessions",
        format_number(total_sessions),
        help="Conversation sessions"
    )

with col3:
    total_tools = tool_stats.get('total_tool_invocations', {}).get('value', 0)
    st.metric(
        "Tool Calls",
        format_number(total_tools),
        help="Total tool invocations"
    )

with col4:
    success_rate = tool_stats.get('tool_success_rate', {}).get('value', 0)
    st.metric(
        "Success Rate",
        format_percentage(success_rate),
        help="Tool call success percentage"
    )

with col5:
    total_code_lines = code_stats.get('total_lines_added', {}).get('value', 0)
    st.metric(
        "Lines Added",
        format_number(total_code_lines),
        help="Total lines of code added"
    )

# Secondary metrics
st.markdown("---")
st.subheader("📈 Usage Breakdown")

col1, col2, col3, col4 = st.columns(4)

with col1:
    user_msgs = message_stats.get('user_messages', {}).get('value', 0)
    user_pct = message_stats.get('user_messages', {}).get('percentage', 0)
    st.metric(
        "User Messages",
        format_number(user_msgs),
        delta=f"{user_pct:.1f}% of total",
        help="Messages sent by you"
    )

with col2:
    ai_msgs = message_stats.get('ai_messages', {}).get('value', 0)
    ai_pct = message_stats.get('ai_messages', {}).get('percentage', 0)
    st.metric(
        "AI Messages",
        format_number(ai_msgs),
        delta=f"{ai_pct:.1f}% of total",
        help="Messages from Cursor AI"
    )

with col3:
    msgs_with_code = message_stats.get('messages_with_code_blocks', {}).get('value', 0)
    code_pct = message_stats.get('messages_with_code_blocks', {}).get('percentage', 0)
    st.metric(
        "Messages with Code",
        format_number(msgs_with_code),
        delta=f"{code_pct:.1f}% of total",
        help="Messages containing code blocks"
    )

with col4:
    msgs_with_thinking = message_stats.get('messages_with_thinking', {}).get('value', 0)
    thinking_pct = message_stats.get('messages_with_thinking', {}).get('percentage', 0)
    st.metric(
        "Messages with Thinking",
        format_number(msgs_with_thinking),
        delta=f"{thinking_pct:.1f}% of total",
        help="AI messages with extended reasoning"
    )

# Charts section
st.markdown("---")
st.subheader("📊 Visual Insights")

# Top row: 2 charts
col1, col2 = st.columns(2)

with col1:
    # Message type distribution
    st.markdown("#### Message Type Distribution")
    msg_labels = ['User Messages', 'AI Messages']
    msg_values = [user_msgs, ai_msgs]
    fig = create_pie_chart(msg_labels, msg_values, "", height=300)
    st.plotly_chart(fig, use_container_width=True)

with col2:
    # Tool usage by status
    st.markdown("#### Tool Usage by Status")
    tool_status = tool_stats.get('tool_status_distribution', {}).get('breakdown', {})
    if tool_status:
        status_labels = list(tool_status.keys())
        status_values = [tool_status[s]['count'] for s in status_labels]
        fig = create_pie_chart(status_labels, status_values, "", height=300)
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("No tool status data available")

# Top tools used
st.markdown("---")
st.subheader("🔧 Top Tools Used")

most_used_tools = tool_stats.get('most_used_tools', {}).get('breakdown', {}).get('top_10', [])
if most_used_tools:
    # Create DataFrame
    tools_df = pd.DataFrame(most_used_tools)
    tools_df = tools_df.head(10)  # Top 10
    
    # Create horizontal bar chart
    fig = create_bar_chart(
        tools_df,
        x='count',
        y='tool',
        title="",
        horizontal=True,
        height=400
    )
    st.plotly_chart(fig, use_container_width=True)
else:
    st.info("No tool usage data available")

# Session insights
st.markdown("---")
st.subheader("💬 Session Insights")

col1, col2, col3 = st.columns(3)

with col1:
    avg_msgs_per_session = session_stats.get('messages_per_session', {}).get('value', 0)
    median_msgs = session_stats.get('messages_per_session', {}).get('median', 0)
    st.metric(
        "Avg Messages/Session",
        format_number(avg_msgs_per_session, decimals=1),
        delta=f"Median: {format_number(median_msgs)}",
        help="Average messages per session"
    )

with col2:
    avg_duration = session_stats.get('average_session_duration', {}).get('value', 0)
    st.metric(
        "Avg Session Duration",
        format_duration(avg_duration),
        help="Average time spent per session"
    )

with col3:
    active_sessions = session_stats.get('active_sessions', {}).get('value', 0)
    active_pct = session_stats.get('active_sessions', {}).get('percentage', 0)
    st.metric(
        "Active Sessions",
        format_number(active_sessions),
        delta=f"{active_pct:.1f}% of total",
        help="Sessions that are currently active"
    )

# Code insights
st.markdown("---")
st.subheader("💻 Code Activity")

col1, col2, col3, col4 = st.columns(4)

with col1:
    lines_added = code_stats.get('total_lines_added', {}).get('value', 0)
    st.metric(
        "Lines Added",
        format_number(lines_added),
        help="Total lines of code added"
    )

with col2:
    lines_removed = code_stats.get('total_lines_removed', {}).get('value', 0)
    st.metric(
        "Lines Removed",
        format_number(lines_removed),
        help="Total lines of code removed"
    )

with col3:
    net_lines = code_stats.get('net_lines_changed', {}).get('value', 0)
    st.metric(
        "Net Change",
        format_number(net_lines),
        delta="+" if net_lines > 0 else "",
        help="Net lines added (added - removed)"
    )

with col4:
    total_diffs = code_stats.get('total_diffs', {}).get('value', 0)
    st.metric(
        "Code Diffs",
        format_number(total_diffs),
        help="Total code modifications"
    )

# Context insights
st.markdown("---")
st.subheader("📝 Context & Environment")

col1, col2, col3, col4 = st.columns(4)

with col1:
    contexts_with_lints = context_stats.get('contexts_with_linter_errors', {}).get('value', 0)
    st.metric(
        "Linter Errors",
        format_number(contexts_with_lints),
        help="Contexts with linter errors"
    )

with col2:
    contexts_with_todos = context_stats.get('contexts_with_todos', {}).get('value', 0)
    st.metric(
        "TODOs",
        format_number(contexts_with_todos),
        help="Contexts with TODO items"
    )

with col3:
    contexts_with_git = context_stats.get('contexts_with_git_changes', {}).get('value', 0)
    st.metric(
        "Git Changes",
        format_number(contexts_with_git),
        help="Contexts with git modifications"
    )

with col4:
    contexts_with_files = context_stats.get('contexts_with_file_context', {}).get('value', 0)
    st.metric(
        "File Context",
        format_number(contexts_with_files),
        help="Contexts with file information"
    )

# Footer
st.markdown("---")
st.caption("💡 Tip: Use the sidebar to navigate to other pages for detailed analysis")

