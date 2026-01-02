# Tabs Data Views Plan - January 1, 2026

## Overview

Currently, the dashboard has tabs for MESSAGES, CONVERSATIONS, SESSIONS, CODE, DAILY, TOOLS, and CONTEXT. The MESSAGES and CONVERSATIONS tabs show actual data (message lists, conversation threads), while the other tabs (SESSIONS, CODE, DAILY, TOOLS, CONTEXT) only show aggregated statistics.

**Goal:** Transform the stats-only tabs into data browsing experiences that show the underlying data that generates those stats, similar to how MESSAGES and CONVERSATIONS work.

---

## Current State

### ✅ Already Implemented
- **ALL STATS Tab**: Shows 124+ aggregated statistics across all categories (perfect as-is)
- **MESSAGES Tab**: Paginated list of individual messages with filters (type, code, thinking, tools, search)
- **CONVERSATIONS Tab**: List of sessions/conversations with full message threads

### 🔄 Need Data Views
- **SESSIONS Tab**: Currently shows session stats → Should show list of sessions with details
- **CODE Tab**: Currently shows code stats → Should show list of code diffs
- **DAILY Tab**: Currently shows daily stats → Should show calendar/timeline view of daily activity
- **TOOLS Tab**: Currently shows tool stats → Should show list of tool calls
- **CONTEXT Tab**: Currently shows context stats → Should show context items (linter errors, git status, etc.)

---

## Detailed Tab Plans

### 1. SESSIONS Tab 🎯

**What to Show**: List of all coding sessions with details

**Primary View**: Session Cards/List
```
┌─────────────────────────────────────────────────────┐
│ Session Name                    Duration: 2h 34m    │
│ Created: Jan 1, 2026 10:30 AM                      │
│                                                     │
│ 📊 42 messages  │  📝 +234/-12 lines  │  📁 5 files│
│ 🤖 Agent Mode   │  🎯 Claude Sonnet   │  ⏱️ Active │
│                                                     │
│ Tags: [Python] [API] [Refactoring]                │
│ [View Details →]                                    │
└─────────────────────────────────────────────────────┘
```

**Data to Display Per Session**:
- Session name
- Created date & last updated
- Duration (minutes/hours)
- Message count (calculated)
- Lines added/removed
- Files modified count
- Agent mode indicator
- Model used (if consistent across session)
- Current status (active/completed)
- Quick stats: thinking time, tool usage count

**Filters**:
- Sort: Recent, Oldest, Longest duration, Most messages, Most code changes
- Filter: Agent mode only, By model, By date range, By duration
- Search: By session name

**Actions**:
- Click to expand full conversation (same as CONVERSATIONS tab)
- Show session timeline/activity graph
- Export session data

**API Endpoint**: `/api/sessions` (already exists!)

**Additional Stats Panel**: Show aggregated session stats for the filtered view
- Total sessions: X
- Avg duration: Y minutes
- Total messages: Z
- Agent mode %: W%

---

### 2. CODE Tab 💻

**What to Show**: List of all code diffs with file context

**Primary View**: Code Diff Cards
```
┌─────────────────────────────────────────────────────┐
│ 📄 src/api/handlers.py                             │
│ Session: "Add authentication middleware"           │
│ Timestamp: Jan 1, 2026 2:15 PM                     │
│                                                     │
│ Changes:                                            │
│ ├─ Lines Added: 45                                 │
│ ├─ Lines Removed: 12                               │
│ └─ Net Change: +33                                 │
│                                                     │
│ [View Diff →]                                       │
└─────────────────────────────────────────────────────┘
```

**Data to Display Per Diff**:
- File path
- Session it belongs to (link to session)
- Timestamp (when diff was created)
- Lines added count
- Lines removed count
- Net lines changed
- Language/file type
- Change summary (if available)

**Filters**:
- Sort: Recent, Oldest, Most changes, By file type
- Filter: By session, By language, By file path pattern, Date range
- Search: File name/path

**Actions**:
- Click to expand and show actual diff (side-by-side or unified view)
- Jump to session
- Group by session/file/date

**API Endpoint**: `/api/code-diffs` (NEW - needs to be created)

**Additional Stats Panel**:
- Total diffs: X
- Total lines added: Y
- Total lines removed: Z
- Most edited file
- Most active session

**Data Source**: `orchestrator.code_diffs` (already extracted)

---

### 3. DAILY Tab 📅

**What to Show**: Calendar/timeline view of daily activity with stats

**Primary View**: Calendar Grid + Daily Details
```
┌─────────────────────────────────────────────────────┐
│           December 2025                             │
│  M   T   W   T   F   S   S                         │
│ [1] [2] [3] [4] [5] [6] [7]  ← color-coded by      │
│ [8] [9][10][11][12][13][14]    activity level      │
│                                                     │
│ Selected: December 10, 2025                        │
│ ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━│
│ 📊 Activity Summary:                               │
│   • 12 sessions                                    │
│   • 248 messages                                   │
│   • 1,456 lines added                              │
│   • 234 lines removed                              │
│   • 3.5 hours active                               │
│                                                     │
│ 🗂️ Sessions on this day:                          │
│   └─ [List of sessions from this day]             │
│                                                     │
│ 📈 Code Stats:                                     │
│   • Composer suggested: 2,340 lines                │
│   • Composer accepted: 1,234 lines (52.8%)         │
│   • Tab suggested: 456 lines                       │
│   • Tab accepted: 234 lines (51.3%)                │
└─────────────────────────────────────────────────────┘
```

