"""
Diagnostic script to identify stat calculation issues.

This script analyzes the raw data to verify:
1. Activity streak calculation accuracy
2. Inactive days calculation
3. Sessions per workspace accuracy
4. Whether workspace databases are being used
"""

import sys
import os
from pathlib import Path

# Fix Windows console encoding for emojis/unicode
if sys.platform == 'win32':
    os.environ['PYTHONIOENCODING'] = 'utf-8'
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')
    sys.stderr.reconfigure(encoding='utf-8', errors='replace')

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

from stats.extractors.message_extractor import MessageExtractor
from stats.extractors.session_extractor import SessionExtractor
from utils.config import Config
from datetime import datetime, timedelta
from collections import defaultdict
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def diagnose_activity_streak(messages):
    """Diagnose activity streak calculation."""
    print("\n" + "="*80)
    print("ACTIVITY STREAK DIAGNOSIS")
    print("="*80)
    
    if not messages:
        print("❌ No messages found!")
        return
    
    # Get all unique dates
    dates = sorted(set(m.created_at.date() for m in messages))
    print(f"\n📊 Total unique active days: {len(dates)}")
    print(f"📅 First activity: {dates[0]}")
    print(f"📅 Last activity: {dates[-1]}")
    print(f"📅 Total span: {(dates[-1] - dates[0]).days + 1} days")
    
    # Calculate streaks
    longest_streak = 1
    current_streak = 1
    streaks = []
    streak_start = dates[0]
    
    for i in range(1, len(dates)):
        if (dates[i] - dates[i-1]).days == 1:
            current_streak += 1
            longest_streak = max(longest_streak, current_streak)
        else:
            if current_streak > 1:
                streaks.append((streak_start, dates[i-1], current_streak))
            current_streak = 1
            streak_start = dates[i]
    
    # Add final streak
    if current_streak > 1:
        streaks.append((streak_start, dates[-1], current_streak))
    
    print(f"\n🔥 Longest streak: {longest_streak} days")
    
    if streaks:
        print(f"\n📈 All streaks over 1 day ({len(streaks)} found):")
        for start, end, length in sorted(streaks, key=lambda x: x[2], reverse=True)[:10]:
            print(f"   {length} days: {start} to {end}")
    else:
        print("\n⚠️  No consecutive day streaks found!")
        print("\n🔍 Showing sample of dates to understand gaps:")
        for i in range(min(20, len(dates))):
            if i > 0:
                gap = (dates[i] - dates[i-1]).days
                print(f"   {dates[i]:<12} (gap: {gap} days)")
            else:
                print(f"   {dates[i]}")
    
    # Calculate current streak
    today = datetime.now().date()
    current_streak_days = 0
    for i in range(len(dates) - 1, -1, -1):
        expected_date = today - timedelta(days=current_streak_days)
        if dates[i] == expected_date:
            current_streak_days += 1
        else:
            break
    
    print(f"\n🔥 Current streak (from today): {current_streak_days} days")
    
    if longest_streak == 1:
        print("\n❌ ISSUE DETECTED: Longest streak is 1 day")
        print("   This means no consecutive days of activity were found.")
        print("   Possible causes:")
        print("   1. Data extraction is only getting messages from single days")
        print("   2. Timezone issues causing date grouping problems")
        print("   3. Missing historical data")


