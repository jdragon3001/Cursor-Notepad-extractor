# Cursor Data Extractor - Project Structure

## 🎯 **CURRENT STATUS: DATA EXPLORATION COMPLETE**

**December 22, 2025** - We have completed exhaustive exploration of Cursor's data storage.

### Critical Discovery
**Complete chat history requires reading from MULTIPLE sources:**
- Global `cursorDiskKV` table: October 2025 → Present (1,076 sessions)
- Workspace databases: November 2024 → Present (1,858 sessions)
- **Combined: 2,934 sessions across 402 days**

### Verified Metrics
- 68,636 total messages
- 292M+ input tokens
- 429,700 lines of code added
- Data spans Nov 14, 2024 → Dec 22, 2025

---

## 📁 **Project Structure**

### **Data Exploration Scripts (Reference)**
```
recover_all_chat_data.py       # ⭐ CRITICAL: Multi-source data recovery
extract_daily_stats.py         # Daily usage extraction
verify_model_and_tokens.py     # Validate model/token data
deep_model_token_search.py     # Deep model/token search
check_all_sources_deep.py      # Content verification
final_comprehensive_check.py   # Complete verification
exhaustive_exploration.py      # Complete data catalog
explore_cursorDiskKV.py        # Deep dive chat data
find_earliest_entry.py         # Find timeline boundaries
quick_analysis.py              # Quick stats overview
map_all_cursor_data.py         # Filesystem mapping
comprehensive_data_explorer.py # Initial deep dive
```

**Note:** These scripts were used during exploration and serve as reference for implementation.

### **Data Documentation**
```
cursor-data-docs/
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

### **Project Planning**
```
nextsteps/
├── APP-ARCHITECTURE.md            # ⭐ Complete app design
└── CURSOR-DATA-EXTRACTION-PLAN.md # Implementation roadmap
```

### **Core Modules (Existing)**
```
database/
├── __init__.py
├── cursor_db.py               # ⭐ CursorDatabase class (SQLite access)
└── __pycache__/

utils/
├── __init__.py
├── config.py                  # ⭐ Config class (paths, DB discovery)
└── __pycache__/
```

**Note:** See `nextsteps/APP-ARCHITECTURE.md` for complete module structure to be built.

### **Project Documentation**
```
README.md                      # Usage guide
STRUCTURE.md                   # This file
EXPLORATION-COMPLETE.md        # ⭐ Final exploration summary
QUICK-REFERENCE.md             # ⭐ Developer quick reference
COMPLETE-STATS-CATALOG.md      # ⭐ ALL possible stats/metrics (600+)
CLEANUP-SUMMARY.md             # Project cleanup log
EXHAUSTIVE_DATA_REPORT.md      # Data exploration report
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
conda activate cursor-notepad-browser

# Run data recovery (comprehensive)
python recover_all_chat_data.py

# Find data timeline
python find_earliest_entry.py

# Verify metrics
python verify_model_and_tokens.py

# Original note GUI
python note_search_gui.py
```

---

## 📝 **Next Steps**

1. **Build Data Extractors** - GlobalExtractor, WorkspaceExtractor
2. **Create Aggregator** - Combine and deduplicate from all sources
3. **Build Analytics** - Calculate metrics, generate insights
4. **Create Dashboard** - Year Wrapped style UI

See `nextsteps/CURSOR-DATA-EXTRACTION-PLAN.md` for full roadmap.

---

## 🔍 **Key Discoveries**

1. **cursorDiskKV is the goldmine** - 68K+ messages with full content
2. **Workspace DBs have older data** - Nov 2024 sessions not in global
3. **Model info available** - Can track Claude, GPT-5, etc. usage
4. **Token counts exist** - Though often zero in bubbleId
5. **Lines added/removed tracked** - 429K lines added total
6. **402 days of history** - Complete timeline available

---

*Last updated: December 22, 2025*
