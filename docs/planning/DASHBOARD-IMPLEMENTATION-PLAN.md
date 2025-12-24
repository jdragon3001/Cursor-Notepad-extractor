# Streamlit Dashboard Implementation Plan

**Date**: December 22, 2025

## Overview

Building a 7-page Streamlit dashboard to visualize all 139 stats from the Cursor data extraction system.

---

## Architecture

### File Structure
```
streamlit_app/
├── app.py                    # Main entry point
├── config.py                 # App configuration
├── utils/
│   ├── __init__.py
│   ├── data_loader.py       # Load data from orchestrator
│   ├── formatters.py        # Format numbers, dates, etc.
│   └── chart_builder.py     # Reusable chart functions
└── pages/
    ├── __init__.py
    ├── 1_📊_Overview.py     # High-level summary
    ├── 2_🔍_Browse.py       # Search/filter messages
    ├── 3_📈_Stats.py        # All 139 stats index
    ├── 4_📉_Analytics.py    # Charts & visualizations
    ├── 5_📅_Calendar.py     # Timeline view
    ├── 6_🧠_Intelligence.py # Actionable insights
    └── 7_💾_Export.py       # Export functionality
```

### Technology Stack
- **Streamlit**: Main framework
- **Plotly**: Interactive charts
- **Pandas**: Data manipulation
- **Altair**: Alternative charting (lighter weight)

### Design Principles
1. **Mobile-first**: Responsive layouts
2. **Fast loading**: Cache data aggressively
3. **Clean UI**: Minimal clutter
4. **Accessible**: Clear labels, good contrast
5. **Modular**: Reusable components

---

## Page Designs

### 1. Overview Page 📊
**Purpose**: Quick summary of key metrics

**Layout**:
```
┌─────────────────────────────────────────────────┐
│  🎯 Cursor Stats Overview                       │
├─────────────────────────────────────────────────┤
│  [Key Metrics Cards]                            │
│  ┌───────┐ ┌───────┐ ┌───────┐ ┌───────┐      │
│  │ 70K   │ │ 1K    │ │ 47K   │ │ 60%   │      │
│  │ Msgs  │ │ Sess. │ │ Tools │ │ Succ. │      │
│  └───────┘ └───────┘ └───────┘ └───────┘      │
│                                                  │
│  [Recent Activity Chart]                        │
│  [Top Tools Used]                               │
│  [Quick Stats Grid]                             │
└─────────────────────────────────────────────────┘
```

**Components**:
- Metric cards (4 columns)
- Activity timeline (line chart)
- Top tools (bar chart)
- Quick stats (expandable sections)

---

### 2. Browse Page 🔍
**Purpose**: Search and filter messages/sessions

**Layout**:
```
┌─────────────────────────────────────────────────┐
│  🔍 Browse Messages & Sessions                  │
├─────────────────────────────────────────────────┤
│  [Search Box]                                    │
│  [Filters: Type | Date | Session | Tools]       │
│                                                  │
│  [Results Table]                                │
│  ┌─────────┬───────────┬──────────┬──────────┐ │
│  │ Date    │ Type      │ Text     │ Session  │ │
│  ├─────────┼───────────┼──────────┼──────────┤ │
│  │ 12/22   │ User      │ Build... │ abc123   │ │
│  │ 12/22   │ AI        │ I'll...  │ abc123   │ │
│  └─────────┴───────────┴──────────┴──────────┘ │
│                                                  │
│  [Pagination]                                    │
└─────────────────────────────────────────────────┘
```

**Features**:
- Full-text search
- Multi-select filters
- Date range picker
- Pagination
- Export filtered results
- Message detail modal

---

### 3. Stats Page 📈
**Purpose**: Display all 139 stats in organized categories

**Layout**:
```
┌─────────────────────────────────────────────────┐
│  📈 Statistics Index                            │
├─────────────────────────────────────────────────┤
│  [Category Tabs]                                │
│  Messages | Sessions | Code | Daily | Tools... │
│                                                  │
│  [Stats Grid]                                   │
│  ┌────────────────────────────────────────────┐ │
│  │ 📊 Total Messages                          │ │
│  │ 70,026                                     │ │
│  │ ─────────────────────────────────────      │ │
│  │ Median: 122  |  Range: 2-1,629           │ │
│  └────────────────────────────────────────────┘ │
│                                                  │
│  [Download Stats as CSV]                        │
└─────────────────────────────────────────────────┘
```

**Features**:
- Tabbed categories
- Stat cards with details
- Expandable breakdowns
- Copy stat values
- Export category/all stats

---

### 4. Analytics Page 📉
**Purpose**: Visual insights with interactive charts

