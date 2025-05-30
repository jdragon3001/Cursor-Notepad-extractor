# Cursor Notepad Extractor

A streamlined utility for finding, extracting, and managing notes stored in Cursor editor databases.

## ✅ **Project Status: Cleaned & Optimized**

Successfully extracted 214 note entries from 163 Cursor workspace databases. Project has been cleaned up to remove unnecessary files and minimize dependencies.

## 🚀 **Quick Setup (Any Computer)**

### **Option 1: New Computer Setup (Automated)**
```bash
# 1. Download/copy the project folder to any computer
# 2. Double-click this file to set everything up:
setup_for_new_computer.bat
```

### **Option 2: Manual Setup**
```bash
# 1. Install Miniconda (if not already installed)
# Download from: https://docs.conda.io/en/latest/miniconda.html

# 2. Run the application (it will create environment automatically)
start_note_search.bat
```

### **Option 3: If you have conda already**
```bash
conda create -n cursor-notepad-browser python=3.10 -y
conda activate cursor-notepad-browser
pip install reportlab python-docx
python note_search_gui.py
```

## 🌍 **Portability Features**

**✅ Works on any Windows computer** - No hardcoded paths
**✅ Works for any user** - Automatically finds the current user's Cursor data
**✅ Auto-setup** - Creates conda environment if it doesn't exist
**✅ Minimal dependencies** - Only uses built-in Python modules for core functionality

### **What's Automatically Detected:**
- **User home directory** - `%USERPROFILE%\AppData\Roaming\Cursor\...`
- **Cursor workspace databases** - Finds all workspace storage automatically  
- **Conda environment** - Creates one if none exists
- **Dependencies** - Installs optional PDF/DOCX support

## Features

- **Auto-scanning on startup** - Automatically finds your notes when you open the GUI
- **Smart search** - Search through notes content and titles with real-time filtering  
- **Individual note parsing** - Separates individual notes within notepad files
- **Multiple export formats** - Export to TXT, PDF, DOCX, and Markdown formats
- **Copy to clipboard** - Quick copying of note content
- **Sort and filter** - Sort notes by title or modification date

## 📁 **Project Structure (Portable)**

After cleanup, the project contains only essential files:

```
📁 Cursor Notepad Extractor/
├── 🚀 setup_for_new_computer.bat  # First-time setup (run this on new computer)
├── 🚀 start_note_search.bat       # Daily launcher (double-click to run)
├── note_search_gui.py             # Main application
├── note_finder.py                 # Database scanner (auto-detects user paths)
├── note_parser.py                 # Note content parser
├── requirements.txt               # Dependencies
├── cursor_notes_found.txt         # Your extracted notes (763KB)
├── your_cursor_notes.txt          # Clean notepad content (18KB)
├── 📁 database/
│   ├── cursor_db.py              # Database access
│   └── __init__.py
├── 📁 utils/
│   ├── config.py                 # Auto-detects user paths
│   └── __init__.py
└── 📁 docs/
    ├── README.md                 # This file
    ├── STRUCTURE.md              # Project architecture
    ├── PROBLEM_LOG.txt           # Issue tracking
    └── DEPRECATED.txt            # What to avoid
```

## 📋 **System Requirements**

**Required:**
- Windows 10/11 (uses Windows-specific paths)
- Python 3.10+ (installed automatically via conda)
- Cursor editor installed (with workspace data)

**Automatically Installed:**
- Miniconda (if you run setup script)
- reportlab (PDF export)
- python-docx (Word export)

**Built-in (no installation needed):**
- tkinter (GUI)
- sqlite3 (database access)
- pathlib, json, threading (utilities)

## 🎮 **Usage Examples**

### **First Time on New Computer:**
1. Copy project folder to computer
2. Double-click `setup_for_new_computer.bat`
3. Wait for setup to complete
4. Application launches automatically

### **Daily Use:**
1. Double-click `start_note_search.bat`
2. Wait for auto-scan: "Auto-scan complete: Found X notes"
3. Search for notepad content: Type `notepad`
4. Browse and export your notes

### **Find Specific Projects:**
- Type `notepad` → Your actual notepad content
- Type `macro` → Automation project notes
- Type `RAG` → AI system specifications  
- Type `ghost` → Desktop widget project
- Type `download` → File sharing tool ideas

## 🎯 Quick Start - Find Your Notepads

### Simple Method (Recommended):
```bash
python note_search_gui.py
```

**The GUI will automatically scan for notes when it starts!** Just wait for it to complete, then type `notepad` in the search box to filter your notepad entries.

### Manual Method:
```bash
python note_finder.py    # Extract notes
python simple_note_search.py    # Alternative GUI
```

## 🛠️ Troubleshooting

### "No notes file found"
Run `python note_finder.py` first to scan databases

### "Memory issues"
Use `simple_note_search.py` instead of `main.py`

### "Can't find specific notes"
Try different search terms - notes might be stored under different keys

## 📝 Next Steps

1. **Search for your notepad content** using the GUI
2. **Export important notes** to separate files
3. **Organize by project** using filtered exports
4. **Set up regular backups** of important notes

---

**Success!** 🎉 Your Cursor notepad content has been successfully extracted and is now searchable and exportable.

## Development Notes

Created by Claude Sonnet 4 for extracting Cursor editor notepad content from SQLite workspace storage databases. Handles memory efficiently and provides practical search/export functionality. 