# Cursor Data Extractor App - Complete Architecture

**Created: December 22, 2025**

This document defines the complete architecture for the Cursor data extraction and analytics application.

---

## Project Vision

**Build a comprehensive tool that extracts EVERY piece of available local Cursor data and presents it to users for exploration, analysis, and export.**

### Core Principles

1. **Extract Everything** - No data left behind
2. **Raw Data First** - Give users access to unprocessed data
3. **Flexible Export** - JSON, CSV, markdown, PDF
4. **Visual Analytics** - Charts, graphs, timelines
5. **Honest About Gaps** - Clear about data limitations

---

## Data Layers

```
┌──────────────────────────────────────────────────────────────────┐
│                    PRESENTATION LAYER                            │
│  Dashboard UI · Charts · Tables · Export Functions               │
└────────────────┬─────────────────────────────────────────────────┘
                 │
┌────────────────▼─────────────────────────────────────────────────┐
│                    ANALYTICS LAYER                               │
│  Aggregations · Statistics · Calculations · Insights             │
└────────────────┬─────────────────────────────────────────────────┘
                 │
┌────────────────▼─────────────────────────────────────────────────┐
│                    DATA MODEL LAYER                              │
│  Message · Session · CodeMetrics · DailyStats · FileHistory      │
└────────────────┬─────────────────────────────────────────────────┘
                 │
┌────────────────▼─────────────────────────────────────────────────┐
│                    EXTRACTION LAYER                              │
│  cursorDiskKV · ItemTable · Workspaces · FileHistory            │
└────────────────┬─────────────────────────────────────────────────┘
                 │
┌────────────────▼─────────────────────────────────────────────────┐
│                    DATABASE LAYER                                │
│  SQLite Connector · Safe Copying · Transaction Handling          │
└──────────────────────────────────────────────────────────────────┘
```

---

## Complete Data Inventory

### From cursorDiskKV (119,747 rows)

| Key Type | Count | Extract To | Contains |
|----------|-------|------------|----------|
| `bubbleId:*` | 68,657 | `Message` | Text, code, thinking, timestamps |
| `composerData:*` | 1,076 | `Session` | Metadata, headers, token counts |
| `agentKv:blob:*` | 17,471 | `AgentState` | Agent execution state |
| `agentKv:bubbleCheckpoint:*` | 466 | `Checkpoint` | Session checkpoints |
| `codeBlockDiff:*` | 10,527 | `CodeDiff` | Code changes |
| `checkpointId:*` | 14,220 | `SessionCheckpoint` | File states |
| `messageRequestContext:*` | 4,339 | `RequestContext` | Context data |
| `inlineDiffs:*` | 282 | `InlineDiff` | Inline changes |

### From ItemTable (1,288 keys)

| Key Pattern | Type | Extract To | Contains |
|-------------|------|------------|----------|
| `aiCodeTrackingLines` | BLOB | `CodeTracking` | 10,000 AI-written lines |
| `aiCodeTracking.dailyStats.*` | JSON | `DailyStats` | 28 days of usage |
| `aiCodeTrackingScoredCommits` | JSON | `ScoredCommits` | 386 scored commits |
| `terminal.history.entries.commands` | JSON | `TerminalHistory` | Command history |
| `terminal.history.entries.dirs` | JSON | `TerminalHistory` | Directory history |
| `history.recentlyOpenedPathsList` | JSON | `RecentProjects` | Recent folders |
| `freeBestOfN.promptCount` | Number | `Stats` | Total prompts (1,477) |
| `workbench.panel.composerChatViewPane.*` | JSON | `ChatPanelState` | UI state (1,106 keys) |
| `cursorai/serverConfig` | JSON | `ServerConfig` | Server settings |
| `cursorai/featureStatusCache` | JSON | `FeatureFlags` | Feature flags |

### From Workspace Databases (245 databases, 2,354 unique keys)

| Key | Extract To | Contains |
|-----|------------|----------|
| `composer.composerData` | `WorkspaceSession` | Per-workspace sessions (1,858 total) |
| `notepadData` | `Notepad` | Notepad content |
| `aiService.prompts` | `AIPrompts` | AI service prompts |
| `aiService.generations` | `AIGenerations` | AI generations |
| `terminal` | `TerminalState` | Terminal state |
| `editor state keys` | `EditorState` | Editor configuration |

### From File History (2,621 files)

| File | Extract To | Contains |
|------|------------|----------|
| `User/History/{hash}/entries.json` | `FileEditHistory` | Edit timestamps, source |

