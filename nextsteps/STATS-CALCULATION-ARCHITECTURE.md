# Stats Calculation Architecture

**Created: December 22, 2025**
**Purpose: Design the stat calculation system for accuracy, maintainability, and performance**

---

## Architecture Overview

```
Raw Data (Databases)
    ↓
Extractors (Pull & Transform)
    ↓
Data Models (Structured Objects)
    ↓
Calculators (Compute Stats)
    ↓
Stats Cache (Store Results)
    ↓
Dashboard (Display)
```

---

## File Structure

```
stats/
├── __init__.py
├── orchestrator.py              # Main coordinator
├── cache.py                     # Caching system
│
├── extractors/                  # Pull raw data from DBs
│   ├── __init__.py
│   ├── base_extractor.py        # Base class
│   ├── message_extractor.py     # Extract bubbleId data
│   ├── session_extractor.py     # Extract composerData
│   ├── diff_extractor.py        # Extract codeBlockDiff
│   ├── daily_stats_extractor.py # Extract dailyStats
│   ├── tracking_extractor.py    # Extract aiCodeTrackingLines
│   ├── context_extractor.py     # Extract messageRequestContext
│   ├── agent_extractor.py       # Extract agentKv
│   ├── workspace_extractor.py   # Extract from workspaces
│   ├── file_history_extractor.py # Extract file history
│   └── error_extractor.py       # Extract error data
│
├── calculators/                 # Calculate stats from data
│   ├── __init__.py
│   ├── base_calculator.py       # Base class with common utilities
│   ├── message_calculator.py    # Stats 1-66 (Messages)
│   ├── session_calculator.py    # Stats 67-93 (Sessions)
│   ├── code_calculator.py       # Stats 94-105 (Code & Diffs)
│   ├── daily_calculator.py      # Stats 106-111 (Daily Usage)
│   ├── workspace_calculator.py  # Stats 112-117 (Workspaces)
│   ├── file_calculator.py       # Stats 118-122 (File History)
│   ├── error_calculator.py      # Stats 123-149 (Errors)
│   ├── terminal_calculator.py   # Stats 150-153 (Terminal)
│   ├── context_calculator.py    # Stats 154-163 (Context)
│   ├── agent_calculator.py      # Stats 165-169 (Agent)
│   ├── effectiveness_calculator.py # Stats 170-200 (Effectiveness)
│   ├── productivity_calculator.py  # Stats 201-210 (Productivity)
│   ├── patterns_calculator.py   # Stats 211-217 (Patterns)
│   ├── correlation_calculator.py # Stats 218-223 (Correlations)
│   └── detection_calculator.py  # Stats 224-232 (Advanced)
│
└── models/                      # Data models
    ├── __init__.py
    ├── message.py               # Message data class
    ├── session.py               # Session data class
    ├── code_diff.py             # CodeDiff data class
    ├── daily_stat.py            # DailyStat data class
    ├── error.py                 # Error data class
    └── stat_result.py           # StatResult data class
```

---

## Design Principles

### 1. Separation of Concerns
- **Extractors** only pull and transform raw data
- **Calculators** only compute stats from clean data
- **No mixing** of extraction and calculation logic

### 2. Single Responsibility
- Each extractor handles one data source
- Each calculator handles one category of stats
- Each file has one clear job

### 3. Dependency Injection
- Calculators receive data, don't pull it themselves
- Easy to test with mock data
- Clear data flow

### 4. Immutability
- Extracted data is read-only
- Calculations don't modify source data
- Predictable behavior

### 5. Testability
- Each component testable in isolation
- Mock data for testing calculators
- Mock DBs for testing extractors

---

## Layer 1: Extractors

### Purpose
Pull raw data from databases and transform into clean, typed objects.

### Base Extractor

```python
# extractors/base_extractor.py
from abc import ABC, abstractmethod
from typing import Any, List
from pathlib import Path

class BaseExtractor(ABC):
    """Base class for all extractors."""
    
    def __init__(self, db_path: Path):
        self.db_path = db_path
        self.db = None
    
    @abstractmethod
    def extract(self) -> List[Any]:
        """Extract and return data."""
        pass
    
    def connect(self):
        """Connect to database."""
        # Use our existing CursorDatabase class
        pass
    
    def disconnect(self):
        """Disconnect from database."""
        pass
    
    def __enter__(self):
        self.connect()
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.disconnect()
```

