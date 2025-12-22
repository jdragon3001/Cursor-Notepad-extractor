# UI/UX Design & Implementation Plan

**Created: December 22, 2025**
**Purpose: Complete design specification for the Cursor Data Extractor dashboard**

---

## Design Principles

1. **Clean & Minimal** - No clutter, focus on one thing at a time
2. **Progressive Disclosure** - Start broad, drill down to details
3. **Consistent Navigation** - Same filters/controls across all pages
4. **Fast & Responsive** - Cached data, instant updates
5. **Mobile-Friendly** - Responsive layouts (though desktop-first)

---

## Page Structure

```
┌─────────────────────────────────────────────────┐
│  🎯 Cursor Data Extractor                       │  ← Header (always visible)
│  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ │
│  [Overview] [Stats] [Analytics] [Calendar] [Intel] [Export]
│                                                 │
│  📅 Dec 2024 - Dec 2025  |  🔍 All Workspaces  │  ← Global filters
│  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ │
│                                                 │
│          [Page Content Here]                    │
│                                                 │
└─────────────────────────────────────────────────┘
```

### Navigation Tabs
1. **Overview** - Dashboard with key metrics
2. **Browse** - Search & filter conversations/messages/logs
3. **Stats** - Searchable stat catalog
4. **Analytics** - Year Wrapped style insights
5. **Calendar** - Timeline view with drill-down
6. **Intelligence** - Actionable insights (future)
7. **Export** - Data export options

---

## Global Controls (Persistent Across All Pages)

```
┌──────────────────────────────────────────────────────────┐
│  Date Range: [Dec 2024 - Dec 2025]  ▼                   │
│              [Custom Range] [All Time]                    │
│                                                           │
│  Workspace:  [All Workspaces]  ▼                         │
│              [Project A] [Project B] [Project C]...       │
│                                                           │
│  Time View:  [○ Day] [○ Week] [● Month] [○ Year]         │
│                                                           │
│  Mode:       [☑ Agent] [☑ Chat]                          │
└──────────────────────────────────────────────────────────┘
```

**Implementation:** Streamlit sidebar with:
- Date range selector (date_input)
- Workspace multi-select
- Time granularity radio buttons
- Mode checkboxes

---

## Page 1: Overview (Dashboard)

**Purpose:** High-level summary, entry point to deeper views

### Layout

```
┌───────────────────────────────────────────────────────┐
│  📊 Overview                                          │
│  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ │
│                                                       │
│  Key Metrics (Cards)                                  │
│  ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌─────────┐ │
│  │ 2,934    │ │ 68,657   │ │ 429,700  │ │  48.7%  │ │
│  │ Sessions │ │ Messages │ │ Lines    │ │ Accept  │ │
│  └──────────┘ └──────────┘ └──────────┘ └─────────┘ │
│                                                       │
│  Recent Activity (Last 30 Days)                       │
│  ┌───────────────────────────────────────────────┐   │
│  │                                               │   │
│  │  [Activity Line Chart]                        │   │
│  │   ╱╲    ╱╲                                    │   │
│  │  ╱  ╲  ╱  ╲╱╲  ╱                              │   │
│  │ ╱    ╲╱      ╲╱                               │   │
│  └───────────────────────────────────────────────┘   │
│     Click chart → Jump to Calendar view               │
│                                                       │
│  Quick Insights (Top 3)                               │
│  ┌───────────────────────────────────────────────┐   │
│  │ 💡 Most productive: Tuesdays (avg 8,500 lines)│   │
│  │ 🎯 Best acceptance: Prompts with examples 62% │   │
│  │ 🔥 Current streak: 14 days active             │   │
│  └───────────────────────────────────────────────┘   │
│                                                       │
│  Most Active Projects                                 │
│  1. Project Alpha      2,500 lines  ████████░░        │
│  2. Project Beta       1,200 lines  ████░░░░░░        │
│  3. Project Gamma        800 lines  ███░░░░░░░        │
│                                                       │
└───────────────────────────────────────────────────────┘
```

### Interactions
- **Click metric card** → Jump to relevant Stats page section
- **Click chart** → Jump to Calendar view at that date
- **Click insight** → Jump to Analytics page with details
- **Click project** → Filter entire dashboard to that workspace

### Components
- `st.metric()` for key metrics with deltas
- `st.plotly_chart()` for activity chart
- `st.info()` for insights
- `st.progress()` for project bars

---

## Page 2: Browse (Search & Filter Conversations)

**Purpose:** Comprehensive search through all conversations, messages, and error logs

### Layout

