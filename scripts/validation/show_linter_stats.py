import json
d = json.load(open('stats_output.json'))
ctx = d.get('context', {})

print('='*80)
print('LINTER ERROR STATS (Already Working!)')
print('='*80)

linter_stats = {k:v for k,v in ctx.items() if 'linter' in k.lower() or 'error' in k.lower()}

for stat_name, stat_data in linter_stats.items():
    print(f"\n{stat_name}:")
    print(f"  Value: {stat_data.get('value')}")
    print(f"  Label: {stat_data.get('label')}")
    if 'breakdown' in stat_data:
        print(f"  Details: {stat_data['breakdown']}")

