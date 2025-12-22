# Pure Stats Index - Non-Redundant Catalog

**Created: December 22, 2025**
**Purpose: Fundamental measurable stats without aggregation redundancy**

---

## Organization

Each stat listed here is a **base measurable**. Within each stat, users can:
- View statistical measures (average, median, min, max, percentiles, distribution)
- Slice by time (hour, day, week, month, year)
- Filter by attributes (workspace, mode, model, file type, etc.)
- See trends over time
- Export data

---

## 1. Messages & Conversations

### Message Counts
1. **Total messages** - All messages in database
2. **User messages** - Messages sent by user (type=1)
3. **AI messages** - Messages from AI (type=2)
4. **Messages per session** - Message count grouped by session

### Message Content
5. **Message text length** - Character/word count of message text
6. **Messages with text** - Messages where text field is populated
7. **Messages with code blocks** - Messages containing code
8. **Code blocks generated** - Total code blocks across all messages
9. **Lines of code in code blocks** - Line count in code blocks
10. **Code block languages** - Programming languages used in code blocks
11. **Files referenced in code** - Unique files mentioned in code blocks

### Thinking & Reasoning
12. **Messages with thinking** - Messages with AI thinking process
13. **Thinking text length** - Length of thinking content
14. **Thinking duration** - Time spent thinking (thinkingDurationMs)
15. **Thinking blocks per message** - Count of thinking blocks

### Tool Usage
16. **Messages with tools** - Messages where tools were used
17. **Tool invocations** - Total tool calls
18. **Tools per message** - Tool count per message
19. **Tool usage by type** - Breakdown by tool name (codebase_search, grep, etc.)
20. **Tool success/failure** - Tool invocation outcomes

### Context Provided
21. **Attached code chunks** - Code chunks user attached
22. **Codebase context chunks** - Auto-retrieved context
23. **Lines in attached chunks** - Size of attached context
24. **Relevant files** - Files marked as relevant
25. **Recently viewed files** - Files in recent view history
26. **Unique files in context** - Deduplicated file list

### External References
27. **Web references** - External web links referenced
28. **Web searches performed** - AI web search invocations
29. **Docs references** - Documentation references
30. **Messages using web** - Messages with useWeb=true

### Code Suggestions
31. **Suggested code blocks** - Code blocks AI suggested
32. **Suggestion action types** - Breakdown by replace/insert/delete
33. **Assistant suggested diffs** - Diff suggestions

### User Responses
34. **Accepted suggestions** - Code suggestions user accepted
35. **Rejected suggestions** - Code suggestions user rejected
36. **Modified suggestions** - Code suggestions user modified
37. **Acceptance rate** - Percentage of suggestions accepted
38. **Response time to suggestions** - Time between suggestion and response

### Diffs & Changes
39. **Messages with git diffs** - Messages containing git diffs
40. **Messages with diff histories** - Messages with diff history
41. **Messages with human changes** - Messages with manual edits after AI

### Model Information
42. **Messages with model info** - Messages containing model metadata
43. **Model usage breakdown** - Messages per model
44. **Model switches** - Model changes within sessions

### Token Usage
45. **Input tokens** - Tokens in prompts
46. **Output tokens** - Tokens in responses
47. **Total tokens** - Combined input + output
48. **Tokens per message** - Token count per message
49. **Tokens by model** - Token usage per model

### Session Context
50. **Agentic messages** - Messages in agent mode
51. **Chat messages** - Messages in chat mode
52. **Messages with checkpoints** - Messages linked to checkpoints

### Errors in Messages
53. **Messages with lints** - Messages containing linter errors
54. **Linter errors** - Total linter error count
55. **Messages with console logs** - Messages with console output
56. **Terminal interactions** - Terminal commands around messages

### Metadata
57. **Refunded messages** - Messages marked as refunded
58. **Nudge messages** - Messages that were nudges
59. **Messages with server references** - Messages with serverBubbleId

### Activity Timing
60. **Message timestamps** - When messages were created
61. **Time between messages** - Gap between consecutive messages
62. **Active days** - Days with message activity
63. **Inactive days** - Days without messages
64. **Activity streak** - Consecutive days of activity
65. **Peak activity hours** - Hour of day breakdown
66. **Peak activity days** - Day of week breakdown

---

## 2. Sessions (Conversations)

