# File History

**Created: December 21, 2025**

Edit history for individual files.

## Location

```
Windows: %APPDATA%\Cursor\User\History\{file-hash}\
```

## Overview

| Property | Value |
|----------|-------|
| Total Entries | 2,605 file histories |
| Total Size | ~152 MB |
| Format | JSON + file snapshots |

## Structure

Each file has a folder named with a hash ID containing:

```
{file-hash}/
├── entries.json       # Metadata and version list
├── {version-id}.json  # Content snapshot (for JSON files)
├── {version-id}.ts    # Content snapshot (preserves extension)
├── {version-id}.py    # Content snapshot (preserves extension)
└── ...
```

## entries.json Format

```json
{
  "version": 1,
  "resource": "file:///c%3A/path/to/file.ts",
  "entries": [
    {
      "id": "abc123.ts",
      "source": "Undo Create Diff",
      "timestamp": 1745297572507
    },
    {
      "id": "def456.ts",
      "source": "Auto Save",
      "timestamp": 1745298123456
    }
  ]
}
```

## Entry Sources

| Source | Description |
|--------|-------------|
| `Auto Save` | Automatic save |
| `Undo Create Diff` | Undo operation created a diff |
| `Manual Save` | User-initiated save |
| `AI Edit` | AI-generated edit (needs verification) |

## Sample Entries

Files with most history versions:

| File | Versions |
|------|----------|
| `ScreenshotService.ts` | 50 versions |
| `griffonix-site.css` | 23 versions |
| `StepListItem.tsx` | 2 versions |
| `alfalfa-logo.svg` | 1 version |

## Accessing File History

### Python Example

```python
import json
from pathlib import Path
from datetime import datetime
from urllib.parse import unquote

history_path = Path.home() / 'AppData/Roaming/Cursor/User/History'

all_history = []

for folder in history_path.iterdir():
    entries_file = folder / 'entries.json'
    if not entries_file.exists():
        continue
    
    with open(entries_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    # Decode file path
    resource = data.get('resource', '')
    file_path = unquote(resource.replace('file:///', ''))
    
    entries = data.get('entries', [])
    
    for entry in entries:
        timestamp = entry.get('timestamp', 0)
        dt = datetime.fromtimestamp(timestamp / 1000)
        
        all_history.append({
            'file': file_path,
            'version_id': entry.get('id'),
            'source': entry.get('source'),
            'timestamp': dt,
            'folder': folder.name
        })

# Sort by timestamp
all_history.sort(key=lambda x: x['timestamp'], reverse=True)

# Show recent edits
for h in all_history[:20]:
    print(f"{h['timestamp']}: {h['source']} - {h['file']}")
```

### Reading File Snapshots

```python
# Get actual file content at a specific version
def get_file_version(folder_name, version_id):
    history_path = Path.home() / 'AppData/Roaming/Cursor/User/History'
    version_file = history_path / folder_name / version_id
    
    if version_file.exists():
        with open(version_file, 'r', encoding='utf-8', errors='ignore') as f:
            return f.read()
    return None

# Example
content = get_file_version('-3c360721', '3cjm.json')
print(content)
```

## Analytics Potential

### Edit Metrics
- Total edits over time
- Most frequently edited files
- Edit patterns (time of day, day of week)
- Average edits per file

### File Type Analysis
- Most edited file types (.ts, .py, .json, etc.)
- Edit frequency by project

### Timeline Analysis
- Daily/weekly edit counts
- Active development periods
- Edit sources breakdown (Auto Save vs Manual vs AI)

## Notes

- File content may be large (MB+)
- History is cumulative (doesn't auto-delete)
- Timestamps are Unix milliseconds
- Resource paths are URL-encoded

