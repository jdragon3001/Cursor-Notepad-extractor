# Complete List of Extractable Stats & Metrics

**Created: December 22, 2025**
**Purpose: Comprehensive catalog of EVERY stat that can be extracted, calculated, and analyzed**

---

## Data Source: bubbleId (68,657 messages)

### Basic Message Counts
- [ ] Total messages (all time)
- [ ] Total user messages (type=1)
- [ ] Total AI messages (type=2)
- [ ] Messages per day (timeline)
- [ ] Messages per week
- [ ] Messages per month
- [ ] Messages per year
- [ ] Messages per session (average)
- [ ] Messages per session (median)
- [ ] Messages per session (distribution)
- [ ] User messages per session (average)
- [ ] AI messages per session (average)
- [ ] Conversation turns per session (user → AI pairs)

### Message Content Stats
- [ ] Messages with text field populated (count & %)
- [ ] Messages with no text field (count & %)
- [ ] Average text length (characters)
- [ ] Average text length (words)
- [ ] Median text length
- [ ] Text length distribution
- [ ] Shortest message (length)
- [ ] Longest message (length)
- [ ] Total characters sent by user
- [ ] Total characters received from AI
- [ ] Total words sent by user
- [ ] Total words received from AI

### Code Block Stats
- [ ] Messages with code blocks (count & %)
- [ ] Messages without code blocks (count & %)
- [ ] Total code blocks generated
- [ ] Average code blocks per message
- [ ] Code blocks per session
- [ ] Total lines of code in code blocks
- [ ] Average lines per code block
- [ ] Code block languages used (breakdown)
- [ ] Most common programming language
- [ ] Code blocks with file paths (count & %)
- [ ] Code blocks without file paths (count & %)
- [ ] Unique files referenced in code blocks

### Thinking Stats
- [ ] Messages with thinking (count & %)
- [ ] Messages without thinking (count & %)
- [ ] Average thinking text length
- [ ] Total thinking text generated
- [ ] Messages with thinkingDurationMs (count)
- [ ] Average thinking duration (ms)
- [ ] Median thinking duration (ms)
- [ ] Shortest thinking duration
- [ ] Longest thinking duration
- [ ] Total thinking time (cumulative)
- [ ] Thinking duration distribution
- [ ] Messages with allThinkingBlocks (count)
- [ ] Average thinking blocks per message

### Tool Usage Stats
- [ ] Messages with tool usage (count & %)
- [ ] Messages without tool usage (count & %)
- [ ] Total tool invocations
- [ ] Average tools per message
- [ ] Tools per session
- [ ] Unique tools used
- [ ] Usage count per tool type:
  - [ ] codebase_search
  - [ ] grep
  - [ ] read_file
  - [ ] write
  - [ ] search_replace
  - [ ] web_search
  - [ ] terminal commands
  - [ ] list_dir
  - [ ] delete_file
  - [ ] (all other tools)
- [ ] Tool success rate (if available)
- [ ] Tool failure rate (if available)
- [ ] Average results per tool invocation

### Context Stats
- [ ] Messages with attachedCodeChunks (count & %)
- [ ] Total attached code chunks (all messages)
- [ ] Average attached chunks per message
- [ ] Total lines in attached chunks
- [ ] Average lines per attached chunk
- [ ] Messages with codebaseContextChunks (count & %)
- [ ] Total codebase context chunks
- [ ] Average codebase chunks per message
- [ ] Messages with relevantFiles (count & %)
- [ ] Total relevant files referenced
- [ ] Average relevant files per message
- [ ] Messages with recentlyViewedFiles (count & %)
- [ ] Unique files in context (deduplicated)

### Web/External Reference Stats
- [ ] Messages with web references (count & %)
- [ ] Total web references
- [ ] Messages with aiWebSearchResults (count & %)
- [ ] Total web searches performed
- [ ] Messages with docsReferences (count & %)
- [ ] Messages with useWeb=true (count & %)

