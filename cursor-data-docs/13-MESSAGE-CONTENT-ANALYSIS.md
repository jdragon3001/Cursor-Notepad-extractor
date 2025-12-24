# Message Content & Effectiveness Analysis - Complete Guide

**Created: December 22, 2025**
**Purpose: Document ALL message/content data available for effectiveness analysis**

---

## Overview

This document catalogs EVERY piece of content data available in Cursor's local storage, where it's stored, how to extract it, and what analyses we can perform.

---

## Data Sources for Content Analysis

### 1. bubbleId (68,657 entries) - PRIMARY SOURCE

**Location:** `cursorDiskKV` table
**Key Pattern:** `bubbleId:{composerId}:{messageId}`
**Data Type:** JSON blob

#### What Each Entry Contains

```python
{
  # IDENTIFIERS
  "bubbleId": "abc123-def456...",
  "composerId": "session-uuid",
  "type": 1 or 2,  # 1 = user prompt, 2 = AI response
  "createdAt": 1734567890123,  # Unix ms timestamp
  
  # MESSAGE CONTENT
  "text": "please make the education section look better...",
  "richText": "{\"root\":{\"children\":[{\"type\":\"paragraph\",\"children\":[...]}]}}",
  
  # CODE CONTENT
  "codeBlocks": [
    {
      "code": "export const Component = () => {...}",
      "language": "typescript",
      "filePath": "/path/to/file.tsx",
      "startLine": 10,
      "endLine": 50
    }
  ],
  
  # AI REASONING
  "thinking": "Let me analyze the current implementation...",
  "thinkingDurationMs": 1234,
  "allThinkingBlocks": [...],
  
  # TOOL USAGE
  "toolResults": [
    {
      "toolName": "codebase_search",
      "query": "education component",
      "results": [...]
    }
  ],
  "supportedTools": ["codebase_search", "grep", "read_file"],
  
  # CONTEXT PROVIDED
  "attachedCodeChunks": [
    {
      "content": "...",
      "uri": "file:///path/to/file.ts",
      "startLine": 1,
      "endLine": 100
    }
  ],
  "codebaseContextChunks": [...],  # Auto-retrieved context
  "relevantFiles": [...],
  "recentlyViewedFiles": [...],
  
  # WEB/EXTERNAL REFERENCES
  "webReferences": [...],
  "aiWebSearchResults": [...],
  "docsReferences": [...],
  "useWeb": true/false,
  
  # CODE SUGGESTIONS & EDITS
  "suggestedCodeBlocks": [
    {
      "code": "...",
      "filePath": "...",
      "action": "replace" | "insert" | "delete"
    }
  ],
  "assistantSuggestedDiffs": [...],
  
  # USER RESPONSES (ACCEPTANCE DATA!)
  "userResponsesToSuggestedCodeBlocks": [
    {
      "blockId": "...",
      "action": "accept" | "reject" | "modify",
      "timestamp": 1734567890123
    }
  ],
  
  # DIFFS & CHANGES
  "gitDiffs": [...],
  "diffHistories": [...],
  "diffsSinceLastApply": [...],
  "humanChanges": [...],  # Manual edits after AI
  
  # MODEL & PERFORMANCE
  "modelInfo": {
    "modelName": "claude-4.5-sonnet-thinking"
  },
  "tokenCount": {
    "inputTokens": 12345,
    "outputTokens": 2345
  },
  "timingInfo": {...},
  
  # SESSION CONTEXT
  "isAgentic": true,
  "unifiedMode": "agent" | "chat",
  "context": {...},
  "checkpointId": "...",
  
  # LINTING & ERRORS
  "lints": [...],
  "approximateLintErrors": [],
  "multiFileLinterErrors": [...],
  
  # TERMINAL INTERACTION
  "existedPreviousTerminalCommand": true,
  "existedSubsequentTerminalCommand": true,
  "consoleLogs": [...],
  
  # SERVER REFERENCES
  "serverBubbleId": "...",
  "usageUuid": "...",
  "requestId": "...",
  
  # METADATA
  "isRefunded": false,
  "skipRendering": false,
  "isNudge": false
}
```

