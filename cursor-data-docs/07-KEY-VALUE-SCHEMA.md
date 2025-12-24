# Key-Value Schema Reference

**Created: December 21, 2025**

Documented keys from Cursor's SQLite databases.

## Global Database Keys (ItemTable)

### AI/Cursor Category

| Key | Size | Type | Description |
|-----|------|------|-------------|
| `aiCodeTrackingLines` | 2.8 MB | JSON | AI-generated code line tracking |
| `aiCodeTrackingScoredCommits` | 19 KB | JSON | AI contribution per commit |
| `cursorai/serverConfig` | 24 KB | JSON | AI server configuration |
| `cursorai/featureStatusCache` | 1 KB | JSON | Feature flag status |
| `cursorai/featureConfigCache` | 628 B | JSON | Feature configuration |
| `cursor/copyPasteMentions` | 686 B | JSON | Copy/paste AI mentions |

### Terminal Category

| Key | Size | Type | Schema |
|-----|------|------|--------|
| `terminal.history.entries.commands` | 12.5 KB | JSON | Array of command entries |
| `terminal.history.entries.dirs` | 4.2 KB | JSON | Array of directory entries |
| `terminal.history.timestamp.commands` | 13 B | Number | Last command timestamp |
| `terminal.history.timestamp.dirs` | 13 B | Number | Last dir timestamp |
| `terminal.hidden` | 36 B | JSON | Hidden state |

#### terminal.history.entries.commands Schema

```json
[
  {
    "command": "git status",
    "timestamp": 1734567890123,
    "cwd": "/path/to/project"
  },
  ...
]
```

### History Category

| Key | Size | Type | Schema |
|-----|------|------|--------|
| `history.recentlyOpenedPathsList` | 8.6 KB | JSON | Recent files/folders |

#### history.recentlyOpenedPathsList Schema

```json
{
  "entries": [
    {
      "folderUri": "file:///c%3A/path/to/project",
      "label": "Project Name",
      "remoteAuthority": null
    },
    {
      "fileUri": "file:///c%3A/path/to/file.ts"
    }
  ]
}
```

### Workbench Category

| Key | Size | Description |
|-----|------|-------------|
| `workbench.experiments.statsigBootstrap` | 128 KB | Statsig experiment config |
| `workbench.auxiliarybar.placeholderPanels` | 117 KB | Auxiliary bar panels |
| `workbench.auxiliarybar.pinnedPanels` | 103 KB | Pinned panels |
| `workbench.panel.placeholderPanels` | 940 B | Panel placeholders |
| `workbench.panel.pinnedPanels` | 487 B | Pinned panel list |
| `workbench.view.extensions.state.hidden` | 1.6 KB | Extension view state |
| `workbench.view.debug.state.hidden` | 480 B | Debug view state |

### Git Category

| Key | Size | Description |
|-----|------|-------------|
| `vscode.github` | 2 KB | GitHub extension state |
| `vscode.github-authentication` | 1.5 KB | GitHub auth state |
| `vscode.git` | 270 B | Git extension state |
| `secret://...github.auth` | 792 B | Encrypted auth token |

### Theme Category

| Key | Size | Description |
|-----|------|-------------|
| `iconThemeData` | 97 KB | Icon theme data |
| `colorThemeData` | 15 KB | Color theme data |

### Extension Category

| Key | Size | Description |
|-----|------|-------------|
| `ms-python.python` | 26 KB | Python extension state |
| `ms-vscode-remote.remote-containers` | 1.8 KB | Remote containers |
| `ms-azuretools.vscode-containers` | 1.8 KB | Azure containers |
| `ms-vscode-remote.remote-ssh` | 1.7 KB | Remote SSH state |
| `vscode.typescript-language-features` | 1.6 KB | TypeScript features |
| `golang.go` | 793 B | Go extension state |

---

## Workspace Database Keys (ItemTable)

### Core Keys

| Key | Type | Description |
|-----|------|-------------|
| `__$__isNewStorageMarker` | Boolean | Storage initialization marker |
| `__$__targetStorageMarker` | String | Target storage reference |