def diagnose_inactive_days(messages):
    """Diagnose inactive days calculation."""
    print("\n" + "="*80)
    print("INACTIVE DAYS DIAGNOSIS")
    print("="*80)
    
    if not messages:
        print("❌ No messages found!")
        return
    
    dates = set(m.created_at.date() for m in messages)
    min_date = min(dates)
    max_date = max(dates)
    total_days = (max_date - min_date).days + 1
    active_days = len(dates)
    inactive_days = total_days - active_days
    
    print(f"\n📊 Date range: {min_date} to {max_date}")
    print(f"📊 Total days in range: {total_days}")
    print(f"✅ Active days: {active_days}")
    print(f"❌ Inactive days: {inactive_days}")
    print(f"📈 Activity rate: {(active_days/total_days*100):.1f}%")
    
    if inactive_days == 0:
        print("\n⚠️  ISSUE DETECTED: Zero inactive days")
        print("   This means you were active EVERY single day in the date range.")
        print("   Possible causes:")
        print("   1. Data range is too small (only spans days you were active)")
        print("   2. Missing older historical data")
        
        # Show date distribution
        print(f"\n🔍 Checking for gaps in the {len(dates)} active days...")
        sorted_dates = sorted(dates)
        gaps = []
        for i in range(1, len(sorted_dates)):
            gap_size = (sorted_dates[i] - sorted_dates[i-1]).days - 1
            if gap_size > 0:
                gaps.append((sorted_dates[i-1], sorted_dates[i], gap_size))
        
        if gaps:
            print(f"   Found {len(gaps)} gaps totaling {sum(g[2] for g in gaps)} days:")
            for start, end, size in sorted(gaps, key=lambda x: x[2], reverse=True)[:10]:
                print(f"   {size} days gap: {start} to {end}")
        else:
            print("   No gaps found - truly active every day!")


def diagnose_sessions_per_workspace(sessions):
    """Diagnose sessions per workspace calculation."""
    print("\n" + "="*80)
    print("SESSIONS PER WORKSPACE DIAGNOSIS")
    print("="*80)
    
    if not sessions:
        print("❌ No sessions found!")
        return
    
    print(f"\n📊 Total sessions: {len(sessions)}")
    
    # Group by workspace ID
    workspace_sessions = defaultdict(list)
    sessions_with_workspace = 0
    
    for session in sessions:
        if hasattr(session, 'workspace_folder') and session.workspace_folder:
            workspace_sessions[session.workspace_folder].append(session)
            sessions_with_workspace += 1
        elif hasattr(session, 'folder_path') and session.folder_path:
            workspace_sessions[session.folder_path].append(session)
            sessions_with_workspace += 1
    
    print(f"📁 Unique workspaces detected: {len(workspace_sessions)}")
    print(f"📊 Sessions with workspace info: {sessions_with_workspace}")
    print(f"📊 Sessions without workspace info: {len(sessions) - sessions_with_workspace}")
    
    if len(workspace_sessions) <= 1:
        print("\n❌ ISSUE DETECTED: Only 1 or 0 workspaces detected")
        print("   This makes 'sessions per workspace' equal to total sessions.")
        print("   Possible causes:")
        print("   1. Only extracting from global DB (not workspace DBs)")
        print("   2. Workspace information not being parsed correctly")
        print("   3. All sessions are from the same workspace")
        
        # Check what workspace data exists
        print("\n🔍 Checking session workspace data:")
        sample_sessions = sessions[:5]
        for i, session in enumerate(sample_sessions, 1):
            print(f"\n   Session {i} (ID: {session.session_id[:20]}...):")
            print(f"      workspace_folder: {getattr(session, 'workspace_folder', 'N/A')}")
            print(f"      folder_path: {getattr(session, 'folder_path', 'N/A')}")
            print(f"      created_at: {session.created_at}")
    else:
        print(f"\n✅ Multiple workspaces detected ({len(workspace_sessions)} total)")
        print(f"\n📊 Top 10 workspaces by session count:")
        sorted_workspaces = sorted(workspace_sessions.items(), key=lambda x: len(x[1]), reverse=True)
        for workspace, ws_sessions in sorted_workspaces[:10]:
            print(f"   {len(ws_sessions):4d} sessions: {workspace}")