### Code Suggestion Stats
- [ ] Messages with suggestedCodeBlocks (count & %)
- [ ] Total suggested code blocks
- [ ] Average suggested blocks per message
- [ ] Suggested blocks by action type:
  - [ ] replace
  - [ ] insert
  - [ ] delete
- [ ] Messages with assistantSuggestedDiffs (count & %)

### Acceptance/Response Stats
- [ ] Messages with userResponsesToSuggestedCodeBlocks (count & %)
- [ ] Total user responses to suggestions
- [ ] Accepted suggestions (count & %)
- [ ] Rejected suggestions (count & %)
- [ ] Modified suggestions (count & %)
- [ ] Acceptance rate (accepted / total)
- [ ] Rejection rate (rejected / total)
- [ ] Modification rate (modified / total)
- [ ] Average response time to suggestions

### Diff & Change Stats
- [ ] Messages with gitDiffs (count & %)
- [ ] Total git diffs
- [ ] Messages with diffHistories (count & %)
- [ ] Messages with diffsSinceLastApply (count & %)
- [ ] Messages with humanChanges (count & %)
- [ ] Total human changes after AI suggestions

### Model Stats
- [ ] Messages with modelInfo (count & %)
- [ ] Messages without modelInfo (count & %)
- [ ] Usage breakdown by model:
  - [ ] claude-4.5-sonnet-thinking
  - [ ] claude-4-sonnet
  - [ ] claude-3.5-sonnet
  - [ ] gpt-4
  - [ ] (all other models)
- [ ] Most used model
- [ ] Least used model
- [ ] Model usage over time (trend)
- [ ] Model switches per session

### Token Stats
- [ ] Messages with tokenCount (count & %)
- [ ] Total input tokens (all messages)
- [ ] Total output tokens (all messages)
- [ ] Total tokens (input + output)
- [ ] Average input tokens per message
- [ ] Average output tokens per message
- [ ] Median input tokens
- [ ] Median output tokens
- [ ] Highest token message (input)
- [ ] Highest token message (output)
- [ ] Token distribution (histogram)
- [ ] Tokens by model (breakdown)
- [ ] Tokens by date (timeline)
- [ ] Tokens per session (average)

### Session Context Stats
- [ ] Agentic messages (isAgentic=true) (count & %)
- [ ] Non-agentic messages (count & %)
- [ ] Agent mode messages (count)
- [ ] Chat mode messages (count)
- [ ] Messages with checkpointId (count & %)
- [ ] Unique checkpoints referenced

### Linting & Error Stats
- [ ] Messages with lints (count & %)
- [ ] Total linter errors
- [ ] Messages with approximateLintErrors (count & %)
- [ ] Messages with multiFileLinterErrors (count & %)
- [ ] Linter errors by severity (if available)

### Terminal Interaction Stats
- [ ] Messages with existedPreviousTerminalCommand=true (count & %)
- [ ] Messages with existedSubsequentTerminalCommand=true (count & %)
- [ ] Messages with consoleLogs (count & %)
- [ ] Terminal interactions per session

### Server Reference Stats
- [ ] Messages with serverBubbleId (count & %)
- [ ] Messages with usageUuid (count & %)
- [ ] Messages with requestId (count & %)

### Metadata Stats
- [ ] Refunded messages (isRefunded=true) (count & %)
- [ ] Messages with skipRendering=true (count & %)
- [ ] Nudge messages (isNudge=true) (count & %)

### Timestamp Stats
- [ ] Earliest message timestamp
- [ ] Latest message timestamp
- [ ] Total time span (days)
- [ ] Average messages per day (over active days)
- [ ] Most active day (date + count)
- [ ] Least active day (date + count)
- [ ] Active days (days with messages)
- [ ] Inactive days (days without messages)
- [ ] Longest streak (consecutive days)
- [ ] Current streak (consecutive days to present)
- [ ] Average time between messages (all)
- [ ] Average time between messages (within sessions)
- [ ] Peak activity hours (0-23)
- [ ] Peak activity day of week
- [ ] Activity heatmap (day x hour)