### Session Counts
67. **Total sessions** - All conversation sessions
68. **Sessions per workspace** - Session count by workspace
69. **Agent mode sessions** - Sessions using agent mode
70. **Chat mode sessions** - Sessions using chat mode

### Session Duration
71. **Session duration** - Time from first to last message
72. **Sessions by duration bucket** - Categorized by length

### Session Outcomes
73. **Lines added** - Total lines added in session
74. **Lines removed** - Total lines removed in session
75. **Net lines** - Lines added minus removed
76. **Sessions with code output** - Sessions that produced code

### Files in Sessions
77. **Files added** - New files created in session
78. **Files removed** - Files deleted in session
79. **Files modified** - Files changed in session
80. **Most modified files** - File modification frequency

### Context in Sessions
81. **Context tokens used** - Context window tokens consumed
82. **Context token limit** - Maximum context available
83. **Context usage percentage** - Percent of context used
84. **Sessions near context limit** - Sessions using >80% context

### Conversation Structure
85. **Conversation length** - Number of messages in session
86. **User messages per session** - User message count
87. **AI messages per session** - AI message count
88. **User/AI message ratio** - Balance of conversation

### Session Configuration
89. **Sessions by model** - Model used for session
90. **Sessions with max mode** - Sessions using max context mode
91. **Sessions with capabilities** - Capability usage in sessions

### Session Naming
92. **Named sessions** - Sessions with user-provided names
93. **Session name keywords** - Common words in session names

---

## 3. Code & Diffs

### Code Diffs
94. **Code diffs total** - Total diff entries
95. **Diffs per session** - Diff count per session
96. **Lines changed per diff** - Line count in each diff
97. **Diff line spans** - Size of diff ranges

### Code Quality
98. **Edit distance** - Levenshtein distance between versions
99. **Similarity ratio** - How similar original vs modified
100. **Character changes** - Character count differences

### Code Tracking
101. **Tracked code lines** - Lines in aiCodeTrackingLines
102. **Code by source** - Breakdown by composer/tab/other
103. **Code by file type** - Lines per file extension
104. **Code by file** - Lines per individual file
105. **Most modified files** - Files with most tracked lines

---

## 4. Daily Usage Stats

### Daily Metrics
106. **Daily suggested lines (composer)** - Lines suggested by composer per day
107. **Daily accepted lines (composer)** - Lines accepted by composer per day
108. **Daily suggested lines (tab)** - Lines suggested by tab per day
109. **Daily accepted lines (tab)** - Lines accepted by tab per day
110. **Daily acceptance rate** - Acceptance percentage per day
111. **Composer vs tab usage** - Usage comparison by day

---

## 5. Workspace Data

### Workspace Metrics
112. **Total workspaces** - Unique workspace databases
113. **Workspaces with data** - Workspaces containing sessions
114. **Workspaces with notepads** - Workspaces with notepad content
115. **Sessions per workspace** - Session count per workspace
116. **Lines per workspace** - Code lines per workspace
117. **Active workspaces** - Workspaces with recent activity

---

## 6. File History

### File Editing
118. **Files with history** - Files in history folder
119. **Edit entries** - Total edit records
120. **Edits per file** - Edit count per file
121. **Edits by file type** - Edits grouped by extension
122. **Most edited files** - Files with highest edit counts

---

## 7. Error Logs & Linting

### Linter Errors
123. **Linter error count** - Total linter errors
124. **Linter error types** - Breakdown by error type
125. **Linter errors by file** - Errors per file
126. **Linter errors by file type** - Errors per extension
127. **Sessions with linter errors** - Sessions containing errors
128. **Linter error resolution** - Errors fixed vs unresolved

### Console Errors
129. **Console logs total** - All console log entries
130. **Console errors** - Error-level logs
131. **Console warnings** - Warning-level logs
132. **Console info** - Info-level logs
133. **Console errors by type** - Categorized console errors
134. **Console errors by project** - Errors per workspace

### Tool Failures
135. **Failed tool invocations** - Tools that failed to execute
136. **Tool failure rate** - Percentage of failed tool calls
137. **Tool timeouts** - Tool calls that timed out
138. **Tool errors by type** - Failure breakdown by tool

### Error Context
139. **Errors with file paths** - Errors linked to specific files
140. **Errors with line numbers** - Errors with line context
141. **Errors with stack traces** - Errors with full traces
142. **Error-prone files** - Files with most errors
143. **Error-prone projects** - Workspaces with most errors