```
┌───────────────────────────────────────────────────────┐
│  🔍 Browse                                            │
│  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ │
│                                                       │
│  [🔍 Search conversations, messages, errors...    ]  │
│                                                       │
│  View: [Conversations] [Messages] [Error Logs]        │
│                                                       │
│  ┌─────────────────────────────────────────────────┐ │
│  │ Filters                              [Clear All] │ │
│  │                                                  │ │
│  │ Content Type:                                    │ │
│  │ ☑ User messages    ☑ AI responses               │ │
│  │ ☑ With code        ☑ With thinking               │ │
│  │ ☑ With files       ☑ With tools                  │ │
│  │                                                   │ │
│  │ Mode: [☑ Agent] [☑ Chat]                         │ │
│  │                                                   │ │
│  │ Has: [Files ▼] [Code ▼] [Errors ▼] [Tools ▼]    │ │
│  │                                                   │ │
│  │ Sort: [Newest ▼] [Oldest] [Most relevant]       │ │
│  └─────────────────────────────────────────────────┘ │
│                                                       │
│  Results: 245 conversations                           │
│  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ │
│                                                       │
│  ┌─────────────────────────────────────────────────┐ │
│  │ 🤖 Build authentication system               [→] │ │
│  │ Dec 22, 2025 • 9:30 AM • Project Alpha           │ │
│  │ 14 messages • 240 lines • 3 files • Agent mode   │ │
│  │                                                   │ │
│  │ "build a login system with JWT auth..."         │ │
│  │ 📎 auth.ts, login.tsx, types.ts                  │ │
│  │ 🔧 codebase_search, read_file                    │ │
│  └─────────────────────────────────────────────────┘ │
│                                                       │
│  ┌─────────────────────────────────────────────────┐ │
│  │ 💬 Fix navigation bug                        [→] │ │
│  │ Dec 22, 2025 • 2:15 PM • Project Beta            │ │
│  │ 8 messages • 80 lines • 1 file • Chat mode       │ │
│  │                                                   │ │
│  │ "the navigation is broken when..."              │ │
│  │ 📎 Nav.tsx                                       │ │
│  └─────────────────────────────────────────────────┘ │
│                                                       │
│  [Load more...] (245 total)                          │
│                                                       │
└───────────────────────────────────────────────────────┘
```

### View: Conversations (Default)

Shows all sessions/conversations with:
- Session name (if available) or first message preview
- Timestamp and project
- Quick stats (messages, lines, files)
- Mode indicator (Agent/Chat)
- Preview of first message
- Attached files list
- Tools used

**Interaction:**
- Click conversation → Open session detail view (same as Calendar drill-down)
- Hover → Show quick preview tooltip
- Right-click → Context menu (Export, Copy link, Mark favorite)

### View: Messages

```
┌───────────────────────────────────────────────────────┐
│  View: [Conversations] [● Messages] [Error Logs]      │
│  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ │
│                                                       │
│  Results: 68,657 messages                             │
│  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ │
│                                                       │
│  ┌─────────────────────────────────────────────────┐ │
│  │ 👤 USER • Dec 22, 9:30 AM • Project Alpha   [→] │ │
│  │ Build authentication system                      │ │
│  │                                                   │ │
│  │ "build a login system with JWT auth and         │ │
│  │  password reset functionality. use bcrypt..."    │ │
│  │                                                   │ │
│  │ 📎 No attachments                                │ │
│  │ Session: Build authentication system            │ │
│  └─────────────────────────────────────────────────┘ │
│                                                       │
│  ┌─────────────────────────────────────────────────┐ │
│  │ 🤖 AI • Dec 22, 9:30 AM • Project Alpha      [→] │ │
│  │ Response with code                               │ │
│  │                                                   │ │
│  │ "I'll help you build a secure JWT               │ │
│  │  authentication system..."                       │ │
│  │                                                   │ │
│  │ 💭 Thinking (12.3s) • 📝 3 code blocks           │ │
│  │ 📎 auth.ts (+180), login.tsx (+50), types.ts    │ │
│  │ 🔧 codebase_search, read_file                    │ │
│  │ ✅ Accepted 240 lines                            │ │
│  │ Session: Build authentication system            │ │
│  └─────────────────────────────────────────────────┘ │
│                                                       │
│  ┌─────────────────────────────────────────────────┐ │
│  │ 👤 USER • Dec 22, 9:35 AM • Project Alpha   [→] │ │
│  │ Follow-up question                               │ │
│  │                                                   │ │
│  │ "add password reset functionality with email    │ │
│  │  verification"                                    │ │
│  │                                                   │ │
│  │ Session: Build authentication system            │ │
│  └─────────────────────────────────────────────────┘ │
│                                                       │
│  [Load more...] (68,657 total)                       │
│                                                       │
└───────────────────────────────────────────────────────┘
```

**Shows individual messages with:**
- User/AI indicator
- Timestamp and project
- Message text (truncated with "Read more")
- Code blocks count
- Thinking indicator
- Files attached/modified
- Tools used
- Acceptance status (for AI messages)
- Parent session link

**Interaction:**
- Click message → Open message detail modal
- Click session link → Jump to session in calendar
- Hover → Preview full text

### View: Error Logs