---

## Data Models

### Core Models

```python
@dataclass
class Message:
    """Individual chat message."""
    bubble_id: str
    composer_id: str
    type: int  # 1=user, 2=AI
    text: Optional[str]
    created_at: datetime
    
    # Model info
    model_info: Optional[Dict]  # modelName, etc
    model_name: Optional[str]
    
    # Content
    code_blocks: List[Dict]
    thinking: Optional[str]
    thinking_duration_ms: Optional[int]
    
    # Metadata
    is_agentic: bool
    token_count: Optional[Dict]  # inputTokens, outputTokens
    tool_results: List[Dict]
    attached_files: List[str]
    
    # Server refs
    server_bubble_id: Optional[str]
    usage_uuid: Optional[str]
    request_id: Optional[str]
    
    # Raw data
    raw_data: Dict

@dataclass
class Session:
    """Chat/Agent session."""
    composer_id: str
    name: Optional[str]
    created_at: datetime
    last_updated_at: Optional[datetime]
    
    # Mode
    unified_mode: str  # "agent" or "chat"
    force_mode: str
    is_agentic: bool
    
    # Messages
    message_ids: List[str]  # bubbleIds
    message_headers: List[Dict]  # from fullConversationHeadersOnly
    
    # Metrics
    total_lines_added: int
    total_lines_removed: int
    context_tokens_used: int
    context_usage_percent: float
    
    # Model
    model_config: Dict
    
    # State
    status: str  # "completed", "none", etc
    is_archived: bool
    has_unread_messages: bool
    
    # Source
    source: str  # "global" or "workspace:{hash}"
    
    # Raw data
    raw_data: Dict

@dataclass
class CodeDiff:
    """Code difference/change."""
    diff_id: str
    composer_id: str
    file_uri: str
    original_lines: List[str]
    new_lines: List[str]
    line_changes: List[Dict]

@dataclass
class DailyStats:
    """Daily usage statistics."""
    date: str  # YYYY-MM-DD
    tab_suggested_lines: int
    tab_accepted_lines: int
    composer_suggested_lines: int
    composer_accepted_lines: int

@dataclass
class CodeTracking:
    """AI code tracking entry."""
    hash: str
    metadata: Dict  # source, composerId, fileExtension, fileName
    
@dataclass
class ScoredCommit:
    """Git commit with AI scoring."""
    commit_hash: str
    commit_message: str
    commit_date: str
    repo_name: str
    branch_name: str
    ai_percentage: float
    lines_added: int
    lines_deleted: int
    composer_lines_added: int
    composer_lines_deleted: int

@dataclass
class TerminalCommand:
    """Terminal command history."""
    command: str
    directory: Optional[str]
    timestamp: Optional[datetime]
    exit_code: Optional[int]

@dataclass
class FileEditHistory:
    """File edit history entry."""
    file_uri: str
    entries: List[Dict]  # id, source, timestamp

@dataclass
class Notepad:
    """Notepad content."""
    workspace_id: str
    content: str
    reactive_storage_id: Optional[str]
```

---

## Extractor Architecture

```
extractors/
├── __init__.py
├── base.py                    # Base extractor interface
│
├── cursordiskkv/
│   ├── __init__.py
│   ├── bubble_extractor.py    # bubbleId extraction
│   ├── composer_extractor.py  # composerData extraction
│   ├── agent_extractor.py     # agentKv extraction
│   ├── diff_extractor.py      # codeBlockDiff extraction
│   └── checkpoint_extractor.py
│
├── itemtable/
│   ├── __init__.py
│   ├── tracking_extractor.py  # aiCodeTrackingLines
│   ├── stats_extractor.py     # dailyStats
│   ├── terminal_extractor.py  # terminal history
│   └── misc_extractor.py      # other ItemTable keys
│
├── workspace/
│   ├── __init__.py
│   ├── workspace_scanner.py   # Find all workspaces
│   ├── session_extractor.py   # composer.composerData
│   └── notepad_extractor.py   # notepadData
│
├── file_history/
│   ├── __init__.py
│   └── history_extractor.py   # User/History scanning
│
└── aggregator.py              # Aggregate from all sources
```

---

## Analytics Modules

