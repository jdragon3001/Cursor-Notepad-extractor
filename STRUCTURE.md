# Cursor Data Extractor - Project Structure

## 🎯 **CURRENT STATUS: 124 STATS COMPLETE + TEMPORAL FILTERING**

**December 23, 2025** - Core stats extraction and calculation pipeline is operational. Temporal filtering and drill-down features added.

### ✅ Completed
- **Data Models**: Message, Session, CodeDiff, DailyStat, CodeTrackingLine, TimeRange (90+ total properties)
- **Extractors**: MessageExtractor, SessionExtractor, CodeDiffExtractor, CodeTrackingExtractor, DailyStatExtractor
- **Calculators**: 
  - **MessageCalculator with ALL 66 message stats** ✅
  - **SessionCalculator with ALL 27 session stats** ✅
  - **CodeCalculator with ALL 12 code & diffs stats** ✅
  - **DailyUsageCalculator with ALL 6 daily usage stats** ✅
  - **ToolCalculator with ALL 10 tool stats** ✅
  - **ContextCalculator with 18 context stats** ✅
  - Modular architecture: 21 focused modules total
  - Each module: 3-7 methods, ~150-200 lines
  - Clean, maintainable, testable code
- **Orchestrator**: Coordinates extraction and calculation with time filtering
- **Temporal Filtering**: Filter stats by time ranges (11 presets + custom)
- **Time Series**: Generate day/week/month aggregations for drill-downs
- **Cache System**: Optimizes performance with smart caching
- **Test Pipeline**: Validates end-to-end functionality
- **Frontend Dashboard**: React + Tailwind with time filtering and drill-down modals

### 🔍 Verified Results (Latest Test)
- **71,204 messages** extracted (0 errors)
- **1,032 sessions** extracted (0 errors)
- **11,051 code diffs** extracted (0 errors)
- **10,000 tracking lines** extracted (0 errors)
- **29 daily stats** extracted (0 errors)
- **4,230 request contexts** extracted (261 errors)
- **124 stats** calculated successfully ✅
- **Temporal filtering** working perfectly ✅
- **Time series generation** functional ✅
- **Progress: 124/232 stats (53.4%)**

### 📊 Sample Stats (124 Stats Working!)
- Total messages: 71,204
- User messages: 4,109 (5.8%)
- AI messages: 66,996 (94.1%)
- Messages per session: avg 189, median 141
- Messages with code: 12,966 (18.2%)
- Messages with thinking: 18,824 (26.4%)
- Total sessions: 1,032
- Agent mode sessions: 45.4%
- Code diffs: 11,051
- Tracked code lines: 10,000
- Composer suggested lines: 157,364 (29 days)
- Composer acceptance rate: 52.8%
- Tool usage: 10 tool stats tracked
- Context stats: 18 context stats tracked

---

## 📁 **Project Structure**