### AI/Chat Keys

| Key | Type | Schema |
|-----|------|--------|
| `composer.composerData` | JSON | Chat/Agent conversations |
| `aiService.prompts` | JSON | AI prompts used |
| `anysphere.cursor-retrieval` | JSON | Cursor retrieval config |

#### composer.composerData Schema

```json
{
  "allComposers": [
    {
      "id": "uuid",
      "type": "chat|agent",
      "messages": [
        {
          "role": "user|assistant",
          "content": "message text",
          "timestamp": 1734567890123
        }
      ]
    }
  ],
  "selectedComposerId": "uuid",
  "selectedChatId": "uuid",
  "hasMigratedChatData": true,
  "hasMigratedUseAutoContext": true,
  "hasMigratedComposerData": true
}
```

### Notepad Keys

| Key | Type | Schema |
|-----|------|--------|
| `notepadData` | JSON | Notepad content |
| `notepad.reactiveStorageId` | String | Storage reference |

#### notepadData Schema

```json
{
  "notepads": {
    "notepad-uuid": {
      "name": "Note Title",
      "text": "Actual note content...",
      "createdAt": 1734567890123,
      "updatedAt": 1734567890456
    }
  }
}
```

### History Keys

| Key | Type | Description |
|-----|------|-------------|
| `history.entries` | JSON | Local file history |

### Editor State Keys

| Key | Type | Description |
|-----|------|-------------|
| `workbench.editor.hidden` | Boolean | Editor hidden state |
| `workbench.editor.centered` | Boolean | Editor centered mode |
| `workbench.explorer.treeViewState` | JSON | Explorer tree state |
| `workbench.explorer.views.state` | JSON | Explorer views state |

### Panel State Keys

| Key | Type | Description |
|-----|------|-------------|
| `workbench.panel.hidden` | Boolean | Panel hidden |
| `workbench.panel.position` | String | Panel position |
| `workbench.panel.output` | JSON | Output panel state |
| `workbench.panel.repl` | JSON | REPL panel state |
| `workbench.panel.wasLastMaximized` | Boolean | Maximize state |
| `workbench.activityBar.hidden` | Boolean | Activity bar hidden |
| `workbench.auxiliaryBar.hidden` | Boolean | Aux bar hidden |

### Terminal Keys

| Key | Type | Description |
|-----|------|-------------|
| `terminal` | JSON | Terminal state |

### Debug Keys

| Key | Type | Description |
|-----|------|-------------|
| `debug.selectedroot` | String | Debug root |
| `debug.uxstate` | JSON | Debug UI state |

### Other Keys

| Key | Type | Description |
|-----|------|-------------|
| `output.activechannel` | String | Active output channel |
| `interactive.sessions` | JSON | Interactive sessions |
| `comments.continueOnComments` | Boolean | Comment setting |
| `lifecyle.lastShutdownReason` | String | Last shutdown reason |
| `workbench.scm.views.state` | JSON | SCM views state |

---

## Value Decoding

### Reading Values

```python
import sqlite3
import json

def get_key_value(db_path, key):
    conn = sqlite3.connect(str(db_path))
    cursor = conn.cursor()
    cursor.execute('SELECT value FROM ItemTable WHERE key = ?', (key,))
    result = cursor.fetchone()
    conn.close()
    
    if result:
        value = result[0]
        # Try to decode as UTF-8 JSON
        if isinstance(value, bytes):
            try:
                return json.loads(value.decode('utf-8'))
            except:
                return value.decode('utf-8', errors='ignore')
        return value
    return None
```

### Common Patterns

1. **JSON blobs**: Most values are JSON-encoded
2. **Timestamps**: Unix milliseconds (divide by 1000 for seconds)
3. **UUIDs**: Used for composer/chat IDs
4. **File paths**: URL-encoded (`file:///c%3A/...`)

## Contributing

Found a new key or decoded a schema? Please document it here!