---

## Data Source: composerData (2,934 sessions)

### Basic Session Counts
- [ ] Total sessions (all time)
- [ ] Sessions per day (timeline)
- [ ] Sessions per week
- [ ] Sessions per month
- [ ] Sessions per year
- [ ] Sessions per workspace (breakdown)
- [ ] Average sessions per workspace
- [ ] Most active workspace (by session count)

### Session Duration Stats
- [ ] Average session duration (createdAt → lastUpdatedAt)
- [ ] Median session duration
- [ ] Shortest session duration
- [ ] Longest session duration
- [ ] Session duration distribution
- [ ] Total time in sessions (cumulative)
- [ ] Sessions by duration bucket:
  - [ ] < 1 minute
  - [ ] 1-5 minutes
  - [ ] 5-15 minutes
  - [ ] 15-30 minutes
  - [ ] 30-60 minutes
  - [ ] > 1 hour

### Session Acceptance Stats
- [ ] Total lines added (all sessions)
- [ ] Total lines removed (all sessions)
- [ ] Net lines added (added - removed)
- [ ] Average lines added per session
- [ ] Median lines added per session
- [ ] Average lines removed per session
- [ ] Median lines removed per session
- [ ] Sessions with 0 lines added (count & %)
- [ ] Sessions with >0 lines added (count & %)
- [ ] Highest lines added (single session)
- [ ] Lines added distribution
- [ ] Lines removed distribution
- [ ] Retention rate (1 - removed/added)

### File Change Stats
- [ ] Total files added (deduplicated)
- [ ] Total files removed (deduplicated)
- [ ] Average files added per session
- [ ] Average files removed per session
- [ ] Sessions with file additions (count & %)
- [ ] Sessions with file removals (count & %)
- [ ] Most commonly modified files
- [ ] File types modified (breakdown)

### Context/Token Stats
- [ ] Sessions with contextTokensUsed (count & %)
- [ ] Total context tokens used (all sessions)
- [ ] Average context tokens per session
- [ ] Median context tokens per session
- [ ] Sessions with contextTokenLimit (count & %)
- [ ] Average context token limit
- [ ] Sessions with contextUsagePercent (count & %)
- [ ] Average context usage percent
- [ ] Sessions near limit (>80% context used) (count & %)
- [ ] Sessions at limit (>95% context used) (count & %)
- [ ] Context usage distribution

### Conversation Structure Stats
- [ ] Sessions with fullConversationHeadersOnly (count & %)
- [ ] Average conversation length (message count)
- [ ] Median conversation length
- [ ] Shortest conversation (message count)
- [ ] Longest conversation (message count)
- [ ] Conversation length distribution
- [ ] Average user messages per session
- [ ] Average AI messages per session
- [ ] User/AI ratio per session

### Model Config Stats
- [ ] Sessions with modelConfig (count & %)
- [ ] Sessions by model:
  - [ ] claude-4.5-sonnet-thinking
  - [ ] claude-4-sonnet
  - [ ] claude-3.5-sonnet
  - [ ] (all other models)
- [ ] Sessions with maxMode=true (count & %)
- [ ] Sessions with maxMode=false (count & %)

### Usage Data Stats
- [ ] Sessions with usageData (count & %)
- [ ] (Specific usageData fields if available)

### Capabilities Stats
- [ ] Sessions with capabilities (count & %)
- [ ] Total capability invocations
- [ ] Unique capability types used
- [ ] Capability breakdown by type code

### Session Mode Stats
- [ ] Agent mode sessions (count & %)
- [ ] Chat mode sessions (count & %)
- [ ] Average lines added (agent mode)
- [ ] Average lines added (chat mode)
- [ ] Agent vs chat effectiveness comparison

