# cursorDiskKV Table - THE GOLDMINE

**Created: December 21, 2025**

This is the most important data source for Cursor analytics. Contains **119,584 rows** of chat, message, and code change data.

## Location

Inside the global state database:
```
%APPDATA%\Cursor\User\globalStorage\state.vscdb
Table: cursorDiskKV
```

## Row Count Breakdown

| Key Prefix | Count | Description |
|------------|-------|-------------|
| `bubbleId:` | **68,574** | Individual messages (user + AI responses) |
| `agentKv:` | 17,962 | Agent mode state/context |
| `checkpointId:` | 14,217 | Session checkpoints |
| `codeBlockDiff:` | 10,525 | Code diff information |
| `messageRequestContext:` | 4,338 | Request context data |
| `codeBlockPartialInlineDiffFates:` | 2,591 | Partial diff data |
| `composerData:` | 1,074 | Chat session metadata |
| `inlineDiffs:` | 282 | Inline code changes |

## bubbleId Schema (Individual Messages)

Each `bubbleId:{composerId}:{messageId}` entry contains:

```json
{
  "_v": 10,
  "type": 1,                          // 1=User, 2=AI
  "text": "user message or AI response...",
  "createdAt": 1734567890123,         // Timestamp!
  "modelInfo": {...},                 // Model used!
  "tokenCount": {...},                // Token counts!
  "isAgentic": true,                  // Agent mode?
  "thinking": {...},                  // AI thinking
  "thinkingDurationMs": 1234,         // Thinking time
  "codeBlocks": [...],                // Code suggestions
  "toolResults": [...],               // Tool usage
  "attachedCodeChunks": [...],        // Context files
  "suggestedCodeBlocks": [...],       // Suggested edits
  "webReferences": [...],             // Web search
  "docsReferences": [...]             // Doc references
}
```

### Message Types
- `type: 1` = User message (prompt)
- `type: 2` = AI response

## composerData Schema (Chat Sessions)

Each `composerData:{uuid}` entry contains:

```json
{
  "_v": 10,
  "composerId": "uuid",
  "name": "Session Name",
  "text": "current input",
  "createdAt": 1734567890123,
  "lastUpdatedAt": 1734567899999,
  
  // Token Usage
  "contextTokensUsed": 12345,
  "contextTokenLimit": 128000,
  "contextUsagePercent": 9.6,
  
  // Code Metrics
  "totalLinesAdded": 500,
  "totalLinesRemoved": 100,
  "addedFiles": ["file1.ts", "file2.ts"],
  "removedFiles": [],
  
  // Mode
  "isAgentic": true,
  "capabilities": ["codebase", "web", "terminal"],
  
  // Model Config
  "modelConfig": {...},
  
  // Usage Data
  "usageData": {...},
  
  // State
  "status": "idle",
  "isArchived": false,
  "hasUnreadMessages": false
}
```

## Accessing the Data

### Python Example

```python
import sqlite3
from pathlib import Path
import json

db_path = Path.home() / 'AppData/Roaming/Cursor/User/globalStorage/state.vscdb'
conn = sqlite3.connect(str(db_path))
cursor = conn.cursor()

# Get all messages
cursor.execute("SELECT key, value FROM cursorDiskKV WHERE key LIKE 'bubbleId:%'")
messages = []
for key, value in cursor.fetchall():
    if value:
        data = json.loads(value)
        messages.append({
            'id': key,
            'type': 'user' if data.get('type') == 1 else 'ai',
            'text': data.get('text', '')[:100],
            'created': data.get('createdAt'),
            'is_agentic': data.get('isAgentic', False)
        })

print(f"Total messages: {len(messages)}")

# Count by type
user_msgs = len([m for m in messages if m['type'] == 'user'])
ai_msgs = len([m for m in messages if m['type'] == 'ai'])
print(f"User messages: {user_msgs}")
print(f"AI responses: {ai_msgs}")

conn.close()
```

### Get Model Usage

```python
# Extract model info from messages
cursor.execute("SELECT value FROM cursorDiskKV WHERE key LIKE 'bubbleId:%' AND value LIKE '%modelInfo%'")
models_used = {}
for (value,) in cursor.fetchall():
    if value:
        data = json.loads(value)
        model_info = data.get('modelInfo', {})
        model_name = model_info.get('modelName', model_info.get('model', 'unknown'))
        models_used[model_name] = models_used.get(model_name, 0) + 1

print("Models used:")
for model, count in sorted(models_used.items(), key=lambda x: x[1], reverse=True):
    print(f"  {model}: {count}")
```

### Get Token Usage

```python
# Sum up token counts from composer sessions
cursor.execute("SELECT value FROM cursorDiskKV WHERE key LIKE 'composerData:%'")
total_tokens = 0
for (value,) in cursor.fetchall():
    if value:
        data = json.loads(value)
        tokens = data.get('contextTokensUsed', 0)
        if isinstance(tokens, int):
            total_tokens += tokens

print(f"Total context tokens used: {total_tokens:,}")
```

## Analytics You Can Build

### 1. Message Analytics
- Total messages sent/received
- Messages per day/week/month
- Average conversation length
- User vs AI message ratio

### 2. Model Usage Analytics
- Which models used most
- Model usage over time
- Token consumption by model

### 3. Code Metrics
- Total lines added/removed
- Files created/deleted
- Code changes over time

### 4. Usage Patterns
- Active hours (from timestamps)
- Agent vs Chat mode ratio
- Session duration

### 5. Feature Usage
- Web search usage
- Doc references
- Tool invocations

## Notes

- Messages are stored per-session, not per-workspace
- Timestamps are Unix milliseconds
- Some fields may be null/empty
- Database may be locked while Cursor is running
- Consider copying database for analysis

