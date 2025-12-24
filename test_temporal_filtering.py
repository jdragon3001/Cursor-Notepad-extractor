"""Test script for temporal filtering functionality."""

import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from stats.orchestrator import StatsOrchestrator
from stats.models.time_range import TimeRange
from utils.config import Config
from datetime import datetime, timedelta

def test_time_range_creation():
    """Test TimeRange creation methods."""
    print("\n" + "="*60)
    print("Testing TimeRange Creation")
    print("="*60)
    
    # Test preset creation
    presets = ['last_7_days', 'last_30_days', 'this_month', 'all_time']
    for preset in presets:
        tr = TimeRange.from_preset(preset)
        print(f"[OK] {preset}: {tr.label} ({tr.duration_days} days)")
    
    # Test custom range
    today = datetime.now()
    start = today - timedelta(days=30)
    tr = TimeRange.from_iso_strings(
        start.isoformat(),
        today.isoformat(),
        "Custom 30 Days"
    )
    print(f"[OK] Custom range: {tr.label} ({tr.duration_days} days)")
    
    print("\n[PASS] TimeRange creation tests passed!")


def test_orchestrator_filtering():
    """Test orchestrator with time filtering."""
    print("\n" + "="*60)
    print("Testing Orchestrator Time Filtering")
    print("="*60)
    
    # Initialize orchestrator
    db_path = Config.get_global_db_path()
    orchestrator = StatsOrchestrator(db_path)
    
    # Test 1: All time stats
    print("\n1. Testing All Time stats...")
    stats_all = orchestrator.calculate_all_stats()
    print(f"   Total messages: {stats_all['messages']['total_messages']['value']:,}")
    print(f"   Total sessions: {stats_all['sessions']['total_sessions']['value']:,}")
    
    # Test 2: Last 30 days
    print("\n2. Testing Last 30 Days filter...")
    time_range = TimeRange.from_preset('last_30_days')
    stats_30d = orchestrator.calculate_all_stats(time_range=time_range)
    print(f"   Messages (last 30 days): {stats_30d['messages']['total_messages']['value']:,}")
    print(f"   Sessions (last 30 days): {stats_30d['sessions']['total_sessions']['value']:,}")
    
    # Test 3: Last 7 days
    print("\n3. Testing Last 7 Days filter...")
    time_range = TimeRange.from_preset('last_7_days')
    stats_7d = orchestrator.calculate_all_stats(time_range=time_range)
    print(f"   Messages (last 7 days): {stats_7d['messages']['total_messages']['value']:,}")
    print(f"   Sessions (last 7 days): {stats_7d['sessions']['total_sessions']['value']:,}")
    
    # Verify filtering is working
    msg_all = stats_all['messages']['total_messages']['value']
    msg_30d = stats_30d['messages']['total_messages']['value']
    msg_7d = stats_7d['messages']['total_messages']['value']
    
    assert msg_7d <= msg_30d <= msg_all, "Filtered counts should be <= unfiltered"
    
    print("\n[PASS] Orchestrator filtering tests passed!")


def test_time_series():
    """Test time series data generation."""
    print("\n" + "="*60)
    print("Testing Time Series Generation")
    print("="*60)
    
    # Initialize orchestrator
    db_path = Config.get_global_db_path()
    orchestrator = StatsOrchestrator(db_path)
    
    # Get time series for last 30 days
    time_range = TimeRange.from_preset('last_30_days')
    
    print("\n1. Testing message time series...")
    series = orchestrator.get_time_series('total_messages', time_range, 'day')
    print(f"   Time range: {series['time_range']['label']}")
    print(f"   Granularity: {series['granularity']}")
    print(f"   Data points: {len(series['series'])}")
    
    if series['series']:
        # Show first 3 and last 3 data points
        dates = list(series['series'].keys())
        print(f"   First day: {dates[0]} - {series['series'][dates[0]]} messages")
        print(f"   Last day: {dates[-1]} - {series['series'][dates[-1]]} messages")
    
    print("\n[PASS] Time series tests passed!")


def main():
    """Run all tests."""
    print("\n" + "="*60)
    print("TEMPORAL FILTERING TEST SUITE")
    print("="*60)
    
    try:
        test_time_range_creation()
        test_orchestrator_filtering()
        test_time_series()
        
        print("\n" + "="*60)
        print("[SUCCESS] ALL TESTS PASSED!")
        print("="*60)
        print("\nTemporal filtering is working correctly.")
        print("You can now test the frontend with:")
        print("  - Time range selector")
        print("  - Stat drill-down modals")
        print("  - Time series charts")
        
    except Exception as e:
        print("\n" + "="*60)
        print("[FAILED] TEST FAILED")
        print("="*60)
        print(f"\nError: {e}")
        import traceback
        traceback.print_exc()
        return 1
    
    return 0


if __name__ == "__main__":
    sys.exit(main())