### Example: Message Extractor

```python
# extractors/message_extractor.py
from typing import List
import json
from .base_extractor import BaseExtractor
from models.message import Message

class MessageExtractor(BaseExtractor):
    """Extract bubbleId messages from database."""
    
    def extract(self) -> List[Message]:
        """
        Extract all messages from cursorDiskKV table.
        
        Returns:
            List of Message objects
        """
        messages = []
        
        # Get all bubbleId entries
        cursor = self.db.execute(
            "SELECT key, value FROM cursorDiskKV WHERE key LIKE 'bubbleId:%'"
        )
        
        for key, value in cursor:
            try:
                # Parse JSON
                data = json.loads(value) if isinstance(value, str) else json.loads(value.decode('utf-8'))
                
                # Create Message object
                message = Message.from_dict(data)
                messages.append(message)
                
            except Exception as e:
                # Log error but continue
                print(f"Error parsing message {key}: {e}")
                continue
        
        return messages
    
    def extract_by_session(self, session_id: str) -> List[Message]:
        """Extract messages for specific session."""
        # Filtered extraction
        pass
    
    def extract_date_range(self, start_date, end_date) -> List[Message]:
        """Extract messages in date range."""
        # Date-filtered extraction
        pass
```

### Why This Works
✅ **Single responsibility** - Only extracts messages
✅ **Clean output** - Returns typed objects
✅ **Error handling** - Continues on individual errors
✅ **Flexible** - Multiple extraction methods
✅ **Testable** - Can mock database

---

## Layer 2: Data Models

### Purpose
Strongly-typed data structures for all extracted data.

### Example: Message Model

```python
# models/message.py
from dataclasses import dataclass, field
from typing import Optional, List, Dict, Any
from datetime import datetime

@dataclass
class Message:
    """Represents a single message (bubbleId entry)."""
    
    # Required fields
    id: str
    composer_id: str
    type: int  # 1=user, 2=AI
    created_at: datetime
    
    # Content fields
    text: Optional[str] = None
    code_blocks: List[Dict[str, Any]] = field(default_factory=list)
    
    # Thinking fields
    thinking: Optional[str] = None
    thinking_duration_ms: Optional[int] = None
    
    # Tool fields
    tool_results: List[Dict[str, Any]] = field(default_factory=list)
    
    # Context fields
    attached_code_chunks: List[Dict[str, Any]] = field(default_factory=list)
    codebase_context_chunks: List[Dict[str, Any]] = field(default_factory=list)
    
    # Model fields
    model_info: Optional[Dict[str, Any]] = None
    token_count: Optional[Dict[str, int]] = None
    
    # Error fields
    lints: List[Dict[str, Any]] = field(default_factory=list)
    console_logs: List[Dict[str, Any]] = field(default_factory=list)
    
    # ... more fields
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Message':
        """Create Message from dictionary."""
        return cls(
            id=data.get('bubbleId', ''),
            composer_id=data.get('composerId', ''),
            type=data.get('type', 0),
            created_at=datetime.fromtimestamp(data.get('createdAt', 0) / 1000),
            text=data.get('text'),
            code_blocks=data.get('codeBlocks', []),
            thinking=data.get('thinking'),
            thinking_duration_ms=data.get('thinkingDurationMs'),
            tool_results=data.get('toolResults', []),
            attached_code_chunks=data.get('attachedCodeChunks', []),
            codebase_context_chunks=data.get('codebaseContextChunks', []),
            model_info=data.get('modelInfo'),
            token_count=data.get('tokenCount'),
            lints=data.get('lints', []),
            console_logs=data.get('consoleLogs', []),
        )
    
    # Helper properties
    @property
    def is_user_message(self) -> bool:
        return self.type == 1
    
    @property
    def is_ai_message(self) -> bool:
        return self.type == 2
    
    @property
    def has_code(self) -> bool:
        return len(self.code_blocks) > 0
    
    @property
    def has_thinking(self) -> bool:
        return self.thinking is not None
    
    @property
    def has_tools(self) -> bool:
        return len(self.tool_results) > 0
    
    @property
    def has_errors(self) -> bool:
        return len(self.lints) > 0 or len(self.console_logs) > 0
    
    def get_text_length(self) -> int:
        """Get text length in characters."""
        return len(self.text) if self.text else 0
    
    def get_code_line_count(self) -> int:
        """Get total lines of code in code blocks."""
        total = 0
        for block in self.code_blocks:
            code = block.get('code', '')
            total += len(code.split('\n'))
        return total
```