```
┌───────────────────────────────────────────────────────┐
│  View: [Conversations] [Messages] [● Error Logs]      │
│  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ │
│                                                       │
│  [🔍 Search error messages, stack traces...       ]  │
│                                                       │
│  ┌─────────────────────────────────────────────────┐ │
│  │ Error Type:                                      │ │
│  │ ☑ Linter errors    ☑ Runtime errors              │ │
│  │ ☑ Console errors   ☑ Tool failures               │ │
│  │                                                   │ │
│  │ Severity: [☑ High] [☑ Medium] [☑ Low]           │ │
│  └─────────────────────────────────────────────────┘ │
│                                                       │
│  Results: 1,247 errors                                │
│  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ │
│                                                       │
│  ┌─────────────────────────────────────────────────┐ │
│  │ 🔴 TypeScript Error • Dec 22, 10:15 AM      [→] │ │
│  │ Project Alpha • Session: Build auth system       │ │
│  │                                                   │ │
│  │ auth.ts:45:12                                    │ │
│  │ Type 'string | undefined' is not assignable to  │ │
│  │ type 'string'                                    │ │
│  │                                                   │ │
│  │ [View in context] [View file]                   │ │
│  └─────────────────────────────────────────────────┘ │
│                                                       │
│  ┌─────────────────────────────────────────────────┐ │
│  │ ⚠️ Linter Warning • Dec 22, 11:20 AM        [→] │ │
│  │ Project Beta • Session: Fix navigation           │ │
│  │                                                   │ │
│  │ Nav.tsx:23:5                                     │ │
│  │ React Hook useEffect has a missing dependency   │ │
│  │                                                   │ │
│  │ [View in context] [View file]                   │ │
│  └─────────────────────────────────────────────────┘ │
│                                                       │
│  ┌─────────────────────────────────────────────────┐ │
│  │ 🔧 Tool Failure • Dec 22, 3:45 PM           [→] │ │
│  │ Project Gamma • Session: Database migration      │ │
│  │                                                   │ │
│  │ codebase_search failed: timeout after 30s       │ │
│  │                                                   │ │
│  │ [View tool call] [View session]                 │ │
│  └─────────────────────────────────────────────────┘ │
│                                                       │
│  [Load more...] (1,247 total)                        │
│                                                       │
└───────────────────────────────────────────────────────┘
```

**Error types tracked:**
1. **Linter errors** (from `lints`, `approximateLintErrors`, `multiFileLinterErrors`)
2. **Console errors** (from `consoleLogs`)
3. **Tool failures** (from `toolResults` with errors)
4. **Runtime errors** (if logged in messages)

**Shows:**
- Error severity/type
- Timestamp and project
- File and line number (if available)
- Error message
- Stack trace (expandable)
- Parent session
- Actions (view in context, view file)

### Advanced Search & Filters

```
┌──────────────────────────────────────────────────────┐
│  Advanced Search                         [✕ Close]   │
│  ──────────────────────────────────────────────────  │
│                                                       │
│  Keyword Search:                                      │
│  [authentication                                   ]  │
│  Match: [● Exact phrase] [○ Any word] [○ All words]  │
│                                                       │
│  Content Filters:                                     │
│  Message Type:                                        │
│  [● All] [○ User only] [○ AI only]                   │
│                                                       │
│  Has Content:                                         │
│  ☑ Text          ☑ Code blocks    ☑ Thinking         │
│  ☑ Tool results  ☑ Attachments    ☐ Web refs         │
│                                                       │
│  Code Filters:                                        │
│  Language: [Any ▼] [TypeScript] [Python] [Go]...     │
│  Has diffs: [☑] Min lines: [50  ]                    │
│                                                       │
│  File Filters:                                        │
│  With attachments: [☑]                                │
│  File extension: [.ts  ] [.tsx  ] [.py  ]            │
│  File path contains: [auth                        ]   │
│                                                       │
│  Tool Filters:                                        │
│  Used tools: [codebase_search ▼] [+ Add]             │
│  Tool count: Min [1  ] Max [5  ]                     │
│                                                       │
│  Acceptance Filters:                                  │
│  [☑ Accepted] [☑ Rejected] [☑ Modified] [☑ Unknown] │
│  Acceptance rate: Min [50 %]                         │
│                                                       │
│  Model Filters:                                       │
│  Model: [Any ▼] [claude-4.5] [claude-4] [gpt-4]      │
│                                                       │
│  Token Filters:                                       │
│  Input tokens: Min [    ] Max [50000]                │
│  Output tokens: Min [    ] Max [10000]               │
│                                                       │
│  Error Filters:                                       │
│  Has errors: [☑]                                      │
│  Error type: [Linter ▼] [+ Add]                      │
│                                                       │
│  Metrics Filters:                                     │
│  Message length: Min [    ] Max [1000 ] words        │
│  Lines added: Min [    ] Max [    ]                  │
│  Session length: Min [5   ] Max [    ] messages      │
│                                                       │
│  [Apply Filters] [Reset] [Save as Preset]            │
│                                                       │
└──────────────────────────────────────────────────────┘
```

### Filter Presets

Quick access to common filter combinations:
- **My questions** - User messages only
- **Code generations** - AI messages with code blocks
- **With thinking** - Messages with AI reasoning
- **Tool-heavy sessions** - Sessions using 3+ tools
- **High acceptance** - Sessions with >70% acceptance
- **Error-prone** - Sessions with errors
- **Recent activity** - Last 7 days
- **Long sessions** - 10+ messages
- **File-heavy** - 5+ files attached/modified

### Search Syntax

```
# Basic search
authentication

# Phrase search
"JWT authentication"

# Boolean operators
JWT AND authentication
(JWT OR OAuth) AND security

# Field-specific search
user:"build a login"
ai:"I'll help you"
file:auth.ts
tool:codebase_search
error:"Type 'string'"

# Wildcards
auth*
*.tsx

# Exclusions
authentication -OAuth
```

### Bulk Actions

Select multiple items and:
- **Export** selected conversations/messages
- **Mark** as favorite/reviewed
- **Tag** with custom labels
- **Compare** side by side
- **Delete** from view (soft delete)

### Implementation