### Session Naming Stats
- [ ] Named sessions (count & %)
- [ ] Unnamed sessions (count & %)
- [ ] Most common session name keywords
- [ ] Average session name length

---

## Data Source: codeBlockDiff (10,527 diffs)

### Basic Diff Counts
- [ ] Total code diffs
- [ ] Diffs per session (average)
- [ ] Diffs per session (median)
- [ ] Sessions with diffs (count & %)
- [ ] Sessions without diffs (count & %)

### Line Change Stats
- [ ] Total lines changed (sum of all diffs)
- [ ] Average lines changed per diff
- [ ] Median lines changed per diff
- [ ] Smallest diff (line count)
- [ ] Largest diff (line count)
- [ ] Lines changed distribution

### Diff Type Stats
- [ ] Diffs with newModelDiffWrtV0 (count)
- [ ] Diffs with originalModelDiffWrtV0 (count)
- [ ] Diffs with multiple versions (count)

### Position Stats
- [ ] Average start line number
- [ ] Average end line number
- [ ] Average line span (end - start)
- [ ] Diffs affecting multiple ranges (count)

### Content Stats
- [ ] Total characters in original content
- [ ] Total characters in modified content
- [ ] Net character change (modified - original)
- [ ] Average characters per diff
- [ ] Edit distance (Levenshtein) per diff
- [ ] Average similarity ratio (original vs modified)

---

## Data Source: aiCodeTracking.dailyStats (28 days)

### Daily Suggestion Stats
- [ ] Total days tracked
- [ ] Date range (earliest → latest)
- [ ] Total composer suggested lines (all days)
- [ ] Total composer accepted lines (all days)
- [ ] Total tab suggested lines (all days)
- [ ] Total tab accepted lines (all days)
- [ ] Combined suggested lines (composer + tab)
- [ ] Combined accepted lines (composer + tab)
- [ ] Average suggested lines per day (composer)
- [ ] Average accepted lines per day (composer)
- [ ] Average suggested lines per day (tab)
- [ ] Average accepted lines per day (tab)
- [ ] Peak suggestion day (composer)
- [ ] Peak acceptance day (composer)

### Daily Acceptance Rates
- [ ] Overall acceptance rate (composer)
- [ ] Overall acceptance rate (tab)
- [ ] Daily acceptance rates (timeline)
- [ ] Best acceptance day (% rate)
- [ ] Worst acceptance day (% rate)
- [ ] Acceptance rate trend (improving/declining)

### Composer vs Tab Comparison
- [ ] Composer suggested vs tab suggested (ratio)
- [ ] Composer accepted vs tab accepted (ratio)
- [ ] Composer acceptance rate vs tab acceptance rate
- [ ] Days with composer usage (count)
- [ ] Days with tab usage (count)
- [ ] Days with both (count)

### Daily Activity Patterns
- [ ] Active days (days with suggestions) (count)
- [ ] Inactive days (days without suggestions) (count)
- [ ] Average lines per active day
- [ ] Most productive day of week
- [ ] Least productive day of week

---

## Data Source: aiCodeTrackingLines (10,000 entries)

### Basic Tracking Stats
- [ ] Total tracked lines
- [ ] Lines by source:
  - [ ] composer
  - [ ] tab
  - [ ] (other sources)
- [ ] Composer lines (count & %)
- [ ] Tab lines (count & %)

### File Type Stats
- [ ] Unique file extensions
- [ ] Lines by file extension (breakdown)
- [ ] Most common file extension
- [ ] Lines per extension (average)

### File Stats
- [ ] Unique files modified
- [ ] Most frequently modified files (top 10)
- [ ] Lines per file (average)
- [ ] Files by composer (count)
- [ ] Files by tab (count)