#### Coverage Statistics (from 100 sample bubbles)

| Field | Coverage | Notes |
|-------|----------|-------|
| `text` | 23% | Actual message text |
| `codeBlocks` | 14% | Generated code |
| `thinking` | 32% | AI reasoning process |
| `toolResults` | 0% (sample) | Tool usage exists in data |
| `attachedCodeChunks` | varies | Context provided |
| `suggestedCodeBlocks` | varies | Code suggestions |

#### Type Distribution

```
Type 1 (User prompts):     3,970 messages (5.8%)
Type 2 (AI responses):    64,681 messages (94.2%)
Type unknown:                 11 messages
```

---

### 2. codeBlockDiff (10,527 entries) - CODE CHANGES

**Location:** `cursorDiskKV` table
**Key Pattern:** `codeBlockDiff:{composerId}:{diffId}`
**Data Type:** JSON blob

#### What Each Entry Contains

```python
{
  "newModelDiffWrtV0": [
    {
      "original": {
        "startLineNumber": 30,
        "endLineNumber": 45,
        "startColumn": 1,
        "endColumn": 80
      },
      "modified": {
        "startLineNumber": 30,
        "endLineNumber": 50,
        "startColumn": 1,
        "endColumn": 80
      },
      "originalContent": ["old line 1", "old line 2", ...],
      "modifiedContent": ["new line 1", "new line 2", ...]
    }
  ],
  "originalModelDiffWrtV0": [...]  # If there were previous versions
}
```

---

### 3. composerData (1,076 entries) - SESSION METRICS

**Location:** `cursorDiskKV` table
**Key Pattern:** `composerData:{composerId}`
**Data Type:** JSON blob

#### Effectiveness-Related Fields

```python
{
  "composerId": "...",
  "name": "Build login system",
  
  # ACCEPTANCE METRICS
  "totalLinesAdded": 2500,      # Total accepted
  "totalLinesRemoved": 100,     # Total removed later
  "addedFiles": ["file1.ts", "file2.tsx"],
  "removedFiles": [],
  
  # TOKEN USAGE
  "contextTokensUsed": 45000,
  "contextTokenLimit": 128000,
  "contextUsagePercent": 35.2,
  
  # CONVERSATION STRUCTURE
  "fullConversationHeadersOnly": [
    {"bubbleId": "msg1", "type": 1},
    {"bubbleId": "msg2", "type": 2},
    {"bubbleId": "msg3", "type": 1}
  ],
  
  # MODEL CONFIG
  "modelConfig": {
    "modelName": "claude-4.5-sonnet-thinking",
    "maxMode": false
  },
  
  # USAGE DATA
  "usageData": {...},
  
  # CAPABILITIES USED
  "capabilities": [
    {"type": 30, "data": {}},  # Various capability codes
    {"type": 34, "data": {}}
  ],
  
  # TIMESTAMPS
  "createdAt": 1734567890123,
  "lastUpdatedAt": 1734567899999
}
```

---

### 4. messageRequestContext (4,339 entries) - REQUEST CONTEXT

**Location:** `cursorDiskKV` table
**Key Pattern:** `messageRequestContext:{requestId}`
**Data Type:** JSON blob

#### What It Contains

```python
{
  # FILES IN CONTEXT
  "attachedFileCodeChunksMetadataOnly": [...],
  "currentFileLocationData": {...},
  "deletedFiles": [...],
  
  # PROJECT CONTEXT
  "projectLayouts": [...],
  "cursorRules": [...],
  "knowledgeItems": [...],
  
  # DIFFS & CHANGES
  "diffsSinceLastApply": [...],
  
  # GIT CONTEXT
  "gitStatusRaw": "...",
  
  # TERMINAL CONTEXT
  "terminalFiles": [...],
  
  # LINTING
  "multiFileLinterErrors": [...],
  
  # OTHER CONTEXT
  "attachedFoldersListDirResults": [...],
  "summarizedComposers": [...],
  "todos": [...]
}
```

