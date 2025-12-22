# Cursor Data Extraction & Analytics Tool - Project Plan

**Created: December 22, 2025**
**Status: Data Exploration Complete - Ready for Implementation**

---

## Executive Summary

We have completed exhaustive exploration of Cursor's local data storage. **CRITICAL FINDING:** Complete chat history requires reading from MULTIPLE sources - the global database only has data from October 2025, but workspace databases contain data back to November 2024.

---

## PART 1: VERIFIED DATA INVENTORY

### 1.1 Total Data Available

| Metric | Value | Notes |
|--------|-------|-------|
| **Total Chat Sessions** | 2,934 | Combined from all sources |
| **Total Messages** | 68,636 | From cursorDiskKV |
| **Total Input Tokens** | 292,321,753 | ~292M tokens! |
| **Total Output Tokens** | 3,566,388 | |
| **Lines of Code Added** | 429,700 | From AI assistance |
| **Lines of Code Removed** | 74,570 | |
| **Data Span** | 402 days | Nov 14, 2024 → Dec 22, 2025 |
| **Workspace Databases** | 227 | With chat data |

### 1.2 Data Source Timeline

```
Nov 2024 ─────────────────────────────────────────────> Dec 2025
    │                                                       │
    │  [WORKSPACE DATABASES: 1,858 sessions]               │
    │  ════════════════════════════════════════════════════│
    │                                                       │
    │                          [cursorDiskKV: 1,076 sessions]
    │                          ════════════════════════════│
    │                          │                           │
    └──────────────────────────┴───────────────────────────┘
                              Oct 2025
                         (Global DB reset?)
```

### 1.3 Model Usage Breakdown

```
claude-4.5-sonnet-thinking:    5,610 messages (71.2%)
claude-4.5-opus-high-thinking: 1,251 messages (15.9%)
gpt-5:                           537 messages  (6.8%)
composer-1:                      313 messages  (4.0%)
gemini-3-pro-preview:            114 messages  (1.4%)
gemini-3-pro:                     20 messages  (0.3%)
gpt-5.1:                          12 messages  (0.2%)
grok-4-fast-reasoning:            10 messages  (0.1%)
gpt-5-codex:                       5 messages  (0.1%)
```

---

## PART 2: DATA SOURCES (VERIFIED)

### 2.1 Primary: Global cursorDiskKV Table

**Location:** `%APPDATA%\Cursor\User\globalStorage\state.vscdb` → Table: `cursorDiskKV`
**Date Range:** October 8, 2025 → Present

| Key Prefix | Count | Description |
|------------|-------|-------------|
| `bubbleId:` | 68,636 | Individual messages (user + AI) |
| `agentKv:` | 17,962 | Agent state data |
| `checkpointId:` | 14,220 | Session checkpoints |
| `codeBlockDiff:` | 10,527 | Code diff information |
| `messageRequestContext:` | 4,339 | Request context |
| `composerData:` | 1,076 | Chat session metadata |
| `inlineDiffs:` | 282 | Inline code changes |

**Contains:**
- ✅ Full message text
- ✅ Model info (modelName)
- ✅ Token counts (input/output)
- ✅ Timestamps (createdAt)
- ✅ Agentic mode flag
- ✅ Code blocks and diffs

### 2.2 Secondary: Workspace Databases

**Location:** `%APPDATA%\Cursor\User\workspaceStorage\{hash}\state.vscdb`
**Date Range:** November 14, 2024 → Present
**Count:** 227 workspaces with chat data

**Key:** `composer.composerData`

**Contains:**
- ✅ Session metadata (composerId, name, createdAt)
- ✅ Lines added/removed
- ✅ Unified mode (agent/chat)
- ⚠️ Limited message content (headers only for older sessions)

### 2.3 Other Sources

