"""
Test script for the stats extraction and calculation pipeline.

This script tests the end-to-end flow:
1. Extract data from database
2. Calculate stats
3. Display results
"""

from pathlib import Path
import json
import logging
from utils.config import Config
from stats import StatsOrchestrator

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def main():
    """Test the stats pipeline."""
    print("="* 60)
    print("CURSOR DATA STATS - PIPELINE TEST")
    print("="* 60)
    print()
    
    # Get global database path directly
    db_path = Path.home() / 'AppData' / 'Roaming' / 'Cursor' / 'User' / 'globalStorage' / 'state.vscdb'
    
    if not db_path.exists():
        print(f"ERROR: Global state database not found at: {db_path}")
        return
    
    print(f"Database: {db_path}")
    print(f"Database size: {db_path.stat().st_size / (1024**3):.2f} GB")
    print()
    
    # Initialize orchestrator with cache
    cache_dir = Path('.cache/stats')
    orchestrator = StatsOrchestrator(db_path, cache_dir)
    
    # Force fresh extraction for testing
    print("Forcing fresh data extraction (ignoring cache)...")
    orchestrator.invalidate_cache()
    
    # Get quick summary
    print("Getting data summary...")
    summary = orchestrator.get_summary()
    print(f"  Messages: {summary['total_messages']:,}")
    print(f"  Sessions: {summary['total_sessions']:,}")
    print(f"  Cache enabled: {summary['cache_enabled']}")
    print()
    
    # Calculate all stats
    print("Calculating stats...")
    all_stats = orchestrator.calculate_all_stats()
    print(f"  Calculated {len(all_stats)} stat categories")
    print()
    
    # Display message stats
    if 'messages' in all_stats:
        print("="* 60)
        print("MESSAGE STATS")
        print("="* 60)
        print()
        
        message_stats = all_stats['messages']
        
        # Display key stats
        key_stats = [
            'total_messages',
            'user_messages',
            'ai_messages',
            'messages_per_session',
            'message_text_length',
            'messages_with_code_blocks',
            'code_blocks_generated',
            'messages_with_thinking',
            'thinking_duration',
            'messages_with_tools',
            'tool_invocations'
        ]
        
        for stat_id in key_stats:
            if stat_id in message_stats:
                stat = message_stats[stat_id]
                print(f"{stat['label']}:")
                print(f"  Value: {stat['value']:,.2f}")
                
                # Show additional fields if available
                if 'percentage' in stat:
                    print(f"  Percentage: {stat['percentage']:.1f}%")
                if 'median' in stat:
                    print(f"  Median: {stat['median']:,.2f}")
                if 'min' in stat and 'max' in stat:
                    print(f"  Range: {stat['min']:,.0f} - {stat['max']:,.0f}")
                
                print()
    
    # Save full stats to file
    output_file = Path('stats_output.json')
    print(f"Saving full stats to {output_file}...")
    with open(output_file, 'w') as f:
        # Convert to JSON-serializable format
        json_stats = {}
        for category, stats in all_stats.items():
            json_stats[category] = {}
            for stat_name, stat_data in stats.items():
                # Remove numpy arrays and other non-serializable items
                serializable_data = {}
                for key, value in stat_data.items():
                    if key == 'distribution':
                        # Skip distribution for now (contains numpy arrays)
                        continue
                    elif isinstance(value, (int, float, str, bool, type(None))):
                        serializable_data[key] = value
                    elif isinstance(value, dict):
                        serializable_data[key] = value
                    elif isinstance(value, list):
                        serializable_data[key] = value
                
                json_stats[category][stat_name] = serializable_data
        
        json.dump(json_stats, f, indent=2)
    
    print(f"[OK] Stats saved to {output_file}")
    print()
    
    print("="* 60)
    print("TEST COMPLETE")
    print("="* 60)


if __name__ == '__main__':
    main()