---

### 5. Daily Stats (28 entries) - ACCEPTANCE METRICS

**Location:** `ItemTable`
**Key Pattern:** `aiCodeTracking.dailyStats.v1.5.{YYYY-MM-DD}`
**Data Type:** JSON

```python
{
  "date": "2025-12-22",
  "tabSuggestedLines": 0,
  "tabAcceptedLines": 0,
  "composerSuggestedLines": 5049,
  "composerAcceptedLines": 2783
}
```

**Date Range:** Nov 20, 2025 → Present
**Total:** 137,144 suggested, 66,771 accepted (48.7% rate)

---

### 6. agentKv (17,962 entries) - AGENT STATE

**Location:** `cursorDiskKV` table
**Key Patterns:**
- `agentKv:blob:{hash}` (17,471 entries)
- `agentKv:bubbleCheckpoint:{sessionId}:{checkpointId}` (466 entries)
- `agentKv:checkpoint:{id}` (25 entries)

**Purpose:** Agent execution state, may contain intermediate steps

---

### 7. Workspace Sessions (1,858 total across 227 workspaces)

**Location:** Workspace databases
**Key:** `composer.composerData` in ItemTable
**Data Type:** JSON

```python
{
  "allComposers": [
    {
      "composerId": "...",
      "createdAt": 1731602748440,
      "name": "...",
      "totalLinesAdded": 1200,
      "totalLinesRemoved": 50,
      "unifiedMode": "agent",
      # ... similar to global composerData
    }
  ]
}
```

---

## Extraction Plan

### Phase 1: Core Message Data

```python
# Extract all messages with content
messages = []
for bubble in cursorDiskKV.get_all("bubbleId:*"):
    messages.append({
        'id': bubble.bubbleId,
        'type': bubble.type,  # 1=user, 2=AI
        'text': bubble.text,
        'created_at': bubble.createdAt,
        'composer_id': bubble.composerId,
        
        # Content
        'has_code': len(bubble.codeBlocks) > 0,
        'has_thinking': bubble.thinking is not None,
        'has_tools': len(bubble.toolResults) > 0,
        
        # Model
        'model': bubble.modelInfo.get('modelName'),
        'tokens_in': bubble.tokenCount.get('inputTokens'),
        'tokens_out': bubble.tokenCount.get('outputTokens')
    })
```

### Phase 2: Link to Sessions

```python
# Build session context
for session in composerData.get_all():
    session_messages = [
        m for m in messages 
        if m.composer_id == session.composerId
    ]
    
    session.messages = session_messages
    session.message_count = len(session_messages)
    session.user_messages = len([m for m in session_messages if m.type == 1])
    session.ai_messages = len([m for m in session_messages if m.type == 2])
```

### Phase 3: Extract Code Diffs

```python
# Get all code changes
diffs = []
for diff in cursorDiskKV.get_all("codeBlockDiff:*"):
    diffs.append({
        'composer_id': extract_composer_id(diff.key),
        'changes': diff.newModelDiffWrtV0,
        'line_count': count_lines_changed(diff)
    })
```

### Phase 4: Calculate Acceptance

```python
# From dailyStats (recent)
daily_acceptance = {
    date: {
        'suggested': stats.composerSuggestedLines,
        'accepted': stats.composerAcceptedLines,
        'rate': stats.composerAcceptedLines / stats.composerSuggestedLines
    }
    for date, stats in dailyStats
}

# From sessions (all time)
session_acceptance = {
    session.id: {
        'added': session.totalLinesAdded,
        'removed': session.totalLinesRemoved,
        'net': session.totalLinesAdded - session.totalLinesRemoved
    }
    for session in sessions
}
```

