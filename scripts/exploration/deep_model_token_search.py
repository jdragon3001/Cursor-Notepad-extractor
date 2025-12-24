#!/usr/bin/env python3
"""
DEEP SEARCH: Find ALL model and token data
Goal: Account for 100% of messages, not just the ones with obvious modelInfo
"""

import sqlite3
from pathlib import Path
import json
from collections import defaultdict
from datetime import datetime

CURSOR_BASE = Path.home() / 'AppData/Roaming/Cursor'

def safe_json(val):
    if val is None: return None
    if isinstance(val, bytes):
        try: return json.loads(val.decode('utf-8'))
        except: return None
    if isinstance(val, str):
        try: return json.loads(val)
        except: return val
    return val

def search_for_model_in_dict(d, path=""):
    """Recursively search a dict for any model-related keys."""
    findings = []
    if not isinstance(d, dict):
        return findings
    
    model_keywords = ['model', 'Model', 'claude', 'gpt', 'gemini', 'opus', 'sonnet']
    
    for key, value in d.items():
        current_path = f"{path}.{key}" if path else key
        
        # Check if key contains model-related terms
        if any(kw.lower() in key.lower() for kw in model_keywords):
            findings.append((current_path, value))
        
        # Check string values for model names
        if isinstance(value, str) and any(kw.lower() in value.lower() for kw in model_keywords):
            findings.append((current_path, value))
        
        # Recurse into nested dicts
        if isinstance(value, dict):
            findings.extend(search_for_model_in_dict(value, current_path))
        elif isinstance(value, list):
            for i, item in enumerate(value[:3]):  # Check first 3 items
                if isinstance(item, dict):
                    findings.extend(search_for_model_in_dict(item, f"{current_path}[{i}]"))
    
    return findings

print("=" * 70)
print("DEEP MODEL & TOKEN DATA SEARCH")
print("=" * 70)

db_path = CURSOR_BASE / 'User/globalStorage/state.vscdb'
conn = sqlite3.connect(str(db_path))
cursor = conn.cursor()

# 1. Analyze ALL bubbleId entries for model data
print("\n### 1. Analyzing ALL bubbleId entries ###")

cursor.execute("SELECT key, value FROM cursorDiskKV WHERE key LIKE 'bubbleId:%'")
all_bubbles = cursor.fetchall()

model_locations = defaultdict(int)
all_models = defaultdict(int)
messages_with_model = 0
messages_without_model = 0

# Token tracking
total_input = 0
total_output = 0
messages_with_tokens = 0

# Sample a bubble to see ALL fields
print("\nSampling bubble structure...")
sample_count = 0
all_keys_found = set()

for key, value in all_bubbles[:100]:  # Sample 100
    data = safe_json(value)
    if data and isinstance(data, dict):
        all_keys_found.update(data.keys())

print(f"ALL keys in bubbleId entries ({len(all_keys_found)}):")
for k in sorted(all_keys_found):
    print(f"  - {k}")

# Now analyze ALL bubbles
print("\nAnalyzing all bubbles for model data...")
for key, value in all_bubbles:
    data = safe_json(value)
    if not data or not isinstance(data, dict):
        continue
    
    found_model = False
    
    # Check modelInfo
    model_info = data.get('modelInfo', {})
    if isinstance(model_info, dict) and model_info:
        model_name = model_info.get('modelName', model_info.get('model'))
        if model_name:
            all_models[model_name] += 1
            model_locations['modelInfo.modelName'] += 1
            found_model = True
    
    # Check other potential model fields
    for field in ['model', 'modelType', 'selectedModel', 'currentModel', 'modelId']:
        val = data.get(field)
        if val:
            all_models[val] += 1
            model_locations[field] += 1
            found_model = True
    
    # Check timingInfo for model
    timing = data.get('timingInfo', {})
    if isinstance(timing, dict):
        model_in_timing = timing.get('model', timing.get('modelName'))
        if model_in_timing:
            all_models[model_in_timing] += 1
            model_locations['timingInfo.model'] += 1
            found_model = True
    
    # Check codeBlocks for model info
    code_blocks = data.get('codeBlocks', [])
    if isinstance(code_blocks, list):
        for block in code_blocks:
            if isinstance(block, dict):
                block_model = block.get('model', block.get('modelName'))
                if block_model:
                    all_models[block_model] += 1
                    model_locations['codeBlocks.model'] += 1
                    found_model = True
    
    if found_model:
        messages_with_model += 1
    else:
        messages_without_model += 1
    
    # Token analysis
    token_count = data.get('tokenCount', {})
    if isinstance(token_count, dict):
        inp = token_count.get('inputTokens', 0) or 0
        out = token_count.get('outputTokens', 0) or 0
        if inp > 0 or out > 0:
            total_input += inp
            total_output += out
            messages_with_tokens += 1

