# Cursor Data Extractor & Analytics

**Comprehensive data extraction and analysis tool for Cursor IDE**

Extract, analyze, and visualize ALL your Cursor usage data including chat history, code metrics, and effectiveness insights.

---

## What This Does

This tool extracts and analyzes your complete Cursor IDE usage data from local storage:

- **68,657 messages** (chat/agent conversations)
- **2,934 sessions** (chat & agent sessions)
- **429,700 lines of code** (AI-generated)
- **402 days of history** (Nov 2024 → Present)
- **Effectiveness analytics** (what works, what doesn't)
- **Usage patterns** (timeline, peak hours, trends)

---

## Features

### Data Extraction
- Extract ALL messages with full content (text, code, thinking)
- Session metadata and metrics
- Code diffs and changes
- Daily usage statistics
- Terminal history
- File edit history
- Notepad content

### Analytics & Insights
- **Prompt effectiveness**: What makes a good prompt?
- **Context impact**: Does more context help or hurt?
- **Tool usage**: Which tools improve results?
- **Acceptance rates**: How much code do you accept?
- **Iteration efficiency**: How many rounds to success?
- **Code quality**: Edit distance after acceptance
- **Conversation patterns**: What conversation styles work?
- **Model usage**: Which models for what tasks? (limited data)

### Visualization & Export
- Activity heatmaps
- Usage timeline
- Code metrics charts
- Export to JSON, CSV, Markdown, PDF
- Raw data browser
- Search and filter

---

## Quick Start

```bash
# Install dependencies
pip install -r requirements.txt

# Run exploration scripts (to verify data)
python recover_all_chat_data.py

# (Coming soon) Launch dashboard
python main.py
```

---

## Project Status

**Phase:** Exploration Complete ✅ | Implementation Starting

- ✅ Complete data source exploration
- ✅ All data documented (see `cursor-data-docs/`)
- ✅ Architecture designed (see `nextsteps/APP-ARCHITECTURE.md`)
- 🚧 Building extractors and analytics
- 📅 Dashboard UI (upcoming)

---

## Documentation

| Document | Purpose |
|----------|---------|
| **`EXPLORATION-COMPLETE.md`** | Complete exploration summary |
| **`QUICK-REFERENCE.md`** | Developer quick reference |
| **`COMPLETE-STATS-CATALOG.md`** | **ALL extractable metrics (600+)** |
| **`cursor-data-docs/`** | 13 detailed documentation files |
| **`nextsteps/APP-ARCHITECTURE.md`** | Complete application design |
| **`STRUCTURE.md`** | Project organization |

### Key Documentation Files

- `cursor-data-docs/README.md` - Overview of all data sources
- `cursor-data-docs/08-CURSORDISKKV-GOLDMINE.md` - Primary chat data
- `cursor-data-docs/13-MESSAGE-CONTENT-ANALYSIS.md` - Content & effectiveness
- `cursor-data-docs/12-DATA-LIMITATIONS.md` - What's available vs not

---

## Data Sources

### Primary: cursorDiskKV Table (119,747 rows)

```
bubbleId:           68,657  (Messages with text, code, thinking)
composerData:        1,076  (Session metadata, acceptance rates)
codeBlockDiff:      10,527  (Code changes)
agentKv:            17,962  (Agent execution state)
checkpointId:       14,220  (Session checkpoints)
```

### ItemTable Keys

```
aiCodeTrackingLines:          10,000 AI-written lines tracked
aiCodeTracking.dailyStats:    28 days of usage (Nov 20+)
terminal.history:             Command history
freeBestOfN.promptCount:      1,477 prompts
```

### Workspace Databases (245 total, 227 with data)

```
composer.composerData:  1,858 older sessions
notepadData:            Notepad content
```

---

## What You Can Learn

### About Your Usage
- Total sessions, messages, and code generated
- Most active days and hours
- Session duration patterns
- Agent vs Chat mode usage

### About Effectiveness
- Which prompt styles get better results
- Impact of providing context
- Tool usage correlation with acceptance
- Iteration patterns (how many rounds?)
- Code quality (retention rate)

### Limitations
- Model usage only 11.5% coverage (local data limitation)
- Daily stats only since Nov 20, 2025
- Token counts partially populated
- Server has more complete data (Year Wrapped)

---

## Tech Stack

- **Python 3.9+**
- **SQLite** - Database access
- **Streamlit** - Dashboard UI (upcoming)
- **Plotly** - Visualizations (upcoming)
- **Pandas** - Data analysis (upcoming)

---

## Project Structure

```
cursor-data-extractor/
├── database/              # SQLite connectivity
├── utils/                 # Utilities
├── cursor-data-docs/      # 13 documentation files
├── nextsteps/             # Architecture & planning
├── *.py                   # Exploration scripts (reference)
├── EXPLORATION-COMPLETE.md
├── QUICK-REFERENCE.md
└── README.md
```

---

## Exploration Scripts (Reference)

These scripts were used to explore and verify the data. They serve as reference for implementation:

- `recover_all_chat_data.py` - Multi-source data recovery
- `extract_daily_stats.py` - Daily usage extraction
- `verify_model_and_tokens.py` - Model/token validation
- `final_comprehensive_check.py` - Complete verification
- `exhaustive_exploration.py` - Full data catalog

---

## Contributing

This is a personal data extraction tool. If you find it useful and want to contribute:

1. Document any new data sources found
2. Add to `cursor-data-docs/`
3. Update `STRUCTURE.md`

---

## Important Notes

### Privacy
This tool only accesses LOCAL data stored on your machine. Nothing is sent anywhere.

### Data Scope
Local storage != Server data. Cursor's "Year Wrapped" uses server-side analytics that are more complete than local storage.

### Limitations
- Model info: Only 11.5% of messages have model data
- Daily stats: Only available since Nov 20, 2025
- Token counts: Often zero in local storage
- See `cursor-data-docs/12-DATA-LIMITATIONS.md` for details

---

## License

For personal use. Built for understanding and analyzing your own Cursor usage data.

---

## Acknowledgments

Built with exhaustive exploration of Cursor IDE's local data storage. All findings documented in `cursor-data-docs/`.

*Last updated: December 22, 2025*