### Why This Works
✅ **Type safety** - Catch errors at design time
✅ **Self-documenting** - Clear what data is available
✅ **Helper methods** - Common operations built-in
✅ **Validation** - Can add validation in from_dict
✅ **Immutable** - Frozen dataclasses for safety

---

## Layer 3: Calculators

### Purpose
Calculate stats from extracted data models.

### Base Calculator

```python
# calculators/base_calculator.py
from abc import ABC, abstractmethod
from typing import Any, Dict, List
import numpy as np
from collections import Counter

class BaseCalculator(ABC):
    """Base class for all calculators with common utilities."""
    
    def __init__(self, data: Any):
        self.data = data
        self._cache = {}
    
    @abstractmethod
    def calculate_all(self) -> Dict[str, Any]:
        """Calculate all stats for this category."""
        pass
    
    # Common statistical functions
    def count(self, items: List[Any]) -> int:
        """Count items."""
        return len(items)
    
    def percentage(self, part: int, total: int) -> float:
        """Calculate percentage."""
        return (part / total * 100) if total > 0 else 0.0
    
    def average(self, values: List[float]) -> float:
        """Calculate average."""
        return np.mean(values) if values else 0.0
    
    def median(self, values: List[float]) -> float:
        """Calculate median."""
        return np.median(values) if values else 0.0
    
    def percentile(self, values: List[float], p: int) -> float:
        """Calculate percentile."""
        return np.percentile(values, p) if values else 0.0
    
    def std_dev(self, values: List[float]) -> float:
        """Calculate standard deviation."""
        return np.std(values) if values else 0.0
    
    def distribution(self, values: List[float], bins: int = 10) -> Dict[str, Any]:
        """Calculate distribution histogram."""
        if not values:
            return {'bins': [], 'counts': []}
        
        counts, bin_edges = np.histogram(values, bins=bins)
        return {
            'bins': bin_edges.tolist(),
            'counts': counts.tolist()
        }
    
    def most_common(self, items: List[Any], n: int = 10) -> List[tuple]:
        """Get most common items."""
        return Counter(items).most_common(n)
    
    def group_by(self, items: List[Any], key_func) -> Dict[Any, List[Any]]:
        """Group items by key function."""
        groups = {}
        for item in items:
            key = key_func(item)
            if key not in groups:
                groups[key] = []
            groups[key].append(item)
        return groups
    
    def filter_by(self, items: List[Any], predicate) -> List[Any]:
        """Filter items by predicate."""
        return [item for item in items if predicate(item)]
    
    def cached(self, key: str, calc_func):
        """Cache calculation result."""
        if key not in self._cache:
            self._cache[key] = calc_func()
        return self._cache[key]
```

### Example: Message Calculator

