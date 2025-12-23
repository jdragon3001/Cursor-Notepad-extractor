# User Guide - Cursor Stats Dashboard

## What is This?

Cursor Stats Dashboard analyzes your **Cursor IDE** usage and presents comprehensive statistics in a beautiful web interface. It reads from Cursor's local database (no data is sent anywhere) and shows you insights about:

- 💬 **Messages**: Chat interactions with the AI
- 📝 **Sessions**: Composer sessions and workflows  
- 🔧 **Tools**: File modifications, searches, and commands
- 📊 **Code**: Diffs, changes, and tracking
- 📅 **Daily Usage**: Activity patterns over time
- 🔍 **Context**: What context you provide to the AI

## For Other Users

### Step 1: Prerequisites

Make sure you have:
- ✅ **Cursor IDE installed** (not VS Code - they use different databases)
- ✅ **Python 3.8 or newer** ([Download here](https://www.python.org/downloads/))
- ✅ **Node.js 16 or newer** ([Download here](https://nodejs.org/))
- ✅ **Some Cursor usage history** (the more you've used Cursor, the better the stats)

### Step 2: Download/Clone

```bash
# If you have git:
git clone <repository-url>
cd Cursor-Notepad-extractor

# Or: Download ZIP from GitHub and extract it
```

### Step 3: Install Dependencies

```bash
# Install Python packages
pip install -r requirements.txt
pip install -r backend/requirements.txt

# Install Node packages
cd frontend
npm install
cd ..
```

**Note**: On some systems you might need to use `pip3` instead of `pip`, or `python3` instead of `python`.

### Step 4: Launch

```bash
python launch_dashboard.py
```

That's it! The dashboard will:
1. Start the backend API server
2. Start the frontend web server  
3. Open your browser automatically to http://localhost:5173

## Understanding the Stats

### Categories

**Messages (51 stats)**
- Total messages sent/received
- Message lengths and token usage
- Tool usage in messages
- Code blocks and file references
- Web searches and browser automation
- Code suggestions and acceptances

**Sessions (27 stats)**
- Total composer sessions
- Session durations and patterns
- Files added, removed, modified
- Context token usage
- Session complexity metrics

**Tools (10 stats)**
- Most used tools
- Tool success rates
- Tool categories
- Usage patterns

**Code & Diffs (12 stats)**
- Total code changes
- Lines added/removed
- Character changes
- Diff metrics
- Tracked code lines (capped at 10,000 by Cursor)

**Daily Usage (6 stats)**
- Activity by day
- Messages per day
- Active days and streaks
- Usage patterns

**Context (18 stats)**
- Attached code chunks
- Files in context
- Codebase context usage
- Linter errors
- Terminal interactions

### Known Limitations

Some stats show 0 or placeholder values:
- **Edit Distance**: Not yet implemented (shows 0)
- **Similarity Ratio**: Not yet implemented (shows 0)
- **Tracked Code Lines**: Cursor caps this at 10,000 entries

### Data Sources

All data comes from your local Cursor database:
- `composerData`: Session information
- `toolFormerData`: Tool usage and file operations
- `codeBlockDiff`: Code changes
- `aiCodeTrackingLines`: Code tracking (max 10,000)
- `messageRequestContext`: Context information

## FAQ

**Q: Is my data being sent anywhere?**  
A: No! Everything runs locally on your computer. The dashboard only reads from your local Cursor database.

**Q: Will this work with VS Code?**  
A: No, only with Cursor IDE. Cursor and VS Code use different database structures.

**Q: Can I export the stats?**  
A: The raw JSON is available at http://localhost:8000/api/stats/all - you can save this and process it however you like.

**Q: Why are some numbers different from what I expected?**  
A: The stats are based on what Cursor stores in its database. Some data might be missing if:
- Features weren't available in older Cursor versions
- Data was cleared/reset
- Storage limits were reached (e.g., the 10,000 tracked code lines limit)

**Q: Does this slow down Cursor?**  
A: No! The dashboard only reads from the database, it doesn't modify anything and Cursor doesn't need to be running.

**Q: Can I run this on a different port?**  
A: Yes! Edit `backend/main.py` (change port in `uvicorn.run()`) and `frontend/src/App.jsx` (change API_BASE_URL).

**Q: How often does the data refresh?**  
A: Stats are calculated when you load the page. Click the refresh button or reload the page to see updated stats.

## Tips

1. **Use the search box** to quickly find specific stats
2. **Filter by category** using the dropdown
3. **Clear cache** if stats seem stale (if that feature is added)
4. **Check the terminal** for detailed logs if something seems wrong
5. **Keep Cursor running** in the background to generate more data over time!

## Sharing Your Stats

If you want to share your stats anonymously:
1. Visit http://localhost:8000/api/stats/all
2. Copy the JSON
3. Remove any sensitive information (file paths, workspace names, etc.)
4. Share the cleaned JSON

## Platform-Specific Notes

### Windows
- Database location: `C:\Users\<YourName>\AppData\Roaming\Cursor\User\globalStorage\state.vscdb`
- Use PowerShell or Command Prompt

### macOS  
- Database location: `~/Library/Application Support/Cursor/User/globalStorage/state.vscdb`
- The Library folder is hidden by default (use `Cmd + Shift + .` to show it in Finder)

### Linux
- Database location: `~/.config/Cursor/User/globalStorage/state.vscdb`
- Make sure you have permission to read the database file

## Support

If you encounter issues:
1. Check `TROUBLESHOOTING.md`
2. Look at the backend terminal for error messages
3. Check browser console (F12) for frontend errors
4. Make sure you're using compatible versions of Python and Node.js

