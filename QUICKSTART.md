# Quick Start Guide - Cursor Data Stats

## Running the Test Pipeline

```bash
# Activate environment
conda activate cursor-notepad-browser

# Run full test with fresh extraction
python test_stats_pipeline.py

# The test will:
# 1. Extract all messages and sessions
# 2. Calculate 18 message stats
# 3. Display key metrics
# 4. Export stats to stats_output.json
```

## Adding a New Stat

### 1. Add to Calculator

Edit `stats/calculators/message_calculator.py` (or relevant calculator):

```python
def stat_020_new_stat_name(self) -> Dict[str, Any]:
    """Stat #20: Description."""
    # Calculate your metric
    values = [calculation for msg in self.messages]
    
    return self.create_stat_result(
        value=self.average(values),  # or count, sum, etc.
        label='Human-readable label',
        category='Messages',
        data_source='bubbleId',
        stat_type='numeric',  # or 'count', 'percentage'
        # Optional fields:
        median=self.median(values),
        min=self.min_val(values),
        max=self.max_val(values),
        # ... add any other relevant fields
    )
```

### 2. Add to calculate_all()

```python
def calculate_all(self) -> Dict[str, Any]:
    stats = {
        # ... existing stats ...
        'new_stat_name': self.stat_020_new_stat_name(),
    }
    return stats
```

### 3. Test it

```python
# Run the test pipeline
python test_stats_pipeline.py

# Check stats_output.json for your new stat
```

## Available Utility Functions

### BaseCalculator provides:

**Counts:**
- `self.count(items)` - Count items
- `self.percentage(part, total)` - Calculate percentage

**Statistics:**
- `self.average(values)` - Mean
- `self.median(values)` - Median
- `self.percentile(values, p)` - Pth percentile
- `self.std_dev(values)` - Standard deviation
- `self.min_val(values)` - Minimum
- `self.max_val(values)` - Maximum
- `self.sum_val(values)` - Sum

**Aggregation:**
- `self.most_common(items, n)` - Top N items
- `self.group_by(items, key_func)` - Group by key
- `self.filter_by(items, predicate)` - Filter items
- `self.distribution(values, bins)` - Histogram

**Caching:**
- `self.cached(key, calc_func)` - Cache expensive calculations

## Message Properties

Access via `msg.property` or `msg.helper_method()`:

**Core:**
- `msg.bubble_id` - Unique ID
- `msg.composer_id` - Session ID
- `msg.message_type` - 1=user, 2=AI
- `msg.created_at` - datetime

**Content:**
- `msg.text` - Message text
- `msg.code_blocks` - List of code blocks
- `msg.suggested_code_blocks` - AI suggestions

**Thinking:**
- `msg.thinking` - Thinking content (str or dict)
- `msg.thinking_duration_ms` - Duration

**Tools:**
- `msg.tool_results` - List of tool results

**Context:**
- `msg.attached_code_chunks` - User context
- `msg.codebase_context_chunks` - Auto context

**Model/Tokens:**
- `msg.model_info` - Model details
- `msg.token_count` - Token counts

**Helper Properties:**
- `msg.is_user_message` - Bool
- `msg.is_ai_message` - Bool
- `msg.has_text` - Bool
- `msg.has_code` - Bool
- `msg.has_thinking` - Bool
- `msg.has_tools` - Bool
- `msg.has_context` - Bool

**Helper Methods:**
- `msg.get_text_length()` - Character count
- `msg.get_text_word_count()` - Word count
- `msg.get_code_block_count()` - Total code blocks
- `msg.get_code_line_count()` - Total lines
- `msg.get_tool_count()` - Number of tools
- `msg.get_tool_types()` - List of tool types
- `msg.get_model_name()` - Model name
- `msg.get_input_tokens()` - Input tokens
- `msg.get_output_tokens()` - Output tokens
- `msg.get_total_tokens()` - Total tokens

## Session Properties

Access via `session.property`:

**Core:**
- `session.composer_id` - Unique ID
- `session.created_at` - datetime
- `session.last_updated_at` - datetime

**Info:**
- `session.name` - Session name
- `session.status` - Status
- `session.is_archived` - Bool

**Tokens:**
- `session.context_tokens_used` - Token count
- `session.context_token_limit` - Limit
- `session.context_usage_percent` - Percentage

**Code:**
- `session.total_lines_added` - Lines added
- `session.total_lines_removed` - Lines removed
- `session.added_files` - List of files
- `session.removed_files` - List of files

**Helper Properties:**
- `session.duration_seconds` - Duration
- `session.duration_minutes` - Duration
- `session.duration_hours` - Duration
- `session.net_lines_changed` - Added - Removed
- `session.total_lines_changed` - Added + Removed

## File Structure Reference

```
stats/
├── extractors/
│   ├── base_extractor.py        # Extend this for new extractors
│   ├── message_extractor.py     
│   └── session_extractor.py     
├── models/
│   ├── message.py               # Message data class
│   └── session.py               # Session data class
├── calculators/
│   ├── base_calculator.py       # Extend this for new calculators
│   └── message_calculator.py    # Add stats here
├── orchestrator.py              # Main coordinator
└── cache.py                     # Caching system
```

## Troubleshooting

### Cache Issues
```python
# Clear cache and force fresh extraction
orchestrator = StatsOrchestrator(db_path, cache_dir)
orchestrator.invalidate_cache()
```

### Check Extraction
```python
# Get summary
summary = orchestrator.get_summary()
print(f"Messages: {summary['total_messages']}")
print(f"Sessions: {summary['total_sessions']}")
```

### Debug Specific Stat
```python
# Get single stat
stat = orchestrator.get_stat('total_messages')
print(stat)
```

## Next Stats to Implement

See `docs/planning/PURE-STATS-INDEX.md` for the complete list of 232 stats.

**Priority stats (20-30):**
- Stat #20: Tool success/failure
- Stat #21-26: Context stats
- Stat #27-30: External references
- Stat #31-41: Code suggestions & acceptance

**After that:**
- Session stats (67-93)
- Code metrics (94-105)
- Daily stats (106-111)

---

*For detailed architecture, see `docs/planning/STATS-CALCULATION-ARCHITECTURE.md`*