```python
# Search engine
from whoosh import index, fields, qparser

# Create search index
schema = fields.Schema(
    id=fields.ID(stored=True),
    type=fields.ID(stored=True),  # conversation, message, error
    content=fields.TEXT(stored=True),
    timestamp=fields.DATETIME(stored=True),
    project=fields.TEXT(stored=True),
    has_code=fields.BOOLEAN(stored=True),
    has_thinking=fields.BOOLEAN(stored=True),
    has_files=fields.BOOLEAN(stored=True),
    tools=fields.KEYWORD(stored=True, commas=True),
    files=fields.KEYWORD(stored=True, commas=True),
    # ... more fields
)

ix = index.create_in("indexdir", schema)

# Index all data
writer = ix.writer()
for msg in messages:
    writer.add_document(
        id=msg.id,
        type='message',
        content=msg.text,
        timestamp=msg.created_at,
        # ... more fields
    )
writer.commit()

# Search
searcher = ix.searcher()
query = qparser.QueryParser("content", ix.schema).parse("authentication")
results = searcher.search(query)

# Streamlit UI
search_query = st.text_input("Search", key="browse_search")
view_type = st.radio("View", ["Conversations", "Messages", "Error Logs"])

# Apply filters
filtered_results = apply_filters(results, st.session_state.filters)

# Display results
for result in filtered_results:
    with st.container():
        st.markdown(f"### {result.title}")
        st.caption(f"{result.timestamp} • {result.project}")
        st.text(result.preview)
        if st.button("View details", key=result.id):
            show_detail_modal(result)
```

---

## Page 3: Stats (Searchable Catalog)

**Purpose:** Find any specific stat, browsable index

### Layout

```
┌───────────────────────────────────────────────────────┐
│  📈 Stats Catalog                                     │
│  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ │
│                                                       │
│  [🔍 Search stats...                    ]             │
│  [Category: All ▼] [Source: All ▼] [Type: All ▼]     │
│                                                       │
│  ┌─────────────────────────────────────────────────┐ │
│  │ 📊 Messages                              [Expand]│ │
│  │ ────────────────────────────────────────────────│ │
│  │                                                  │ │
│  │ Total messages              68,657         ↗     │ │
│  │ User messages                3,970 (5.8%)  ↗     │ │
│  │ AI messages                 64,681 (94.2%) ↗     │ │
│  │ Messages with code           9,610 (14%)   ↗     │ │
│  │ Messages with thinking      21,970 (32%)   ↗     │ │
│  │                                                  │ │
│  │ [Show More...]                                   │ │
│  └─────────────────────────────────────────────────┘ │
│                                                       │
│  ┌─────────────────────────────────────────────────┐ │
│  │ 📝 Sessions                              [Expand]│ │
│  │ ────────────────────────────────────────────────│ │
│  │                                                  │ │
│  │ Total sessions               2,934          ↗     │ │
│  │ Agent mode                   1,850 (63%)    ↗     │ │
│  │ Chat mode                    1,084 (37%)    ↗     │ │
│  │ Avg lines per session          146          ↗     │ │
│  │                                                  │ │
│  └─────────────────────────────────────────────────┘ │
│                                                       │
│  [Continue browsing all categories...]               │
│                                                       │
└───────────────────────────────────────────────────────┘
```

### Interactions
- **Search** → Real-time filter stats by name/keyword
- **Category dropdown** → Filter by category (Messages, Sessions, Code, etc.)
- **Click stat name** → Drill-down modal with:
  - Full value
  - Chart/visualization
  - Trend over time
  - Comparison to average
  - Related stats
- **Click ↗ icon** → Quick chart overlay
- **Expand/Collapse** → Show/hide category sections

### Categories
1. Messages (counts, content, types)
2. Sessions (durations, modes, acceptance)
3. Code (lines, files, diffs)
4. Context (tokens, attachments, files)
5. Tools (usage, effectiveness)
6. Models (usage, performance)
7. Effectiveness (acceptance, quality, iterations)
8. Timeline (daily, weekly, monthly trends)

### Implementation
- `st.text_input()` for search
- `st.selectbox()` for filters
- `st.expander()` for categories
- Custom component for stat rows with click handlers
- Modal: `st.dialog()` or custom HTML/JS

---

## Page 4: Analytics (Year Wrapped Style)

**Purpose:** Beautiful insights, shareable visualizations

### Layout (Scrollable Story Format)

```
┌───────────────────────────────────────────────────────┐
│  🎯 Your Cursor Analytics                             │
│  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ │
│                                                       │
│  ╔═══════════════════════════════════════════════╗   │
│  ║                                               ║   │
│  ║         Your Coding Journey                   ║   │
│  ║                                               ║   │
│  ║         402 days of building                  ║   │
│  ║         Nov 2024 → Dec 2025                   ║   │
│  ║                                               ║   │
│  ╚═══════════════════════════════════════════════╝   │
│                                                       │
│  ───────────────────────────────────────────────────  │
│                                                       │
│  ╔═══════════════════════════════════════════════╗   │
│  ║  You had 2,934 conversations with Cursor     ║   │
│  ║                                               ║   │
│  ║  That's an average of 7.3 sessions per day   ║   │
│  ║                                               ║   │
│  ║  [Session Timeline Visualization]            ║   │
│  ╚═══════════════════════════════════════════════╝   │
│                                                       │
│  ───────────────────────────────────────────────────  │
│                                                       │
│  ╔═══════════════════════════════════════════════╗   │
│  ║  You wrote 429,700 lines of code              ║   │
│  ║  with Cursor's help                           ║   │
│  ║                                               ║   │
│  ║  That's enough to fill 2,865 pages           ║   │
│  ║                                               ║   │
│  ║  [Code Volume Visualization]                 ║   │
│  ╚═══════════════════════════════════════════════╝   │
│                                                       │
│  [Scroll to continue...]                              │
│                                                       │
└───────────────────────────────────────────────────────┘
```