### **Core Modules**
```
database/
├── __init__.py
├── cursor_db.py               # ⭐ CursorDatabase class (SQLite access)
└── __pycache__/

utils/
├── __init__.py
├── config.py                  # ⭐ Config class (paths, DB discovery)
└── __pycache__/

stats/                         # ⭐ Stats calculation system (modular architecture)
├── __init__.py
├── orchestrator.py            # Main coordinator with temporal filtering
├── cache.py                   # Smart caching system
│
├── models/                    # Data models (dataclasses)
│   ├── __init__.py
│   ├── message.py             # ✅ Message model (30+ properties)
│   ├── session.py             # ✅ Session model (20+ properties)
│   ├── code_diff.py           # ✅ CodeDiff, DiffChange, CodeTrackingLine models
│   ├── daily_stat.py          # ✅ DailyStat model
│   ├── time_range.py          # ✅ TimeRange model (NEW - temporal filtering)
│   ├── request_context.py     # ✅ MessageRequestContext model
│   └── workspace.py           # ✅ Workspace model
│
├── filters/                   # ⭐ Data filtering layer (NEW)
│   ├── __init__.py
│   └── temporal_filter.py     # ✅ Time-based filtering & time series generation
│
├── extractors/                # Data extraction layer
│   ├── __init__.py
│   ├── base_extractor.py     # Base class with DB connection
│   ├── message_extractor.py  # ✅ Extract bubbleId data
│   ├── session_extractor.py  # ✅ Extract composerData
│   ├── code_diff_extractor.py # ✅ Extract codeBlockDiff data
│   ├── code_tracking_extractor.py # ✅ Extract aiCodeTrackingLines
│   ├── daily_stat_extractor.py # ✅ Extract daily usage stats
│   ├── request_context_extractor.py # ✅ Extract message contexts
│   └── workspace_extractor.py # ✅ Extract workspace metadata
│
├── calculators/               # Stats calculation layer (modular)
│   ├── __init__.py
│   ├── base_calculator.py    # ✅ Base with 40+ utility functions
│   ├── message_stats/         # ⭐ Modular message stats (66 stats)
│   │   ├── __init__.py        # Exports MessageCalculator
│   │   ├── base.py            # Shared utilities
│   │   ├── counts.py          # Stats 1-4: Message counts
│   │   ├── content.py         # Stats 5-11: Content analysis
│   │   ├── thinking.py        # Stats 12-15: Thinking/reasoning
│   │   ├── tools.py           # Stats 16-20: Tool usage
│   │   ├── context.py         # Stats 21-26: Context provided
│   │   ├── references.py      # Stats 27-30: External references
│   │   ├── suggestions.py     # Stats 31-41: Suggestions & diffs
│   │   ├── models.py          # Stats 42-44: Model information
│   │   ├── tokens.py          # Stats 45-49: Token usage
│   │   ├── session_context.py # Stats 50-52: Session context
│   │   ├── errors.py          # Stats 53-56: Errors in messages
│   │   ├── metadata.py        # Stats 57-59: Message metadata
│   │   └── timing.py          # Stats 60-66: Activity timing
│   ├── session_stats/         # ⭐ Modular session stats (27 stats) ✅
│   │   ├── __init__.py        # Exports SessionCalculator
│   │   ├── base.py            # Shared utilities
│   │   ├── counts.py          # Stats 67-70: Session counts
│   │   ├── duration_outcomes.py # Stats 71-76: Duration & outcomes
│   │   ├── files_context.py   # Stats 77-84: Files & context
│   │   ├── conversation_config.py # Stats 85-91: Conversation & config
│   │   └── naming.py          # Stats 92-93: Session naming
│   ├── code_stats/            # ⭐ Modular code stats (12 stats) ✅
│   │   ├── __init__.py        # Exports CodeCalculator
│   │   ├── base.py            # Shared utilities
│   │   ├── diff_metrics.py    # Stats 94-100: Diff metrics
│   │   └── tracking_lines.py  # Stats 101-105: Tracking lines
│   ├── daily_stats/           # ⭐ Daily usage stats (6 stats) ✅
│   │   └── __init__.py        # DailyUsageCalculator (all stats in one module)
│   ├── tool_stats/            # ⭐ Tool usage stats (10 stats) ✅
│   │   ├── __init__.py
│   │   ├── base.py
│   │   └── usage.py
│   └── context_stats/         # ⭐ Context stats (18 stats) ✅
│       ├── __init__.py
│       ├── base.py
│       ├── file_context.py
│       ├── git.py
│       ├── linter.py
│       └── todos.py
```

### **Scripts (Reference & Utilities)**
```
scripts/
├── exploration/               # Data exploration scripts
│   ├── comprehensive_data_explorer.py
│   ├── exhaustive_exploration.py
│   ├── explore_cursorDiskKV.py
│   ├── map_all_cursor_data.py
│   ├── check_all_sources_deep.py
│   ├── deep_model_token_search.py
│   ├── find_earliest_entry.py
│   └── quick_analysis.py
└── validation/                # Validation & recovery scripts
    ├── recover_all_chat_data.py  # ⭐ CRITICAL: Multi-source recovery
    ├── extract_daily_stats.py
    ├── verify_model_and_tokens.py
    └── final_comprehensive_check.py
```

