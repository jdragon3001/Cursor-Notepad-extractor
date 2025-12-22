"""Chart building utilities."""

import plotly.graph_objects as go
import plotly.express as px
from typing import List, Dict, Any
import pandas as pd
import sys
from pathlib import Path

# Add streamlit_app to path for config
sys.path.insert(0, str(Path(__file__).parent.parent))
from config import CHART_HEIGHT, CHART_HEIGHT_SMALL, CHART_TEMPLATE, PRIMARY_COLOR, SECONDARY_COLOR


def create_line_chart(data: pd.DataFrame, x: str, y: str, title: str, height: int = CHART_HEIGHT) -> go.Figure:
    """Create a line chart."""
    fig = px.line(
        data,
        x=x,
        y=y,
        title=title,
        template=CHART_TEMPLATE,
        height=height
    )
    fig.update_traces(line_color=PRIMARY_COLOR, line_width=2)
    fig.update_layout(
        hovermode='x unified',
        showlegend=False
    )
    return fig


def create_bar_chart(data: pd.DataFrame, x: str, y: str, title: str, horizontal: bool = False, height: int = CHART_HEIGHT) -> go.Figure:
    """Create a bar chart."""
    if horizontal:
        fig = px.bar(
            data,
            x=y,
            y=x,
            title=title,
            template=CHART_TEMPLATE,
            height=height,
            orientation='h'
        )
    else:
        fig = px.bar(
            data,
            x=x,
            y=y,
            title=title,
            template=CHART_TEMPLATE,
            height=height
        )
    
    fig.update_traces(marker_color=PRIMARY_COLOR)
    fig.update_layout(showlegend=False)
    return fig


def create_pie_chart(labels: List[str], values: List[float], title: str, height: int = CHART_HEIGHT) -> go.Figure:
    """Create a pie chart."""
    fig = go.Figure(data=[go.Pie(
        labels=labels,
        values=values,
        hole=0.3,  # Donut chart
        marker=dict(colors=px.colors.qualitative.Set3)
    )])
    
    fig.update_layout(
        title=title,
        template=CHART_TEMPLATE,
        height=height,
        showlegend=True
    )
    return fig


def create_heatmap(data: pd.DataFrame, x: str, y: str, z: str, title: str, height: int = CHART_HEIGHT) -> go.Figure:
    """Create a heatmap."""
    pivot_data = data.pivot(index=y, columns=x, values=z)
    
    fig = go.Figure(data=go.Heatmap(
        z=pivot_data.values,
        x=pivot_data.columns,
        y=pivot_data.index,
        colorscale='Blues',
        hoverongaps=False
    ))
    
    fig.update_layout(
        title=title,
        template=CHART_TEMPLATE,
        height=height
    )
    return fig


def create_histogram(data: List[float], title: str, x_label: str, height: int = CHART_HEIGHT) -> go.Figure:
    """Create a histogram."""
    fig = go.Figure(data=[go.Histogram(
        x=data,
        marker_color=PRIMARY_COLOR,
        nbinsx=30
    )])
    
    fig.update_layout(
        title=title,
        xaxis_title=x_label,
        yaxis_title="Count",
        template=CHART_TEMPLATE,
        height=height,
        showlegend=False
    )
    return fig


def create_box_plot(data: pd.DataFrame, y: str, title: str, height: int = CHART_HEIGHT) -> go.Figure:
    """Create a box plot."""
    fig = go.Figure(data=[go.Box(
        y=data[y],
        marker_color=PRIMARY_COLOR,
        name=y
    )])
    
    fig.update_layout(
        title=title,
        yaxis_title=y,
        template=CHART_TEMPLATE,
        height=height,
        showlegend=False
    )
    return fig


def create_stacked_bar_chart(data: pd.DataFrame, x: str, y_cols: List[str], title: str, height: int = CHART_HEIGHT) -> go.Figure:
    """Create a stacked bar chart."""
    fig = go.Figure()
    
    colors = px.colors.qualitative.Set2
    for i, col in enumerate(y_cols):
        fig.add_trace(go.Bar(
            x=data[x],
            y=data[col],
            name=col,
            marker_color=colors[i % len(colors)]
        ))
    
    fig.update_layout(
        title=title,
        barmode='stack',
        template=CHART_TEMPLATE,
        height=height,
        showlegend=True,
        hovermode='x unified'
    )
    return fig


def create_area_chart(data: pd.DataFrame, x: str, y: str, title: str, height: int = CHART_HEIGHT) -> go.Figure:
    """Create an area chart."""
    fig = px.area(
        data,
        x=x,
        y=y,
        title=title,
        template=CHART_TEMPLATE,
        height=height
    )
    fig.update_traces(line_color=PRIMARY_COLOR, fillcolor=PRIMARY_COLOR)
    return fig


def create_metric_card(value: str, label: str, delta: str = None, delta_color: str = "normal") -> Dict[str, Any]:
    """Create data for a metric card (to be used with st.metric)."""
    return {
        'value': value,
        'label': label,
        'delta': delta,
        'delta_color': delta_color
    }