### Analytics Sections (Cards)

1. **Journey Overview**
   - Total days active
   - Date range
   - Total sessions

2. **Volume Metrics**
   - Total lines
   - Total messages
   - Fun comparisons (e.g., "That's 2,865 pages!")

3. **Acceptance Story**
   - Overall acceptance rate
   - Best performing prompts
   - Quality metrics

4. **Tool Mastery**
   - Most used tools
   - Tool combinations
   - Effectiveness by tool

5. **Thinking Deep Dive**
   - Time spent thinking
   - Thinking impact on quality
   - Longest thinking session

6. **Your Patterns**
   - Most productive time
   - Peak day
   - Longest streak

7. **Model Usage**
   - Models used
   - Lines per model
   - (With "limited data" disclaimer)

8. **Effectiveness Insights**
   - What works best
   - Prompt patterns
   - Context sweet spot

9. **Project Spotlight**
   - Most active project
   - Total projects
   - Project breakdown

10. **Looking Forward**
    - Trends
    - Recommendations
    - Next steps

### Interactions
- **Scroll** → Reveal cards with animations
- **Click card** → Expand for more details
- **Click visualization** → Drill into Calendar or Stats
- **Share button** → Export as PDF or image

### Implementation
- `st.container()` for each card
- CSS animations for reveal on scroll
- `st.plotly_chart()` for visualizations
- Big, bold numbers with `st.markdown()`
- Smooth scrolling with anchor links

---

## Page 5: Calendar (Timeline with Drill-Down)

**Purpose:** Explore data by date, drill into specifics

### Layout

```
┌───────────────────────────────────────────────────────┐
│  📅 Calendar View                                     │
│  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ │
│                                                       │
│  View: [○ Day] [○ Week] [● Month] [○ Year]           │
│  Metric: [Lines Added ▼]                             │
│                                                       │
│  December 2025                        [← Dec | Jan →] │
│  ┌─────────────────────────────────────────────────┐ │
│  │ Mon  Tue  Wed  Thu  Fri  Sat  Sun              │ │
│  │                               1    2            │ │
│  │  3    4    5    6    7    8    9               │ │
│  │ ███  ████  ██  ████  ███  ░░   ░░              │ │
│  │                                                 │ │
│  │ 10   11   12   13   14   15   16               │ │
│  │ ████ ████  ███  ██  ████  ██   ░░              │ │
│  │                                                 │ │
│  │ 17   18   19   20   21   22   23               │ │
│  │ ███  ████ ████  ███ ████ ████  ░░              │ │
│  │                      ⬆ You are here            │ │
│  │ 24   25   26   27   28   29   30               │ │
│  │ ░░   ░░   ░░   ░░   ░░   ░░   ░░               │ │
│  └─────────────────────────────────────────────────┘ │
│                                                       │
│  Heat: ░░ None  ██ Low  ███ Medium  ████ High        │
│                                                       │
│  Selected: December 22, 2025                          │
│  ┌─────────────────────────────────────────────────┐ │
│  │ 6 sessions  •  1,240 lines  •  32 messages      │ │
│  │                                                  │ │
│  │ Sessions:                                        │ │
│  │ ┌────────────────────────────────────┐          │ │
│  │ │ 🤖 Build authentication system  →  │          │ │
│  │ │    9:30 AM • 14 messages • 240 lines│         │ │
│  │ └────────────────────────────────────┘          │ │
│  │ ┌────────────────────────────────────┐          │ │
│  │ │ 💬 Fix navigation bug            →  │          │ │
│  │ │    2:15 PM • 8 messages • 80 lines  │         │ │
│  │ └────────────────────────────────────┘          │ │
│  │ [Show all 6 sessions...]                         │ │
│  └─────────────────────────────────────────────────┘ │
│                                                       │
└───────────────────────────────────────────────────────┘
```

### Interactions

**Calendar Level:**
- **Hover day** → Tooltip with quick stats
- **Click day** → Show day details below calendar
- **Click month arrow** → Navigate months
- **Change view** → Switch between Day/Week/Month/Year
- **Change metric** → Recolor heatmap (lines, messages, tokens, etc.)

**Day Details:**
- **Click session card** → Drill into session view

