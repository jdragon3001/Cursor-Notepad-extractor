import json
d = json.load(open('stats_output.json'))
msgs = d.get('messages', {})
tools = d.get('tools', {})

print('MESSAGE stats with "tool" in name:')
for k, v in msgs.items():
    if 'tool' in k.lower():
        print(f'  {k}: {v.get("value")} (source: {v.get("data_source")})')

print('\nTOOL category stats:')
for k, v in tools.items():
    print(f'  {k}: {v.get("value")} (source: {v.get("data_source")})')



