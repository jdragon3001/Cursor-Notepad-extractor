# COMPREHENSIVE DATA EXPLORATION - FINAL REPORT

**Project:** Cursor Data Extractor
**Date:** December 22, 2025
**Status:** Exploration Complete ✅

---

## Executive Summary

We have completed an exhaustive exploration of Cursor IDE's local data storage. We've identified **every available data source**, documented their structure, verified data availability, and created a complete architecture for the extraction app.

---

## What We Found

### Database Tables (2 tables, 121,035 total rows)

| Table | Rows | Description |
|-------|------|-------------|
| **ItemTable** | 1,288 | Settings, configs, tracking data |
| **cursorDiskKV** | 119,747 | Chat messages, sessions, diffs |

### Complete Data Inventory

#### From cursorDiskKV (119,747 rows)

```
bubbleId:                   68,657  (Individual messages)
agentKv:blob:              17,471  (Agent execution state)
checkpointId:              14,220  (Session checkpoints)
codeBlockDiff:             10,527  (Code changes)
messageRequestContext:      4,339  (Request metadata)
composerData:               1,076  (Session metadata)
agentKv:bubbleCheckpoint:     466  (Checkpoints)
inlineDiffs:                  282  (Inline changes)
agentKv:checkpoint:            25  (Checkpoints)
```

#### From ItemTable (1,288 keys)

```
aiCodeTrackingLines:        1 entry  (10,000 AI-written lines tracked)
aiCodeTracking.dailyStats:  28 days  (Nov 20 - Dec 22, 2025)
aiCodeTrackingScoredCommits: 1 entry (386 scored commits)
terminal.history.commands:  1 entry  (Command history)
terminal.history.dirs:      1 entry  (Directory history)
history.recentlyOpened:     1 entry  (Recent projects)
freeBestOfN.promptCount:    1 entry  (1,477 prompts)
composerChatViewPane.*:     1,106 keys (UI state)
```

#### From Workspace Databases (245 databases)

```
composer.composerData:      Per-workspace sessions (1,858 total)
notepadData:                Notepad content
aiService.prompts:          AI service prompts
terminal:                   Terminal state
editor state keys:          Editor configuration (2,354 unique keys)
```

#### From File History (2,621 files)

```
User/History/{hash}/entries.json:  Edit timestamps, source info
```

---

## Verified Metrics (Local Data)

| Metric | Value | Source |
|--------|-------|--------|
| **Total Messages** | 68,657 | cursorDiskKV.bubbleId |
| **Total Sessions** | 2,934 | cursorDiskKV + workspaces (deduplicated) |
| **Total Prompts** | 1,477 | ItemTable.freeBestOfN.promptCount |
| **Input Tokens** | 292,576,040 | bubbleId.tokenCount |
| **Output Tokens** | 3,596,389 | bubbleId.tokenCount |
| **Context Tokens** | 35,343,084 | composerData.contextTokensUsed |
| **Lines Added** | 429,700 | composerData.totalLinesAdded |
| **Lines Removed** | 74,570 | composerData.totalLinesRemoved |
| **Lines Suggested (recent)** | 137,144 | dailyStats (Nov 20+) |
| **Lines Accepted (recent)** | 66,771 | dailyStats (Nov 20+) |
| **Scored Commits** | 386 | aiCodeTrackingScoredCommits |
| **File Types Tracked** | 10,000 | aiCodeTrackingLines |
| **Data Span** | 402 days | Nov 14, 2024 → Dec 22, 2025 |

### Model Usage (11.5% coverage)

```
claude-4.5-sonnet-thinking:    5,610 messages (71%)
claude-4.5-opus-high-thinking: 1,258 messages (16%)
gpt-5:                           537 messages  (7%)
composer-1:                      313 messages  (4%)
gemini-3-pro-preview:            114 messages  (1%)
gemini-3-pro:                     20 messages
gpt-5.1:                          12 messages
grok-4-fast-reasoning:            10 messages
gpt-5-codex:                       5 messages
```

*Note: Only 7,879 of 68,657 messages (11.5%) have model info populated locally.*

---

## Data Timeline

```
Nov 2024 ──────────────────────────────────────────────> Dec 2025
    │                                                         │
    │  Workspace Sessions (1,858)                            │
    │  ════════════════════════════════════════════════════  │
    │                                                         │
    │            cursorDiskKV Messages (68,657)              │
    │            ═══════════════════════════════════════     │
    │                                                         │
    │                        Daily Stats (28 days)           │
    │                        ════════════════════            │
    │                                                         │
Nov 14                    Oct 8          Nov 20         Dec 22
2024                      2025           2025           2025
```

---

## Data Limitations

### Why Local ≠ Server (Year Wrapped)

| Issue | Explanation |
|-------|-------------|
| **Model info sparse** | Only 11.5% of messages have modelInfo |
| **Daily stats recent** | Only tracked since Nov 20, 2025 |
| **Token counts partial** | bubbleId often shows 0 tokens |
| **Server has more** | Year Wrapped uses server-side analytics |

### What We CANNOT Get Locally

❌ Complete model usage breakdown (server-side)
❌ Usage ranking vs other users (requires comparison)
❌ Exact billing tokens (server billing system)
❌ Historical daily stats (pre-Nov 20, 2025)
❌ Streak calculations (may be server-side)

---

## Documentation Created

