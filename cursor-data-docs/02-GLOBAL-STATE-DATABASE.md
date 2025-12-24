# Global State Database

**Created: December 21, 2025**

The main database storing global Cursor state across all workspaces.

## Location

```
Windows: %APPDATA%\Cursor\User\globalStorage\state.vscdb
Linux:   ~/.config/Cursor/User/globalStorage/state.vscdb
macOS:   ~/Library/Application Support/Cursor/User/globalStorage/state.vscdb
```

## Database Info

| Property | Value |
|----------|-------|
| Format | SQLite 3 |
| Size | ~2.4 GB |
| Tables | `ItemTable`, `cursorDiskKV` |
| Total Keys | 1,285 (in ItemTable) |

## Tables

### ItemTable

Main key-value store with 1,285 keys. This is a simple two-column table:
- **key** (TEXT) - The identifier for the data (e.g., "notepadData", "terminal.history")
- **value** (BLOB) - The actual data, usually JSON-encoded bytes

**Schema:**
```sql
CREATE TABLE ItemTable (
    key TEXT UNIQUE ON CONFLICT REPLACE,  -- Unique key identifier
    value BLOB                             -- Binary data (usually JSON)
);
```

Think of it like a dictionary/hashmap stored in SQLite - you look up data by its key name.

### cursorDiskKV

Additional Cursor-specific key-value store (needs exploration).

## Key Categories

### AI/Cursor Keys (75 keys, 2.9 MB)

| Key | Size | Description |
|-----|------|-------------|
| `aiCodeTrackingLines` | 2.8 MB | ⭐ AI-generated code tracking |
| `cursorai/serverConfig` | 24 KB | AI server configuration |
| `aiCodeTrackingScoredCommits` | 19 KB | AI contribution scoring |
| `cursorai/featureStatusCache` | 1 KB | Feature flags |
| `cursorai/featureConfigCache` | 628 B | Feature configuration |

### Chat/Composer Keys (1,098 keys, 142 KB)

| Key Pattern | Count | Description |
|-------------|-------|-------------|
| `workbench.panel.composerChatViewPane.*` | ~1,000 | Chat panel states |
| `workbench.backgroundComposer.*` | 5 | Background composer data |
| `composer.*` | 5 | Composer settings |

### Terminal Keys (7 keys, 17 KB)

| Key | Size | Description |
|-----|------|-------------|
| `terminal.history.entries.commands` | 12.5 KB | ⭐ Command history |
| `terminal.history.entries.dirs` | 4.2 KB | Directory history |
| `terminal.hidden` | 36 B | Hidden state |
| `terminal.history.timestamp.*` | 13 B | Timestamps |

### Workbench Keys (37 keys, 353 KB)

| Key | Size | Description |
|-----|------|-------------|
| `workbench.experiments.statsigBootstrap` | 128 KB | Statsig config |
| `workbench.auxiliarybar.placeholderPanels` | 117 KB | Auxiliary bar |
| `workbench.auxiliarybar.pinnedPanels` | 103 KB | Pinned panels |
| `workbench.panel.placeholderPanels` | 940 B | Panel placeholders |

### History Keys (1 key, 8.6 KB)

| Key | Size | Description |
|-----|------|-------------|
| `history.recentlyOpenedPathsList` | 8.6 KB | ⭐ Recent files/projects |

### Git Keys (7 keys, 4.8 KB)

| Key | Size | Description |
|-----|------|-------------|
| `vscode.github` | 2 KB | GitHub integration |
| `vscode.github-authentication` | 1.5 KB | Auth state |
| `secret://...github.auth` | 792 B | Auth secrets |
| `vscode.git` | 270 B | Git extension state |

## Top 50 Keys by Size