### Composer/Session Stats
- [ ] Unique composer IDs in tracking
- [ ] Lines per composer ID (average)
- [ ] Most productive session (by tracked lines)

### Hash/Deduplication Stats
- [ ] Unique hashes
- [ ] Duplicate hashes (count)
- [ ] Deduplication rate

---

## Data Source: messageRequestContext (4,339 contexts)

### Request Context Counts
- [ ] Total request contexts
- [ ] Contexts per message (average)
- [ ] Messages with context (count & %)

### Attached Files Stats
- [ ] Contexts with attachedFileCodeChunksMetadataOnly (count & %)
- [ ] Total attached files (all contexts)
- [ ] Average attached files per context
- [ ] Unique files attached (deduplicated)

### Current File Stats
- [ ] Contexts with currentFileLocationData (count & %)
- [ ] Unique current files

### Project Layout Stats
- [ ] Contexts with projectLayouts (count & %)
- [ ] Total project layouts provided

### Rules & Knowledge Stats
- [ ] Contexts with cursorRules (count & %)
- [ ] Total cursor rules provided
- [ ] Contexts with knowledgeItems (count & %)
- [ ] Total knowledge items provided

### Diff Stats
- [ ] Contexts with diffsSinceLastApply (count & %)
- [ ] Total diffs in context

### Git Stats
- [ ] Contexts with gitStatusRaw (count & %)
- [ ] Git status types (if parseable)

### Terminal Stats
- [ ] Contexts with terminalFiles (count & %)
- [ ] Total terminal contexts provided

### Linting Stats
- [ ] Contexts with multiFileLinterErrors (count & %)
- [ ] Total linter errors in context

### Other Context Stats
- [ ] Contexts with attachedFoldersListDirResults (count & %)
- [ ] Contexts with summarizedComposers (count & %)
- [ ] Contexts with todos (count & %)

---

## Data Source: agentKv (17,962 entries)

### Basic Agent Stats
- [ ] Total agent KV entries
- [ ] Agent blob entries (agentKv:blob:*) (count)
- [ ] Agent checkpoint entries (agentKv:bubbleCheckpoint:*) (count)
- [ ] Standalone checkpoints (agentKv:checkpoint:*) (count)

### Agent Session Stats
- [ ] Unique agent sessions
- [ ] Agent entries per session (average)
- [ ] Sessions with agent state (count)

### Checkpoint Stats
- [ ] Total checkpoints
- [ ] Checkpoints per session (average)
- [ ] Sessions with checkpoints (count)

---

## Data Source: Workspace Databases (227 workspaces)

### Workspace Counts
- [ ] Total workspace databases
- [ ] Workspaces with data (count)
- [ ] Empty workspaces (count)
- [ ] Workspaces with composer data (count)
- [ ] Workspaces with notepad data (count)

### Workspace Session Stats
- [ ] Total sessions in workspaces (1,858)
- [ ] Average sessions per workspace
- [ ] Most active workspace (by session count)
- [ ] Workspace with most lines added

### Workspace Timeline Stats
- [ ] Earliest workspace session
- [ ] Latest workspace session
- [ ] Workspaces by creation date
- [ ] Active workspaces (with recent sessions)
- [ ] Inactive workspaces (no recent sessions)

---

## Data Source: File History (2,605 files)

### File History Counts
- [ ] Total files with history
- [ ] Files with edit history (count)
- [ ] Total edit entries (all files)

### Edit Stats
- [ ] Average edits per file
- [ ] Median edits per file
- [ ] File with most edits
- [ ] File with least edits
- [ ] Edits per day (timeline)
- [ ] Edits per file type

### File Timeline Stats
- [ ] Earliest file edit
- [ ] Latest file edit
- [ ] Most edited day (by edit count)
- [ ] Edit frequency trends

---

## Data Source: Terminal History

### Terminal Command Stats
- [ ] Total terminal commands (if available)
- [ ] Unique commands
- [ ] Most common commands
- [ ] Commands per day (timeline)