### **Documentation**
```
docs/
├── planning/                  # Planning & design docs
│   ├── APP-ARCHITECTURE.md                        # ⭐ Complete app design
│   ├── UI-UX-DESIGN.md                            # ⭐ UI/UX specification
│   ├── STATS-CALCULATION-ARCHITECTURE.md          # ⭐ Stat system design
│   ├── TEMPORAL-FILTERING-IMPLEMENTATION-DEC-23-2025.md # ⭐ Phase 1+2 implementation
│   ├── CURSOR-DATA-EXTRACTION-PLAN.md             # Implementation roadmap
│   ├── PURE-STATS-INDEX.md                        # ⭐ 232 core stats
│   ├── COMPLETE-STATS-CATALOG.md                  # Detailed stats catalog
│   ├── BROWSE-PAGE-SUMMARY.md                     # Browse feature design
│   ├── EXPLORATION-COMPLETE.md                    # Exploration summary
│   ├── QUICK-REFERENCE.md                         # Developer reference
│   ├── CLEANUP-SUMMARY.md                         # Cleanup log
│   └── EXHAUSTIVE_DATA_REPORT.md                  # Data report
└── (cursor-data-docs moved here later)

cursor-data-docs/              # Data source documentation
├── README.md                          # Overview with metrics
├── 01-DATA-SOURCES-OVERVIEW.md        # Complete data source map
├── 02-GLOBAL-STATE-DATABASE.md        # Main 2.4GB database
├── 03-WORKSPACE-DATABASES.md          # Per-project databases
├── 04-FILE-HISTORY.md                 # Edit history (2,605 files)
├── 05-LOGS-AND-TELEMETRY.md           # Session logs
├── 06-OTHER-SOURCES.md                # WebStorage, Partitions
├── 07-KEY-VALUE-SCHEMA.md             # Key schemas
├── 08-CURSORDISKKV-GOLDMINE.md        # ⭐ Chat data source!
├── 09-EXHAUSTIVE-DATA-REPORT.md       # Full exploration report
├── 10-CHAT-DATA-RECOVERY-REPORT.md    # ⭐ Multi-source recovery
├── 11-DAILY-USAGE-STATS.md            # Daily line counts
├── 12-DATA-LIMITATIONS.md             # Why numbers differ
├── 13-MESSAGE-CONTENT-ANALYSIS.md     # ⭐ Content & effectiveness
└── workspace_chat_data.json           # Raw workspace data
```

### **Root Files**
```
README.md                      # Usage guide
STRUCTURE.md                   # This file
PROBLEM_LOG.txt                # Known issues
DEPRECATED.txt                 # Deprecated patterns
requirements.txt               # Dependencies
```

---

## 📊 **Data Source Summary**

### Primary Sources (MUST USE BOTH)

| Source | Sessions | Date Range | Contains |
|--------|----------|------------|----------|
| cursorDiskKV | 1,076 | Oct 2025+ | Full messages, tokens |
| Workspace DBs | 1,858 | Nov 2024+ | Older sessions |

### Key Tables

**Global Database** (`state.vscdb`):
- `ItemTable` - Settings, configs, aiCodeTrackingLines
- `cursorDiskKV` - Chat messages, sessions, diffs

**Workspace Databases** (per project):
- `ItemTable` - `composer.composerData`, `notepadData`

---

## 🛠️ **Data Extraction Strategy**

```python
# Pseudocode for complete extraction
def extract_all_data():
    sessions = {}
    
    # 1. Recent data from global cursorDiskKV
    for session in extract_cursorDiskKV():
        sessions[session.id] = session
    
    # 2. Older data from workspace databases
    for workspace in get_all_workspaces():
        for session in extract_workspace(workspace):
            if session.id not in sessions:
                sessions[session.id] = session
            else:
                sessions[session.id].merge(session)
    
    return sessions
```

---

## 🎮 **Commands**

```bash
# Activate environment
conda activate cursor-extractor

# Run data recovery (comprehensive)
python scripts/validation/recover_all_chat_data.py

# Find data timeline
python scripts/exploration/find_earliest_entry.py

# Verify metrics
python scripts/validation/verify_model_and_tokens.py

# Extract daily stats
python scripts/validation/extract_daily_stats.py
```

---

## 📝 **Next Steps**

### Immediate (Current Session)
1. ✅ **Message Calculator** - All 66 message stats complete
2. ✅ **Session Calculator** - All 27 session stats complete
3. ✅ **Code & Diffs Calculator** - All 12 code stats complete
4. ✅ **Daily Usage Calculator** - All 6 daily stats complete
5. ✅ **Tool Stats Calculator** - All 10 tool stats complete
6. ✅ **Context Stats Calculator** - 18 context stats complete
7. ✅ **Temporal Filtering** - Phase 1+2 complete (filtering + drill-down)
8. **Token & Model Usage Calculator** - Next target (stats 112-139) - 28 stats

### Short Term
9. **Error Calculator** - Extract lints and console logs (stats 140-149) - 10 stats
10. **Git Activity Calculator** - Version control metrics (stats 150-159) - 10 stats
11. **Notepad Calculator** - Notepad usage stats (stats 160-169) - 10 stats
12. **Effectiveness Calculator** - Analyze prompt effectiveness (stats 170-200) - 31 stats
13. **Remaining stats** - Complete all 232 stats (108 remaining)