**Session View (Modal/Slide-in):**
```
┌───────────────────────────────────────────────────────┐
│  🤖 Build authentication system                       │
│  December 22, 2025 • 9:30 AM                          │
│  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ │
│                                                       │
│  Metrics:                                             │
│  14 messages  •  240 lines added  •  12 lines removed│
│  3 files modified  •  2 tools used  •  85% accepted  │
│                                                       │
│  Conversation:                                        │
│  ┌─────────────────────────────────────────────────┐ │
│  │ 👤 "build a login system with JWT auth"        │ │
│  │    9:30:15 AM                                    │ │
│  └─────────────────────────────────────────────────┘ │
│                                                       │
│  ┌─────────────────────────────────────────────────┐ │
│  │ 🤖 "I'll help you build a secure JWT..."       │ │
│  │    [Show thinking ▼]                             │ │
│  │    [Code blocks: auth.ts, login.tsx] [Show ▼]   │ │
│  │    9:30:45 AM • claude-4.5-sonnet-thinking       │ │
│  └─────────────────────────────────────────────────┘ │
│                                                       │
│  │ ✅ You accepted 240 lines                        │ │
│                                                       │
│  ┌─────────────────────────────────────────────────┐ │
│  │ 👤 "add password reset functionality"          │ │
│  │    9:35:20 AM                                    │ │
│  └─────────────────────────────────────────────────┘ │
│                                                       │
│  [Continue conversation thread...]                    │
│                                                       │
│  Tools Used:                                          │
│  • codebase_search (2x) • read_file (3x)             │
│                                                       │
│  Files Modified:                                      │
│  • src/auth/auth.ts (+180 lines)                     │
│  • src/components/Login.tsx (+50 lines)              │
│  • src/types.ts (+10 lines)                          │
│                                                       │
└───────────────────────────────────────────────────────┘
```

**Message View (Click individual message):**
- Full message text
- Code blocks (syntax highlighted)
- Thinking process (expandable)
- Tool results (expandable)
- Context provided
- Timestamps
- Acceptance actions

### Implementation
- Custom calendar component or `streamlit-calendar`
- Heatmap coloring with matplotlib/plotly
- `st.expander()` for messages
- Syntax highlighting with `st.code()`
- Lazy loading for conversation (performance)

---

## Page 6: Intelligence (Actionable Insights)

**Purpose:** AI-powered recommendations, patterns, improvements

### Layout (Future State)

```
┌───────────────────────────────────────────────────────┐
│  🧠 Intelligence                                      │
│  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ │
│                                                       │
│  Actionable Insights                                  │
│                                                       │
│  ┌─────────────────────────────────────────────────┐ │
│  │ 💡 Prompt Optimization                           │ │
│  │                                                  │ │
│  │ Your acceptance rate increases by 15% when you: │ │
│  │ • Include specific file paths                   │ │
│  │ • Provide code examples                         │ │
│  │ • Keep prompts under 200 words                  │ │
│  │                                                  │ │
│  │ [See examples] [Copy template]                  │ │
│  └─────────────────────────────────────────────────┘ │
│                                                       │
│  ┌─────────────────────────────────────────────────┐ │
│  │ 🎯 Peak Performance Times                        │ │
│  │                                                  │ │
│  │ You're most effective on Tuesdays 9-11 AM      │ │
│  │ Acceptance rate: 62% (vs 48% average)          │ │
│  │                                                  │ │
│  │ [Schedule focus time] [See pattern]            │ │
│  └─────────────────────────────────────────────────┘ │
│                                                       │
│  ┌─────────────────────────────────────────────────┐ │
│  │ 🔧 Tool Usage Recommendations                    │ │
│  │                                                  │ │
│  │ Sessions using codebase_search + grep have:    │ │
│  │ • 22% higher acceptance                         │ │
│  │ • 30% fewer iterations                          │ │
│  │                                                  │ │
│  │ [Learn tool combinations]                       │ │
│  └─────────────────────────────────────────────────┘ │
│                                                       │
│  Detected Patterns                                    │
│                                                       │
│  ┌─────────────────────────────────────────────────┐ │
│  │ 📊 Context Sweet Spot: 30-50k tokens            │ │
│  │ 🔁 Iteration Pattern: 73% succeed in 1-2 tries │ │
│  │ 🚀 Productivity Trend: ↗ +12% this month        │ │
│  └─────────────────────────────────────────────────┘ │
│                                                       │
└───────────────────────────────────────────────────────┘
```

### Current State (MVP)

```
┌───────────────────────────────────────────────────────┐
│  🧠 Intelligence                                      │
│  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ │
│                                                       │
│  ┌─────────────────────────────────────────────────┐ │
│  │         🚧 Coming Soon                           │ │
│  │                                                  │ │
│  │  AI-powered insights and recommendations        │ │
│  │  will appear here once we have enough data      │ │
│  │  patterns to analyze.                           │ │
│  │                                                  │ │
│  │  For now, explore:                              │ │
│  │  • Analytics for effectiveness patterns         │ │
│  │  • Stats for detailed metrics                   │ │
│  │  • Calendar for timeline insights               │ │
│  │                                                  │ │
│  └─────────────────────────────────────────────────┘ │
│                                                       │
└───────────────────────────────────────────────────────┘
```

### Implementation (Future)
- Pattern detection algorithms
- Correlation analysis
- Recommendation engine
- Template generation
- Export recommendations

---

## Page 7: Export

**Purpose:** Export data and reports

### Layout

