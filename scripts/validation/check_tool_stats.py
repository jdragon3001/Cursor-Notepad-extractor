import json
d = json.load(open('stats_output.json'))
tools = d.get('tools', {})
print('Tool Stats Values:')
for k, v in tools.items():
    print(f'  {k}: {v.get("value")}')