print(f"\nTotal bubbles analyzed: {len(all_bubbles)}")
print(f"Messages with model info: {messages_with_model}")
print(f"Messages WITHOUT model info: {messages_without_model}")
print(f"Coverage: {messages_with_model/len(all_bubbles)*100:.1f}%")

print(f"\nModel data found in these fields:")
for loc, count in sorted(model_locations.items(), key=lambda x: x[1], reverse=True):
    print(f"  {loc}: {count}")

print(f"\nModels found:")
for model, count in sorted(all_models.items(), key=lambda x: x[1], reverse=True):
    print(f"  {model}: {count}")

print(f"\nToken data:")
print(f"  Messages with token counts: {messages_with_tokens}")
print(f"  Total input tokens: {total_input:,}")
print(f"  Total output tokens: {total_output:,}")

# 2. Check composerData for additional model/token info
print("\n" + "=" * 70)
print("### 2. Checking composerData entries ###")

cursor.execute("SELECT key, value FROM cursorDiskKV WHERE key LIKE 'composerData:%'")
composer_rows = cursor.fetchall()

composer_models = defaultdict(int)
composer_tokens = 0

print("\nSampling composerData structure...")
for key, value in composer_rows[:5]:
    data = safe_json(value)
    if data and isinstance(data, dict):
        print(f"\n{key[:50]}...")
        
        # Look for model config
        model_config = data.get('modelConfig', {})
        if model_config:
            print(f"  modelConfig: {model_config}")
        
        # Look for usage data
        usage_data = data.get('usageData', {})
        if usage_data:
            print(f"  usageData: {usage_data}")
        
        # Context tokens
        ctx_tokens = data.get('contextTokensUsed', 0)
        if ctx_tokens:
            print(f"  contextTokensUsed: {ctx_tokens}")

# Aggregate from all composerData
for key, value in composer_rows:
    data = safe_json(value)
    if not data or not isinstance(data, dict):
        continue
    
    # Model config
    model_config = data.get('modelConfig', {})
    if isinstance(model_config, dict):
        model_name = model_config.get('modelName')
        if model_name and model_name != 'default':
            composer_models[model_name] += 1
    
    # Context tokens
    ctx = data.get('contextTokensUsed', 0)
    if isinstance(ctx, (int, float)):
        composer_tokens += ctx

print(f"\nModels from composerData.modelConfig:")
for model, count in sorted(composer_models.items(), key=lambda x: x[1], reverse=True):
    print(f"  {model}: {count}")

print(f"\nTotal contextTokensUsed from composerData: {composer_tokens:,}")

# 3. Check agentKv entries
print("\n" + "=" * 70)
print("### 3. Checking agentKv entries ###")

cursor.execute("SELECT key, value FROM cursorDiskKV WHERE key LIKE 'agentKv:%' LIMIT 20")
agent_rows = cursor.fetchall()

print(f"Sample agentKv entries:")
for key, value in agent_rows[:5]:
    print(f"\n{key[:60]}...")
    data = safe_json(value)
    if data:
        if isinstance(data, dict):
            print(f"  Keys: {list(data.keys())[:10]}")
            # Look for model info
            findings = search_for_model_in_dict(data)
            if findings:
                print(f"  Model-related: {findings[:3]}")
        elif isinstance(data, str):
            if any(kw in data.lower() for kw in ['model', 'claude', 'gpt']):
                print(f"  Contains model reference: {data[:100]}...")

# 4. Check ItemTable for additional model/token data
print("\n" + "=" * 70)
print("### 4. Checking ItemTable for model/token data ###")

cursor.execute("SELECT key FROM ItemTable")
all_item_keys = [row[0] for row in cursor.fetchall()]

model_related_keys = [k for k in all_item_keys if any(
    kw in k.lower() for kw in ['model', 'usage', 'token', 'billing', 'quota', 'limit']
)]

print(f"Potentially relevant ItemTable keys:")
for key in model_related_keys[:20]:
    cursor.execute("SELECT value FROM ItemTable WHERE key = ?", (key,))
    result = cursor.fetchone()
    if result:
        data = safe_json(result[0])
        if data:
            size = len(str(data))
            print(f"  {key}: {type(data).__name__} ({size} chars)")
            if isinstance(data, dict) and size < 500:
                print(f"    {data}")

