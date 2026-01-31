# JGTCore Application Specification

> Master specification for the JGT Core Configuration Library

**Specification Version**: 1.0  
**RISE Framework Compliance**: Full  
**Last Updated**: 2026-01-31

---

## Desired Outcome Definition

**What Users Create**: A unified configuration and settings layer that enables all JGT trading packages to access credentials, preferences, and environment settings through a single consistent interface.

**Achievement Indicator**: Developers can access broker credentials, application settings, and environment state through `jgtcore` without worrying about file locations, environment variables, or configuration cascading.

**Value Proposition**: Separate core configuration logic from CLI dependencies, enabling pure programmatic access to JGT settings for any trading application.

---

## Application Overview

JGTCore is a Python library that:
1. Provides pure programmatic access to JGT configuration and settings
2. Implements hierarchical configuration lookup (system → user → process)
3. Supports demo/live mode credential switching
4. Exports configuration to environment variables
5. Caches settings for performance

---

## Structural Tension

**Current Reality**: Trading packages need credentials and settings from various locations (files, environment variables, command-line), with complex lookup logic repeated across packages.

**Desired State**: All JGT packages import `jgtcore` for unified configuration access, with automatic cascading, caching, and environment export.

**Natural Progression**: Centralized configuration management reduces code duplication and ensures consistent behavior across the entire JGT ecosystem.

---

## Core API

### Configuration Access

```python
import jgtcore

# Simple access
config = jgtcore.get_config()
demo_config = jgtcore.get_config(demo=True)

# Get specific value with default
user_id = jgtcore.get_config_value('user_id')
quotes_count = jgtcore.get_config_value('quotes_count', 1000)
```

### Settings Access

```python
import jgtcore

# Get all settings (cached)
settings = jgtcore.get_settings()

# Get specific setting with default
instrument = jgtcore.get_setting('instrument', 'EUR/USD')
timeframes = jgtcore.get_setting('_timeframes', 'D1')
```

### Environment Setup

```python
import jgtcore

# One-call environment setup
config, settings = jgtcore.setup_environment(demo=True)

# Check demo mode
if jgtcore.is_demo_mode():
    print("Running in demo mode")
```

---

## Configuration Lookup Order

### config.json
1. Current directory: `./config.json`
2. User home: `~/.jgt/config.json`
3. System: `/etc/jgt/config.json`
4. Environment: `JGT_CONFIG`, `JGT_CONFIG_PATH`, `JGT_CONFIG_JSON_SECRET`

### settings.json
1. System: `/etc/jgt/settings.json`
2. User home: `~/.jgt/settings.json`
3. Current directory: `./.jgt/settings.json`
4. YAML variants: `jgt.yml`, `_config.yml`
5. Environment: `JGT_SETTINGS`, `JGT_SETTINGS_PROCESS`

---

## Type Definitions

```python
from typing import Dict, Any, Optional, Tuple

def get_config(demo: bool = False) -> Dict[str, Any]: ...
def get_config_value(key: str, default: Any = None) -> Any: ...
def get_settings() -> Dict[str, Any]: ...
def get_setting(key: str, default: Any = None) -> Any: ...
def setup_environment(demo: bool = False) -> Tuple[Dict, Dict]: ...
def is_demo_mode() -> bool: ...
def readconfig(
    demo: bool = False, 
    export_env: bool = False,
    config_path: Optional[str] = None
) -> Dict[str, Any]: ...
def load_settings(custom_path: Optional[str] = None) -> Dict[str, Any]: ...
```

---

## Creative Advancement Scenarios

### Scenario: First-Time Package Access

**Desired Outcome**: New package imports jgtcore and immediately accesses broker credentials

**Current Reality**: Developer creates new trading tool needing config access

**Natural Progression**:
1. Import jgtcore: `import jgtcore`
2. Get config: `config = jgtcore.get_config()`
3. Access credentials: `user_id = config['user_id']`
4. Automatic file discovery and caching handles complexity

**Resolution**: Developer never writes file-reading logic; config "just works"

### Scenario: Demo/Live Mode Switching

**Desired Outcome**: Application seamlessly switches between demo and live credentials

**Current Reality**: Application starts with `--demo` flag or `JGT_DEMO=true`

**Natural Progression**:
1. Check mode: `jgtcore.is_demo_mode()`
2. Load appropriate config: `config = jgtcore.get_config(demo=True)`
3. Demo credentials replace live if present in config

**Resolution**: Single boolean controls entire credential set

---

## Module Structure

```
jgtcore/
├── __init__.py          # Public API exports
├── core.py              # Main configuration logic
├── constants.py         # Shared constants
├── compatibility.py     # Cross-version compatibility
├── env/                 # Environment detection
├── fx/                  # FX-specific helpers
├── logging/             # Logging configuration
├── os/                  # OS-specific utilities
└── timeframe.py         # Timeframe parsing
```

---

## Integration with JGT Ecosystem

```
jgtcore (this package)
    ↓ used by
jgtutils (adds CLI, utilities)
    ↓ used by
jgtapy (adds indicators)
    ↓ used by
jgtfxcon (adds broker connection)
    ↓ used by
jgtpy (adds data services)
    ↓ used by
jgtml (adds ML/analysis)
    ↓ served by
jgt-data-server (REST API)
    ↓ consumed by
jgt-code (terminal agent)
```

---

## Quality Criteria

✅ **Zero CLI Dependencies**: Pure library, no argparse/click required  
✅ **Cached Settings**: Single load per process, thread-safe  
✅ **Environment Export**: Config values become environment variables  
✅ **Demo Mode Support**: Built-in credential switching  
✅ **Hierarchical Lookup**: System → User → Process precedence