**Layout**:
```
┌─────────────────────────────────────────────────┐
│  📉 Analytics & Insights                        │
├─────────────────────────────────────────────────┤
│  [Chart Selector]                               │
│                                                  │
│  [Main Chart Area]                              │
│  ┌────────────────────────────────────────────┐ │
│  │                                            │ │
│  │  [Interactive Plotly Chart]                │ │
│  │                                            │ │
│  └────────────────────────────────────────────┘ │
│                                                  │
│  [Secondary Charts - 2 Columns]                 │
│  ┌───────────────┐  ┌───────────────┐         │
│  │ Chart 1       │  │ Chart 2       │         │
│  └───────────────┘  └───────────────┘         │
└─────────────────────────────────────────────────┘
```

**Charts**:
1. Messages over time (line)
2. Tool usage distribution (pie/bar)
3. Session duration (histogram)
4. Code lines added/removed (stacked bar)
5. Model usage (pie)
6. Thinking time distribution (box plot)
7. Success rate trends (area)

---

### 5. Calendar Page 📅
**Purpose**: Timeline view of activity

**Layout**:
```
┌─────────────────────────────────────────────────┐
│  📅 Activity Timeline                           │
├─────────────────────────────────────────────────┤
│  [Month Selector]                               │
│                                                  │
│  [Calendar Heatmap]                             │
│  Mon Tue Wed Thu Fri Sat Sun                    │
│  ┌───┬───┬───┬───┬───┬───┬───┐                │
│  │ 5 │ 12│ 8 │ 15│ 3 │ 0 │ 0 │                │
│  └───┴───┴───┴───┴───┴───┴───┘                │
│  (Color intensity = activity level)             │
│                                                  │
│  [Selected Day Details]                         │
│  - Messages: 120                                │
│  - Sessions: 5                                  │
│  - Tools used: 45                               │
└─────────────────────────────────────────────────┘
```

**Features**:
- Heatmap calendar
- Click day for details
- Activity trends
- Streak tracking
- Peak hours chart

---

### 6. Intelligence Page 🧠
**Purpose**: Actionable insights and recommendations

**Layout**:
```
┌─────────────────────────────────────────────────┐
│  🧠 Intelligence & Insights                     │
├─────────────────────────────────────────────────┤
│  [Insight Cards]                                │
│  ┌────────────────────────────────────────────┐ │
│  │ 💡 Your tool error rate is 38%             │ │
│  │ Most failures: search_replace (35%)        │ │
│  │ Tip: Check file paths before operations    │ │
│  └────────────────────────────────────────────┘ │
│                                                  │
│  [Patterns Detected]                            │
│  - Peak productivity: 2-4 PM                    │
│  - Longest sessions: Weekend mornings           │
│  - Most effective prompts: Specific + Context   │
│                                                  │
│  [Recommendations]                              │
│  1. Consider shorter sessions (< 100 msgs)      │
│  2. Use more context attachments                │
│  3. Review failed tool calls patterns           │
└─────────────────────────────────────────────────┘
```

**Insights**:
1. Tool effectiveness
2. Session patterns
3. Time optimization
4. Context usage
5. Model recommendations
6. Error patterns

---

### 7. Export Page 💾
**Purpose**: Export data in multiple formats

**Layout**:
```
┌─────────────────────────────────────────────────┐
│  💾 Export Data                                 │
├─────────────────────────────────────────────────┤
│  [Export Options]                               │
│                                                  │
│  What to export:                                │
│  ☐ Messages                                     │
│  ☐ Sessions                                     │
│  ☐ Stats                                        │
│  ☐ Charts                                       │
│                                                  │
│  Format:                                        │
│  ○ JSON  ○ CSV  ○ Excel  ○ PDF                 │
│                                                  │
│  Date range:                                    │
│  [Start Date] to [End Date]                     │
│                                                  │
│  [📥 Download Export]                           │
└─────────────────────────────────────────────────┘
```

**Features**:
- Multi-select data types
- Multiple formats
- Date range filtering
- Preview before download
- Scheduled exports (future)

---

## Implementation Steps

### Phase 1: Setup (30 min)
1. Create directory structure
2. Install dependencies
3. Create main app.py
4. Setup config and utils

### Phase 2: Core Pages (2-3 hours)
1. Overview page (high priority)
2. Stats page (high priority)
3. Browse page (medium priority)

### Phase 3: Advanced Pages (2-3 hours)
4. Analytics page (charts)
5. Calendar page (timeline)
6. Intelligence page (insights)
7. Export page (downloads)

### Phase 4: Polish (1 hour)
- Mobile responsiveness
- Error handling
- Loading states
- Performance optimization

---

## Testing Strategy

1. **Unit testing**: Test data loading functions
2. **Integration testing**: Test page rendering
3. **Visual testing**: Check responsive layouts
4. **Performance testing**: Test with full dataset (70K messages)

---

## Dependencies

```txt
streamlit>=1.29.0
plotly>=5.18.0
pandas>=2.1.4
altair>=5.2.0
openpyxl>=3.1.2  # For Excel export
fpdf>=1.7.2      # For PDF export
```

---

**Ready to implement, Jack!** 🚀

