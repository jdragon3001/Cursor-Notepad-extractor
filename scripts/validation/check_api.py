import sys, json
d = json.load(sys.stdin)
print('API Tool Stats:')
for k, v in d.items():
    print(f'  {k}: {v.get("value")}')



