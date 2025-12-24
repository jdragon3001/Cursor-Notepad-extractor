import json
data = json.load(open('stats_output.json'))
ctx_stats = data.get('context', {})
print('Context linter stats:')
print(f"  contexts_with_linter_errors: {ctx_stats.get('contexts_with_linter_errors', {}).get('value', 'N/A')}")
print(f"  total_linter_errors: {ctx_stats.get('total_linter_errors', {}).get('value', 'N/A')}")
msg_stats = data.get('messages', {})
print('\nMessage error stats:')
print(f"  messages_with_lints: {msg_stats.get('messages_with_lints', {}).get('value', 'N/A')}")
print(f"  linter_errors: {msg_stats.get('linter_errors', {}).get('value', 'N/A')}")
print(f"  messages_with_console_logs: {msg_stats.get('messages_with_console_logs', {}).get('value', 'N/A')}")
print(f"  terminal_interactions: {msg_stats.get('terminal_interactions', {}).get('value', 'N/A')}")

