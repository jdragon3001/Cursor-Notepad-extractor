# Quick Reference: Data Sources & Extraction

**For developers building the Cursor Data Extractor**

---

## Primary Data Sources

### 1. Messages (bubbleId) - 68,657 entries

**Location:** `cursorDiskKV` table, global database
**Key:** `bubbleId:{composerId}:{messageId}`

```python
# Extract
cursor.execute("SELECT key, value FROM cursorDiskKV WHERE key LIKE 'bubbleId:%'")

# Contains
{
  "type": 1 or 2,  # 1=user, 2=AI
  "text": "message content",
  "codeBlocks": [...],
  "thinking": "AI reasoning",
  "toolResults": [...],
  "modelInfo": {"modelName": "..."},
  "tokenCount": {"inputTokens": X, "outputTokens": Y},
  "createdAt": timestamp,
  ...
}
```

**Key for effectiveness:** `text`, `codeBlocks`, `thinking`, `toolResults`, `attachedCodeChunks`, `userResponsesToSuggestedCodeBlocks`

---

### 2. Sessions (composerData) - 2,934 total

**Location:** 
- Global: `cursorDiskKV` table, key `composerData:*` (1,076 entries)
- Workspaces: `ItemTable`, key `composer.composerData` (1,858 entries across 227 DBs)

```python
# Extract from global
cursor.execute("SELECT key, value FROM cursorDiskKV WHERE key LIKE 'composerData:%'")

# Extract from workspace
ws_cursor.execute("SELECT value FROM ItemTable WHERE key = 'composer.composerData'")

# Contains
{
  "composerId": "uuid",
  "name": "session name",
  "totalLinesAdded": 2500,
  "totalLinesRemoved": 100,
  "contextTokensUsed": 45000,
  "fullConversationHeadersOnly": [...],
  "createdAt": timestamp,
  ...
}
```

**Key for effectiveness:** `totalLinesAdded`, `totalLinesRemoved`, `contextTokensUsed`, `fullConversationHeadersOnly`

---

### 3. Code Diffs (codeBlockDiff) - 10,527 entries

**Location:** `cursorDiskKV` table, global database
**Key:** `codeBlockDiff:{composerId}:{diffId}`

```python
# Extract
cursor.execute("SELECT key, value FROM cursorDiskKV WHERE key LIKE 'codeBlockDiff:%'")

# Contains
{
  "newModelDiffWrtV0": [{
    "original": {"startLineNumber": 30, ...},
    "modified": {"startLineNumber": 30, ...},
    "originalContent": [...],
    "modifiedContent": [...]
  }]
}
```

**Key for effectiveness:** Line-by-line changes, edit distance

---

### 4. Daily Stats - 28 days

**Location:** `ItemTable`, global database
**Key:** `aiCodeTracking.dailyStats.v1.5.{YYYY-MM-DD}`

```python
# Extract
cursor.execute("SELECT key, value FROM ItemTable WHERE key LIKE 'aiCodeTracking.dailyStats%'")

# Contains
{
  "date": "2025-12-22",
  "composerSuggestedLines": 5049,
  "composerAcceptedLines": 2783,
  "tabSuggestedLines": 0,
  "tabAcceptedLines": 0
}
```

**Acceptance rate:** `composerAcceptedLines / composerSuggestedLines`

---

### 5. Code Tracking - 10,000 entries

**Location:** `ItemTable`, global database
**Key:** `aiCodeTrackingLines`

```python
# Extract
cursor.execute("SELECT value FROM ItemTable WHERE key = 'aiCodeTrackingLines'")

# Returns list of
{
  "hash": "abc123",
  "metadata": {
    "source": "composer",
    "composerId": "uuid",
    "fileExtension": "tsx",
    "fileName": "/path/to/file"
  }
}
```

---

## Database Paths

```python
import os
from pathlib import Path

# Global database
GLOBAL_DB = Path.home() / 'AppData/Roaming/Cursor/User/globalStorage/state.vscdb'

# Workspace databases
WORKSPACE_DIR = Path.home() / 'AppData/Roaming/Cursor/User/workspaceStorage'
# Each workspace: {WORKSPACE_DIR}/{hash}/state.vscdb

# File history
HISTORY_DIR = Path.home() / 'AppData/Roaming/Cursor/User/History'
# Each file: {HISTORY_DIR}/{hash}/entries.json
```

---

## Extraction Order

### Phase 1: Foundation
1. Connect to global database
2. Extract all `bubbleId` entries → `Message` objects
3. Extract all `composerData` from global → `Session` objects
4. Extract `dailyStats` → `DailyStats` objects