def check_data_sources(db_path):
    """Check what data sources are available."""
    import sqlite3
    print("\n" + "="*80)
    print("DATA SOURCES CHECK")
    print("="*80)
    
    # Check cursorDiskKV
    try:
        conn = sqlite3.connect(str(db_path))
        cursor = conn.cursor()
        
        cursor.execute("SELECT COUNT(*) FROM cursorDiskKV WHERE key LIKE 'bubbleId:%'")
        bubble_count = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM cursorDiskKV WHERE key LIKE 'composerData:%'")
        composer_count = cursor.fetchone()[0]
        
        print(f"\n📊 cursorDiskKV table:")
        print(f"   bubbleId entries (messages): {bubble_count}")
        print(f"   composerData entries (sessions): {composer_count}")
        
        # Check date range of data
        cursor.execute("SELECT value FROM cursorDiskKV WHERE key LIKE 'bubbleId:%' LIMIT 1000")
        rows = cursor.fetchall()
        
        if rows:
            import json
            dates = []
            for (value,) in rows:
                try:
                    if isinstance(value, bytes):
                        data = json.loads(value.decode('utf-8'))
                    elif isinstance(value, str):
                        data = json.loads(value)
                    else:
                        continue
                    
                    if 'createdAt' in data:
                        try:
                            date = datetime.fromisoformat(data['createdAt'].replace('Z', '+00:00'))
                            dates.append(date)
                        except:
                            pass
                except:
                    pass
            
            if dates:
                dates.sort()
                print(f"\n📅 Data date range (sample of 1000 messages):")
                print(f"   Earliest: {dates[0].date()}")
                print(f"   Latest: {dates[-1].date()}")
                print(f"   Span: {(dates[-1] - dates[0]).days} days")
        
        conn.close()
        
    except Exception as e:
        logger.error(f"Error checking data sources: {e}")
    
    # Check if workspace databases exist
    config = Config()
    workspace_path = Path(config.get_workspace_path())
    if workspace_path.exists():
        workspace_dbs = list(workspace_path.glob('*/state.vscdb'))
        print(f"\n📊 Workspace databases found: {len(workspace_dbs)}")
        
        if workspace_dbs:
            print("   ✅ Workspace databases are available")
            print("   ⚠️  But they may not be used in extraction yet!")
        else:
            print("   ❌ No workspace databases found")
    else:
        print(f"\n❌ Workspace path does not exist: {workspace_path}")


def main():
    """Run all diagnostics."""
    print("\n" + "="*80)
    print("CURSOR STATS DIAGNOSTIC TOOL")
    print("="*80)
    print("\nThis tool will help identify why certain stats appear incorrect.")
    
    try:
        # Get database path from Config
        config = Config()
        user_home = Path.home()
        db_path = user_home / "AppData" / "Roaming" / "Cursor" / "User" / "globalStorage" / "state.vscdb"
        
        if not db_path.exists():
            print(f"\n❌ Database not found at: {db_path}")
            print("   Please verify Cursor is installed and has been used.")
            return 1
        
        print(f"\n✅ Using database: {db_path}")
        
        # Check data sources first
        check_data_sources(db_path)
        
        # Extract messages
        print("\n📥 Extracting messages...")
        with MessageExtractor(db_path) as message_extractor:
            messages = message_extractor.extract()
        print(f"✅ Extracted {len(messages)} messages")
        
        # Extract sessions
        print("\n📥 Extracting sessions...")
        with SessionExtractor(db_path) as session_extractor:
            sessions = session_extractor.extract()
        print(f"✅ Extracted {len(sessions)} sessions")
        
        # Run diagnostics
        diagnose_activity_streak(messages)
        diagnose_inactive_days(messages)
        diagnose_sessions_per_workspace(sessions)
        
        print("\n" + "="*80)
        print("DIAGNOSIS COMPLETE")
        print("="*80)
        print("\nKey Takeaways:")
        print("1. Check if the date ranges look correct")
        print("2. Verify if consecutive days are being detected")
        print("3. Confirm if workspace data is being used")
        print("4. Look for any warnings or issues flagged above")
        
    except Exception as e:
        logger.error(f"Error during diagnosis: {e}", exc_info=True)
        return 1
    
    return 0


if __name__ == '__main__':
    exit(main())

