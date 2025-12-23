import sys
sys.path.insert(0, '.')

from stats.extractors.code_tracking_extractor import CodeTrackingExtractor
from pathlib import Path
import json

db_path = Path.home() / 'AppData' / 'Roaming' / 'Cursor' / 'User' / 'globalStorage' / 'state.vscdb'

with CodeTrackingExtractor(db_path) as extractor:
    # Get raw data
    query = "SELECT value FROM ItemTable WHERE key = 'aiCodeTrackingLines'"
    results = extractor._execute_query(query)
    
    if results and results[0] and results[0][0]:
        data = json.loads(results[0][0])
        print(f"Raw count from database: {len(data)}")
        print(f"Type: {type(data)}")
        
        # Extract using the extractor
        tracking_lines = extractor.extract()
        print(f"Extracted count: {len(tracking_lines)}")
        
        if len(data) != len(tracking_lines):
            print(f"\nWARNING: Mismatch! {len(data) - len(tracking_lines)} items failed to parse")
    else:
        print("No tracking lines found in database")