**Data to Display Per Day**:
- Date
- Total sessions
- Total messages (calculated from messages on that day)
- Lines added/removed (from sessions)
- Composer suggested/accepted lines (from daily_stats)
- Tab suggested/accepted lines (from daily_stats)
- Acceptance rates
- Active time (sum of session durations)
- Models used
- Sessions list (expandable)

**Views**:
1. **Calendar View**: Heatmap of activity
2. **Timeline View**: Linear timeline with events
3. **List View**: Daily summary cards

**Filters**:
- Date range picker
- Show only active days
- Minimum activity threshold

**Actions**:
- Click day to see sessions from that day
- Click session to view full conversation
- Export daily report

**API Endpoint**: `/api/daily-activity` (NEW - needs to be created)

**Additional Features**:
- Activity streaks
- Busiest day/time analysis
- Week-over-week comparison

**Data Source**: 
- `orchestrator.daily_stats` (composer/tab stats)
- `orchestrator.sessions` (filtered by date)
- `orchestrator.messages` (filtered by date)

---

### 4. TOOLS Tab 🛠️

**What to Show**: List of all tool calls with results

**Primary View**: Tool Call Cards
```
┌─────────────────────────────────────────────────────┐
│ 🔧 read_file                                        │
│ File: src/api/handlers.py                          │
│ Session: "Add authentication middleware"           │
│ Timestamp: Jan 1, 2026 2:15 PM                     │
│                                                     │
│ Parameters:                                         │
│   • target_file: "src/api/handlers.py"            │
│   • offset: null                                   │
│   • limit: null                                    │
│                                                     │
│ Result: ✅ 234 lines read                          │
│                                                     │
│ [View Details →]                                    │
└─────────────────────────────────────────────────────┘
```

**Data to Display Per Tool Call**:
- Tool type (read_file, grep, search_replace, etc.)
- Timestamp
- Session it belongs to
- Parameters used
- Result summary (success/failure)
- Result preview
- Duration (if available)
- Message it's associated with

**Tool Categories**:
- 📖 File Operations: read_file, write, delete_file, list_dir
- 🔍 Search: grep, codebase_search, file_search
- ✏️ Editing: search_replace, edit_notebook
- 🌐 Web: web_search, browser tools
- 📝 Tasks: todo_write
- 🔨 Terminal: run_terminal_cmd
- 📊 Diagnostics: read_lints

**Filters**:
- Sort: Recent, By tool type, By session
- Filter: By tool type, By session, Date range, Success/failure
- Search: In parameters or results

**Actions**:
- Click to expand full tool call with complete parameters and results
- Jump to message that triggered this tool
- Jump to session
- Group by tool type or session

**API Endpoint**: `/api/tools` (NEW - needs to be created)

**Additional Stats Panel**:
- Total tool calls: X
- Most used tool: Y (Z calls)
- Success rate: W%
- Tool usage by category (pie chart)

**Data Source**: `orchestrator.messages` → filter messages with `has_tools=True` → extract `tool_results`

---

### 5. CONTEXT Tab 🎯

**What to Show**: List of context items provided to the AI

**Primary View**: Context Cards (Tabbed by Type)
```
Tabs: [Linter Errors] [Git Status] [File Context] [TODOs] [Terminal] [All]

┌─────────────────────────────────────────────────────┐
│ 🔴 Linter Error                                     │
│ File: src/api/handlers.py:42                       │
│ Session: "Fix authentication bugs"                 │
│ Timestamp: Jan 1, 2026 3:20 PM                     │
│                                                     │
│ Error: "unused import 'datetime'"                  │
│ Severity: Warning                                   │
│                                                     │
│ [View in Session →]                                 │
└─────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────┐
│ 🔀 Git Status                                       │
│ Session: "Add authentication middleware"           │
│ Timestamp: Jan 1, 2026 2:15 PM                     │
│                                                     │
│ Modified files: 3                                   │
│ └─ src/api/handlers.py                             │
│ └─ src/auth/middleware.py                          │
│ └─ tests/test_auth.py                              │
│                                                     │
│ Uncommitted changes: 12                             │
│                                                     │
│ [View Details →]                                    │
└─────────────────────────────────────────────────────┘
```

**Context Types**:
1. **Linter Errors**: Multi-file linter errors
2. **Git Status**: Git status and diffs
3. **File Context**: Open editors, current file location
4. **Code Chunks**: Attached file code chunks, codebase context
5. **TODOs**: Todo items provided as context
6. **Terminal**: Terminal file context
7. **Folders**: Attached folder listings
8. **Knowledge**: Cursor rules, knowledge items
9. **Project Layout**: Project structure info

**Data to Display**:
- Context type
- Session it belongs to
- Timestamp
- Content preview
- Associated message (if applicable)
- Relevance score (if available)