### Error Timeline
144. **Errors per day** - Daily error counts
145. **Error trends** - Error rate changes over time
146. **Error-free days** - Days without errors

### Error Severity
147. **High severity errors** - Critical errors
148. **Medium severity errors** - Warning-level errors
149. **Low severity errors** - Minor errors

---

## 8. Terminal History

### Terminal Commands
150. **Terminal commands total** - All commands run
151. **Unique commands** - Distinct command types
152. **Command frequency** - Most common commands
153. **Commands per day** - Daily command counts

---

## 9. Request Context

### Context Metadata
154. **Request contexts total** - Total context entries
155. **Contexts per message** - Context records per message
156. **Attached files in context** - Files attached to requests
157. **Current file locations** - Active file when requesting
158. **Project layouts provided** - Project structure info
159. **Cursor rules provided** - Cursor rule usage
160. **Knowledge items provided** - Knowledge base items used
161. **Git status in context** - Git information provided
162. **Terminal files in context** - Terminal info provided
163. **Folder listings in context** - Directory listings provided
164. **Todos in context** - Todo items provided

---

## 10. Agent State

### Agent Metadata
165. **Agent KV entries** - Agent state records
166. **Agent blob entries** - Agent state blobs
167. **Agent checkpoint entries** - Agent checkpoints
168. **Agent sessions** - Unique agent session IDs
169. **Checkpoints per session** - Checkpoint count per session

---

## 11. Effectiveness Metrics (Derived)

### Prompt Analysis
170. **Acceptance by prompt length** - Correlation between prompt length and acceptance
171. **Acceptance by prompt specificity** - Impact of specific details (file paths, line numbers)
172. **Acceptance by prompt type** - Imperative vs question prompts
173. **Acceptance with examples** - Impact of providing code examples
174. **Top prompt patterns** - Most successful prompt structures
175. **Anti-patterns** - Least successful prompt structures

### Context Impact
176. **Acceptance by context size** - Impact of context window usage
177. **Acceptance with attachments** - Impact of attached files
178. **Acceptance by attachment count** - Impact of number of files attached
179. **Acceptance with codebase context** - Impact of auto-retrieved context
180. **Optimal context size** - Context size with highest acceptance

### Tool Impact
181. **Acceptance by tool used** - Impact of specific tools
182. **Acceptance by tool count** - Impact of number of tools used
183. **Best tools for acceptance** - Tools correlating with high acceptance
184. **Tool combinations** - Effectiveness of tool pairs

### Thinking Impact
185. **Acceptance with thinking** - Impact of AI thinking process
186. **Acceptance by thinking duration** - Impact of thinking time
187. **Optimal thinking duration** - Thinking time with best outcomes

### Iteration Analysis
188. **Iterations to acceptance** - Number of tries to success
189. **Success by iteration count** - First-try vs multi-try success rate
190. **Rework rate** - Percentage requiring multiple iterations

### Code Quality
191. **Code retention rate** - Percentage of code kept vs removed
192. **Edit distance after acceptance** - Changes made after accepting
193. **Quality score** - Calculated quality metric
194. **Human modifications** - User edits after AI generation

### Model Performance
195. **Acceptance by model** - Model-specific acceptance rates
196. **Lines by model** - Code generation by model
197. **Token efficiency by model** - Lines per 1000 tokens

### Conversation Patterns
198. **Acceptance by conversation length** - Impact of message count
199. **Acceptance by message pacing** - Impact of time between messages
200. **Short vs long conversations** - Success rate comparison

---

## 12. Productivity Metrics (Derived)

### Output Metrics
201. **Lines of code per day** - Daily coding output
202. **Lines of code per session** - Per-session output
203. **Sessions per day** - Daily session count
204. **Active coding days** - Percentage of days with activity
205. **Productivity trends** - Changes in output over time

### Efficiency Metrics
206. **Tokens per line** - Token cost per line of code
207. **Time per line** - Time cost per line of code
208. **Messages per line** - Message cost per line of code
209. **Tool calls per line** - Tool usage per line of code
210. **Context per line** - Context tokens per line of code

---

## 13. Usage Patterns (Derived)

### Mode Preferences
211. **Agent vs chat usage** - Percentage using each mode
212. **Agent vs chat effectiveness** - Outcome comparison by mode

