# Logs and Telemetry

**Created: December 21, 2025**

Session logs capturing Cursor usage data.

## Location

```
Windows: %APPDATA%\Cursor\logs\{session-timestamp}\
```

## Overview

| Property | Value |
|----------|-------|
| Total Sessions | 10 (recent) |
| Total Size | ~16.6 MB |
| Total Log Files | 874 |
| Session Format | `YYYYMMDDTHHmmss` |

## Session Structure

Each session folder contains:

```
{timestamp}/
├── main.log                    # Main application logs
├── terminal.log                # Terminal activity
├── telemetry.log               # Usage telemetry
├── ptyhost.log                 # PTY host (terminal backend)
├── sharedprocess.log           # Shared process logs
├── remoteTunnelService.log     # Remote tunnel logs
├── editSessions.log            # Edit session logs
├── userDataSync.log            # User data sync logs
├── network-shared.log          # Network activity
└── window{N}/                  # Per-window logs
    ├── renderer.log            # Renderer process
    ├── network.log             # Window network
    ├── views.log               # Views activity
    ├── fileWatcher.log         # File watcher
    ├── notebook.rendering.log  # Notebook rendering
    └── exthost/                # Extension host
        └── exthost.log         # Extension logs
```

## Log File Details

### main.log

Main application events. Sample:

```
2025-12-21 17:48:04.447 [warning] [CursorProclistService] Native module unavailable
2025-12-21 17:48:04.528 [info] [storage] Running database optimization (VACUUM)
2025-12-21 17:48:04.656 [info] updateURL https://api2.cursor.sh/updates/...
2025-12-21 17:48:04.656 [info] update#setState idle
```

**Useful for:**
- Startup times
- Update checks
- Storage operations
- Error tracking

### terminal.log

Terminal activity. Sample:

```
2025-12-21 17:48:27.596 [info] Latency measurements for local backend
window<->ptyhost (message port): 1.10ms
window<->ptyhostservice<->ptyhost: 2.50ms
ptyhostservice<->ptyhost: 1.09ms []
```

**Useful for:**
- Terminal usage
- Latency metrics
- Command execution timing

### telemetry.log

Usage telemetry (often empty locally).

### process-monitor/ Folder

CPU/memory monitoring logs:

```
%APPDATA%\Cursor\process-monitor\
├── 1766016000000.log    # Timestamped process logs
├── 1766030400000.log
└── ...
```

## Sample Sessions

| Session | Size | Date | Windows |
|---------|------|------|---------|
| 20251221T174803 | 293 KB | Dec 21, 2025 | 3 |
| 20251220T133021 | 4.6 MB | Dec 20, 2025 | 4 |
| 20251219T224632 | 1.6 MB | Dec 19, 2025 | 3 |
| 20251216T123647 | 4.8 MB | Dec 16, 2025 | 6 |
| 20251214T202813 | 1.8 MB | Dec 14, 2025 | 3 |

## Accessing Logs

### Python Example

```python
from pathlib import Path
from datetime import datetime
import re

logs_path = Path.home() / 'AppData/Roaming/Cursor/logs'

# List all sessions
sessions = []
for session in sorted(logs_path.iterdir(), reverse=True):
    if session.is_dir():
        # Parse timestamp from folder name
        try:
            dt = datetime.strptime(session.name, '%Y%m%dT%H%M%S')
            sessions.append({
                'name': session.name,
                'datetime': dt,
                'path': session
            })
        except:
            continue

# Analyze main.log from latest session
latest = sessions[0] if sessions else None
if latest:
    main_log = latest['path'] / 'main.log'
    if main_log.exists():
        with open(main_log, 'r') as f:
            for line in f:
                # Extract log entries
                match = re.match(r'(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}\.\d{3}) \[(\w+)\]', line)
                if match:
                    timestamp, level = match.groups()
                    print(f"{timestamp} [{level}] {line[match.end():].strip()[:60]}")
```

### Parse Session Duration

```python
def get_session_duration(session_path):
    """Estimate session duration from log timestamps."""
    main_log = session_path / 'main.log'
    if not main_log.exists():
        return None
    
    timestamps = []
    with open(main_log, 'r') as f:
        for line in f:
            match = re.match(r'(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2})', line)
            if match:
                dt = datetime.strptime(match.group(1), '%Y-%m-%d %H:%M:%S')
                timestamps.append(dt)
    
    if timestamps:
        return timestamps[-1] - timestamps[0]
    return None
```

## Analytics Potential

### Session Metrics
- Number of sessions per day/week
- Average session duration
- Windows opened per session
- Startup time

### Error Analysis
- Common errors/warnings
- Error frequency over time
- Extension-related issues

### Performance Metrics
- Terminal latency
- Storage operations
- Update frequency

### Usage Patterns
- Active hours
- Daily usage duration
- Feature usage (terminal, debug, etc.)

## Notes

- Logs rotate with each Cursor restart
- Older sessions may be deleted automatically
- Some logs may be empty (telemetry.log)
- Timestamps are local time