| File | Purpose |
|------|---------|
| `cursor-data-docs/README.md` | Master overview |
| `cursor-data-docs/01-DATA-SOURCES-OVERVIEW.md` | Complete data source map |
| `cursor-data-docs/02-GLOBAL-STATE-DATABASE.md` | 2.4GB global database |
| `cursor-data-docs/03-WORKSPACE-DATABASES.md` | Per-project databases |
| `cursor-data-docs/04-FILE-HISTORY.md` | Edit history |
| `cursor-data-docs/05-LOGS-AND-TELEMETRY.md` | Log files |
| `cursor-data-docs/06-OTHER-SOURCES.md` | WebStorage, LevelDB |
| `cursor-data-docs/07-KEY-VALUE-SCHEMA.md` | Key schemas |
| `cursor-data-docs/08-CURSORDISKKV-GOLDMINE.md` | Chat data source |
| `cursor-data-docs/09-EXHAUSTIVE-DATA-REPORT.md` | Full exploration |
| `cursor-data-docs/10-CHAT-DATA-RECOVERY-REPORT.md` | Multi-source recovery |
| `cursor-data-docs/11-DAILY-USAGE-STATS.md` | Daily line counts |
| `cursor-data-docs/12-DATA-LIMITATIONS.md` | Why numbers differ |
| `cursor-data-docs/13-MESSAGE-CONTENT-ANALYSIS.md` | **Message content & effectiveness** |
| `nextsteps/APP-ARCHITECTURE.md` | **Complete app design** |
| `nextsteps/CURSOR-DATA-EXTRACTION-PLAN.md` | Implementation plan |

### Exploration Scripts Created

| Script | Purpose |
|--------|---------|
| `recover_all_chat_data.py` | Multi-source data recovery |
| `extract_daily_stats.py` | Daily usage extraction |
| `find_earliest_entry.py` | Timeline boundaries |
| `verify_model_and_tokens.py` | Model/token validation |
| `deep_model_token_search.py` | Deep model search |
| `check_all_sources_deep.py` | Comprehensive check |
| `final_comprehensive_check.py` | Final verification |
| `exhaustive_exploration.py` | Complete catalog |
| `explore_cursorDiskKV.py` | cursorDiskKV deep dive |

---

## App Architecture (Designed)

### Data Flow

```
Raw SQLite Data
      ↓
Extractors (by source)
      ↓
Data Models (typed)
      ↓
Analytics Engine
      ↓
Dashboard UI (Streamlit)
      ↓
Export (JSON/CSV/PDF)
```

### Key Features

1. **Raw Data Browser** - View ALL extracted data
2. **Message Explorer** - Search, filter, view messages
3. **Session Browser** - Browse chat/agent sessions
4. **Code Metrics** - Lines added/removed, acceptance rates
5. **Timeline View** - Activity heatmap, trends
6. **Export** - Multiple formats (JSON, CSV, Markdown, PDF)

### Data Models Defined

- `Message` - Individual chat message
- `Session` - Chat/agent session
- `CodeDiff` - Code change
- `DailyStats` - Daily usage
- `CodeTracking` - AI-written code
- `ScoredCommit` - Git commit with AI %
- `TerminalCommand` - Command history
- `FileEditHistory` - File edits
- `Notepad` - Notepad content

---

## Implementation Plan

### Phase 1: Foundation
- Database connector
- Base data models
- Base extractors

### Phase 2: Extraction
- All cursorDiskKV extractors
- Workspace aggregation
- Deduplication

### Phase 3: Analytics
- Message analytics
- Session analytics
- Code metrics

### Phase 4: Dashboard
- Streamlit app
- Raw data browser
- Export functions

### Phase 5: Polish
- Visualizations
- Additional pages
- Documentation

---

## Key Insights

1. **Multi-source required** - Must read from cursorDiskKV + workspaces
2. **cursorDiskKV is richest** - Full message content, code, thinking
3. **Workspaces have older data** - Sessions from Nov 2024
4. **Daily stats are recent** - Only since Nov 20, 2025
5. **Model info is sparse** - Only 11.5% of messages
6. **Local ≠ Server** - Year Wrapped uses server data

---

## What the App Will Do

### ✅ WILL Provide

- Complete message history (68K messages) with full text/code/thinking
- Session metadata (2,934 sessions)
- Lines of code metrics (429K added)
- Daily usage trends (28 days)
- Code tracking data (10K entries)
- Terminal history
- File edit history
- Notepad content
- **Effectiveness analysis:**
  - Prompt quality metrics
  - Context impact analysis
  - Tool usage effectiveness
  - Thinking correlation
  - Iteration efficiency
  - Code quality indicators
  - Conversation patterns
  - Acceptance/rejection tracking
- Export in multiple formats
- Search and filter all data
- Timeline visualizations

### ⚠️ WITH Caveats

- Model usage (only 11.5% coverage)
- Token counts (partial data)
- Daily stats (only recent)

### ❌ CANNOT Provide

- Usage ranking vs other users
- Exact billing/cost data
- Complete model breakdown
- Server-side analytics

---

## Conclusion

We have **successfully mapped every local data source** in Cursor IDE. We know exactly what data is available, where it's stored, how to extract it, and what the limitations are.

**The app architecture is complete and ready for implementation.**

**Next Step: Begin Phase 1 - Build the foundation (database connector, models, base extractors).**

---

*Exploration conducted December 21-22, 2025. All data verified against live Cursor installation.*