| Source | Location | Contains |
|--------|----------|----------|
| ItemTable | Global state.vscdb | aiCodeTrackingLines, terminal history |
| File History | User/History/ | 2,621 file edit entries |
| Local Storage | Local Storage/leveldb | Minimal data (6.8KB) |
| IndexedDB | Partitions/*/IndexedDB | Browser data (2 partitions) |
| Backups | Backups/ | Empty (0 MB) |

---

## PART 3: IMPLEMENTATION PLAN

### Phase 1: Core Data Extraction (Priority: CRITICAL)

#### 1.1 Multi-Source Aggregator

```python
class CursorDataAggregator:
    """Aggregates chat data from ALL sources."""
    
    def __init__(self, cursor_base_path: Path):
        self.global_db = cursor_base_path / 'User/globalStorage/state.vscdb'
        self.workspace_dir = cursor_base_path / 'User/workspaceStorage'
    
    def extract_all_sessions(self) -> Dict[str, Session]:
        """Extract and deduplicate sessions from all sources."""
        all_sessions = {}
        
        # 1. Global cursorDiskKV (richest data, Oct 2025+)
        for session in self._extract_from_global():
            all_sessions[session.composer_id] = session
        
        # 2. Workspace databases (older data, Nov 2024+)
        for workspace in self._get_workspaces():
            for session in self._extract_from_workspace(workspace):
                if session.composer_id not in all_sessions:
                    all_sessions[session.composer_id] = session
                else:
                    # Merge data from both sources
                    all_sessions[session.composer_id].merge(session)
        
        return all_sessions
```

#### 1.2 Data Models

```python
@dataclass
class Message:
    bubble_id: str
    composer_id: str
    type: int  # 1=user, 2=AI
    text: str
    created_at: datetime
    model_info: Optional[Dict]
    token_count: Optional[Dict]
    is_agentic: bool
    code_blocks: List[Dict]

@dataclass
class Session:
    composer_id: str
    name: str
    created_at: datetime
    last_updated_at: Optional[datetime]
    unified_mode: str  # "agent" or "chat"
    messages: List[Message]
    total_lines_added: int
    total_lines_removed: int
    context_tokens_used: int
    source: str  # "global" or "workspace:{hash}"

@dataclass 
class CursorAnalytics:
    total_sessions: int
    total_messages: int
    total_input_tokens: int
    total_output_tokens: int
    total_lines_added: int
    total_lines_removed: int
    model_usage: Dict[str, int]
    sessions_by_date: Dict[str, int]
    earliest_date: datetime
    latest_date: datetime
```

### Phase 2: Analytics Engine

#### 2.1 Metrics to Calculate

| Category | Metrics |
|----------|---------|
| **Usage** | Total sessions, messages, tokens |
| **Timeline** | Sessions/day, peak hours, streak days |
| **Models** | Usage by model, model preference over time |
| **Code** | Lines added/removed, net contribution, velocity |
| **Behavior** | Agent vs Chat ratio, avg conversation length |

#### 2.2 Implementation

```python
class CursorAnalytics:
    def __init__(self, sessions: Dict[str, Session]):
        self.sessions = sessions
    
    def calculate_all(self) -> AnalyticsReport:
        return AnalyticsReport(
            total_sessions=len(self.sessions),
            total_messages=self._count_messages(),
            total_tokens=self._sum_tokens(),
            model_usage=self._calculate_model_usage(),
            timeline=self._build_timeline(),
            code_metrics=self._calculate_code_metrics(),
            insights=self._generate_insights()
        )
```

### Phase 3: Dashboard UI

- Streamlit or Gradio app
- "Year Wrapped" style summary cards
- Interactive charts (Plotly)
- Export functionality

---

## PART 4: TECHNICAL ARCHITECTURE

```
cursor-data-extractor/
├── extractors/
│   ├── __init__.py
│   ├── base.py                 # Base extractor interface
│   ├── global_extractor.py     # cursorDiskKV extraction
│   ├── workspace_extractor.py  # Workspace DB extraction
│   └── aggregator.py           # Multi-source aggregation
├── models/
│   ├── __init__.py
│   ├── message.py              # Message dataclass
│   ├── session.py              # Session dataclass
│   └── analytics.py            # Analytics dataclass
├── analytics/
│   ├── __init__.py
│   ├── calculator.py           # Metrics calculation
│   ├── timeline.py             # Timeline analysis
│   └── insights.py             # Insight generation
├── dashboard/
│   ├── __init__.py
│   ├── app.py                  # Streamlit app
│   └── components/
│       ├── summary_cards.py
│       ├── charts.py
│       └── export.py
├── database/
│   ├── __init__.py
│   ├── connector.py            # Safe DB connection
│   └── cursor_db.py            # Existing code (enhanced)
├── utils/
│   ├── __init__.py
│   ├── config.py               # Configuration
│   └── timestamps.py           # Timestamp utilities
├── cursor-data-docs/           # Documentation
│   └── *.md
├── main.py                     # Entry point
└── requirements.txt
```

---

## PART 5: IMPLEMENTATION CHECKLIST

### Immediate Tasks (This Session)

- [x] Explore all data sources exhaustively
- [x] Verify data availability and timestamps
- [x] Document multi-source requirement
- [x] Create recovery report
- [ ] Build `GlobalExtractor` class
- [ ] Build `WorkspaceExtractor` class
- [ ] Build `DataAggregator` class
- [ ] Test extraction on sample data

### Short Term

- [ ] Build analytics calculator
- [ ] Create CLI report generator
- [ ] Validate all metrics match exploration findings
- [ ] Handle edge cases (locked DBs, missing fields)

### Medium Term

- [ ] Build Streamlit dashboard
- [ ] Add visualizations (charts, heatmaps)
- [ ] Create "Year Wrapped" summary view
- [ ] Add export to JSON/PDF

---

## PART 6: DATA QUALITY NOTES

### Confirmed Working

| Field | Source | Status |
|-------|--------|--------|
| Message text | bubbleId.text | ✅ |
| Message type | bubbleId.type | ✅ (1=user, 2=AI) |
| Model name | bubbleId.modelInfo.modelName | ✅ |
| Token counts | bubbleId.tokenCount | ⚠️ (often zero) |
| Session name | composerData.name | ✅ |
| Created at | composerData.createdAt | ✅ |
| Lines added | composerData.totalLinesAdded | ✅ |
| Agentic mode | bubbleId.isAgentic | ✅ |

### Caveats

- ~96% of bubble entries have zero token counts
- Token data more reliable from composerData.contextTokensUsed
- Must aggregate from BOTH global and workspace DBs for complete history
- Database may be locked while Cursor is running - copy first

### Not Available Locally

- Usage ranking vs other users (server-side)
- Exact billing/cost data (server-side)
- Streak calculations (may be server-side)

---

## PART 7: KEY FILE LOCATIONS

```
GLOBAL DATABASE:
  %APPDATA%\Cursor\User\globalStorage\state.vscdb
  └── Tables: ItemTable, cursorDiskKV

WORKSPACE DATABASES:
  %APPDATA%\Cursor\User\workspaceStorage\{hash}\state.vscdb
  └── Table: ItemTable (key: composer.composerData)

FILE HISTORY:
  %APPDATA%\Cursor\User\History\{hash}\entries.json

LOGS:
  %APPDATA%\Cursor\logs\
```

---

## Appendix: Data Exploration Scripts

| Script | Purpose |
|--------|---------|
| `recover_all_chat_data.py` | Find chat data from ALL sources |
| `find_earliest_entry.py` | Determine data timeline |
| `verify_model_and_tokens.py` | Validate model/token extraction |
| `exhaustive_exploration.py` | Full data catalog |
| `explore_cursorDiskKV.py` | Deep dive into chat data |
| `quick_analysis.py` | Quick stats overview |

---

*Document updated after comprehensive data exploration. All findings verified against actual database queries.*
