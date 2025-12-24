# Workspace Databases

**Created: December 21, 2025**

Per-project databases storing workspace-specific state.

## Location

```
Windows: %APPDATA%\Cursor\User\workspaceStorage\{workspace-id}\state.vscdb
```

## Overview

| Property | Value |
|----------|-------|
| Total Workspaces | 245 |
| Total Size | ~290 MB |
| Size Range | 40 KB - 1.4 MB per workspace |
| Database Format | SQLite 3 |

## Workspace ID Mapping

Each workspace folder has a `workspace.json` file mapping the ID to project path:

```json
{
  "folder": "file:///c%3A/Users/jackw/OneDrive/Python%20Projects"
}
```

## Common Keys Across Workspaces

These keys appear in every workspace database:

| Key | Description |
|-----|-------------|
| `__$__isNewStorageMarker` | Storage initialization marker |
| `__$__targetStorageMarker` | Target storage marker |
| `aiService.prompts` | ⭐ AI prompts used in workspace |
| `anysphere.cursor-retrieval` | Cursor AI retrieval config |
| `comments.continueOnComments` | Continue comments setting |
| `composer.composerData` | ⭐ Chat/Agent conversations |
| `debug.selectedroot` | Debug configuration |
| `debug.uxstate` | Debug UI state |
| `history.entries` | ⭐ Local file history |
| `interactive.sessions` | Interactive sessions |
| `lifecyle.lastShutdownReason` | Shutdown info |
| `notepad.reactiveStorageId` | Notepad storage reference |
| `notepadData` | ⭐ Notepad content |
| `output.activechannel` | Output channel |
| `terminal` | Terminal state |
| `workbench.activityBar.hidden` | Activity bar state |
| `workbench.auxiliaryBar.hidden` | Auxiliary bar state |
| `workbench.editor.hidden` | Editor state |
| `workbench.explorer.treeViewState` | Explorer tree state |

## Key Details

### composer.composerData

Chat and agent conversation data. Structure:

```json
{
  "allComposers": [...],
  "selectedComposerId": "uuid",
  "selectedChatId": "uuid",
  "hasMigratedChatData": true,
  "hasMigratedUseAutoContext": true,
  "hasMigratedComposerData": true
}
```

### notepadData

Notepad content with structure:

```json
{
  "notepads": {
    "notepad-id": {
      "name": "My Notes",
      "text": "Actual notepad content..."
    }
  }
}
```

### aiService.prompts

AI prompts used in the workspace.

### history.entries

Local file edit history for the workspace.

## Anysphere Folder

Each workspace may have an `anysphere.cursor-retrieval/` folder containing:

| File | Description |
|------|-------------|
| `embeddable_files.txt` | List of files for RAG/embedding |
| `high_level_folder_description.txt` | AI-generated project description |

Example `high_level_folder_description.txt`:
```
This folder contains a Python web scraping project for extracting
product data from e-commerce websites...
```

## Sample Workspaces (Sorted by Size)

| Workspace ID | Size | Project |
|--------------|------|---------|
| 0800ab1dfb4c9c2458c53f08ad33bbe7 | 1.4 MB | Large project |
| 1005b2db2de521354f33d0042aca728a | 836 KB | Medium project |
| 010299b466d3ee6862f358dbd2fd3b3e | 872 KB | Medium project |
| ... | ... | ... |

## Accessing Workspace Data

### Python Example

```python
import sqlite3
import json
from pathlib import Path

workspace_path = Path.home() / 'AppData/Roaming/Cursor/User/workspaceStorage'

for ws in workspace_path.iterdir():
    db_file = ws / 'state.vscdb'
    ws_json = ws / 'workspace.json'
    
    if not db_file.exists():
        continue
    
    # Get project path
    project_path = None
    if ws_json.exists():
        with open(ws_json) as f:
            data = json.load(f)
            project_path = data.get('folder', 'Unknown')
    
    # Get chat data
    conn = sqlite3.connect(str(db_file))
    cursor = conn.cursor()
    cursor.execute('SELECT value FROM ItemTable WHERE key = ?', ('composer.composerData',))
    result = cursor.fetchone()
    
    if result:
        chat_data = json.loads(result[0].decode('utf-8'))
        print(f"Project: {project_path}")
        print(f"Composers: {len(chat_data.get('allComposers', []))}")
    
    conn.close()
```

## Analytics Potential

### Per-Workspace Metrics
- Number of chat sessions
- Total prompts sent
- Notepad usage
- File edit history
- AI-generated project descriptions

### Cross-Workspace Metrics
- Most active projects
- Total chat sessions across all projects
- Common patterns in AI usage