---

## Effectiveness Analyses We Can Perform

### 1. Prompt Effectiveness

**Question:** What makes a good prompt?

**Data Sources:**
- User messages (type=1) → `text`
- AI responses (type=2) → `codeBlocks`, `suggestedCodeBlocks`
- Session → `totalLinesAdded`, `totalLinesRemoved`

**Analyses:**
```python
# Prompt characteristics
analyze_prompt_length(user_messages)
analyze_prompt_specificity(user_messages)  # Has file names, line numbers?
analyze_prompt_examples(user_messages)     # Includes code examples?

# Correlation with results
prompts_with_files = filter(has_file_references)
acceptance_rate = calculate_acceptance(prompts_with_files.sessions)

# By prompt type
imperative = filter(starts_with=["make", "create", "build"])
questions = filter(starts_with=["how", "why", "what"])
```

### 2. Context Impact

**Question:** Does more context help or hurt?

**Data Sources:**
- `attachedCodeChunks` (user-provided)
- `codebaseContextChunks` (auto-retrieved)
- `contextTokensUsed`
- `totalLinesAdded`

**Analyses:**
```python
# Context vs acceptance
by_context_size = group_by(sessions, 'contextTokensUsed', bins=[0, 10000, 50000, 100000])
for group in by_context_size:
    group.avg_acceptance = mean(s.totalLinesAdded for s in group)

# Attached files impact
with_attachments = filter(has_attached_files)
without_attachments = filter(not has_attached_files)
compare_acceptance(with_attachments, without_attachments)
```

### 3. Tool Usage Effectiveness

**Question:** Which tools improve results?

**Data Sources:**
- `toolResults` → tool name, query, results
- Session acceptance rate

**Analyses:**
```python
# Tool correlation
messages_by_tool = group_by(messages, 'toolResults.toolName')
for tool, messages in messages_by_tool:
    sessions = get_sessions(messages)
    tool_acceptance[tool] = mean(s.totalLinesAdded for s in sessions)

# Tool combinations
multi_tool = filter(len(toolResults) > 1)
single_tool = filter(len(toolResults) == 1)
no_tool = filter(len(toolResults) == 0)
```

### 4. Thinking Analysis

**Question:** Does AI thinking correlate with quality?

**Data Sources:**
- `thinking` text (32% of messages)
- `thinkingDurationMs`
- Acceptance metrics

**Analyses:**
```python
# Thinking presence
with_thinking = filter(has_thinking=True)
without_thinking = filter(has_thinking=False)

# Duration analysis
by_thinking_time = group_by(with_thinking, 'thinkingDurationMs', bins)
plot(thinking_time, acceptance_rate)

# Thinking content analysis
thinking_texts = [m.thinking for m in with_thinking]
analyze_reasoning_patterns(thinking_texts)
```

### 5. Iteration Efficiency

**Question:** How many rounds to get it right?

**Data Sources:**
- `fullConversationHeadersOnly` (message sequence)
- Message text patterns (feedback, corrections)
- Acceptance actions

**Analyses:**
```python
# Identify tasks and iterations
for session in sessions:
    tasks = identify_tasks(session.messages)  # Group related messages
    for task in tasks:
        iterations = count_iterations(task)
        success = was_accepted(task)
        task_metrics[task.type] = {
            'avg_iterations': mean(iterations),
            'success_rate': success_rate
        }
```

### 6. Code Quality Indicators

**Question:** How much editing after acceptance?

**Data Sources:**
- `codeBlockDiff` → original vs modified
- `humanChanges` → manual edits
- `totalLinesAdded` vs `totalLinesRemoved`

**Analyses:**
```python
# Edit distance analysis
for diff in code_diffs:
    if has_later_human_changes(diff):
        edit_distance = calculate_levenshtein(
            diff.originalContent,
            get_final_version(diff)
        )
        quality_score = 1 - (edit_distance / len(diff.originalContent))
```