```
┌───────────────────────────────────────────────────────┐
│  📥 Export                                            │
│  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ │
│                                                       │
│  Export Options                                       │
│                                                       │
│  ┌─────────────────────────────────────────────────┐ │
│  │ 📊 Analytics Report (PDF)                        │ │
│  │                                                  │ │
│  │ Beautiful year-wrapped style report             │ │
│  │ ☑ Include visualizations                        │ │
│  │ ☑ Include insights                              │ │
│  │ ☐ Anonymize data                                │ │
│  │                                                  │ │
│  │ [Generate PDF]                                  │ │
│  └─────────────────────────────────────────────────┘ │
│                                                       │
│  ┌─────────────────────────────────────────────────┐ │
│  │ 📁 Raw Data (JSON/CSV)                           │ │
│  │                                                  │ │
│  │ Export raw data for external analysis           │ │
│  │ Format: [JSON ▼] [CSV] [Excel]                  │ │
│  │                                                  │ │
│  │ Include:                                         │ │
│  │ ☑ Messages   ☑ Sessions   ☑ Code diffs         │ │
│  │ ☑ Daily stats ☑ Metrics   ☐ Raw blobs          │ │
│  │                                                  │ │
│  │ [Download Data]                                 │ │
│  └─────────────────────────────────────────────────┘ │
│                                                       │
│  ┌─────────────────────────────────────────────────┐ │
│  │ 📋 Stats Summary (Markdown)                      │ │
│  │                                                  │ │
│  │ Text report with all stats                      │ │
│  │ Perfect for documentation                       │ │
│  │                                                  │ │
│  │ [Download Markdown]                             │ │
│  └─────────────────────────────────────────────────┘ │
│                                                       │
│  ┌─────────────────────────────────────────────────┐ │
│  │ 🖼️ Share Graphics                               │ │
│  │                                                  │ │
│  │ Export individual charts as images              │ │
│  │ Chart: [Activity Timeline ▼]                    │ │
│  │ Format: [PNG ▼] [SVG] [PDF]                     │ │
│  │                                                  │ │
│  │ [Download Image]                                │ │
│  └─────────────────────────────────────────────────┘ │
│                                                       │
└───────────────────────────────────────────────────────┘
```

### Implementation
- PDF generation with ReportLab or WeasyPrint
- CSV export with pandas
- JSON export with native json module
- Image export from Plotly charts
- Zip file creation for bulk exports

---

## Common UI Components

### Filters Panel (Sidebar)

```
┌──────────────────────────────┐
│  Filters                     │
│  ──────────────────────────  │
│                              │
│  📅 Date Range               │
│  [Nov 2024] to [Dec 2025]   │
│  Quick: [Last 7] [30] [90]  │
│                              │
│  🏢 Workspace                │
│  ☑ All workspaces            │
│  ☐ Project Alpha             │
│  ☐ Project Beta              │
│  ☐ Project Gamma             │
│  [+ 224 more]                │
│                              │
│  📊 Time Granularity         │
│  ○ Hour                      │
│  ○ Day                       │
│  ● Week                      │
│  ○ Month                     │
│  ○ Year                      │
│                              │
│  🤖 Mode                     │
│  ☑ Agent                     │
│  ☑ Chat                      │
│                              │
│  🔧 Models (optional)        │
│  ☐ Filter by model           │
│                              │
│  [Reset Filters]             │
│                              │
└──────────────────────────────┘
```

### Stat Detail Modal

```
┌────────────────────────────────────────┐
│  Total Messages              [✕ Close] │
│  ────────────────────────────────────  │
│                                        │
│  68,657                                │
│  +1,240 from last period (+1.8%)      │
│                                        │
│  Trend (Last 30 days)                 │
│  ┌──────────────────────────────────┐ │
│  │     ╱╲                           │ │
│  │    ╱  ╲  ╱╲                      │ │
│  │   ╱    ╲╱  ╲                     │ │
│  └──────────────────────────────────┘ │
│                                        │
│  Breakdown:                            │
│  • User messages:    3,970 (5.8%)     │
│  • AI messages:     64,681 (94.2%)    │
│  • Unknown:             11 (0.02%)    │
│                                        │
│  Related Metrics:                      │
│  • Avg messages/session: 23.4         │
│  • Peak day: Dec 15 (320 messages)    │
│  • Messages with code: 9,610 (14%)    │
│                                        │
│  [View in Calendar] [Export Data]     │
│                                        │
└────────────────────────────────────────┘
```

### Loading States

```
┌──────────────────────────────┐
│  Loading data...             │
│  ████████████░░░░░░░ 75%     │
│                              │
│  Processing 68,657 messages  │
└──────────────────────────────┘
```

### Empty States

```
┌────────────────────────────────────┐
│                                    │
│         📭                         │
│                                    │
│  No data for selected filters      │
│                                    │
│  Try adjusting your date range     │
│  or workspace selection            │
│                                    │
│  [Reset Filters]                   │
│                                    │
└────────────────────────────────────┘
```

---

## Interaction Patterns

### Drill-Down Flow

```
Overview Page
    │
    ├─> Click "Messages" metric
    │   └─> Stats Page (filtered to Messages category)
    │       └─> Click specific stat
    │           └─> Detail modal with chart
    │               └─> Click chart data point
    │                   └─> Calendar page at that date
    │                       └─> Click session
    │                           └─> Session detail view
    │                               └─> Click message
    │                                   └─> Message detail
    │
    ├─> Click activity chart
    │   └─> Calendar page at clicked date
    │       └─> (continue drill-down)
    │
    └─> Click project
        └─> Entire dashboard filtered to that project
```

### Filter Propagation

