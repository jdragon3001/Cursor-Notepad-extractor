# Cursor IDE Data Documentation

**Created: December 21, 2025**
**Updated: December 22, 2025**

This documentation catalogs all data sources found in Cursor IDE's local storage.

---

## ⚠️ CRITICAL: Local Data vs Server Data

**Cursor Year Wrapped uses SERVER-SIDE data which is more complete than local storage.**

Local limitations:
- Model info only available for 11.5% of messages
- Daily stats only since Nov 20, 2025
- Token counts partially populated
- Server has authoritative billing/usage data

See `12-DATA-LIMITATIONS.md` for full details.

---

## 🎯 Verified Local Data (What We CAN Extract)

| Metric | Value | Source |
|--------|-------|--------|
| **Total Chat Sessions** | 2,934 | cursorDiskKV + workspaces |
| **Total Messages** | 68,657 | cursorDiskKV |
| **Total Prompts** | 1,477 | freeBestOfN.promptCount |
| **Input Tokens** | 292,576,040 | bubbleId.tokenCount |
| **Output Tokens** | 3,596,389 | bubbleId.tokenCount |
| **Lines of Code Added** | 429,700 | composerData.totalLinesAdded |
| **Lines Removed** | 74,570 | composerData.totalLinesRemoved |
| **Scored Commits** | 386 | aiCodeTrackingScoredCommits |
| **Data Span** | 402 days | Nov 14, 2024 → Dec 22, 2025 |

### Model Usage (11.5% of messages)
```
claude-4.5-sonnet-thinking:    5,610 (71%)
claude-4.5-opus-high-thinking: 1,258 (16%)
gpt-5:                           537 (7%)
composer-1:                      313 (4%)
gemini-3-pro-preview:            114 (1%)
```
*Note: Only 7,879 of 68,657 messages have model info.*

### Daily Stats (Since Nov 20, 2025)
```
Composer Lines Suggested: 137,144
Composer Lines Accepted:   66,771 (48.7% rate)
Tab Lines Suggested:          195
Tab Lines Accepted:             2
```

---

## Data Source Timeline

```
Nov 2024 ─────────────────────────────────────────────> Dec 2025
    │                                                       │
    │  [WORKSPACE DATABASES: Sessions since Nov 14, 2024]  │
    │  ════════════════════════════════════════════════════│
    │                                                       │
    │                     [cursorDiskKV: Messages Oct 8, 2025+]
    │                     ═════════════════════════════════│
    │                                                       │
    │                              [Daily Stats: Nov 20, 2025+]
    │                              ════════════════════════│
```

---

## Documentation Files

| File | Description |
|------|-------------|
| [01-DATA-SOURCES-OVERVIEW.md](01-DATA-SOURCES-OVERVIEW.md) | Complete data source map |
| [02-GLOBAL-STATE-DATABASE.md](02-GLOBAL-STATE-DATABASE.md) | Main 2.4GB database |
| [03-WORKSPACE-DATABASES.md](03-WORKSPACE-DATABASES.md) | Per-project databases (245) |
| [04-FILE-HISTORY.md](04-FILE-HISTORY.md) | Edit history (2,605 files) |
| [05-LOGS-AND-TELEMETRY.md](05-LOGS-AND-TELEMETRY.md) | Session logs |
| [06-OTHER-SOURCES.md](06-OTHER-SOURCES.md) | WebStorage, Partitions |
| [07-KEY-VALUE-SCHEMA.md](07-KEY-VALUE-SCHEMA.md) | Key schemas |
| [**08-CURSORDISKKV-GOLDMINE.md**](08-CURSORDISKKV-GOLDMINE.md) | Chat data source |
| [09-EXHAUSTIVE-DATA-REPORT.md](09-EXHAUSTIVE-DATA-REPORT.md) | Full exploration |
| [**10-CHAT-DATA-RECOVERY-REPORT.md**](10-CHAT-DATA-RECOVERY-REPORT.md) | Multi-source recovery |
| [**11-DAILY-USAGE-STATS.md**](11-DAILY-USAGE-STATS.md) | Daily line counts |
| [**12-DATA-LIMITATIONS.md**](12-DATA-LIMITATIONS.md) | Why numbers differ |
| [**13-MESSAGE-CONTENT-ANALYSIS.md**](13-MESSAGE-CONTENT-ANALYSIS.md) | **Content & effectiveness data** |

