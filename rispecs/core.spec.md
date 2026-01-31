# jgtcore Specification

> Core Configuration and Tracing Infrastructure

**Specification Version**: 1.0  
**Module**: `jgtcore/core.py`, `jgtcore/tracer.py`  
**RISE Framework Compliance**: Full  
**Last Updated**: 2026-01-31

---

## Desired Outcome Definition

**What Users Create**: Centralized configuration management and tracing infrastructure that all JGT packages depend on for settings and observability.

**Achievement Indicator**: Any package can:
- Load settings from `~/.jgt/config.json`
- Override with environment variables
- Trace operations for debugging
- Access consistent timeframe utilities

**Value Proposition**: Foundation layer that ensures consistent behavior across all packages.

---

## Configuration Management

### Settings Loading

```python
def get_settings(
    args: Optional[argparse.Namespace] = None,
    force_refresh: bool = False
) -> Dict[str, Any]:
    """
    Load settings from multiple sources with priority.
    
    Priority Order (highest first):
        1. Command line arguments (args)
        2. Environment variables (JGT_*)
        3. User config (~/.jgt/config.json)
        4. Pattern config (~/.jgt/patterns/{pn}.json)
        5. Package defaults
    
    Cached after first load unless force_refresh=True.
    """

def _load_settings_from_path(path: str) -> Dict[str, Any]:
    """Load settings from JSON file."""

def _load_settings_from_path_yaml(
    path: str,
    key: Optional[str] = None
) -> Dict[str, Any]:
    """Load settings from YAML file (optional dependency)."""

def update_settings(
    old_settings: Dict[str, Any],
    new_settings: Dict[str, Any],
    keys: List[str] = ["patterns"]
) -> None:
    """Merge settings, handling special keys like 'patterns' separately."""
```

### Configuration Files

```
~/.jgt/
├── config.json           # Main configuration
├── config.yaml           # YAML alternative (optional)
├── patterns/
│   ├── mz.json           # Pattern: mz columns
│   └── full.json         # Pattern: full columns
└── secrets.json          # API tokens (not committed)
```

### Config Structure

```json
{
  "columns_to_remove": ["aocolor", "accolor"],
  "patterns": {
    "mz": {
      "columns": ["mfi_sig", "zone_sig", "ao"]
    }
  },
  "ttf_columns_to_remove": [],
  "default_quotescount": 335
}
```

---

## Tracing Infrastructure

### JGTTracer Class

```python
class JGTTracer:
    """
    Tracing infrastructure for observability.
    
    Usage:
        tracer = JGTTracer("jgtml", "fdb_scanner")
        with tracer.trace_operation("scan_all", metadata) as trace_id:
            tracer.add_step("step1", input_data={...})
            # ... operation ...
            tracer.add_step("step1_complete", output_data={...})
    """
    
    def __init__(
        self,
        package_name: str,
        component_name: str
    ):
        """Initialize tracer for a package/component."""
    
    def start_operation(
        self,
        operation_name: str,
        metadata: Dict[str, Any]
    ) -> str:
        """Start a traced operation, return trace_id."""
    
    def add_step(
        self,
        step_name: str,
        input_data: Optional[Dict] = None,
        output_data: Optional[Dict] = None
    ) -> None:
        """Add a step to the current trace."""
    
    def end_operation(
        self,
        trace_id: str,
        success: bool = True,
        error: Optional[str] = None
    ) -> None:
        """End a traced operation."""
    
    @contextmanager
    def trace_operation(
        self,
        operation_name: str,
        metadata: Dict[str, Any]
    ):
        """Context manager for traced operations."""
```

### Trace Output

```json
{
  "trace_id": "fdb_scan_260131_140500",
  "package": "jgtml",
  "component": "fdb_scanner",
  "operation": "scan_all",
  "start_time": "2026-01-31T14:05:00Z",
  "steps": [
    {
      "name": "load_instruments",
      "timestamp": "2026-01-31T14:05:01Z",
      "input": {"count": 28}
    },
    {
      "name": "scan_complete",
      "timestamp": "2026-01-31T14:06:30Z",
      "output": {"signals_found": 5}
    }
  ],
  "end_time": "2026-01-31T14:06:30Z",
  "success": true
}
```

