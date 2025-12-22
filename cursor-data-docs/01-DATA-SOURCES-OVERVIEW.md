# Cursor Data Sources Overview

**Created: December 21, 2025**

Complete map of all data stored by Cursor IDE.

## Top-Level Directory Structure

```
%APPDATA%\Cursor\
├── User/                          # 7.7 GB - PRIMARY USER DATA
│   ├── globalStorage/             # 7.3 GB - Global state
│   │   └── state.vscdb            # 2.4 GB - Main database (CRITICAL)
│   ├── workspaceStorage/          # 290 MB - Per-project data
│   │   └── {workspace-id}/
│   │       └── state.vscdb        # Per-workspace database
│   └── History/                   # 152 MB - File edit history
│       └── {file-hash}/
│           └── entries.json
│
├── WebStorage/                    # 1.3 GB - Browser-style storage
├── CachedData/                    # 1.1 GB - Chrome cache
├── Partitions/                    # 131 MB - Browser partitions
├── logs/                          # 16.6 MB - Session logs
├── Session Storage/               # 25 KB - LevelDB
├── Local Storage/                 # 6.8 KB - LevelDB
└── ... (other folders)
```

## Data Sources by Type

### SQLite Databases (246 total)

| Database | Location | Size | Description |
|----------|----------|------|-------------|
| **Global State** | `User/globalStorage/state.vscdb` | 2.4 GB | Main data store |
| **Workspace DBs** | `User/workspaceStorage/{id}/state.vscdb` | 40KB-1.4MB each | Per-project data |

**Tables in state.vscdb:**
- `ItemTable` - Key-value storage (1,285 keys in global)
- `cursorDiskKV` - Additional Cursor-specific storage

### LevelDB Databases (21 total)

| Database | Location | Description |
|----------|----------|-------------|
| Session Storage | `Session Storage/` | Current session data |
| Local Storage | `Local Storage/leveldb/` | Persistent local storage |
| Partition DBs | `Partitions/cursor-browser-{id}/` | Per-browser-view storage |

### JSON Files (3,556 total)

| Type | Location | Count | Description |
|------|----------|-------|-------------|
| File History | `User/History/{hash}/entries.json` | 2,605 | Edit versions |
| Config | `User/globalStorage/storage.json` | 1 | Profile associations |
| Settings | `User/settings.json` | 1 | User preferences |
| Keybindings | `User/keybindings.json` | 1 | Custom keybindings |

### Log Files (1,016 total)

Located in `logs/{session-timestamp}/`:

| Log File | Description |
|----------|-------------|
| `main.log` | Main application logs |
| `terminal.log` | Terminal activity |
| `telemetry.log` | Usage telemetry |
| `ptyhost.log` | PTY host logs |
| `window{N}/exthost/` | Extension host logs |
| `window{N}/renderer.log` | Renderer process |

## Folder Size Summary

| Folder | Size | Files | Priority for Analytics |
|--------|------|-------|----------------------|
| User | 7.7 GB | 18,948 | ⭐⭐⭐ CRITICAL |
| WebStorage | 1.3 GB | 689 | ⭐ Low (cache) |
| CachedData | 1.1 GB | 796 | ⭐ Low (cache) |
| Partitions | 131 MB | 1,357 | ⭐⭐ Medium |
| logs | 16.6 MB | 874 | ⭐⭐ Medium |
| Session Storage | 25 KB | 6 | ⭐⭐ Medium |
| Local Storage | 6.8 KB | 6 | ⭐⭐ Medium |

## Unexplored/Low Priority

| Folder | Size | Why Low Priority |
|--------|------|------------------|
| CachedExtensionVSIXs | 130 MB | Extension packages |
| GPUCache | 5.6 MB | GPU shader cache |
| DawnCache | 544 KB | WebGPU cache |
| Network | 71 KB | Cookies, transport |
| Crashpad | 40 B | Crash dumps |

