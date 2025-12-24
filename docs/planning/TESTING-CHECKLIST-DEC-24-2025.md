# Pre-Reddit Release Testing Checklist

## Testing Goals

1. Verify Windows setup works perfectly
2. Ensure Mac/Linux setup script is correct (will be validated by Reddit users)
3. Confirm documentation is clear and complete
4. Validate safety (virtual environment isolation)

---

## Windows Testing (You Can Do This)

### Test 1: Fresh Install Test

**Setup:**
1. Copy project to a new location (simulate fresh download)
2. Ensure no existing venv in the folder

**Steps:**
```powershell
cd setup
.\setup-windows.ps1
```

**Verify:**
- [ ] Script detects Python version correctly
- [ ] Script detects Node.js version correctly
- [ ] Creates `venv` folder in project root
- [ ] Installs packages without errors
- [ ] Verification step passes (6/6 complete)
- [ ] Creates `launch.ps1` in project root

**Check Isolation:**
```powershell
# Outside venv - should NOT have packages
python -c "import fastapi"  # Should fail

# Inside venv - should have packages
venv\Scripts\Activate.ps1
python -c "import fastapi"  # Should succeed
deactivate
```

---

### Test 2: Launch Test

**Steps:**
```powershell
.\launch.ps1
```

**Verify:**
- [ ] Backend starts on port 8000
- [ ] Frontend starts on port 5173
- [ ] Browser opens automatically
- [ ] Dashboard loads without errors
- [ ] Stats display correctly
- [ ] No console errors in browser (F12)

---

### Test 3: Existing Python Projects Test

**Setup:**
Create a separate Python project with different package versions.

**Steps:**
1. In another folder, create a test project
2. Install different package versions globally or in another venv
3. Run Cursor Stats setup in its own folder
4. Verify no conflicts

**Verify:**
- [ ] Cursor Stats venv is separate
- [ ] Other project still works
- [ ] No version conflicts

---

### Test 4: Clean Uninstall Test

**Steps:**
1. Stop dashboard (Ctrl+C)
2. Delete entire project folder
3. Check system:
   ```powershell
   # These should be unchanged from before install
   python -m pip list
   ```

**Verify:**
- [ ] No leftover files outside project folder
- [ ] System Python unchanged
- [ ] No global packages installed

---

### Test 5: Port Conflict Test

**Setup:**
Start something else on port 8000 first.

**Steps:**
```powershell
# Start a dummy server
python -m http.server 8000
# In another terminal, try to launch dashboard
.\launch.ps1
```

**Verify:**
- [ ] Clear error message about port in use
- [ ] Deploy.ps1 would clean this up automatically
- [ ] User knows how to fix it

---

### Test 6: Documentation Accuracy

**Read through and verify:**
- [ ] REDDIT_GUIDE.md - Windows section accurate
- [ ] README.md - Quick start works
- [ ] setup/README.md - Clear instructions
- [ ] INSTALLATION.md - Manual steps correct

---

## Mac/Linux Validation (Reddit Users Will Test)

### What Mac Users Should Verify

**Expected results:**
```bash
cd setup
chmod +x setup-mac.sh
./setup-mac.sh
```

Should:
- Detect `python3` command correctly
- Detect `pip3` command correctly  
- Create `venv` folder
- Install all packages without errors
- Create `launch.sh` file
- Work with both Intel and Apple Silicon Macs

**Common Mac Issues to Watch For:**
1. Permission errors (fixed with `chmod +x`)
2. `python3` vs `python` command
3. `pip3` vs `pip` command
4. macOS Ventura+ security prompts
5. Homebrew Python vs system Python

---

## Pre-Release Documentation Review

### Files to Review Before Posting

- [ ] **REDDIT_GUIDE.md** - Main guide for Reddit
  - Concise, no emojis
  - Clear Windows vs Mac sections
  - Troubleshooting included

- [ ] **README.md** - Project homepage
  - Points to setup scripts
  - Clear quick start
  - Links to detailed docs

- [ ] **setup/README.md** - Setup folder guide
  - Explains both scripts
  - Why virtual environment

- [ ] **setup/setup-windows.ps1** - Windows setup
  - Creates venv
  - Installs isolated
  - Creates launch.ps1

- [ ] **setup/setup-mac.sh** - Mac/Linux setup
  - Executable permissions clear
  - Creates venv
  - Creates launch.sh

- [ ] **.gitignore** - Excludes venv
  - Has `venv/` entry
  - Protects user data

---

## Reddit Post Checklist

### Before Posting

- [ ] All Windows tests pass
- [ ] Documentation proofread
- [ ] No sensitive data in repo
- [ ] .gitignore protects user data
- [ ] Virtual environment isolation confirmed
- [ ] Clear uninstall process

### Post Content Should Include

- [ ] Brief description (what it does)
- [ ] Link to REDDIT_GUIDE.md
- [ ] Mention it's 100% local (privacy)
- [ ] Note: virtual environment (safe)
- [ ] Request: Mac users test and report issues
- [ ] Your usage stats as example

### Example Reddit Post Template

```
Title: I made a dashboard to visualize your Cursor IDE usage stats [Windows/Mac/Linux]

Body:
Built a local web dashboard that analyzes your Cursor IDE history and shows 
124+ statistics about your usage patterns.

Key features:
- 100% local (your data never leaves your computer)
- Works on Windows, Mac, and Linux
- Uses virtual environment (won't affect your Python setup)
- Shows message counts, tool usage, code changes, daily trends

Setup: 5-10 minutes
See detailed guide: [link to REDDIT_GUIDE.md]

Windows users: Tested and working
Mac users: Script follows best practices, please test and report issues

[Screenshot of dashboard]
```

---

## After Reddit Post

### Monitor for Issues

Watch for comments about:
- Mac-specific errors (most likely)
- Python version edge cases
- Node.js version issues
- Database not found (Cursor not installed)
- Port conflicts
- Permission errors

### Quick Fixes You Can Make

If Mac users report issues:
1. Update setup-mac.sh based on feedback
2. Update REDDIT_GUIDE.md troubleshooting
3. Push fixes quickly
4. Reply to comments with fixes

---

## Success Criteria

**Minimum:**
- Windows setup works flawlessly (you verify)
- Mac setup script is correct (standard bash practices)
- Documentation is clear
- Virtual environment isolates packages
- Clean uninstall (just delete folder)

**Ideal:**
- Zero Windows issues
- Mac users report it works first try
- Linux users can use Mac script
- Clear enough for non-technical users
- Reddit post gets helpful feedback

---

## Timeline Recommendation

1. **Today**: Test all Windows scenarios (1-2 hours)
2. **Today**: Fix any issues found
3. **Today**: Proofread all documentation
4. **Post to Reddit**: After Windows testing complete
5. **Monitor**: First 24 hours for Mac feedback
6. **Iterate**: Fix Mac issues as reported

You don't need a Mac to post - the script is solid, and Mac users will quickly validate and report any issues.