# 5. Check workspace databases for model info
print("\n" + "=" * 70)
print("### 5. Checking workspace databases ###")

ws_path = CURSOR_BASE / 'User/workspaceStorage'
ws_models = defaultdict(int)
ws_tokens = 0

for ws in list(ws_path.iterdir())[:50]:  # Sample 50
    db_file = ws / 'state.vscdb'
    if not db_file.exists():
        continue
    
    try:
        ws_conn = sqlite3.connect(str(db_file))
        ws_cursor = ws_conn.cursor()
        
        # Check composer.composerData
        ws_cursor.execute("SELECT value FROM ItemTable WHERE key = 'composer.composerData'")
        result = ws_cursor.fetchone()
        
        if result:
            data = safe_json(result[0])
            if data and isinstance(data, dict):
                composers = data.get('allComposers', [])
                for comp in composers:
                    if isinstance(comp, dict):
                        # Check for model in workspace composer data
                        model_config = comp.get('modelConfig', {})
                        if isinstance(model_config, dict):
                            model = model_config.get('modelName')
                            if model and model != 'default':
                                ws_models[model] += 1
        
        # Check for aiService.prompts
        ws_cursor.execute("SELECT value FROM ItemTable WHERE key = 'aiService.prompts'")
        result = ws_cursor.fetchone()
        if result:
            data = safe_json(result[0])
            if data and isinstance(data, (list, dict)):
                # Look for model info in prompts
                if isinstance(data, list):
                    for prompt in data[:5]:
                        if isinstance(prompt, dict):
                            model = prompt.get('model', prompt.get('modelName'))
                            if model:
                                ws_models[f"prompts:{model}"] += 1
        
        ws_conn.close()
    except Exception as e:
        continue

print(f"Models found in workspace databases:")
for model, count in sorted(ws_models.items(), key=lambda x: x[1], reverse=True):
    print(f"  {model}: {count}")

# 6. Look for server config with model info
print("\n" + "=" * 70)
print("### 6. Server config and feature flags ###")

cursor.execute("SELECT value FROM ItemTable WHERE key = 'cursorai/serverConfig'")
result = cursor.fetchone()
if result:
    data = safe_json(result[0])
    if data and isinstance(data, dict):
        print("Server config keys:")
        for k in data.keys():
            print(f"  - {k}")
        
        # Look for model migrations or config
        if 'modelMigrations' in data:
            print(f"\nmodelMigrations: {data['modelMigrations']}")
        if 'chatConfig' in data:
            print(f"\nchatConfig: {json.dumps(data['chatConfig'], indent=2)[:500]}")

conn.close()

# Final summary
print("\n" + "=" * 70)
print("FINAL SUMMARY")
print("=" * 70)
print(f"""
WHAT WE FOUND:
  - Total bubbleId entries: {len(all_bubbles)}
  - Entries with model info: {messages_with_model} ({messages_with_model/len(all_bubbles)*100:.1f}%)
  - Entries WITHOUT model info: {messages_without_model}
  
TOKEN DATA:
  - From bubbleId.tokenCount: {total_input:,} input, {total_output:,} output
  - From composerData.contextTokensUsed: {composer_tokens:,}

POSSIBLE REASONS FOR GAPS:
  1. Model info only tracked for AI responses (type=2), not user messages (type=1)
  2. Some older entries may not have model field populated
  3. Token data might be tracked server-side for billing
  4. Data may have been pruned/archived

WHAT TO CHECK NEXT:
  1. Are user messages (type=1) expected to have model info?
  2. Is there a separate usage/billing database?
  3. Check Local Storage LevelDB for additional data
  4. Check IndexedDB partitions
""")

# Check message type distribution
print("\n### Message Type Distribution ###")
type_with_model = defaultdict(int)
type_without_model = defaultdict(int)

for key, value in all_bubbles:
    data = safe_json(value)
    if not data:
        continue
    
    msg_type = data.get('type', 'unknown')
    has_model = bool(data.get('modelInfo', {}).get('modelName'))
    
    if has_model:
        type_with_model[msg_type] += 1
    else:
        type_without_model[msg_type] += 1

print("Messages by type:")
for t in sorted(set(list(type_with_model.keys()) + list(type_without_model.keys()))):
    with_m = type_with_model.get(t, 0)
    without_m = type_without_model.get(t, 0)
    total = with_m + without_m
    print(f"  Type {t}: {total} total, {with_m} with model ({with_m/total*100:.1f}%)")

