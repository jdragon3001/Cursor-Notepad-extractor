# Stat Accuracy Fixes - December 22, 2025

## Summary
Fixed multiple categories of incorrect stats by identifying the correct data sources and fields in Cursor's database schema.

## Stats Fixed

### 1. Code Block Languages & File References (Previously 0 → Now Correct)
**Problem:** Stats were checking for `language` and `filePath` fields, but Cursor stores them as `languageId` and `uri`.

**Fix:** Updated field lookups in `stats/calculators/message_stats/content.py`
- `code_block_languages`: 0 → 28 unique languages (14,743 total blocks)
- `files_referenced_in_code`: 0 → 2,614 unique files (11,277 references)

### 2. Web Search & Browser Tools (Previously 0 → Now Correct)
**Problem:** Stats were checking non-existent `webReferences` and `useWeb` fields. Actual data is in `toolFormerData`.

**Fix:** Updated `stats/calculators/message_stats/references.py` to check `toolFormerData` for tool names
- `web_references` (web_search tool): 0 → 176
- `messages_using_web` (browser tools): 0 → 468

**Tools Found:**
- `web_search`: 176 invocations
- MCP browser tools: 292 invocations (navigate, snapshot, screenshot, click, type, etc.)

### 3. Code Suggestions & User Responses (Previously 0 → Now Correct)
**Problem:** Stats were checking empty `suggestedCodeBlocks` and `userResponsesToSuggestedCodeBlocks` arrays. Real data is in:
- Assistant messages (type=2) with code blocks
- `toolFormerData` with `userDecision` field

**Fix:** Completely rewrote `stats/calculators/message_stats/suggestions.py`
- `suggested_code_blocks`: 0 → 14,762
- `assistant_suggested_diffs`: 0 → 8,987
- `accepted_suggestions`: 0 → 14,809
- `rejected_suggestions`: 0 → 770
- `acceptance_rate`: 0% → 95.06%

**Acceptance Breakdown:**
- `search_replace_accepted`: 7,848
- `run_terminal_cmd_accepted`: 3,392
- `write_accepted`: 2,326
- `apply_patch_accepted`: 472
- Total rejections: Only 770 across all tools

### 4. Duplicate Stats Removed

#### A. MESSAGE Tool Stats (Duplicates of TOOLS Category)
**Removed from `message_stats/tools.py`:**
- `messages_with_tools`: Always 0 (checked wrong field)
- `tool_invocations`: Always 0
- `tools_per_message`: Always 0
- `tool_usage_by_type`: Always 0
- `tool_success_failure`: Always 0

**Reason:** TOOLS category already has correct stats from `toolFormerData`:
- `total_tool_invocations`: 48,020
- `tool_success_rate`: 60.17%
- `unique_tool_types`: 39

#### B. MESSAGE Context Stats (Wrong Data Source)
**Removed from `message_stats/context.py`:**
- `attached_code_chunks`: Always 0
- `codebase_context_chunks`: Always 0
- `lines_in_attached_chunks`: Always 0
- `relevant_files`: Always 0
- `recently_viewed_files`: Always 0
- `unique_files_in_context`: Always 0

**Reason:** Context data lives in `MessageRequestContext`, not `Message`. CONTEXT category already has correct stats:
- `contexts_with_attached_chunks`: 105
- `contexts_with_editor_state`: 3,408
- `contexts_with_file_context`: Present

#### C. Response Time Stat (No Data Available)
**Removed:** `response_time_to_suggestions` - timing data between suggestion and acceptance is not stored in the database schema.

### 5. Legitimately Zero Stats (Verified Accurate)
These stats are correctly showing 0 because you haven't used these features:
- `messages_with_git_diffs`: 0 (checked - field exists but empty)
- `messages_with_diff_histories`: 0 (checked - field exists but empty)
- `messages_with_human_changes`: 0 (checked - field exists but empty)
- `docs_references`: 0 (checked - you haven't used doc references)

## Root Causes Identified

### 1. Wrong Field Names
Cursor's schema uses different field names than expected:
- `languageId` not `language`
- `uri` (as dict) not `filePath`
- `toolFormerData` with `name` field for tool names

### 2. Wrong Data Source
Some data lives in different tables:
- Tool usage: `toolFormerData` field in messages
- Context data: `MessageRequestContext` entries, not in `Message` objects
- User decisions: `userDecision` field in `toolFormerData`

### 3. Empty Arrays That Were Never Populated
Cursor doesn't populate these fields (always empty arrays):
- `message.tool_results`
- `message.lints`
- `message.console_logs`
- `message.suggestedCodeBlocks`
- `message.userResponsesToSuggestedCodeBlocks`
- `message.attachedCodeChunks`
- `message.codebaseContextChunks`

## Files Modified
1. `stats/calculators/message_stats/content.py` - Fixed field names
2. `stats/calculators/message_stats/references.py` - Check toolFormerData for web tools
3. `stats/calculators/message_stats/suggestions.py` - Complete rewrite using correct sources
4. `stats/calculators/message_stats/context.py` - Removed duplicate stats
5. `stats/calculators/message_stats/__init__.py` - Removed MessageToolStats import
6. `stats/calculators/message_stats/tools.py` - Deprecated (renamed to .deprecated)

## Impact
- **Before:** 30+ stats showing incorrect 0 values
- **After:** All stats now show accurate data from correct sources
- **User confidence:** Restored - stats now match actual usage patterns