```python
# calculators/message_calculator.py
from typing import Dict, Any, List
from .base_calculator import BaseCalculator
from models.message import Message

class MessageCalculator(BaseCalculator):
    """Calculate message-related stats (Stats 1-66)."""
    
    def __init__(self, messages: List[Message]):
        super().__init__(messages)
        self.messages = messages
    
    def calculate_all(self) -> Dict[str, Any]:
        """Calculate all message stats."""
        return {
            # Counts (1-4)
            'total_messages': self.stat_001_total_messages(),
            'user_messages': self.stat_002_user_messages(),
            'ai_messages': self.stat_003_ai_messages(),
            'messages_per_session': self.stat_004_messages_per_session(),
            
            # Content (5-11)
            'message_text_length': self.stat_005_message_text_length(),
            'messages_with_text': self.stat_006_messages_with_text(),
            'messages_with_code': self.stat_007_messages_with_code(),
            # ... continue for all 66 stats
        }
    
    # Individual stat methods
    def stat_001_total_messages(self) -> Dict[str, Any]:
        """Stat #1: Total messages."""
        return {
            'value': self.count(self.messages),
            'label': 'Total messages',
            'category': 'Messages',
            'data_source': 'bubbleId',
            'type': 'count'
        }
    
    def stat_002_user_messages(self) -> Dict[str, Any]:
        """Stat #2: User messages."""
        user_msgs = self.filter_by(self.messages, lambda m: m.is_user_message)
        total = len(self.messages)
        
        return {
            'value': len(user_msgs),
            'percentage': self.percentage(len(user_msgs), total),
            'label': 'User messages',
            'category': 'Messages',
            'data_source': 'bubbleId',
            'type': 'count',
            'breakdown': {
                'total': total,
                'user': len(user_msgs),
                'ai': total - len(user_msgs)
            }
        }
    
    def stat_005_message_text_length(self) -> Dict[str, Any]:
        """Stat #5: Message text length."""
        lengths = [m.get_text_length() for m in self.messages if m.text]
        
        return {
            'value': self.average(lengths),
            'median': self.median(lengths),
            'min': min(lengths) if lengths else 0,
            'max': max(lengths) if lengths else 0,
            'p95': self.percentile(lengths, 95),
            'std_dev': self.std_dev(lengths),
            'distribution': self.distribution(lengths, bins=20),
            'label': 'Message text length (characters)',
            'category': 'Messages',
            'data_source': 'bubbleId',
            'type': 'numeric',
            'sample_size': len(lengths)
        }
    
    def stat_012_messages_with_thinking(self) -> Dict[str, Any]:
        """Stat #12: Messages with thinking."""
        with_thinking = self.filter_by(self.messages, lambda m: m.has_thinking)
        total = len(self.messages)
        
        return {
            'value': len(with_thinking),
            'percentage': self.percentage(len(with_thinking), total),
            'label': 'Messages with thinking',
            'category': 'Messages',
            'data_source': 'bubbleId',
            'type': 'count',
            'breakdown': {
                'with': len(with_thinking),
                'without': total - len(with_thinking)
            }
        }
    
    # ... methods for all 66 message stats
```

### Why This Works
✅ **One stat = one method** - Easy to find and fix
✅ **Consistent output** - All stats return same structure
✅ **Rich metadata** - Label, category, source, type
✅ **Statistical depth** - Multiple measures for numeric stats
✅ **Testable** - Can test individual stat methods
✅ **Cacheable** - Results can be cached

---

## Layer 4: Orchestrator

### Purpose
Coordinate extraction and calculation, manage dependencies, provide caching.

