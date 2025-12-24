# Context Stats Cleanup - December 22, 2025

## Problem
MESSAGE category has context-related stats that are ALWAYS 0:
- `attached_code_chunks`: 0
- `codebase_context_chunks`: 0
- `lines_in_attached_chunks`: 0
- `relevant_files`: 0
- `recently_viewed_files`: 0
- `unique_files_in_context`: 0
- `web_references`: 0

## Root Cause
**Wrong Data Source:** These stats check `Message` objects (from `bubbleId`), but context data is actually stored in `MessageRequestContext` (from `messageRequestContext` entries).

### Data Distribution:
```
Message objects (70,748):
  - attached_code_chunks: 0 messages
  - codebase_context_chunks: 0 messages
  - relevant_files: 0 messages
  - recently_viewed_files: 0 messages
  - web_references: 0 messages

MessageRequestContext objects (4,210):
  - attached_file_code_chunks: 105 contexts ✓
  - ide_editors_state: 3,408 contexts ✓
  - current_file_location_data: 2,870 contexts ✓
```

## Solution
**Remove duplicate MESSAGE category context stats** because:
1. They check the wrong data source (Message vs MessageRequestContext)
2. They're always 0 (fields never populated in Message objects)
3. **CONTEXT category already has working stats** from MessageRequestContext:
   - `contexts_with_file_context`
   - `contexts_with_attached_chunks`
   - `attached_chunks_per_context`
   - `contexts_with_editor_state`

## Files Modified
- `stats/calculators/message_stats/context.py`:
  - Removed all stat calculations from `calculate()` method
  - Added note explaining context data is in MessageRequestContext
  - Kept stat functions for reference but they won't be called

## Verification
After removal:
- MESSAGE category won't have misleading 0s for context stats
- CONTEXT category still has accurate context stats from correct source
- No duplicate stat names