---

## Timeframe Utilities

### Point of View (POV) Functions

```python
def get_higher_tf_array(timeframe: str) -> List[str]:
    """
    Get all timeframes higher than specified.
    
    Examples:
        "H1" -> ["H4", "D1", "W1", "MN"]
        "m15" -> ["m30", "H1", "H4", "D1", "W1", "MN"]
    """

def get_lower_tf_array(timeframe: str) -> List[str]:
    """Get all timeframes lower than specified."""

def is_higher_tf(tf1: str, tf2: str) -> bool:
    """Check if tf1 is higher than tf2."""

def get_tf_minutes(timeframe: str) -> int:
    """
    Get minutes for a timeframe.
    
    Examples:
        "m1" -> 1
        "H1" -> 60
        "D1" -> 1440
    """
```

### Timeframe Constants

```python
TIMEFRAMES = [
    "m1", "m5", "m15", "m30",
    "H1", "H2", "H3", "H4", "H6", "H8",
    "D1", "W1", "MN"
]

TF_MINUTES = {
    "m1": 1, "m5": 5, "m15": 15, "m30": 30,
    "H1": 60, "H2": 120, "H3": 180, "H4": 240,
    "H6": 360, "H8": 480, "D1": 1440,
    "W1": 10080, "MN": 43200
}
```

---

## Exception Handling

```python
def print_exception(e: Exception) -> None:
    """
    Print exception with traceback.
    
    Handles:
        - Standard exceptions
        - System exits
        - Keyboard interrupts
    """

def handle_keyboard_interrupt():
    """Clean handler for Ctrl+C."""
```

---

## Environment Variables

```python
# Data paths
JGTPY_DATA = os.getenv("JGTPY_DATA", "/src/jgtml/data/current")
JGTPY_DATA_FULL = os.getenv("JGTPY_DATA_FULL", "/var/lib/jgt/full/data")

# Configuration
JGT_CONFIG = os.getenv("JGT_CONFIG", "~/.jgt/config.json")

# Broker connection
FXCON_CONFIG = os.getenv("FXCON_CONFIG")

# Tracing
JGT_TRACE_ENABLED = os.getenv("JGT_TRACE_ENABLED", "false")
JGT_TRACE_OUTPUT = os.getenv("JGT_TRACE_OUTPUT", "~/.jgt/traces/")
```

---

## CLI Argument Parsing

```python
def new_parser(
    description: str,
    epilog: str = "",
    prog_name: str = "",
    add_exiting_quietly_flag: bool = False
) -> argparse.ArgumentParser:
    """Create new argument parser with JGT defaults."""

def add_instrument_timeframe_arguments(
    parser: argparse.ArgumentParser
) -> argparse.ArgumentParser:
    """Add -i and -t arguments."""

def add_use_fresh_argument(
    parser: argparse.ArgumentParser
) -> argparse.ArgumentParser:
    """Add --fresh argument."""

def add_verbose_argument(
    parser: argparse.ArgumentParser
) -> argparse.ArgumentParser:
    """Add -v/--verbose argument."""

def parse_args(
    parser: argparse.ArgumentParser
) -> argparse.Namespace:
    """Parse arguments with JGT defaults applied."""
```

---

## Dependencies

```python
import json
import os
import sys
import traceback
from datetime import datetime, time, timedelta, timezone
from typing import Any, Dict, Optional, Tuple

# Optional
import ruamel.yaml  # YAML support
```

---

## Quality Criteria

✅ **Central Config**: Single settings source for all packages  
✅ **Priority Cascade**: CLI > ENV > File > Defaults  
✅ **Tracing**: Full observability infrastructure  
✅ **TF Utilities**: Consistent timeframe handling  
✅ **Graceful Fallbacks**: Works without optional dependencies