### 7. Model Performance

**Question:** Which models work best for what?

**Data Sources:**
- `modelInfo.modelName` (11.5% coverage)
- Session acceptance
- Task type (from message analysis)

**Analyses:**
```python
# By model (limited data)
by_model = group_by(messages_with_model, 'modelInfo.modelName')
for model, messages in by_model:
    acceptance = calculate_acceptance(get_sessions(messages))
    
# Caveat: Only 7,879 of 68,657 messages have model info
```

### 8. Conversation Patterns

**Question:** What conversation styles work best?

**Data Sources:**
- Message sequence in sessions
- Time between messages
- Message types and lengths

**Analyses:**
```python
# Conversation characteristics
rapid_sessions = filter(avg_time_between_messages < 60)  # < 1 min
thoughtful_sessions = filter(avg_time_between_messages > 300)  # > 5 min

short_conversations = filter(message_count < 5)
long_conversations = filter(message_count > 10)

# Effectiveness comparison
compare_acceptance(rapid_sessions, thoughtful_sessions)
compare_acceptance(short_conversations, long_conversations)
```

---

## Data Extraction Priority

### Priority 1: Foundation
1. Extract all bubbleId entries → `Message` objects
2. Extract all composerData entries → `Session` objects
3. Link messages to sessions
4. Extract dailyStats → `DailyStats` objects

### Priority 2: Content Analysis
5. Parse message text → categorize prompts
6. Extract code blocks → link to files
7. Extract thinking → analyze reasoning
8. Parse tool usage → track effectiveness

### Priority 3: Acceptance Tracking
9. Extract userResponsesToSuggestedCodeBlocks
10. Link to codeBlockDiff entries
11. Calculate acceptance rates
12. Track human edits

### Priority 4: Advanced Analysis
13. Context analysis (attachments, tokens)
14. Iteration tracking
15. Model correlation (limited)
16. Conversation patterns

---

## File References

### Source Locations

| Data | Database | Table | Key Pattern |
|------|----------|-------|-------------|
| Messages | state.vscdb (global) | cursorDiskKV | `bubbleId:*` |
| Sessions | state.vscdb (global) | cursorDiskKV | `composerData:*` |
| Code Diffs | state.vscdb (global) | cursorDiskKV | `codeBlockDiff:*` |
| Daily Stats | state.vscdb (global) | ItemTable | `aiCodeTracking.dailyStats.*` |
| Request Context | state.vscdb (global) | cursorDiskKV | `messageRequestContext:*` |
| Workspace Sessions | {workspace}/state.vscdb | ItemTable | `composer.composerData` |

### Extraction Scripts

| Script | Purpose |
|--------|---------|
| `deep_model_token_search.py` | Model and token analysis |
| `check_all_sources_deep.py` | Content verification |
| `final_comprehensive_check.py` | Complete inventory |

---

## Implementation Notes

### Data Quality

- **Text coverage:** ~23% of messages have text field populated
- **Code coverage:** ~14% have codeBlocks
- **Thinking coverage:** ~32% have thinking
- **Model info:** Only 11.5% have modelInfo

### Performance Considerations

- 68,657 messages to process
- Each message can be several KB (with code)
- Full extraction may take several minutes
- Consider caching extracted data

### Data Relationships

```
Session (composerData)
  ↓ has many
Messages (bubbleId)
  ↓ may have
CodeDiffs (codeBlockDiff)
  ↓ may have
Context (messageRequestContext)
```

---

## Next Steps for Implementation

1. **Create Message extractor** → Parse bubbleId entries
2. **Create Session extractor** → Parse composerData entries
3. **Build linking logic** → Connect messages to sessions
4. **Extract acceptance data** → From dailyStats and sessions
5. **Build analysis functions** → For each effectiveness metric
6. **Create dashboard** → Visualize results

---

*This document provides the complete blueprint for extracting and analyzing ALL message/content data in Cursor.*