**Filters**:
- Sort: Recent, By type, By session
- Filter: By context type, By session, Date range
- Search: In context content

**Actions**:
- Click to expand full context
- Jump to session/message
- Group by type or session

**API Endpoint**: `/api/context` (NEW - needs to be created)

**Additional Stats Panel**:
- Total context items: X
- By type breakdown
- Most common linter errors
- Most frequently attached files

**Data Source**: `orchestrator._request_contexts` (already extracted: 4,230 items)

---

## Implementation Priority

### Phase 1: Essential Tabs (High Value, Already Have Data)
1. ✅ **SESSIONS Tab** - API exists, just needs frontend
2. 🎯 **CODE Tab** - Data exists, needs API endpoint
3. 🎯 **DAILY Tab** - Data exists, needs API endpoint + calendar UI

### Phase 2: Advanced Tabs (Requires Parsing)
4. 🎯 **TOOLS Tab** - Requires parsing tool_results from messages
5. 🎯 **CONTEXT Tab** - Data exists, needs API endpoint + parsing

---

## Technical Implementation Notes

### Backend (API Endpoints Needed)

```python
# backend/api/code.py
@router.get("/code-diffs")
async def get_code_diffs(
    page: int = 1,
    limit: int = 20,
    sort: str = "recent",
    session_id: Optional[str] = None,
    file_path: Optional[str] = None,
    language: Optional[str] = None,
):
    """Get paginated list of code diffs."""
    # Return orchestrator.code_diffs with pagination

# backend/api/daily.py
@router.get("/daily-activity")
async def get_daily_activity(
    start_date: Optional[str] = None,
    end_date: Optional[str] = None,
):
    """Get daily activity breakdown."""
    # Return orchestrator.daily_stats + calculated session/message counts per day

@router.get("/daily-activity/{date}")
async def get_daily_detail(date: str):
    """Get full details for a specific day."""
    # Return sessions, messages, stats for that specific day

# backend/api/tools.py
@router.get("/tools")
async def get_tool_calls(
    page: int = 1,
    limit: int = 20,
    tool_type: Optional[str] = None,
    session_id: Optional[str] = None,
):
    """Get paginated list of tool calls."""
    # Parse tool_results from messages and return as flat list

# backend/api/context.py
@router.get("/context")
async def get_context_items(
    page: int = 1,
    limit: int = 20,
    context_type: Optional[str] = None,
    session_id: Optional[str] = None,
):
    """Get paginated list of context items."""
    # Return orchestrator._request_contexts with pagination
```

### Frontend Components Needed

```
frontend/src/components/
├── SessionsView.jsx        (NEW)
├── CodeDiffsView.jsx       (NEW)
├── DailyActivityView.jsx   (NEW)
│   ├── CalendarView.jsx    (NEW)
│   └── DayDetailCard.jsx   (NEW)
├── ToolsView.jsx           (NEW)
└── ContextView.jsx         (NEW)
```

### Routing Logic in App.jsx

```javascript
// In App.jsx, modify the tab content rendering:
{activeCategory === 'sessions' && <SessionsView />}
{activeCategory === 'code' && <CodeDiffsView />}
{activeCategory === 'daily' && <DailyActivityView />}
{activeCategory === 'tools' && <ToolsView />}
{activeCategory === 'context' && <ContextView />}
```

---

## Design Consistency

All new data views should follow the established pattern from MESSAGES and CONVERSATIONS:

1. **Consistent Layout**:
   - Search/filter bar at top
   - Pagination controls at bottom
   - Card-based design for items
   - Sidebar stats panel (optional)

2. **Consistent Filters**:
   - Page/limit for pagination
   - Sort options
   - Type filters
   - Date range (uses TimeRangeSelector)
   - Search text

3. **Consistent Actions**:
   - Click card to expand details
   - Link to related session/message
   - Export functionality

4. **Consistent Styling**:
   - Tailwind CSS classes matching existing design
   - Lucide icons
   - Color scheme: primary (blue), success (green), warning (yellow), error (red)

---

## Benefits of This Approach

1. **Discoverability**: Users can see exactly what data generates each stat
2. **Debugging**: Users can trace issues by viewing actual data
3. **Exploration**: Users can browse their coding history in multiple ways
4. **Context**: Each tab provides different lens on same underlying data
5. **Validation**: Users can verify stat accuracy by checking raw data
6. **Insights**: Drill down from aggregates to specifics

---

## Next Steps

1. **Get User Feedback**: Confirm this approach before implementation
2. **Phase 1 Implementation**:
   - Create `SessionsView.jsx` (reuse existing `/api/sessions` endpoint)
   - Create `/api/code-diffs` endpoint + `CodeDiffsView.jsx`
   - Create `/api/daily-activity` endpoint + `DailyActivityView.jsx`
3. **Phase 2 Implementation**:
   - Create `/api/tools` endpoint + `ToolsView.jsx`
   - Create `/api/context` endpoint + `ContextView.jsx`
4. **Polish & Test**: Ensure all views work with time filtering

---

*Created: January 1, 2026*