```
 1. [ 2,815,698 bytes] aiCodeTrackingLines
 2. [   128,009 bytes] workbench.experiments.statsigBootstrap
 3. [   116,606 bytes] workbench.auxiliarybar.placeholderPanels
 4. [   103,158 bytes] workbench.auxiliarybar.pinnedPanels
 5. [    96,841 bytes] iconThemeData
 6. [    90,897 bytes] __$__targetStorageMarker
 7. [    80,535 bytes] src.vs.platform.reactivestorage.browser...
 8. [    25,941 bytes] ms-python.python
 9. [    23,942 bytes] cursorai/serverConfig
10. [    18,831 bytes] aiCodeTrackingScoredCommits
11. [    15,291 bytes] colorThemeData
12. [    12,522 bytes] terminal.history.entries.commands
13. [     8,589 bytes] history.recentlyOpenedPathsList
14. [     4,239 bytes] terminal.history.entries.dirs
15. [     3,541 bytes] memento/cachedResourceLabelFormatters2
16. [     1,979 bytes] vscode.github
17. [     1,849 bytes] ms-vscode-remote.remote-containers
18. [     1,816 bytes] ms-azuretools.vscode-containers
19. [     1,718 bytes] remote.tunnels.toRestore.ssh-remote+...
20. [     1,651 bytes] ms-vscode-remote.remote-ssh
21. [     1,629 bytes] workbench.view.extensions.state.hidden
22. [     1,554 bytes] vscode.typescript-language-features
23. [     1,554 bytes] vscode.github-authentication
24. [     1,358 bytes] vscode.microsoft-authentication
25. [     1,298 bytes] memento/customEditors
26. [     1,071 bytes] cursorai/featureStatusCache
27. [       940 bytes] workbench.panel.placeholderPanels
28. [       793 bytes] golang.go
29. [       792 bytes] secret://{"extensionId":"vscode.github-auth...
30. [       729 bytes] workbench.panel.composerChatViewPane.37232...
31. [       729 bytes] workbench.panel.composerChatViewPane.019a5...
32. [       724 bytes] notifications.perSourceDoNotDisturbMode
33. [       686 bytes] cursor/copyPasteMentions
34. [       631 bytes] memento/notebookEditors
35. [       628 bytes] cursorai/featureConfigCache
36-39. [   547 bytes] workbench.panel.composerChatViewPane.* (4 more)
40. [       492 bytes] extensionsAssistant/recommendations
41. [       491 bytes] editorFontInfo
42-43. [   490 bytes] remote.tunnels.toRestore.* (2 more)
44. [       487 bytes] workbench.panel.pinnedPanels
45. [       480 bytes] workbench.view.debug.state.hidden
46. [       468 bytes] editorOverrideService.cache
47-50. [   456 bytes] workbench.panel.composerChatViewPane.* (4 more)
```

**Note:** Many `composerChatViewPane.*` keys are chat panel state - each represents a different chat session's UI state.

## Accessing the Database

### Python Example

```python
import sqlite3
from pathlib import Path
import json

db_path = Path.home() / 'AppData/Roaming/Cursor/User/globalStorage/state.vscdb'
conn = sqlite3.connect(str(db_path))
cursor = conn.cursor()

# Get all keys
cursor.execute('SELECT key FROM ItemTable')
keys = [row[0] for row in cursor.fetchall()]

# Get specific value
cursor.execute('SELECT value FROM ItemTable WHERE key = ?', ('terminal.history.entries.commands',))
result = cursor.fetchone()
if result:
    data = json.loads(result[0].decode('utf-8'))
    print(data)

conn.close()
```

## High-Value Keys for Analytics

### 1. aiCodeTrackingLines (2.8 MB)
AI-generated code tracking. Likely contains:
- Lines of code generated by AI
- File paths modified
- Timestamps
- Model used

### 2. terminal.history.entries.commands (12.5 KB)
Terminal command history. JSON array of:
- Commands executed
- Timestamps
- Working directories

### 3. history.recentlyOpenedPathsList (8.6 KB)
Recently opened files and projects. JSON with:
- File paths
- Project folders
- Access timestamps

### 4. aiCodeTrackingScoredCommits (19 KB)
AI contribution scoring. Likely contains:
- Commit hashes
- AI contribution scores
- File changes attributed to AI

## Notes

- Database may be locked while Cursor is running
- Consider making a copy for analysis
- Values are often JSON-encoded blobs
- Some values may be binary (need decoding)