```
User changes filter in sidebar
    │
    ├─> All pages update instantly
    │   └─> Charts rerender
    │   └─> Stats recalculate
    │   └─> Calendar updates heatmap
    │
    └─> URL updates with filter params
        └─> Shareable link created
```

### Search Flow (Stats Page)

```
User types in search box
    │
    ├─> Real-time filtering (debounced)
    │   └─> Matching stats highlighted
    │   └─> Non-matching stats hidden
    │   └─> Category counts update
    │
    └─> Click result
        └─> Detail modal opens
```

---

## Responsive Design

### Desktop (Default)
- Sidebar always visible
- Charts full width
- Multi-column layouts

### Tablet (768px - 1024px)
- Collapsible sidebar
- Single column charts
- Touch-friendly buttons

### Mobile (< 768px)
- Hidden sidebar (hamburger menu)
- Stacked layouts
- Simplified visualizations
- Touch gestures (swipe between pages)

---

## Performance Optimizations

### Data Loading Strategy

```python
# 1. Load minimal data on startup
initial_data = load_summary_stats()  # Fast

# 2. Cache processed data
@st.cache_data
def get_all_messages():
    return process_messages(db)

# 3. Lazy load details
def load_session_details(session_id):
    # Only load when user clicks
    return get_session(session_id)

# 4. Paginate large lists
def show_messages(page=1, per_page=50):
    return messages[page*per_page:(page+1)*per_page]
```

### Rendering Strategy

- Use `st.empty()` for dynamic content updates
- Implement virtual scrolling for long lists
- Defer rendering of off-screen content
- Use lightweight components for repeated elements

---

## Color Scheme

### Primary Colors
```
Primary:     #7C3AED  (Purple - Cursor brand)
Secondary:   #10B981  (Green - success/acceptance)
Accent:      #F59E0B  (Amber - warnings/highlights)
Background:  #0F172A  (Dark slate)
Surface:     #1E293B  (Slate)
Text:        #F1F5F9  (Light slate)
Muted:       #64748B  (Gray)
```

### Semantic Colors
```
Success:     #10B981  (Green)
Warning:     #F59E0B  (Amber)
Error:       #EF4444  (Red)
Info:        #3B82F6  (Blue)
```

### Heatmap Colors
```
None:    #1E293B  (Dark slate)
Low:     #7C3AED20 (Purple 20% opacity)
Medium:  #7C3AED60 (Purple 60% opacity)
High:    #7C3AED   (Purple 100%)
```

---

## Typography

```
Headings:    'Inter', sans-serif
             Bold, 24-32px

Body:        'Inter', sans-serif
             Regular, 14-16px

Numbers:     'JetBrains Mono', monospace
             Medium, 18-24px (for big metrics)

Code:        'JetBrains Mono', monospace
             Regular, 14px
```

---

## Implementation Plan

### Phase 1: Foundation (Week 1)
- [ ] Set up Streamlit app structure
- [ ] Implement global filters (sidebar)
- [ ] Create common components (cards, modals)
- [ ] Set up caching strategy
- [ ] Build Overview page (basic version)

### Phase 2: Core Pages (Week 2)
- [ ] Build Browse page with search engine
- [ ] Implement advanced filters
- [ ] Add error log extraction
- [ ] Build Stats page with search
- [ ] Build Calendar page with heatmap
- [ ] Implement drill-down navigation
- [ ] Add detail modals

### Phase 3: Analytics (Week 3)
- [ ] Build Analytics page (year wrapped)
- [ ] Create all visualizations
- [ ] Add scroll animations
- [ ] Polish transitions

### Phase 4: Polish & Export (Week 4)
- [ ] Build Export page
- [ ] Add Intelligence page (placeholder)
- [ ] Responsive design pass
- [ ] Performance optimization
- [ ] User testing and refinement

---

## Technical Stack

```
Frontend:    Streamlit
Charts:      Plotly (interactive)
             Altair (declarative)
Styling:     Custom CSS
             Streamlit components
Calendar:    streamlit-calendar (or custom)
Export:      ReportLab (PDF)
             Pandas (CSV/Excel)
             Matplotlib (static images)
State:       st.session_state
Caching:     @st.cache_data
```

---

## File Structure

```
dashboard/
├── main.py                      # Entry point
├── config.py                    # App config
├── styles.css                   # Custom CSS
│
├── pages/
│   ├── 01_overview.py
│   ├── 02_browse.py             # NEW: Search & filter page
│   ├── 03_stats.py
│   ├── 04_analytics.py
│   ├── 05_calendar.py
│   ├── 06_intelligence.py
│   └── 07_export.py
│
├── components/
│   ├── __init__.py
│   ├── filters.py               # Sidebar filters
│   ├── cards.py                 # Metric cards
│   ├── modals.py                # Detail modals
│   ├── charts.py                # Chart components
│   ├── calendar.py              # Calendar component
│   └── search.py                # NEW: Search components
│
├── utils/
│   ├── __init__.py
│   ├── data_loader.py           # Data loading
│   ├── formatters.py            # Format numbers/dates
│   ├── search_engine.py         # NEW: Search indexing
│   └── export_utils.py          # Export functions
│
└── assets/
    ├── logo.png
    └── empty-state.svg
```

---

*This is the complete UI/UX design specification. Ready to build a beautiful, intuitive dashboard, Jack!*