---

## Derived/Calculated Metrics

### Effectiveness Metrics

#### Prompt Effectiveness
- [ ] Acceptance rate by prompt length (bins)
- [ ] Acceptance rate by prompt specificity (has files/lines)
- [ ] Acceptance rate by prompt type (imperative vs question)
- [ ] Acceptance rate by prompt with examples vs without
- [ ] Best performing prompt patterns (top 10)
- [ ] Worst performing prompt patterns (bottom 10)

#### Context Impact
- [ ] Acceptance rate by context size (bins)
- [ ] Acceptance rate with vs without attachments
- [ ] Acceptance rate by number of attached files
- [ ] Acceptance rate with vs without codebase context
- [ ] Optimal context size (highest acceptance rate)

#### Tool Effectiveness
- [ ] Acceptance rate by tool used
- [ ] Acceptance rate by number of tools (0, 1, 2+)
- [ ] Best tool for acceptance rate
- [ ] Tool combinations effectiveness (pairwise analysis)

#### Thinking Impact
- [ ] Acceptance rate with vs without thinking
- [ ] Acceptance rate by thinking duration (bins)
- [ ] Optimal thinking duration range

#### Iteration Efficiency
- [ ] Iterations to acceptance (average)
- [ ] Success rate by iteration count (1st try, 2nd try, etc.)
- [ ] Sessions requiring multiple iterations (count & %)
- [ ] Rework rate (iterations > 1 / total sessions)

#### Code Quality
- [ ] Code retention rate (lines kept vs removed)
- [ ] Edit distance after acceptance (average)
- [ ] Quality score (1 - edit_distance/original_length)
- [ ] Human modifications per code block (average)

#### Model Effectiveness
- [ ] Acceptance rate by model (limited data)
- [ ] Lines generated by model (breakdown)
- [ ] Token efficiency by model (lines per 1000 tokens)

#### Conversation Patterns
- [ ] Acceptance rate by conversation length (bins)
- [ ] Acceptance rate by message pacing (rapid vs thoughtful)
- [ ] Success rate for short vs long conversations

### Productivity Metrics
- [ ] Lines of code per day (average)
- [ ] Lines of code per session (average)
- [ ] Sessions per day (average)
- [ ] Active coding days (%)
- [ ] Productivity trend (lines per day over time)
- [ ] Most productive hour of day
- [ ] Most productive day of week
- [ ] Productivity by month (comparison)

### Quality Metrics
- [ ] Overall acceptance rate
- [ ] Code retention rate (overall)
- [ ] Iteration rate (iterations per successful task)
- [ ] First-time success rate (sessions with 1 user message)
- [ ] Quality trend (acceptance rate over time)

### Usage Pattern Metrics
- [ ] Agent vs chat preference (% usage)
- [ ] Model switching frequency
- [ ] Context usage patterns (low, medium, high)
- [ ] Tool usage diversity (unique tools / total uses)
- [ ] Session length patterns (short, medium, long %)

### Efficiency Metrics
- [ ] Tokens per line of code (efficiency)
- [ ] Time per line of code (if timestamps available)
- [ ] Messages per line of code
- [ ] Tool invocations per successful line
- [ ] Context efficiency (lines per 1k context tokens)

### Comparison Metrics
- [ ] Agent mode vs chat mode (all metrics)
- [ ] With thinking vs without thinking (all metrics)
- [ ] With tools vs without tools (all metrics)
- [ ] High context vs low context (all metrics)
- [ ] Recent performance vs historical (trend)

### Timeline Metrics
- [ ] Daily active users (always 1 for personal)
- [ ] Weekly active periods
- [ ] Monthly growth in usage
- [ ] Usage consistency (variance in daily usage)
- [ ] Peak usage periods (identify)

