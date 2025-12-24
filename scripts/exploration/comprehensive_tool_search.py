"""Deep dive into finding ANY tool usage data in the database."""

import sqlite3
import json
from pathlib import Path

db_path = Path.home() / "AppData" / "Roaming" / "Cursor" / "User" / "globalStorage" / "state.vscdb"
conn = sqlite3.connect(str(db_path))
cursor = conn.cursor()

print("=" * 60)
print("COMPREHENSIVE TOOL DATA SEARCH")
print("=" * 60)

# 1. Check all cursorDiskKV keys for tool-related prefixes
print("\n1. Checking for tool-related key prefixes...")
cursor.execute("""
    SELECT DISTINCT substr(key, 1, instr(key || ':', ':') - 1) as prefix, COUNT(*) as count
    FROM cursorDiskKV
    GROUP BY prefix
    ORDER BY count DESC
""")

prefixes = cursor.fetchall()
tool_prefixes = [p for p in prefixes if p[0] and 'tool' in p[0].lower()]
print(f"Key prefixes with 'tool': {tool_prefixes}")

# 2. Search for tool-related keys explicitly
print("\n2. Searching for explicit tool keys...")
patterns = ['%tool%', '%Tool%', '%TOOL%']
for pattern in patterns:
    cursor.execute(f"SELECT COUNT(*) FROM cursorDiskKV WHERE key LIKE ?", (pattern,))
    count = cursor.fetchone()[0]
    if count > 0:
        print(f"Keys matching '{pattern}': {count}")
        # Get samples
        cursor.execute(f"SELECT key FROM cursorDiskKV WHERE key LIKE ? LIMIT 5", (pattern,))
        samples = cursor.fetchall()
        for key, in samples:
            print(f"  - {key}")

# 3. Check messages for non-empty toolResults
print("\n3. Searching for messages with actual tool results...")
cursor.execute("""
    SELECT COUNT(*) FROM cursorDiskKV 
    WHERE key LIKE 'bubbleId:%' 
    AND value LIKE '%"toolResults":[{%'
""")
count = cursor.fetchone()[0]
print(f"Messages with populated toolResults: {count}")

# 4. Check agentKv for tool data (agents might have tool usage)
print("\n4. Checking agentKv entries...")
cursor.execute("SELECT COUNT(*) FROM cursorDiskKV WHERE key LIKE 'agentKv:%'")
agent_count = cursor.fetchone()[0]
print(f"agentKv entries: {agent_count}")

# Sample an agentKv entry
cursor.execute("SELECT key, value FROM cursorDiskKV WHERE key LIKE 'agentKv:%' LIMIT 1")
result = cursor.fetchone()
if result:
    key, value_bytes = result
    print(f"\nSample agentKv key: {key}")
    try:
        data = json.loads(value_bytes)
        print(f"Top-level keys: {list(data.keys())}")
        if 'tool' in str(data).lower():
            print("Contains 'tool' in data!")
            print(json.dumps(data, indent=2)[:500])
    except:
        print(f"Value preview: {str(value_bytes)[:200]}")

# 5. Check for messageRequestContext (might have tool info)
print("\n5. Checking messageRequestContext...")
cursor.execute("SELECT COUNT(*) FROM cursorDiskKV WHERE key LIKE 'messageRequestContext:%'")
context_count = cursor.fetchone()[0]
print(f"messageRequestContext entries: {context_count}")

# Sample one
cursor.execute("SELECT key, value FROM cursorDiskKV WHERE key LIKE 'messageRequestContext:%' LIMIT 1")
result = cursor.fetchone()
if result:
    key, value_bytes = result
    try:
        data = json.loads(value_bytes)
        if 'tool' in str(data).lower():
            print("Contains tool data!")
            print(json.dumps(data, indent=2)[:500])
    except:
        pass

# 6. Check ItemTable for tool data
print("\n6. Checking ItemTable for tool-related keys...")
cursor.execute("SELECT key FROM ItemTable WHERE key LIKE '%tool%' LIMIT 10")
tool_keys = cursor.fetchall()
if tool_keys:
    print(f"Found {len(tool_keys)} tool-related keys in ItemTable:")
    for key, in tool_keys:
        print(f"  - {key}")
else:
    print("No tool-related keys in ItemTable")

conn.close()

print(f"\n{'='*60}")
print("SEARCH COMPLETE")
print(f"{'='*60}")