```
analytics/
├── __init__.py
├── base.py                    # Base analytics
│
├── message_analytics.py
│   ├── total_count()
│   ├── by_type()             # User vs AI
│   ├── by_date()             # Timeline
│   ├── avg_length()
│   ├── with_code_blocks()
│   └── content_analysis()    # NEW: Text analysis
│
├── session_analytics.py
│   ├── total_count()
│   ├── by_mode()             # Agent vs Chat
│   ├── by_duration()
│   ├── avg_messages_per_session()
│   └── most_active_sessions()
│
├── effectiveness_analytics.py  # NEW MODULE
│   ├── prompt_effectiveness()
│   │   ├── by_length()
│   │   ├── by_specificity()
│   │   └── by_type()
│   ├── context_impact()
│   │   ├── by_tokens_used()
│   │   ├── with_attachments()
│   │   └── with_codebase_context()
│   ├── tool_effectiveness()
│   │   ├── by_tool_type()
│   │   └── tool_combinations()
│   ├── thinking_analysis()
│   │   ├── with_vs_without()
│   │   └── by_duration()
│   ├── iteration_efficiency()
│   │   ├── rounds_to_acceptance()
│   │   └── by_task_type()
│   ├── code_quality()
│   │   ├── retention_rate()
│   │   └── edit_distance()
│   └── conversation_patterns()
│       ├── by_length()
│       └── by_pacing()
│
├── model_analytics.py
│   ├── usage_breakdown()     # With caveat
│   ├── usage_over_time()
│   └── by_mode()
│
├── code_analytics.py
│   ├── total_lines()
│   ├── lines_by_date()
│   ├── acceptance_rate()
│   ├── by_file_type()
│   └── commits_scored()
│
├── token_analytics.py
│   ├── total_tokens()
│   ├── by_session()
│   ├── by_model()
│   └── efficiency_metrics()
│
└── timeline_analytics.py
    ├── activity_heatmap()
    ├── peak_hours()
    ├── daily_usage()
    └── trends()
```

---

## Dashboard UI (Streamlit)

```
dashboard/
├── __init__.py
├── app.py                     # Main Streamlit app
│
├── pages/
│   ├── 01_raw_data.py         # Raw data browser
│   ├── 02_messages.py         # Message explorer
│   ├── 03_sessions.py         # Session browser
│   ├── 04_code_metrics.py     # Code analytics
│   ├── 05_effectiveness.py    # NEW: Effectiveness analysis
│   ├── 06_timeline.py         # Timeline view
│   └── 07_export.py           # Export functions
│
├── components/
│   ├── summary_cards.py       # Metric cards
│   ├── charts.py              # Plotly charts
│   ├── tables.py              # Data tables
│   └── filters.py             # Filter components
│
└── utils/
    ├── formatting.py
    └── export.py
```

---

## Dashboard Pages

### Page 1: Overview / Year Wrapped Style

```
┌─────────────────────────────────────────────────────────┐
│  🎯 Your Cursor Data (Nov 14, 2024 → Dec 22, 2025)     │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  [2,934 Sessions]  [68,657 Messages]  [1,477 Prompts] │
│                                                         │
│  [429,700 Lines Added]  [74,570 Removed]  [386 Commits]│
│                                                         │
│  📊 Activity Heatmap (GitHub style)                    │
│  ████░░░███████░░░░████░░████░░░░░░███                 │
│                                                         │
│  📈 Usage Over Time                                    │
│  [Line chart showing sessions/day]                     │
│                                                         │
│  🤖 Model Usage (11.5% coverage - see note)           │
│  Claude Sonnet: 71% | Opus: 16% | GPT-5: 7%           │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

### Page 2: Raw Data Browser

```
┌─────────────────────────────────────────────────────────┐
│  📊 Raw Data Explorer                                   │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  Select Data Source:                                    │
│  ▼ [Messages (68,657)]                                 │
│    Sessions (2,934)                                     │
│    Code Diffs (10,527)                                  │
│    Daily Stats (28 days)                                │
│    ...                                                  │
│                                                         │
│  Filters:                                               │
│  Date Range: [Nov 2024] to [Dec 2025]                  │
│  Type: [All] [User] [AI]                                │
│  Has Code: [All] [Yes] [No]                             │
│                                                         │
│  [Search: ________________]                             │
│                                                         │
│  Results (100 of 68,657):                               │
│  ┌─────────────────────────────────────────────────┐  │
│  │ bubble_id  | type | text          | created_at │  │
│  ├─────────────────────────────────────────────────┤  │
│  │ abc123...  |  1   | "please make" | 2025-12-21 │  │
│  │ def456...  |  2   | "I'll help"   | 2025-12-21 │  │
│  └─────────────────────────────────────────────────┘  │
│                                                         │
│  [Export Filtered] [Export All] [View Details]         │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

### Page 3: Messages