### Medium Term (Future Phases)
14. **Period Comparison** - Phase 3: Compare two time ranges side-by-side
15. **Advanced Drill-Down** - Show underlying messages/sessions in modals
16. **Add Workspace Extraction** - Extract from 246 workspace DBs for full history
17. **Build Streamlit Dashboard** - 7-page UI (Overview, Browse, Stats, Analytics, Calendar, Intelligence, Export)
18. **Full-text Search** - Implement Whoosh for message/session search
19. **Export System** - JSON, CSV, PDF exports

See `docs/planning/APP-ARCHITECTURE.md` for complete roadmap.

---

## 🎨 Frontend Structure (`frontend/`)

React + Vite application for the dashboard UI.

### Core Application
- `App.jsx` - Main application with stats dashboard and view routing
- `main.jsx` - React entry point
- `index.html` - HTML template

### Components (`src/components/`)
- `Tooltip.jsx` - Info tooltips for stat descriptions
- `TimeRangeSelector.jsx` - Time range filtering (presets + custom)
- `StatDetailModal.jsx` - Drill-down modal with time series charts
- `MessageDetailModal.jsx` - Full message detail view with raw/formatted toggle
- `MessagesView.jsx` - Browse messages tab with pagination and filters
- `ConversationsView.jsx` - Browse conversations/sessions tab
- `SessionsView.jsx` - Browse all sessions with detail modals ✨ NEW
- `CodeDiffsView.jsx` - Browse code diffs with change details ✨ NEW
- `DailyActivityView.jsx` - Calendar heatmap and daily activity ✨ NEW
- `ToolsView.jsx` - Browse AI tool calls with parameters/results ✨ NEW
- `ContextView.jsx` - Browse context items (linter, git, etc.) ✨ NEW

### Pages (`src/pages/`)
- `BrowsePage.jsx` - Browse messages, sessions, and raw data
  - `MessagesTab` component - Paginated message list with filters
  - `MessageCard` component - Individual message preview cards

### Configuration
- `statDescriptions.js` - Descriptions for all statistics
- `tailwind.config.js`, `postcss.config.js` - Styling
- `vite.config.js` - Build configuration
- `package.json` - Dependencies and scripts

### Features
✅ Stats dashboard with 124+ metrics
✅ Temporal filtering (11 presets + custom ranges)
✅ Drill-down modals with time series charts
✅ Browse messages with pagination and filters
✅ Browse conversations/sessions with full threads
✅ Browse all sessions with details ✨ NEW
✅ Browse code diffs with change previews ✨ NEW
✅ Calendar heatmap view of daily activity ✨ NEW
✅ Browse AI tool calls with parameters/results ✨ NEW
✅ Browse context items (linter, git, files, etc.) ✨ NEW
✅ Search, filter, and sort across all views
✅ Modal detail views for all data types
✅ Responsive design (desktop optimized)

---

## 🆕 **Recent Updates - January 1, 2026**

### Tab Data Views Implementation
Transformed 5 tabs from stats-only views to full data browsing experiences:

1. **SESSIONS Tab**: Browse all coding sessions with durations, message counts, code changes
2. **CODE Tab**: View all code diffs with line-by-line changes
3. **DAILY Tab**: Calendar heatmap + daily activity breakdowns (composer/tab stats)
4. **TOOLS Tab**: Browse all AI tool calls (read_file, grep, search_replace, etc.)
5. **CONTEXT Tab**: View context provided to AI (linter errors, git status, file context, TODOs)

**New Backend Endpoints**:
- `/api/code-diffs` - List and detail code diffs
- `/api/daily-activity` - Daily activity calendar and day details
- `/api/tools` - List and detail tool calls
- `/api/context` - List and detail context items

**New Frontend Components**:
- `SessionsView.jsx`, `CodeDiffsView.jsx`, `DailyActivityView.jsx`
- `ToolsView.jsx`, `ContextView.jsx`

See `docs/planning/TABS-DATA-VIEWS-IMPLEMENTATION-COMPLETE-JAN-1-2026.md` for full details.

---

## 🔍 **Key Discoveries**

1. **cursorDiskKV is the goldmine** - 68K+ messages with full content
2. **Workspace DBs have older data** - Nov 2024 sessions not in global
3. **Model info available** - Can track Claude, GPT-5, etc. usage
4. **Token counts exist** - Though often zero in bubbleId
5. **Lines added/removed tracked** - 429K lines added total
6. **402 days of history** - Complete timeline available

---

*Last updated: January 1, 2026 - Tab Data Views Implementation Complete*