### Phase 2: Workspace Data
5. Scan all workspace databases
6. Extract `composer.composerData` from each
7. Deduplicate sessions by `composerId`
8. Merge workspace sessions with global sessions

### Phase 3: Code Data
9. Extract `codeBlockDiff` entries
10. Extract `aiCodeTrackingLines`
11. Link diffs to sessions

### Phase 4: Linking
12. Link messages to sessions (by `composerId`)
13. Link diffs to sessions
14. Build conversation sequences

---

## Key Relationships

```
Session (composerData)
  ├─> Messages (bubbleId) - linked by composerId
  │     ├─> CodeBlocks - embedded in message
  │     ├─> ToolResults - embedded in message
  │     └─> Thinking - embedded in message
  ├─> CodeDiffs (codeBlockDiff) - linked by composerId
  └─> Metrics - totalLinesAdded, contextTokensUsed
```

---

## Data Quality Notes

| Field | Coverage | Notes |
|-------|----------|-------|
| `bubbleId.text` | ~23% | Not all messages have text |
| `bubbleId.codeBlocks` | ~14% | Code generation messages |
| `bubbleId.thinking` | ~32% | AI reasoning process |
| `bubbleId.modelInfo` | 11.5% | Model name (sparse!) |
| `bubbleId.tokenCount` | ~4% | Often zero |
| `composerData.totalLinesAdded` | 100% | Always present |
| `dailyStats` | 28 days | Only since Nov 20, 2025 |

---

## Effectiveness Calculations

### Acceptance Rate (Recent)
```python
daily = get_daily_stats()
total_suggested = sum(d.composerSuggestedLines for d in daily)
total_accepted = sum(d.composerAcceptedLines for d in daily)
acceptance_rate = total_accepted / total_suggested  # 48.7%
```

### Prompt Effectiveness
```python
messages = get_all_messages()
user_prompts = [m for m in messages if m.type == 1]

# Categorize
specific = [p for p in user_prompts if has_file_references(p.text)]
general = [p for p in user_prompts if not has_file_references(p.text)]

# Get acceptance for sessions
specific_sessions = get_sessions(specific)
specific_acceptance = mean(s.totalLinesAdded for s in specific_sessions)
```

### Context Impact
```python
sessions = get_all_sessions()
high_context = [s for s in sessions if s.contextTokensUsed > 50000]
low_context = [s for s in sessions if s.contextTokensUsed < 10000]

high_acceptance = mean(s.totalLinesAdded for s in high_context)
low_acceptance = mean(s.totalLinesAdded for s in low_context)
```

---

## Documentation References

| Topic | File |
|-------|------|
| Complete data sources | `cursor-data-docs/01-DATA-SOURCES-OVERVIEW.md` |
| cursorDiskKV schema | `cursor-data-docs/08-CURSORDISKKV-GOLDMINE.md` |
| Daily stats | `cursor-data-docs/11-DAILY-USAGE-STATS.md` |
| Data limitations | `cursor-data-docs/12-DATA-LIMITATIONS.md` |
| **Message/content analysis** | **`cursor-data-docs/13-MESSAGE-CONTENT-ANALYSIS.md`** |
| App architecture | `nextsteps/APP-ARCHITECTURE.md` |

---

## Code Snippets

### Connect to Database
```python
import sqlite3
from pathlib import Path

db_path = Path.home() / 'AppData/Roaming/Cursor/User/globalStorage/state.vscdb'
conn = sqlite3.connect(str(db_path))
cursor = conn.cursor()
```

### Extract Messages
```python
import json

cursor.execute("SELECT key, value FROM cursorDiskKV WHERE key LIKE 'bubbleId:%'")
messages = []
for key, value in cursor.fetchall():
    data = json.loads(value) if isinstance(value, str) else json.loads(value.decode('utf-8'))
    messages.append(data)
```

### Extract Sessions
```python
cursor.execute("SELECT key, value FROM cursorDiskKV WHERE key LIKE 'composerData:%'")
sessions = []
for key, value in cursor.fetchall():
    data = json.loads(value) if isinstance(value, str) else json.loads(value.decode('utf-8'))
    sessions.append(data)
```

### Link Messages to Sessions
```python
from collections import defaultdict

by_session = defaultdict(list)
for message in messages:
    composer_id = message.get('composerId')
    if composer_id:
        by_session[composer_id].append(message)

# Add to sessions
for session in sessions:
    session['messages'] = by_session[session['composerId']]
```

---

*Quick reference for building the Cursor Data Extractor. See full documentation for details.*

