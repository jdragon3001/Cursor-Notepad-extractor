import json
d = json.load(open('stats_output.json'))
msgs = d.get('messages', {})

print('Current stats_output.json:')
print(f'  messages_with_lints exists: {"messages_with_lints" in msgs}')
print(f'  linter_errors exists: {"linter_errors" in msgs}')
print(f'  messages_with_console_logs exists: {"messages_with_console_logs" in msgs}')
print(f'  terminal_interactions exists: {"terminal_interactions" in msgs}')

if "terminal_interactions" in msgs:
    print(f'  terminal_interactions value: {msgs["terminal_interactions"].get("value")}')

print(f'\nTotal message stats in file: {len(msgs)}')

# Check if these are the OLD removed stats
if "messages_with_lints" in msgs:
    print('\n❌ OLD STATS STILL IN FILE - Frontend is reading stale data!')
else:
    print('\n✅ Removed stats are gone from file')