```python
# stats/orchestrator.py
from typing import Dict, Any, List, Optional
from pathlib import Path
import pickle
from datetime import datetime, timedelta

from extractors.message_extractor import MessageExtractor
from extractors.session_extractor import SessionExtractor
# ... import all extractors

from calculators.message_calculator import MessageCalculator
from calculators.session_calculator import SessionCalculator
# ... import all calculators

from .cache import StatsCache

class StatsOrchestrator:
    """Coordinates data extraction and stat calculation."""
    
    def __init__(self, db_path: Path, cache_dir: Path = None):
        self.db_path = db_path
        self.cache = StatsCache(cache_dir) if cache_dir else None
        
        # Extracted data (loaded once)
        self._messages = None
        self._sessions = None
        self._diffs = None
        # ... other data
    
    def extract_all_data(self, force: bool = False):
        """
        Extract all data from databases.
        
        Args:
            force: Force re-extraction even if cached
        """
        # Check cache first
        if not force and self.cache:
            cached_data = self.cache.load_extracted_data()
            if cached_data:
                self._messages = cached_data['messages']
                self._sessions = cached_data['sessions']
                # ... load other data
                return
        
        print("Extracting data from databases...")
        
        # Extract messages
        with MessageExtractor(self.db_path) as extractor:
            self._messages = extractor.extract()
        print(f"  Extracted {len(self._messages)} messages")
        
        # Extract sessions
        with SessionExtractor(self.db_path) as extractor:
            self._sessions = extractor.extract()
        print(f"  Extracted {len(self._sessions)} sessions")
        
        # Extract diffs
        with DiffExtractor(self.db_path) as extractor:
            self._diffs = extractor.extract()
        print(f"  Extracted {len(self._diffs)} diffs")
        
        # ... extract all other data
        
        # Cache extracted data
        if self.cache:
            self.cache.save_extracted_data({
                'messages': self._messages,
                'sessions': self._sessions,
                'diffs': self._diffs,
                # ... other data
            })
    
    def calculate_all_stats(self, force: bool = False) -> Dict[str, Any]:
        """
        Calculate all stats.
        
        Args:
            force: Force recalculation even if cached
            
        Returns:
            Dictionary of all stats organized by category
        """
        # Check cache
        if not force and self.cache:
            cached_stats = self.cache.load_stats()
            if cached_stats:
                return cached_stats
        
        # Ensure data is extracted
        if self._messages is None:
            self.extract_all_data()
        
        print("Calculating stats...")
        all_stats = {}
        
        # Calculate message stats (1-66)
        print("  Calculating message stats...")
        message_calc = MessageCalculator(self._messages)
        all_stats['messages'] = message_calc.calculate_all()
        
        # Calculate session stats (67-93)
        print("  Calculating session stats...")
        session_calc = SessionCalculator(self._sessions, self._messages)
        all_stats['sessions'] = session_calc.calculate_all()
        
        # Calculate code stats (94-105)
        print("  Calculating code stats...")
        code_calc = CodeCalculator(self._diffs, self._tracking_lines)
        all_stats['code'] = code_calc.calculate_all()
        
        # ... calculate all other categories
        
        # Calculate derived stats (effectiveness, etc.)
        print("  Calculating effectiveness stats...")
        effectiveness_calc = EffectivenessCalculator(
            messages=self._messages,
            sessions=self._sessions,
            daily_stats=self._daily_stats
        )
        all_stats['effectiveness'] = effectiveness_calc.calculate_all()
        
        # Cache results
        if self.cache:
            self.cache.save_stats(all_stats)
        
        return all_stats
    
    def calculate_category(self, category: str) -> Dict[str, Any]:
        """Calculate stats for single category."""
        # Implement targeted calculation
        pass
    
    def get_stat(self, stat_id: str) -> Optional[Dict[str, Any]]:
        """Get a single stat by ID."""
        all_stats = self.calculate_all_stats()
        
        # Search through categories
        for category, stats in all_stats.items():
            for stat_name, stat_data in stats.items():
                if stat_name == stat_id or stat_data.get('id') == stat_id:
                    return stat_data
        
        return None
    
    def invalidate_cache(self):
        """Clear cached data and stats."""
        if self.cache:
            self.cache.clear()
        self._messages = None
        self._sessions = None
        # ... clear all data
```

### Why This Works
✅ **Single entry point** - One place to get stats
✅ **Lazy loading** - Only loads what's needed
✅ **Caching** - Avoids recalculation
✅ **Dependencies** - Manages data dependencies
✅ **Flexible** - Can calculate all or partial stats

---

## Layer 5: Caching

### Purpose
Store extracted data and calculated stats for performance.

