"""Quick test for time series endpoint."""

import requests

API_BASE = 'http://127.0.0.1:8000'

# Test time series endpoint
print("Testing time series endpoint...")
print("-" * 60)

test_stats = ['user_messages', 'total_sessions', 'total_diffs']

for stat_id in test_stats:
    print(f"\nTesting: {stat_id}")
    try:
        response = requests.get(
            f'{API_BASE}/api/stats/time-series/{stat_id}',
            params={'preset': 'last_30_days', 'granularity': 'day'}
        )
        
        if response.status_code == 200:
            data = response.json()
            series = data.get('series', {})
            print(f"  ✓ Success! Got {len(series)} data points")
            if series:
                first_key = list(series.keys())[0]
                print(f"  Sample: {first_key} -> {series[first_key]}")
        else:
            print(f"  ✗ Error {response.status_code}: {response.text}")
    except Exception as e:
        print(f"  ✗ Exception: {e}")

print("\n" + "=" * 60)
print("Test complete!")

