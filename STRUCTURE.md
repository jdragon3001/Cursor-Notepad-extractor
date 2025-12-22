# Cursor Data Extractor - Project Structure

## 🎯 **CURRENT STATUS: 105 STATS COMPLETE**

**December 22, 2025** - Core stats extraction and calculation pipeline is operational.

### ✅ Completed
- **Data Models**: Message, Session, CodeDiff, CodeTrackingLine (70+ total properties)
- **Extractors**: MessageExtractor, SessionExtractor, CodeDiffExtractor, CodeTrackingExtractor
- **Calculators**: 
  - **MessageCalculator with ALL 66 message stats** ✅
  - **SessionCalculator with ALL 27 session stats** ✅
  - **CodeCalculator with ALL 12 code & diffs stats** ✅
  - Modular architecture: 20 focused modules total
  - Each module: 3-7 methods, ~150-200 lines
  - Clean, maintainable, testable code
- **Orchestrator**: Coordinates extraction and calculation
- **Cache System**: Optimizes performance with smart caching
- **Test Pipeline**: Validates end-to-end functionality

### 🔍 Verified Results (Latest Test)
- **69,667 messages** extracted (0 errors)
- **1,018 sessions** extracted (0 errors)
- **10,767 code diffs** extracted (0 errors)
- **10,000 tracking lines** extracted (0 errors)
- **66 message stats** calculated successfully ✅
- **27 session stats** calculated successfully ✅
- **12 code stats** calculated successfully ✅
- **Total: 105 stats** working perfectly ✅

### 📊 Sample Stats (105 Stats Working!)
- Total messages: 69,667
- User messages: 4,031 (5.8%)
- AI messages: 65,624 (94.2%)
- Messages per session: avg 187, median 124
- Messages with code: 12,814 (18.4%)
- Messages with thinking: 18,743 (26.9%)
- Total sessions: 1,018
- Agent mode sessions: 45.2%
- Chat mode sessions: 54.8%
- Code diffs: 10,767
- Tracked code lines: 10,000
- Unique file types: ~50

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
├── orchestrator.py            # Main coordinator
├── cache.py                   # Smart caching system
│
├── extractors/                # Data extraction layer
│   ├── __init__.py
│   ├── base_extractor.py     # Base class with DB connection
│   ├── message_extractor.py  # ✅ Extract bubbleId data
│   └── session_extractor.py  # ✅ Extract composerData
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
│   └── session_stats/         # ⭐ Modular session stats (27 stats) ✅
│       ├── __init__.py        # Exports SessionCalculator
│       ├── base.py            # Shared utilities
│       ├── counts.py          # Stats 67-70: Session counts
│       ├── duration_outcomes.py # Stats 71-76: Duration & outcomes
│       ├── files_context.py   # Stats 77-84: Files & context
│       ├── conversation_config.py # Stats 85-91: Conversation & config
│       └── naming.py          # Stats 92-93: Session naming
│   └── code_stats/            # ⭐ Modular code stats (12 stats) ✅
│       ├── __init__.py        # Exports CodeCalculator
│       ├── base.py            # Shared utilities
│       ├── diff_metrics.py    # Stats 94-100: Diff metrics
│       └── tracking_lines.py  # Stats 101-105: Tracking lines
│
└── models/                    # Data models (dataclasses)
    ├── __init__.py
    ├── message.py             # ✅ Message model (30+ properties)
    ├── session.py             # ✅ Session model (20+ properties)
    └── code_diff.py           # ✅ CodeDiff, DiffChange, CodeTrackingLine models
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
│   ├── APP-ARCHITECTURE.md            # ⭐ Complete app design
│   ├── UI-UX-DESIGN.md                # ⭐ UI/UX specification
│   ├── STATS-CALCULATION-ARCHITECTURE.md # ⭐ Stat system design
│   ├── CURSOR-DATA-EXTRACTION-PLAN.md # Implementation roadmap
│   ├── PURE-STATS-INDEX.md            # ⭐ 232 core stats
│   ├── COMPLETE-STATS-CATALOG.md      # Detailed stats catalog
│   ├── BROWSE-PAGE-SUMMARY.md         # Browse feature design
│   ├── EXPLORATION-COMPLETE.md        # Exploration summary
│   ├── QUICK-REFERENCE.md             # Developer reference
│   ├── CLEANUP-SUMMARY.md             # Cleanup log
│   └── EXHAUSTIVE_DATA_REPORT.md      # Data report
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
conda activate cursor-notepad-browser

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
4. **Daily Usage Calculator** - Implement daily patterns (stats 106-111) - 6 stats ⬅️ NEXT

### Short Term
5. **Token & Model Usage Calculator** - Comprehensive usage stats (stats 112-139) - 28 stats
6. **Error Calculator** - Extract lints and console logs (stats 140-149) - 10 stats
7. **Git Activity Calculator** - Version control metrics (stats 150-159) - 10 stats
8. **Notepad Calculator** - Notepad usage stats (stats 160-169) - 10 stats
9. **Effectiveness Calculator** - Analyze prompt effectiveness (stats 170-200) - 31 stats

### Medium Term
10. **Add Workspace Extraction** - Extract from 227 workspace DBs for full history
11. **Build Streamlit Dashboard** - 7-page UI (Overview, Browse, Stats, Analytics, Calendar, Intelligence, Export)
12. **Full-text Search** - Implement Whoosh for message/session search
13. **Export System** - JSON, CSV, PDF exports

See `docs/planning/APP-ARCHITECTURE.md` for complete roadmap.

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
