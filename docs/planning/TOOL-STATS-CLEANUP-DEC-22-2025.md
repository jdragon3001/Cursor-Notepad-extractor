# Tool Stats Cleanup - December 22, 2025

## Problem
We have **duplicate tool statistics** from two different sources:

### 1. MESSAGE Category (BROKEN - Always 0)
Source: `bubbleId` → checking `message.tool_results` array (always empty)
- `messages_with_tools`: 0
- `tool_invocations`: 0
- `tools_per_message`: 0
- `tool_usage_by_type`: 0
- `tool_success_failure`: 0

### 2. TOOLS Category (WORKING - Real Data)
Source: `toolFormerData` → checking `message.tool_former_data` (populated)
- `messages_with_tools`: 48,020
- `total_tool_invocations`: 48,020
- `tools_per_message`: 1.0
- `most_used_tools`: [real data]
- `tool_status_distribution`: [real data]
- `tool_success_rate`: 60.17%
- `tool_error_rate`: 37.69%
- `tool_cancellation_rate`: 1.95%
- `unique_tool_types`: 39

## Root Cause
The Message model has properties that check `self.tool_results`:
- `has_tools` → checks `tool_results` array
- `get_tool_count()` → counts `tool_results`
- `get_tool_types()` → extracts from `tool_results`

But `tool_results` is never populated because Cursor stores tool data in `toolFormerData`, not in a `toolResults` array within the bubble data.

## Solution
**Remove the duplicate MESSAGE category tool stats** because:
1. They're always 0 (checking wrong field)
2. We already have correct stats in TOOLS category
3. Having both is confusing (same stat names, different values)

## Files Being Removed
- `stats/calculators/message_stats/tools.py` (entire file)

## Files Being Modified
- `stats/calculators/message_stats/__init__.py`:
  - Remove import of `MessageToolStats`
  - Remove initialization of `self.tools`
  - Remove `stats.update(self.tools.calculate())`

## Verification
After removal, verify:
1. TOOLS category stats still work (48k+ invocations)
2. MESSAGE category no longer has tool stats
3. No duplicate stat names in output
4. Frontend shows only working tool stats