---

## Data Sources

### Primary: cursorDiskKV Table (119,605 rows)

| Key Prefix | Count | Contains |
|------------|-------|----------|
| `bubbleId:` | 68,657 | Messages (user + AI) |
| `agentKv:` | 17,962 | Agent state |
| `checkpointId:` | 14,220 | Checkpoints |
| `codeBlockDiff:` | 10,527 | Code diffs |
| `composerData:` | 1,076 | Session metadata |

### Secondary: ItemTable Keys

| Key | Data |
|-----|------|
| `aiCodeTrackingLines` | 10,000 AI-written code entries |
| `aiCodeTracking.dailyStats.*` | 28 days of usage stats |
| `aiCodeTrackingScoredCommits` | 386 scored commits |
| `freeBestOfN.promptCount` | 1,477 prompts |
| `terminal.history.*` | Command history |

### Tertiary: Workspace Databases

- 227 workspaces with chat data
- Contains older sessions (Nov 2024+)
- Has `composer.composerData` with `allComposers`

---

## Data Extraction Strategy

```python
def extract_complete_data():
    data = {}
    
    # 1. Recent messages from cursorDiskKV
    data['messages'] = extract_from_cursorDiskKV()  # 68K messages
    
    # 2. Sessions from cursorDiskKV + workspaces (dedupe by composerId)
    data['sessions'] = aggregate_sessions()  # 2,934 sessions
    
    # 3. Daily stats
    data['daily_stats'] = extract_daily_stats()  # 28 days
    
    # 4. Code metrics from composerData
    data['code_metrics'] = extract_code_metrics()  # 429K lines
    
    # 5. Other stats
    data['prompt_count'] = get_prompt_count()  # 1,477
    data['commits'] = get_scored_commits()  # 386
    
    return data
```

---

## Scripts

| Script | Purpose |
|--------|---------|
| `recover_all_chat_data.py` | Multi-source data recovery |
| `extract_daily_stats.py` | Daily usage statistics |
| `deep_model_token_search.py` | Model/token analysis |
| `check_all_sources_deep.py` | Comprehensive source check |
| `find_earliest_entry.py` | Timeline boundaries |
| `verify_model_and_tokens.py` | Data validation |

---

## Key Insights

1. **Local ≠ Server** - Year Wrapped uses server-side data
2. **Multi-source required** - Must aggregate cursorDiskKV + workspaces
3. **Model info sparse** - Only 11.5% has modelInfo
4. **Daily stats recent** - Only since Nov 20, 2025
5. **Lines of code solid** - 429K from composerData is reliable
6. **Messages complete** - 68K messages with full text

---

## What to Build

The data extraction app should:
1. ✅ Show total sessions/messages (reliable)
2. ✅ Show lines of code added/removed (reliable)
3. ✅ Show daily usage trends (since Nov 20)
4. ✅ **Extract ALL message content for analysis** (text, code, thinking)
5. ✅ **Perform effectiveness analyses** (prompt quality, acceptance rates)
6. ⚠️ Show model usage (with "partial data" caveat)
7. ⚠️ Show token usage (local data, not billing)
8. ❌ Skip usage ranking (server-side only)

### Effectiveness Analysis Features

**Available data for analysis:**
- 68,657 messages with text, code, and thinking
- User prompts vs AI responses (3,970 vs 64,681)
- Acceptance/rejection tracking
- Tool usage data (codebase search, web search, etc.)
- Context provided (attached files, codebase chunks)
- Code diffs (10,527 changes)
- Thinking process (32% of messages)
- Iteration patterns

**See:** `13-MESSAGE-CONTENT-ANALYSIS.md` for complete details

---

## Disclaimer

This documentation is for educational purposes. Local data extraction cannot replicate server-side analytics like Year Wrapped.
