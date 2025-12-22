# Chat Data Recovery Report

**Generated:** 2025-12-22 00:19:24

## Executive Summary

- **Total Chat Sessions:** 2934
- **Total Messages:** 68636
- **Earliest Data:** 2024-11-14 11:45:48.440000
- **Latest Data:** 2025-12-22 00:15:49.667000
- **Data Span:** 402 days

## Data Sources

| Source | Sessions | Date Range |
|--------|----------|------------|
| Global Database (cursorDiskKV) | 1076 | 2025-10-08 00:03:45.726000 to 2025-12-22 00:15:49.667000 |
| Workspace Databases | 1858 | 2024-11-14 11:45:48.440000 to 2025-12-22 00:15:49.667000 |
| Local Storage (LevelDB) | N/A | N/A |

## Critical Finding: Data Gap

The `cursorDiskKV` table in the global database only contains data from **October 2025**.
However, **workspace databases contain data from November 2024**.

### Implication

To get complete chat history, the data extraction app MUST:
1. Read from `cursorDiskKV` for recent data (Oct 2025+)
2. Read from individual workspace `state.vscdb` files for older data (Nov 2024+)
3. Check backup folder for any additional data
4. Deduplicate sessions that may appear in multiple sources

## Workspace Database Details

Found **227** workspace databases with chat data.

### Workspaces by Date (Oldest First)

| Workspace | Sessions | Earliest | Latest |
|-----------|----------|----------|--------|
| `8cf2b428cdb17fae085f` | 5 | 2024-11-14 | 2024-12-02 |
| `2b94c74f6f0c926708f3` | 4 | 2024-11-15 | 2024-11-29 |
| `6cb62dff3a970dc66521` | 4 | 2024-11-20 | 2024-11-28 |
| `2873e530303e4e66b7d1` | 21 | 2024-11-28 | 2025-01-10 |
| `c32b2eab41cb3468ee00` | 5 | 2024-11-29 | 2024-11-29 |
| `599bcfffca83fd1155d2` | 3 | 2024-12-01 | 2024-12-01 |
| `899355b53bd09c948eb6` | 2 | 2024-12-01 | 2024-12-01 |
| `96ae192a669798fe3481` | 8 | 2024-12-01 | 2024-12-07 |
| `69563bb3cc8f7200edd7` | 2 | 2024-12-07 | 2024-12-07 |
| `daf08902bd4bf62d51c2` | 2 | 2024-12-07 | 2024-12-07 |
| `eb34eff26768c6869581` | 4 | 2024-12-13 | 2024-12-14 |
| `44272c4c34d0070f93d2` | 2 | 2024-12-14 | 2024-12-14 |
| `208b5f840d2d2c310939` | 3 | 2024-12-15 | 2024-12-15 |
| `53f8219bdf1a9bdb2b2d` | 2 | 2024-12-15 | 2024-12-15 |
| `80045d9da6a28bca293a` | 5 | 2024-12-16 | 2024-12-18 |
| `010299b466d3ee6862f3` | 16 | 2024-12-26 | 2024-12-30 |
| `1847af884a529a75ed75` | 2 | 2024-12-27 | 2024-12-27 |
| `2b4a8ca7b15d767acf20` | 3 | 2024-12-28 | 2024-12-28 |
| `9092cbb51fcb8b6caac2` | 11 | 2024-12-31 | 2025-01-10 |
| `9081d360ff7da8cd6649` | 2 | 2025-01-01 | 2025-01-01 |
| `a4f9dce2fd081508ad02` | 2 | 2025-01-04 | 2025-01-04 |
| `57f14887cc5541a7d2f2` | 4 | 2025-01-04 | 2025-01-05 |
| `e17ba2ce97f87d084c44` | 2 | 2025-01-05 | 2025-01-05 |
| `8b982214db3b72d68ab6` | 3 | 2025-01-08 | 2025-01-13 |
| `e9ddbeef0b7a63ffd05b` | 3 | 2025-01-08 | 2025-01-12 |
| `3a93bbdce92b4cecc230` | 10 | 2025-01-10 | 2025-01-21 |
| `6f6eeb83619dcd92ebab` | 7 | 2025-01-10 | 2025-01-21 |
| `7aeaa97ae70f08086e0c` | 3 | 2025-01-11 | 2025-01-11 |
| `c343cb574b83543aba72` | 2 | 2025-01-12 | 2025-01-12 |
| `85b74031751afaac0cb2` | 2 | 2025-01-12 | 2025-01-12 |

## Recovery Strategy

```python
# Pseudocode for complete data extraction
def extract_all_chat_data():
    all_sessions = {}
    
    # 1. Extract from global cursorDiskKV (recent data)
    global_sessions = extract_from_cursorDiskKV(global_db)
    for session in global_sessions:
        all_sessions[session.id] = session
    
    # 2. Extract from ALL workspace databases (older data)
    for workspace in get_all_workspaces():
        ws_sessions = extract_from_workspace(workspace)
        for session in ws_sessions:
            if session.id not in all_sessions:
                all_sessions[session.id] = session
            else:
                # Merge/deduplicate
                all_sessions[session.id].merge(session)
    
    return all_sessions
```

## Data Quality Notes

### Global Database (cursorDiskKV)
- Contains: Full message content, model info, token counts
- Date range: October 2025 onwards
- 68,000+ message entries

### Workspace Databases
- Contains: Session metadata, some message headers
- Date range: November 2024 onwards
- May not have full message content for all sessions
- Has: composerId, createdAt, name, unifiedMode, lines added/removed

## Files Generated

- `10-CHAT-DATA-RECOVERY-REPORT.md` - This file
- `workspace_chat_data.json` - Raw workspace chat data
