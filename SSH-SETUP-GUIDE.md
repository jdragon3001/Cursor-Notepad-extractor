# SSH Key Setup for GitHub - Quick Guide

**Date Created:** December 22, 2025

## Your SSH Key (Already Generated! ✅)

You already have an SSH key at: `~/.ssh/id_ed25519`

**Your Public Key:**
```
ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAILhhrJVAXmaKK/kX10UasHLstpqH0JFsfuMZ7ljR3RI0 jackwilber@osmailmerge.com
```

---

## Step 1: Add SSH Key to GitHub (2 minutes)

1. **Copy your public key** (already shown above, or run):
   ```powershell
   cat ~/.ssh/id_ed25519.pub | clip
   ```
   This copies it to your clipboard.

2. **Go to GitHub SSH Settings:**
   - Visit: https://github.com/settings/keys
   - Or: GitHub.com → Profile → Settings → SSH and GPG keys

3. **Add New SSH Key:**
   - Click **"New SSH key"** button
   - Title: `Windows PC - Cursor` (or whatever you want)
   - Key: Paste your public key (from step 1)
   - Click **"Add SSH key"**

4. **Verify it's added:**
   ```powershell
   ssh -T git@github.com
   ```
   You should see: `Hi jdragon3001! You've successfully authenticated...`

---

## Step 2: Switch Remote to SSH

Currently your remote uses HTTPS (requires credentials):
```
https://github.com/jdragon3001/Cursor-Notepad-extractor.git
```

**Change it to SSH** (no credentials needed):

```powershell
cd "c:\notepad extractor\Cursor-Notepad-extractor"
git remote set-url origin git@github.com:jdragon3001/Cursor-Notepad-extractor.git
```

**Verify the change:**
```powershell
git remote -v
```
Should now show:
```
origin  git@github.com:jdragon3001/Cursor-Notepad-extractor.git (fetch)
origin  git@github.com:jdragon3001/Cursor-Notepad-extractor.git (push)
```

---

## Step 3: Push! 🚀

```powershell
cd "c:\notepad extractor\Cursor-Notepad-extractor"
git push
```

**Should work instantly** - no hanging, no prompts! ✅

---

## Why SSH is Better

✅ **No authentication prompts** - Just works  
✅ **No credential manager issues** - Bypass Windows Credential Manager entirely  
✅ **More secure** - Key-based auth is stronger than tokens  
✅ **Faster** - No HTTPS overhead  
✅ **No timeouts** - Direct SSH connection  

---

## Troubleshooting

### If `ssh -T git@github.com` asks "Are you sure you want to continue connecting?"
Just type `yes` and press Enter. This adds GitHub to your known hosts.

### If SSH test fails
Make sure:
1. SSH key is added to GitHub (check https://github.com/settings/keys)
2. SSH agent is running (usually automatic on Windows)
3. Firewall allows SSH (port 22)

### If git push still hangs after switching to SSH
Check if SSH is blocked:
```powershell
ssh -vT git@github.com
```
This shows verbose output to debug connection issues.

---

## Quick Commands Summary

```powershell
# 1. Copy public key to clipboard
cat ~/.ssh/id_ed25519.pub | clip

# 2. Add to GitHub: https://github.com/settings/keys

# 3. Test SSH connection
ssh -T git@github.com

# 4. Switch remote to SSH
cd "c:\notepad extractor\Cursor-Notepad-extractor"
git remote set-url origin git@github.com:jdragon3001/Cursor-Notepad-extractor.git

# 5. Push!
git push
```

---

## Current Status
- ✅ SSH key exists: `~/.ssh/id_ed25519`
- ⏳ Needs to be added to GitHub
- ⏳ Remote needs to switch from HTTPS → SSH
- ✅ 3 commits ready to push

**Total time: ~2 minutes to set up, then pushing works forever!**