```python
# stats/cache.py
from pathlib import Path
import pickle
import json
from datetime import datetime, timedelta
from typing import Any, Dict, Optional

class StatsCache:
    """Manage caching of extracted data and calculated stats."""
    
    def __init__(self, cache_dir: Path):
        self.cache_dir = Path(cache_dir)
        self.cache_dir.mkdir(parents=True, exist_ok=True)
        
        self.data_cache_file = self.cache_dir / "extracted_data.pkl"
        self.stats_cache_file = self.cache_dir / "calculated_stats.pkl"
        self.metadata_file = self.cache_dir / "cache_metadata.json"
    
    def save_extracted_data(self, data: Dict[str, Any]):
        """Save extracted data to cache."""
        with open(self.data_cache_file, 'wb') as f:
            pickle.dump(data, f)
        
        self._update_metadata('data')
    
    def load_extracted_data(self) -> Optional[Dict[str, Any]]:
        """Load extracted data from cache."""
        if not self.data_cache_file.exists():
            return None
        
        # Check if cache is stale (> 1 hour old)
        if self._is_stale('data', hours=1):
            return None
        
        with open(self.data_cache_file, 'rb') as f:
            return pickle.load(f)
    
    def save_stats(self, stats: Dict[str, Any]):
        """Save calculated stats to cache."""
        with open(self.stats_cache_file, 'wb') as f:
            pickle.dump(stats, f)
        
        self._update_metadata('stats')
    
    def load_stats(self) -> Optional[Dict[str, Any]]:
        """Load calculated stats from cache."""
        if not self.stats_cache_file.exists():
            return None
        
        # Check if cache is stale (> 5 minutes old)
        if self._is_stale('stats', minutes=5):
            return None
        
        with open(self.stats_cache_file, 'rb') as f:
            return pickle.load(f)
    
    def clear(self):
        """Clear all cached data."""
        if self.data_cache_file.exists():
            self.data_cache_file.unlink()
        if self.stats_cache_file.exists():
            self.stats_cache_file.unlink()
        if self.metadata_file.exists():
            self.metadata_file.unlink()
    
    def _update_metadata(self, cache_type: str):
        """Update cache metadata."""
        metadata = {}
        if self.metadata_file.exists():
            with open(self.metadata_file, 'r') as f:
                metadata = json.load(f)
        
        metadata[cache_type] = {
            'timestamp': datetime.now().isoformat(),
            'size': self._get_cache_size(cache_type)
        }
        
        with open(self.metadata_file, 'w') as f:
            json.dump(metadata, f, indent=2)
    
    def _is_stale(self, cache_type: str, hours: int = 0, minutes: int = 0) -> bool:
        """Check if cache is stale."""
        if not self.metadata_file.exists():
            return True
        
        with open(self.metadata_file, 'r') as f:
            metadata = json.load(f)
        
        if cache_type not in metadata:
            return True
        
        timestamp = datetime.fromisoformat(metadata[cache_type]['timestamp'])
        age = datetime.now() - timestamp
        max_age = timedelta(hours=hours, minutes=minutes)
        
        return age > max_age
    
    def _get_cache_size(self, cache_type: str) -> int:
        """Get cache file size in bytes."""
        cache_file = self.data_cache_file if cache_type == 'data' else self.stats_cache_file
        return cache_file.stat().st_size if cache_file.exists() else 0
```

---

## Usage Example

```python
# In your app or CLI
from pathlib import Path
from stats.orchestrator import StatsOrchestrator

# Initialize
db_path = Path.home() / 'AppData/Roaming/Cursor/User/globalStorage/state.vscdb'
cache_dir = Path('.cache/stats')

orchestrator = StatsOrchestrator(db_path, cache_dir)

# Extract all data (runs once, then cached)
orchestrator.extract_all_data()

# Calculate all stats (fast with cache)
all_stats = orchestrator.calculate_all_stats()

# Access specific categories
message_stats = all_stats['messages']
session_stats = all_stats['sessions']

# Get specific stat
total_messages = orchestrator.get_stat('total_messages')
print(f"Total messages: {total_messages['value']}")

# Force refresh (ignore cache)
fresh_stats = orchestrator.calculate_all_stats(force=True)
```

---

## Testing Strategy

### Unit Tests

```python
# tests/test_message_calculator.py
import pytest
from datetime import datetime
from models.message import Message
from calculators.message_calculator import MessageCalculator

def test_stat_001_total_messages():
    """Test total messages calculation."""
    messages = [
        Message(id='1', composer_id='s1', type=1, created_at=datetime.now()),
        Message(id='2', composer_id='s1', type=2, created_at=datetime.now()),
        Message(id='3', composer_id='s2', type=1, created_at=datetime.now()),
    ]
    
    calc = MessageCalculator(messages)
    result = calc.stat_001_total_messages()
    
    assert result['value'] == 3
    assert result['label'] == 'Total messages'
    assert result['category'] == 'Messages'

def test_stat_002_user_messages():
    """Test user messages calculation."""
    messages = [
        Message(id='1', composer_id='s1', type=1, created_at=datetime.now()),
        Message(id='2', composer_id='s1', type=2, created_at=datetime.now()),
        Message(id='3', composer_id='s2', type=1, created_at=datetime.now()),
    ]
    
    calc = MessageCalculator(messages)
    result = calc.stat_002_user_messages()
    
    assert result['value'] == 2
    assert result['percentage'] == pytest.approx(66.67, 0.01)
```

### Integration Tests

