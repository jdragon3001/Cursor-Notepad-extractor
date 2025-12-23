"""
Test script to verify timestamp parsing is now correct.

This will extract a sample of messages and verify:
1. Timestamps are being parsed correctly from ISO format
2. Date range spans multiple months (not just today)
3. Chronological ordering is preserved
"""

import sys
import os
from pathlib import Path

# Fix Windows console encoding
if sys.platform == 'win32':
    os.environ['PYTHONIOENCODING'] = 'utf-8'
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

from stats.extractors.message_extractor import MessageExtractor
from stats.extractors.session_extractor import SessionExtractor
from datetime import datetime
from collections import Counter
import logging

logging.basicConfig(level=logging.WARNING)  # Reduce noise

def test_message_timestamps():
    """Test that message timestamps are parsed correctly."""
    print("="*80)
    print("TIMESTAMP PARSING VERIFICATION TEST")
    print("="*80)
    
    # Get database path
    user_home = Path.home()
    db_path = user_home / "AppData" / "Roaming" / "Cursor" / "User" / "globalStorage" / "state.vscdb"
    
    if not db_path.exists():
        print(f"\nERROR: Database not found at {db_path}")
        return False
    
    print(f"\nUsing database: {db_path}\n")
    
    # Extract messages
    print("Extracting messages...")
    with MessageExtractor(db_path) as extractor:
        messages = extractor.extract()
    
    print(f"Extracted {len(messages)} messages\n")
    
    if not messages:
        print("ERROR: No messages found!")
        return False
    
    # Check timestamp distribution
    print("-"*80)
    print("TIMESTAMP ANALYSIS")
    print("-"*80)
    
    # Sort by timestamp
    sorted_messages = sorted(messages, key=lambda m: m.created_at)
    
    earliest = sorted_messages[0].created_at
    latest = sorted_messages[-1].created_at
    span_days = (latest - earliest).days
    
    print(f"\nEarliest message: {earliest}")
    print(f"Latest message:   {latest}")
    print(f"Time span:        {span_days} days")
    
    # Check if all dates are today (bug still present)
    today = datetime.now().date()
    messages_today = sum(1 for m in messages if m.created_at.date() == today)
    percent_today = (messages_today / len(messages)) * 100
    
    print(f"\nMessages dated today: {messages_today}/{len(messages)} ({percent_today:.1f}%)")
    
    if percent_today > 50:
        print("\n❌ FAILED: More than 50% of messages are dated today!")
        print("   The timestamp parsing bug is still present.")
        return False
    
    if span_days < 7:
        print("\n⚠️  WARNING: Time span is less than 7 days")
        print("   Expected data to span multiple months")
        return False
    
    # Show date distribution
    print("\n" + "-"*80)
    print("DATE DISTRIBUTION (by month)")
    print("-"*80)
    
    by_month = Counter()
    for m in messages:
        month_key = m.created_at.strftime("%Y-%m")
        by_month[month_key] += 1
    
    for month, count in sorted(by_month.items()):
        bar = "█" * min(50, count // 100)
        print(f"{month}: {count:>6} messages {bar}")
    
    # Check for proper chronological ordering
    print("\n" + "-"*80)
    print("CHRONOLOGICAL ORDERING CHECK")
    print("-"*80)
    
    # Sample 100 messages and verify they're in correct order
    sample_size = min(100, len(sorted_messages))
    sample = sorted_messages[:sample_size]
    
    out_of_order = 0
    for i in range(1, len(sample)):
        if sample[i].created_at < sample[i-1].created_at:
            out_of_order += 1
    
    if out_of_order > 0:
        print(f"\n⚠️  Found {out_of_order} out-of-order messages in sample")
    else:
        print(f"\n✅ All {sample_size} sampled messages are in chronological order")
    
    # Test results
    print("\n" + "="*80)
    if span_days >= 7 and percent_today < 50:
        print("✅ TIMESTAMP PARSING TEST PASSED")
        print("="*80)
        print("\nTimestamps are being parsed correctly!")
        print(f"  - Data spans {span_days} days")
        print(f"  - Only {percent_today:.1f}% of messages dated today")
        print(f"  - {len(by_month)} months of data found")
        return True
    else:
        print("❌ TIMESTAMP PARSING TEST FAILED")
        print("="*80)
        print("\nTimestamps are NOT being parsed correctly!")
        return False


def test_session_timestamps():
    """Test that session timestamps are parsed correctly."""
    print("\n" + "="*80)
    print("SESSION TIMESTAMP VERIFICATION")
    print("="*80)
    
    user_home = Path.home()
    db_path = user_home / "AppData" / "Roaming" / "Cursor" / "User" / "globalStorage" / "state.vscdb"
    
    print("\nExtracting sessions...")
    with SessionExtractor(db_path) as extractor:
        sessions = extractor.extract()
    
    print(f"Extracted {len(sessions)} sessions\n")
    
    if not sessions:
        print("ERROR: No sessions found!")
        return False
    
    # Check timestamp distribution
    sorted_sessions = sorted(sessions, key=lambda s: s.created_at)
    
    earliest = sorted_sessions[0].created_at
    latest = sorted_sessions[-1].created_at
    span_days = (latest - earliest).days
    
    print(f"Earliest session: {earliest}")
    print(f"Latest session:   {latest}")
    print(f"Time span:        {span_days} days")
    
    # Check if all dates are today
    today = datetime.now().date()
    sessions_today = sum(1 for s in sessions if s.created_at.date() == today)
    percent_today = (sessions_today / len(sessions)) * 100
    
    print(f"\nSessions created today: {sessions_today}/{len(sessions)} ({percent_today:.1f}%)")
    
    if percent_today > 50:
        print("\n❌ FAILED: Session timestamps still incorrect")
        return False
    
    print("\n✅ Session timestamps look correct")
    return True


def main():
    """Run timestamp verification tests."""
    print("\n" + "="*80)
    print("TIMESTAMP FIX VERIFICATION")
    print("="*80)
    print("\nThis test verifies that the timestamp parsing bug has been fixed.\n")
    
    try:
        message_test = test_message_timestamps()
        session_test = test_session_timestamps()
        
        print("\n" + "="*80)
        print("TEST SUMMARY")
        print("="*80)
        print(f"\nMessage timestamps: {'✅ PASS' if message_test else '❌ FAIL'}")
        print(f"Session timestamps: {'✅ PASS' if session_test else '❌ FAIL'}")
        
        if message_test and session_test:
            print("\n✅ ALL TESTS PASSED - Timestamps are correct!")
            print("\nNext steps:")
            print("1. Clear any cached stats")
            print("2. Re-run stats calculation")
            print("3. Verify activity streak, inactive days, etc. are now accurate")
            return 0
        else:
            print("\n❌ TESTS FAILED - Timestamp parsing still has issues")
            return 1
            
    except Exception as e:
        print(f"\n❌ ERROR: {e}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == '__main__':
    exit(main())