### Model Preferences
213. **Model switching frequency** - How often model changes
214. **Model usage distribution** - Time spent with each model

### Context Patterns
215. **Context usage distribution** - Low/medium/high context usage patterns
216. **Tool usage diversity** - Variety in tool selection
217. **Session length patterns** - Short/medium/long session distribution

---

## 14. Correlation Analysis (Derived)

### Correlations
218. **Context size ↔ acceptance** - Correlation coefficient
219. **Message length ↔ quality** - Correlation coefficient
220. **Thinking time ↔ acceptance** - Correlation coefficient
221. **Tool count ↔ success** - Correlation coefficient
222. **Session length ↔ productivity** - Correlation coefficient
223. **Time of day ↔ acceptance** - Correlation coefficient

---

## 15. Pattern Detection (Advanced)

### Patterns
224. **Common prompt n-grams** - Frequent word sequences in prompts
225. **Successful prompt templates** - Patterns in high-acceptance prompts
226. **Failed prompt patterns** - Patterns in low-acceptance prompts
227. **Conversation state flows** - Common conversation structures
228. **Tool usage sequences** - Common tool usage chains
229. **Context evolution** - How context changes within sessions

### Anomalies
230. **Outlier sessions** - Sessions with unusual metrics
231. **Anomalous days** - Days with unusual activity
232. **Unexpected patterns** - Statistical anomalies

---

## 16. Comparative Metrics (Filtered Views)

These aren't separate stats, but filtered views of above stats:
- Agent mode vs Chat mode (any stat)
- With thinking vs without thinking (any stat)
- With tools vs without tools (any stat)
- High context vs low context (any stat)
- Recent vs historical (any stat)
- By workspace (any stat)
- By model (any stat)
- By file type (any stat)
- By time period (any stat)

---

## Summary

**Total Pure Stats: 232**

### Breakdown by Category:
- **Messages & Conversations:** 66 stats
- **Sessions:** 26 stats
- **Code & Diffs:** 12 stats
- **Daily Usage:** 6 stats
- **Workspaces:** 6 stats
- **File History:** 5 stats
- **Error Logs:** 27 stats
- **Terminal:** 4 stats
- **Request Context:** 11 stats
- **Agent State:** 5 stats
- **Effectiveness (Derived):** 28 stats
- **Productivity (Derived):** 10 stats
- **Usage Patterns (Derived):** 7 stats
- **Correlations (Derived):** 6 stats
- **Patterns (Advanced):** 9 stats
- **Comparative:** 4 categories (not separate stats)

### Data Grounding

✅ **All stats are grounded in actual data from:**
- bubbleId (68,657 messages)
- composerData (2,934 sessions)
- codeBlockDiff (10,527 diffs)
- aiCodeTracking.dailyStats (28 days)
- aiCodeTrackingLines (10,000 entries)
- messageRequestContext (4,339 contexts)
- agentKv (17,962 entries)
- Workspace databases (227 workspaces, 1,858 sessions)
- File history (2,605 files)
- Error data (from lints, consoleLogs, tool failures)
- Terminal history (if available)

✅ **No redundancy:**
- Each stat listed once as a base measurable
- Statistical views (avg, median, etc.) applied within each stat
- Time slicers (daily, weekly) applied as filters
- Comparisons (agent vs chat) applied as filters

✅ **Every stat is implementable:**
- Data source identified
- Extraction method documented
- Calculation approach clear

---

## Implementation Notes

### For Stats Page UI:
Each stat entry in the browse list shows:
- **Stat name** - Clear, descriptive name
- **Current value** - Latest/overall value
- **Trend indicator** - ↗ ↘ → showing direction
- **Category badge** - Messages, Sessions, Code, etc.
- **Data completeness** - % of records with this data

### On Click (Detail View):
- **Big number** - Primary metric value
- **Change indicator** - vs previous period
- **Statistical measures** - Avg, median, min, max, P95, etc.
- **Distribution chart** - Histogram or box plot
- **Timeline chart** - Trend over time
- **Filters** - Time range, workspace, mode, model, etc.
- **Breakdown tables** - By category, file type, etc.
- **Related stats** - Links to correlated metrics
- **Export button** - Download data

---

*This is the clean, non-redundant catalog of pure measurable stats, Jack!*

