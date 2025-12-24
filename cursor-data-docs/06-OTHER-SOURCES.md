# Other Data Sources

**Created: December 21, 2025**

Additional data sources that may contain valuable information.

## WebStorage (1.3 GB)

Browser-style cache storage.

### Location
```
%APPDATA%\Cursor\WebStorage\
```

### Structure
```
WebStorage/
├── 1/                    # 693 MB
│   └── CacheStorage/
├── 2/                    # 28 KB
├── 3/                    # 9 KB
├── 4/                    # 8 KB
├── 5/                    # 15 MB
├── 6/                    # 617 MB
├── 7/                    # 8 KB
├── QuotaManager          # 40 KB (SQLite)
└── QuotaManager-journal
```

### Notes
- Contains browser cache for webviews
- Large size suggests cached web content
- May contain AI response caches
- QuotaManager tracks storage quotas

## Partitions (131 MB)

Per-browser-view partitions for webviews.

### Location
```
%APPDATA%\Cursor\Partitions\cursor-browser-{workspace-id}\
```

### Structure
```
cursor-browser-{id}/
├── blob_storage/
├── Cache/
├── Code Cache/
├── DawnGraphiteCache/
├── DawnWebGPUCache/
├── DIPS
├── DIPS-wal
├── GPUCache/
├── IndexedDB/           # May contain chat history!
├── Local Storage/       # LevelDB
├── Network/
├── Preferences
├── Session Storage/     # LevelDB
└── Service Worker/
```

### Key Areas
- **IndexedDB**: May contain chat message storage
- **Local Storage**: Per-partition state
- **Session Storage**: Real-time session data

## LevelDB Databases (21 total)

Chrome-style key-value stores.

### Main LevelDB Locations
```
Session Storage/                    # 25 KB
Local Storage/leveldb/              # 6.8 KB
Partitions/*/Local Storage/leveldb/
Partitions/*/Session Storage/
Service Worker/Database/            # 185 KB
```

### Reading LevelDB

Requires `plyvel` library:

```python
# pip install plyvel
import plyvel

db = plyvel.DB('path/to/leveldb/')
for key, value in db:
    print(f"{key}: {value}")
db.close()
```

**Note**: May need to copy database while Cursor is closed.

## Service Worker (308 KB)

Service worker data for background processing.

### Location
```
%APPDATA%\Cursor\Service Worker\
```

### Structure
```
Service Worker/
├── Database/           # LevelDB (185 KB)
│   ├── 000004.log
│   ├── 000005.ldb
│   └── ...
└── ScriptCache/        # Cached scripts (122 KB)
    └── {hash}_0, {hash}_1
```

## CachedData (1.1 GB)

Chrome V8 code cache.

### Location
```
%APPDATA%\Cursor\CachedData\{hash}\chrome\
```

### Notes
- Contains compiled JavaScript bytecode
- One folder per Cursor version
- Not directly useful for analytics
- Safe to delete for space

## Network Folder (71 KB)

Network-related data.

### Location
```
%APPDATA%\Cursor\Network\
```

### Contents
| File | Size | Description |
|------|------|-------------|
| Cookies | 24 KB | Session cookies |
| Network Persistent State | 4.6 KB | Network configuration |
| TransportSecurity | 3.1 KB | HTTPS security |
| Trust Tokens | 36 KB | Privacy tokens |

## Configuration Files

### User Settings
```
%APPDATA%\Cursor\User\settings.json
```
User preferences and settings.

### Keybindings
```
%APPDATA%\Cursor\User\keybindings.json
```
Custom keyboard shortcuts.

### Profile Associations
```
%APPDATA%\Cursor\User\globalStorage\storage.json
```
Maps workspaces to profiles.

## Backups (14 KB)

Workspace backup data.

### Location
```
%APPDATA%\Cursor\Backups\{hash}\
```

### Contents
- Workspace recovery data
- Usually small
- Created on crashes

## Analytics Priority

| Source | Priority | Reason |
|--------|----------|--------|
| Partitions/IndexedDB | ⭐⭐⭐ | May have chat history |
| WebStorage | ⭐⭐ | Large, may have caches |
| LevelDB databases | ⭐⭐ | Session/local storage |
| Service Worker | ⭐ | Background data |
| CachedData | ⭐ | Just bytecode cache |
| Network | ⭐ | Just cookies/config |

## Exploration Script

```python
from pathlib import Path
import os

cursor_path = Path.home() / 'AppData/Roaming/Cursor'

# Check IndexedDB in partitions
partitions = cursor_path / 'Partitions'
if partitions.exists():
    for partition in partitions.iterdir():
        idb = partition / 'IndexedDB'
        if idb.exists():
            print(f"\nIndexedDB found in: {partition.name}")
            for item in idb.iterdir():
                print(f"  - {item.name}")

# Check WebStorage
webstorage = cursor_path / 'WebStorage'
if webstorage.exists():
    for item in webstorage.iterdir():
        if item.is_dir():
            size = sum(f.stat().st_size for f in item.rglob('*') if f.is_file())
            print(f"WebStorage/{item.name}: {size/1024/1024:.1f} MB")
```