```python
# tests/test_orchestrator.py
import pytest
from pathlib import Path
from stats.orchestrator import StatsOrchestrator

def test_full_extraction_and_calculation(tmp_path):
    """Test full pipeline."""
    # Use test database
    test_db = Path('tests/fixtures/test_db.vscdb')
    cache_dir = tmp_path / 'cache'
    
    orch = StatsOrchestrator(test_db, cache_dir)
    
    # Extract
    orch.extract_all_data()
    assert orch._messages is not None
    assert len(orch._messages) > 0
    
    # Calculate
    stats = orch.calculate_all_stats()
    assert 'messages' in stats
    assert 'sessions' in stats
    
    # Check specific stat
    total = stats['messages']['total_messages']
    assert total['value'] > 0
```

---

## Accuracy Validation

### Validation Script

```python
# scripts/validate_stats.py
"""
Validate stat calculations against known ground truth.
"""

from stats.orchestrator import StatsOrchestrator
from pathlib import Path

def validate_message_counts():
    """Validate message counts match database."""
    orch = StatsOrchestrator(db_path)
    
    # Get calculated stat
    stats = orch.calculate_all_stats()
    calculated_total = stats['messages']['total_messages']['value']
    
    # Query database directly
    with orch.db.connect() as conn:
        cursor = conn.execute(
            "SELECT COUNT(*) FROM cursorDiskKV WHERE key LIKE 'bubbleId:%'"
        )
        db_total = cursor.fetchone()[0]
    
    # Validate
    assert calculated_total == db_total, f"Mismatch: {calculated_total} != {db_total}"
    print(f"✓ Message count validated: {calculated_total}")

def validate_session_counts():
    """Validate session counts."""
    # Similar validation
    pass

# Run all validations
validate_message_counts()
validate_session_counts()
# ... more validations
```

---

## Performance Optimization

### Strategies

1. **Lazy Loading**
   - Only extract data when needed
   - Only calculate requested stats

2. **Caching**
   - Cache extracted data (expensive)
   - Cache calculated stats (cheap but frequent)
   - Different TTLs for different cache levels

3. **Batch Processing**
   - Extract all data in one pass
   - Calculate related stats together

4. **Incremental Updates**
   - Only recalculate changed stats
   - Track dependencies between stats

5. **Parallel Processing**
   - Calculate independent stat categories in parallel
   - Use multiprocessing for CPU-bound calculations

---

## Maintainability Features

### Adding New Stats

```python
# To add a new stat:

# 1. Add method to appropriate calculator
def stat_XXX_new_metric(self) -> Dict[str, Any]:
    """Stat #XXX: New metric description."""
    # Calculate metric
    value = ...
    
    return {
        'value': value,
        'label': 'New metric',
        'category': 'Messages',
        'data_source': 'bubbleId',
        'type': 'count'
    }

# 2. Add to calculate_all() method
def calculate_all(self) -> Dict[str, Any]:
    return {
        # ... existing stats
        'new_metric': self.stat_XXX_new_metric(),
    }

# 3. Add test
def test_stat_XXX_new_metric():
    # Test implementation
    pass

# That's it! No other changes needed.
```

### Debugging

```python
# Enable debug logging
orchestrator.set_log_level('DEBUG')

# Validate specific stat
orchestrator.validate_stat('total_messages')

# Export stat calculation details
orchestrator.export_stat_debug_info('total_messages', 'debug.json')
```

---

## Summary

### File Organization
- ✅ **10 extractors** (one per data source)
- ✅ **15 calculators** (one per stat category)
- ✅ **5 data models** (typed data structures)
- ✅ **1 orchestrator** (coordination)
- ✅ **1 cache manager** (performance)

### Benefits
- ✅ **Maintainable** - Clear separation, easy to find code
- ✅ **Testable** - Each component tested independently
- ✅ **Accurate** - Validation scripts ensure correctness
- ✅ **Performant** - Caching and lazy loading
- ✅ **Extensible** - Easy to add new stats
- ✅ **Debuggable** - Clear data flow, logging at each step

### Development Workflow
1. Extract data (once, cached)
2. Implement stat calculation (one method)
3. Test stat calculation (unit test)
4. Validate against database (integration test)
5. Use in dashboard (orchestrator handles everything)

---

*This architecture ensures accurate, maintainable, and performant stat calculation, Jack!*

