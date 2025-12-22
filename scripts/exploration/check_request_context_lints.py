"""Check RequestContext for linter errors."""

import sys
sys.stdout.reconfigure(encoding='utf-8')
sys.stderr.reconfigure(encoding='utf-8')

from pathlib import Path
import sys
# Add parent to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from stats.orchestrator import StatsOrchestrator
from utils.config import Config

user_home = Path.home()
global_db_path = user_home / "AppData" / "Roaming" / "Cursor" / "User" / "globalStorage" / Config.DB_FILENAME

orchestrator = StatsOrchestrator(global_db_path)
orchestrator.extract_all_data()

request_contexts = orchestrator._request_contexts

print(f"Total request contexts: {len(request_contexts):,}")

# Check for linter errors
with_linter_errors = [rc for rc in request_contexts if rc.has_linter_errors]
print(f"With linter errors: {len(with_linter_errors):,}")

if with_linter_errors:
    print(f"\nSample linter errors:")
    sample = with_linter_errors[0]
    print(f"  Context: {sample.context_id}")
    print(f"  Errors: {len(sample.multi_file_linter_errors)} files with errors")
    if sample.multi_file_linter_errors:
        import json
        print(json.dumps(sample.multi_file_linter_errors[0], indent=4)[:500])

# Check other useful fields
with_todos = [rc for rc in request_contexts if rc.has_todos]
with_git = [rc for rc in request_contexts if rc.has_git_changes]
with_file_context = [rc for rc in request_contexts if rc.has_file_context]

print(f"\nWith TODOs: {len(with_todos):,}")
print(f"With git changes: {len(with_git):,}")
print(f"With file context: {len(with_file_context):,}")

