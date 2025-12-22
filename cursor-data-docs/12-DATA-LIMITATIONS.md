# Data Limitations & Discrepancies

**Created: December 22, 2025**

This document explains why local data extraction shows different numbers than Cursor's Year Wrapped.

## Key Finding: Multiple Data Sources with Different Date Ranges

| Data Source | Date Range | What It Contains |
|-------------|------------|------------------|
| **cursorDiskKV** (global) | Oct 8, 2025 → Present | Full chat messages |
| **Workspace DBs** | Nov 14, 2024 → Present | Session metadata |
| **Daily Stats** | Nov 20, 2025 → Present | Lines suggested/accepted |
| **AI Code Tracking** | Oct 8, 2025 → Present | File-level tracking |

## Why Numbers Don't Match Year Wrapped

### 1. Model Info Incomplete (11.5% coverage)

**Problem:** Only 7,879 of 68,657 messages (11.5%) have `modelInfo.modelName` populated.

**Reasons:**
- User messages (type=1) have model info (99.8%)
- AI responses (type=2) only have model info in 6.1% of cases
- Model migrations changed stored model names
- Older data didn't track this field

**Impact:** Model usage breakdown is incomplete for historical data.

### 2. Token Counts Partially Populated

**Problem:** Token data exists but is inconsistent.

| Source | Data |
|--------|------|
| `bubbleId.tokenCount` | 292M input, 3.5M output |
| `composerData.contextTokensUsed` | 35M |

**Reasons:**
- `tokenCount` often shows 0 for older messages
- Server-side billing tracks authoritative totals
- Local storage is for display, not billing

### 3. Lines of Code Discrepancy

| Source | Lines Added | Time Range |
|--------|-------------|------------|
| `composerData.totalLinesAdded` | 429,700 | Nov 2024 → Present |
| `aiCodeTracking.dailyStats` | 137,144 suggested | Nov 20, 2025 → Present |

**Gap:** ~290,000 lines were added before Nov 20, 2025 when daily stats started.

### 4. Model Migrations

Cursor migrates model preferences over time:

```
claude-4-sonnet → claude-4.5-sonnet
claude-4-sonnet-thinking → claude-4.5-sonnet-thinking
claude-4.5-sonnet → claude-4.5-opus-high
```

Stored data shows the **migrated** name, not the original model used.

## What We CAN Extract Locally

| Metric | Available? | Notes |
|--------|------------|-------|
| Total messages | ✅ Yes | 68,657 messages |
| User messages | ✅ Yes | 3,970 messages |
| AI responses | ✅ Yes | 64,681 messages |
| Total sessions | ✅ Yes | 2,934 sessions |
| Lines added (total) | ✅ Yes | 429,700 lines |
| Token counts | ⚠️ Partial | ~292M input tokens |
| Model usage | ⚠️ Partial | Only 11.5% coverage |
| Daily breakdown | ⚠️ Partial | Only since Nov 20, 2025 |
| Prompt count | ✅ Yes | 1,477 prompts |

## What We CANNOT Extract Locally

| Metric | Why |
|--------|-----|
| Complete model breakdown | Server-side tracking |
| Exact billing tokens | Server-side billing |
| Usage ranking (Top X%) | Requires all-user comparison |
| Streak calculations | Server-side logic |
| Historical daily stats | Not stored locally pre-Nov 2025 |

## Server-Side vs Local Data

```
                    ┌─────────────────────────────────┐
                    │        CURSOR SERVER            │
                    │  - Complete usage history       │
                    │  - Billing/payment data         │
                    │  - All user comparisons         │
                    │  - Year Wrapped analytics       │
                    └─────────────┬───────────────────┘
                                  │
                                  │ Partial sync
                                  ▼
                    ┌─────────────────────────────────┐
                    │        LOCAL STORAGE            │
                    │  - Chat messages (recent)       │
                    │  - Session metadata             │
                    │  - Daily stats (since Nov 20)  │
                    │  - Workspace-level data         │
                    └─────────────────────────────────┘
```

## Recommendation

**For the data extraction app:**

1. **Aggregate from ALL sources** - cursorDiskKV + workspaces + daily stats
2. **Accept incomplete model data** - Show what's available with caveat
3. **Use multiple token sources** - bubbleId + composerData + contextTokensUsed
4. **Note limitations** - Be transparent about data gaps
5. **Focus on available metrics** - Messages, sessions, lines of code are solid

## Data We DO Have (Verified)

```
Total Chat Sessions:     2,934
Total Messages:         68,657
Total Prompts:           1,477
Input Tokens:      292,576,040 (from local data)
Lines of Code Added:   429,700
Lines Accepted (recent): 66,771 (since Nov 20)
Scored Commits:            386
Subscription Status:    active
Data Span:           402 days (Nov 14, 2024 → Dec 22, 2025)
```

This is still valuable data for building analytics!