- Filter by date, type, has code, has thinking
- Search full text
- View individual message details
- Export to JSON/CSV

### Page 4: Sessions

- List all sessions with metadata
- Filter by mode (agent/chat), archived, date
- View session details with all messages
- Session metrics (duration, messages, tokens)

### Page 5: Effectiveness Analysis

```
┌─────────────────────────────────────────────────────────┐
│  🎯 Effectiveness Analysis                              │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  Overall Acceptance Rate: 48.7%                         │
│  ███████████████████████░░░░░░░░░░░░░░░░░░░░░░░        │
│                                                         │
│  📊 Prompt Effectiveness                                │
│  ┌───────────────────────────────────────────────────┐ │
│  │ Specific requests:    52% ████████████            │ │
│  │ General questions:    42% ███████████             │ │
│  │ With context:         56% ██████████████          │ │
│  │ With examples:        58% ███████████████         │ │
│  └───────────────────────────────────────────────────┘ │
│                                                         │
│  🛠️ Tool Impact                                        │
│  ┌───────────────────────────────────────────────────┐ │
│  │ Codebase search:      54% █████████████           │ │
│  │ Web search:           49% ████████████            │ │
│  │ No tools:             45% ███████████             │ │
│  └───────────────────────────────────────────────────┘ │
│                                                         │
│  💭 Thinking Analysis                                   │
│  With thinking: 51% | Without: 46%                     │
│                                                         │
│  🔄 Iteration Patterns                                  │
│  1-2 messages:  38% | 3-5 messages: 51% | 6+: 47%     │
│                                                         │
│  📝 Best Practices (Top 10)                             │
│  1. Include specific file paths → 62% acceptance       │
│  2. Provide code examples → 58% acceptance             │
│  3. Attach relevant files → 56% acceptance             │
│  ...                                                    │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

### Page 6: Timeline

- Lines added/removed over time
- Acceptance rates
- File types modified
- Scored commits
- Daily breakdown

### Page 6: Timeline

- Activity heatmap
- Peak usage hours
- Daily/weekly/monthly trends
- Session frequency

### Page 7: Export

- Select data types
- Choose format (JSON, CSV, Markdown, PDF)
- Batch export options
- Save configurations

---

## Export Formats

### JSON Export
```json
{
  "metadata": {
    "exported_at": "2025-12-22T00:00:00Z",
    "data_range": {"start": "2024-11-14", "end": "2025-12-22"},
    "cursor_version": "0.43.0"
  },
  "messages": [...],
  "sessions": [...],
  "code_metrics": {...},
  "daily_stats": [...]
}
```

### CSV Exports
- `messages.csv` - All messages
- `sessions.csv` - All sessions
- `daily_stats.csv` - Daily usage
- `code_tracking.csv` - Code tracking entries

### Markdown Report
```markdown
# Cursor Usage Report

Generated: 2025-12-22

## Summary
- Total Messages: 68,657
- Total Sessions: 2,934
...

## Daily Breakdown
| Date | Sessions | Messages | Lines Added |
|------|----------|----------|-------------|
...
```

---

## Implementation Priority

### Phase 1: Foundation (Week 1)
- [ ] Database connector with safe copying
- [ ] Base data models (Message, Session, etc)
- [ ] Base extractors (bubble, composer, ItemTable)

### Phase 2: Extraction (Week 2)
- [ ] All cursorDiskKV extractors
- [ ] Workspace aggregation
- [ ] File history extraction
- [ ] Data deduplication

### Phase 3: Analytics (Week 3)
- [ ] Message analytics
- [ ] Session analytics
- [ ] Code metrics
- [ ] Timeline calculations

### Phase 4: Dashboard (Week 4)
- [ ] Streamlit app structure
- [ ] Overview page
- [ ] Raw data browser
- [ ] Export functionality

### Phase 5: Polish (Week 5)
- [ ] Charts and visualizations
- [ ] Additional analytics pages
- [ ] Documentation
- [ ] Testing

---

## File Structure

```
cursor-data-extractor/
├── extractors/         # Data extraction
├── models/             # Data models
├── analytics/          # Analytics calculations
├── dashboard/          # Streamlit UI
├── database/           # DB connectivity
├── utils/              # Utilities
├── tests/              # Tests
├── docs/               # Documentation
├── cursor-data-docs/   # Exploration findings
├── main.py             # CLI entry point
├── requirements.txt
└── README.md
```

---

*This architecture extracts EVERY piece of local Cursor data and makes it available for exploration and analysis.*

