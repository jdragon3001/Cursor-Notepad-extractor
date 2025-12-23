# Data Field Audit Report - December 22, 2025

## 🔍 COMPREHENSIVE STAT ACCURACY AUDIT

### Issue Reported
User questioned stats showing all zeros for:
- Messages with linter errors: 0
- Total linter errors: 0  
- Messages with console logs: 0
- Messages with terminal interactions: 0

### Investigation Results

Analyzed 50,000 messages from the Cursor database to determine data availability.

## ✅ ACCURATE "ZERO" STATS

These stats ARE accurate - Cursor doesn't populate these fields:

| Field | Messages with Data | Actual Usage |
|-------|-------------------|--------------|
| `lints` array | **0 (0%)** | ❌ Not used by Cursor |
| `consoleLogs` array | **0 (0%)** | ❌ Not used by Cursor |
| `toolResults` array | **0 (0%)** | ❌ Not used by Cursor |
| `approximateLintErrors` | **0 (0%)** | ❌ Not populated |
| `multiFileLinterErrors` | **0 (0%)** | ❌ Not populated |

**Conclusion:** The "0 linter errors" and "0 console logs" stats are technically correct because Cursor doesn't store this data in the expected fields.

## ✅ DATA THAT EXISTS

These fields DO have data and should be tracked:

| Field | Messages with Data | Percentage | Status |
|-------|-------------------|------------|---------|
| `toolFormerData` | **22,428** | **44.9%** | ✅ Being extracted (68.1%) |
| `lastTerminalCwd` | **1,505** | **3.0%** | ⚠️ Not extracted |
| `errorDetails` | **35** | **0.1%** | ⚠️ Not extracted |
| `existedPreviousTerminalCommand` | **116** | **0.2%** | ⚠️ Not extracted |
| `existedSubsequentTerminalCommand` | Unknown | Unknown | ⚠️ Not extracted |

## 📊 WHAT THE DATA ACTUALLY TELLS US

### Tool Usage (Real Data)
- **44.9%** of messages involve tool usage
- Primary tool: `codebase_search` (semantic code search)
- Tools tracked in `toolFormerData` field
- Already being extracted correctly ✅

### Terminal Activity (Real Data)  
- **3.0%** of messages have terminal context (`lastTerminalCwd`)
- **0.2%** have explicit terminal command references
- This data EXISTS but isn't being extracted yet ⚠️

### Error Information (Limited Data)
- Only **0.1%** (35 messages) have `errorDetails`
- Lint errors are NOT tracked by Cursor in message data
- Console logs are NOT tracked by Cursor in message data

## 🎯 RECOMMENDATIONS

### 1. Update Dashboard Labels ✅ HIGH PRIORITY

**Current (Misleading):**
- "Messages with linter errors: 0"
- "Total linter errors: 0"
- "Messages with console logs: 0"

**Should Be (Accurate):**
- Remove these stats entirely (data doesn't exist)
- OR label as "Not tracked by Cursor"
- OR show "N/A - Data not available"

### 2. Add Terminal Stats ⚠️ MEDIUM PRIORITY

**Add these stats:**
- Messages with terminal context: ~3% (1,505 messages)
- Messages with terminal commands: ~0.2% (116 messages)
- Terminal working directories used: (extract unique paths)

**Implementation:**
- Extract `lastTerminalCwd` field
- Extract `existedPreviousTerminalCommand` / `existedSubsequentTerminalCommand`
- Add to Message model
- Create terminal-specific calculator

### 3. Enhance Error Tracking ⚠️ LOW PRIORITY

**Current:** Only 35 messages (0.1%) have `errorDetails`

**Options:**
1. Show this tiny number honestly: "35 errors captured (0.05%)"
2. Remove error stats entirely (too sparse to be meaningful)
3. Clarify that Cursor doesn't comprehensively track errors

## 🔧 IMPLEMENTATION NEEDED

### Phase 1: Remove Misleading Stats (IMMEDIATE)
```python
# Remove or mark as N/A:
- messages_with_lints
- linter_errors  
- messages_with_console_logs
- terminal_interactions (until we extract terminal data)
```

### Phase 2: Add Terminal Extraction (NEXT)
```python
# Add to Message model:
last_terminal_cwd: Optional[str] = None
had_prev_terminal_command: bool = False
had_next_terminal_command: bool = False

# Extract in from_dict:
last_terminal_cwd=data.get('lastTerminalCwd'),
had_prev_terminal_command=bool(data.get('existedPreviousTerminalCommand')),
had_next_terminal_command=bool(data.get('existedSubsequentTerminalCommand')),
```

### Phase 3: Create Terminal Stats (LATER)
- Messages with terminal context
- Unique terminal directories  
- Terminal command frequency
- Terminal context by session

## 📈 STAT ACCURACY SUMMARY

| Category | Status | Accuracy | Action Needed |
|----------|--------|----------|---------------|
| Timestamps | ✅ Fixed | 100% | None - verified correct |
| Activity streaks | ✅ Fixed | 100% | None - now showing 39 days |
| Tool usage | ✅ Working | ~68% | Already extracted from toolFormerData |
| Sessions | ✅ Working | 100% | None - 1,024 sessions accurate |
| Code diffs | ✅ Working | 100% | None - 10,944 diffs extracted |
| **Linter errors** | ❌ Zero (correct) | N/A | **Remove stat - no data exists** |
| **Console logs** | ❌ Zero (correct) | N/A | **Remove stat - no data exists** |
| **Terminal** | ⚠️ Zero (incorrect) | 0% | **Add extraction - data exists!** |
| Workspace info | ⚠️ Missing | 0% | **Add extraction** |

## 🎯 THE BOTTOM LINE

**User Instinct Was Correct!**

Jack was right to question zeros because:
1. ✅ Some zeros are real (lint/console - Cursor doesn't track this)
2. ❌ Some zeros are wrong (terminal - we're not extracting it)
3. 🎯 Dashboard labels are misleading users

**Fix Priority:**
1. **IMMEDIATE:** Remove/relabel misleading zero stats
2. **NEXT:** Extract terminal context data (exists in 3% of messages)
3. **LATER:** Add workspace extraction for per-project stats

---

## 📝 FIELD MAPPING REFERENCE

**Fields that DON'T exist (remove stats):**
- `lints[]` - empty
- `consoleLogs[]` - empty
- `toolResults[]` - empty  
- `approximateLintErrors` - not used
- `multiFileLinterErrors` - not used

**Fields that DO exist (extract these):**
- ✅ `toolFormerData` - already extracted
- ⚠️ `lastTerminalCwd` - need to extract
- ⚠️ `existedPreviousTerminalCommand` - need to extract
- ⚠️ `errorDetails` - minimal data, optional

---

*Audit completed: December 22, 2025*
*Data verified: 50,000+ messages analyzed*
*Recommendation: Update dashboard immediately*