### Correlation Metrics
- [ ] Context size ↔ acceptance rate (correlation)
- [ ] Message length ↔ code quality (correlation)
- [ ] Thinking time ↔ acceptance rate (correlation)
- [ ] Tool count ↔ success rate (correlation)
- [ ] Session length ↔ productivity (correlation)
- [ ] Time of day ↔ acceptance rate (correlation)

### Advanced Pattern Analysis
- [ ] Common prompt patterns (n-gram analysis)
- [ ] Successful prompt templates (extract patterns)
- [ ] Failed prompt patterns (anti-patterns)
- [ ] Conversation flow patterns (state machine)
- [ ] Tool usage sequences (common chains)
- [ ] Context evolution within sessions

### Anomaly Detection
- [ ] Outlier sessions (unusually high/low metrics)
- [ ] Anomalous days (spike/drop in activity)
- [ ] Unexpected patterns (statistical detection)

---

## Aggregation Levels

Each metric above can potentially be calculated at multiple aggregation levels:

### Time-based Aggregations
- [ ] Per hour
- [ ] Per day
- [ ] Per week
- [ ] Per month
- [ ] Per quarter
- [ ] Per year
- [ ] All time

### Session-based Aggregations
- [ ] Per session
- [ ] Per workspace
- [ ] Per mode (agent/chat)
- [ ] Per model

### Content-based Aggregations
- [ ] Per file type
- [ ] Per programming language
- [ ] Per project/workspace
- [ ] Per task type (if classifiable)

---

## Statistical Measures

For most numeric metrics, these statistical measures can be calculated:
- [ ] Count
- [ ] Sum/Total
- [ ] Mean/Average
- [ ] Median
- [ ] Mode
- [ ] Standard deviation
- [ ] Variance
- [ ] Min/Max
- [ ] Range
- [ ] Percentiles (25th, 50th, 75th, 90th, 95th, 99th)
- [ ] Quartiles (Q1, Q2, Q3)
- [ ] Interquartile range (IQR)
- [ ] Outliers (values beyond 1.5*IQR)

---

## Visualization Opportunities

- [ ] Timeline charts (any metric over time)
- [ ] Heatmaps (day x hour activity)
- [ ] Distribution histograms (any numeric metric)
- [ ] Pie charts (categorical breakdowns)
- [ ] Bar charts (comparisons)
- [ ] Scatter plots (correlation analysis)
- [ ] Box plots (statistical distribution)
- [ ] Line charts (trends)
- [ ] Stacked area charts (composition over time)
- [ ] Sankey diagrams (flow analysis)
- [ ] Word clouds (prompt keywords)
- [ ] Network graphs (tool usage chains)

---

## Export Formats

Each metric can be exported in:
- [ ] JSON (structured data)
- [ ] CSV (tabular data)
- [ ] Markdown (documentation)
- [ ] PDF (reports)
- [ ] Excel/XLSX (spreadsheet)
- [ ] SQL (database insert)

---

## Meta Stats

Stats about the stats:
- [ ] Total number of metrics calculable
- [ ] Metrics with full data coverage (%)
- [ ] Metrics with partial data coverage (%)
- [ ] Data completeness score
- [ ] Earliest data point (overall)
- [ ] Latest data point (overall)
- [ ] Total data span (days)
- [ ] Database size (bytes)
- [ ] Processing time (if timed)

---

## Total Metric Count

**Estimated total individual metrics: 600+**

This includes:
- ~200 direct extractions from data sources
- ~150 derived/calculated metrics
- ~100 effectiveness/comparison metrics
- ~100 statistical variations (mean, median, etc.)
- ~50 aggregation levels x metrics

**Note:** Many metrics can be calculated at multiple aggregation levels (hourly, daily, weekly, etc.) and with different groupings (by session, by workspace, by model, etc.), potentially yielding thousands of unique stat variations.

---

*This is a comprehensive catalog. Not all metrics may be immediately valuable, but they are all extractable from the available data.*

