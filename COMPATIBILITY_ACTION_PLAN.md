# jgtpy & jgtml Compatibility Action Plan
## Comprehensive Migration Strategy for jgtcore Integration

### 🎯 **EXECUTIVE SUMMARY**

After analyzing both jgtpy and jgtml codebases, **59 Python files** need updates to ensure compatibility with the migrated jgtcore library. The migration affects **25+ CLI tools**, core data processing pipelines, and trading automation systems.

**Critical Dependencies Identified:**
- **jgtpy**: 28 files importing jgtutils across CLI, data services, and infrastructure
- **jgtml**: 31 files importing jgtutils across ML pipelines, CLI tools, and trading systems  
- **Key Risk Areas**: CLI frameworks, constants, file operations, trading logic

---

## 📋 **DELEGATION PLAN - SPECIFIC PROMPTS**

### **PHASE 1: IMMEDIATE COMPATIBILITY FIXES**

#### **Task 1.1: Update jgtpy Dependencies**
**Prompt for execution:**
```
Update the jgtpy project dependencies to support the migrated jgtcore library:

1. **Update pyproject.toml dependencies:**
   - Change `jgtutils>=1.0.11` to `jgtutils>=1.0.11,jgtcore>=0.2.0` 
   - Add graceful fallback support during transition

2. **Create compatibility imports** in jgtpy/__init__.py:
   ```python
   # Add backward compatibility layer
   try:
       from jgtcore import *
       JGTCORE_AVAILABLE = True
   except ImportError:
       JGTCORE_AVAILABLE = False
       # Continue with jgtutils for now
   ```

3. **Test basic import compatibility** by running:
   ```bash
   cd /src/jgtpy && python -c "import jgtpy; print('Import successful')"
   ```

Files to modify: `/src/jgtpy/pyproject.toml`, `/src/jgtpy/jgtpy/__init__.py`
```

#### **Task 1.2: Update jgtml Dependencies**  
**Prompt for execution:**
```
Update the jgtml project dependencies to support the migrated jgtcore library:

1. **Update pyproject.toml dependencies:**
   - Add explicit jgtcore dependency: `jgtcore>=0.2.0`
   - Ensure jgtpy and jgtutils remain compatible during transition
   
2. **Add version detection** in jgtml/__init__.py:
   ```python
   # Check available libraries and versions
   try:
       import jgtcore
       JGTCORE_VERSION = jgtcore.__version__
   except ImportError:
       JGTCORE_VERSION = None
   
   try: 
       import jgtutils
       JGTUTILS_VERSION = jgtutils.version
   except ImportError:
       JGTUTILS_VERSION = None
   ```

3. **Test compatibility** by verifying all CLI tools still import correctly.

Files to modify: `/src/jgtml/pyproject.toml`, `/src/jgtml/jgtml/__init__.py`
```

### **PHASE 2: CLI FRAMEWORK MIGRATION**

#### **Task 2.1: Migrate jgtpy CLI Tools**
**Prompt for execution:**
```
Migrate jgtpy CLI tools from jgtutils.jgtcommon to jgtcore.cli:

**Priority Files to Update (High Impact):**
- `/src/jgtpy/jgtpy/jgtcli.py`
- `/src/jgtpy/jgtpy/cdscli.py` 
- `/src/jgtpy/jgtpy/jgtapycli.py`
- `/src/jgtpy/jgtpy/JGTADS.py`

**Migration Pattern:**
```python
# OLD (jgtutils)
from jgtutils import jgtcommon
parser = jgtcommon.new_parser(description)
args = jgtcommon.parse_args(parser)

# NEW (jgtcore compatible)
try:
    from jgtcore.cli import new_parser, parse_args
except ImportError:
    from jgtutils.jgtcommon import new_parser, parse_args

parser = new_parser(description)
args = parse_args(parser)
```

**Systematic approach:**
1. Search for `from jgtutils import jgtcommon` in each file
2. Replace with compatibility import pattern above
3. Update function calls to use direct imports
4. Test each CLI tool: `python -m jgtpy.jgtcli --help`

**Validation:** All CLI tools should display help correctly and maintain existing functionality.
```

#### **Task 2.2: Migrate jgtml CLI Tools**
**Prompt for execution:**  
```
Migrate jgtml CLI tools from jgtutils.jgtcommon to jgtcore.cli:

**Priority Files to Update (High Impact):**
- `/src/jgtml/jgtml/jgtmlcli.py`
- `/src/jgtml/jgtml/mlfcli.py`
- `/src/jgtml/jgtml/ttfcli.py`
- `/src/jgtml/jgtml/mxcli.py`
- `/src/jgtml/jgtml/automated_fdb_trading_system.py`

**Migration Pattern:**
```python
# OLD  
from jgtutils import jgtcommon
parser = jgtcommon.new_parser(TTFCLI_DESCRIPTION, TTFCLI_EPILOG, TTFCLI_PROG_NAME)
parser = jgtcommon.add_instrument_timeframe_arguments(parser)
args = jgtcommon.parse_args(parser)

# NEW
try:
    from jgtcore.cli import new_parser, parse_args, add_settings_argument
    from jgtcore.cli.common import load_arg_default_from_settings
except ImportError:
    from jgtutils.jgtcommon import new_parser, parse_args, add_settings_argument
    from jgtutils.jgtcommon import load_arg_default_from_settings

parser = new_parser(TTFCLI_DESCRIPTION, TTFCLI_EPILOG, TTFCLI_PROG_NAME)
# Add instrument/timeframe args - may need custom implementation
args = parse_args(parser)
```

**Additional CLI tools to update:**
- `fdbscan.py`, `pncli.py`, `jgtalligator.py`, `enhancedfdbscan.py`

**Test each tool:** Verify `--help` and basic functionality works.
```

### **PHASE 3: CONSTANTS AND CONFIGURATION MIGRATION**

#### **Task 3.1: Migrate jgtpy Constants Usage**
**Prompt for execution:**
```
Migrate jgtpy from jgtutils.jgtconstants to jgtcore equivalents:

**High Priority Files (Heavy Constants Usage):**
- `/src/jgtpy/jgtpy/JGTIDS.py` (has wildcard import!)
- `/src/jgtpy/jgtpy/JGTCDS.py`
- `/src/jgtpy/jgtpy/JGTADS.py`
- `/src/jgtpy/jgtpy/jgtapyhelper.py`

**Migration Strategy:**

1. **Handle wildcard imports** (JGTIDS.py):
   ```python
   # OLD - DANGEROUS!
   from jgtutils.jgtconstants import *
   
   # NEW - Explicit imports
   try:
       from jgtcore.constants import (
           NB_BARS_BY_DEFAULT_IN_CDS, JAW, TEETH, LIPS, 
           OPEN, HIGH, LOW, CLOSE, FH, FL, MFI, AO, AC
       )
   except ImportError:
       from jgtutils.jgtconstants import (
           NB_BARS_BY_DEFAULT_IN_CDS, JAW, TEETH, LIPS,
           OPEN, HIGH, LOW, CLOSE, FH, FL, MFI, AO, AC  
       )
   ```

2. **Most Critical Constants to Migrate:**
   - `NB_BARS_BY_DEFAULT_IN_CDS`
   - Column names: `JAW`, `TEETH`, `LIPS`, `OPEN`, `HIGH`, `LOW`, `CLOSE`
   - Fractal constants: `FH`, `FL`, `FH3`, `FL3`, `FH5`, `FL5`
   - MFI constants: `MFI`, `MFI_SQUAT`, `MFI_GREEN`, `MFI_FADE`
   - IDS column normalization: `IDS_COLUMNS_TO_NORMALIZE`

3. **Check if constants exist in jgtcore** - if not, may need to add them to jgtcore.constants module.

**Validation:** Run data processing tests to ensure column operations still work.
```

#### **Task 3.2: Migrate jgtml Constants Usage**
**Prompt for execution:**
```
Migrate jgtml from jgtutils.jgtconstants to jgtcore equivalents:

**High Priority Files:**
- `/src/jgtml/jgtml/jtc.py` (heavy constants usage)
- `/src/jgtml/jgtml/mldatahelper.py`
- `/src/jgtml/jgtml/ptottf.py`  
- `/src/jgtml/jgtml/unified_trading_system.py`

**Key Constants Used in jgtml:**
```python
# Most critical constants to migrate
try:
    from jgtcore.constants import (
        # Core trading constants
        VECTOR_AO_FDBS, VECTOR_AO_FDBB, FDBB, FDBS, AO,
        OPEN, LOW, CLOSE, HIGH, DATE,
        
        # Alligator constants  
        JAW, TEETH, LIPS, BJAW, BTEETH, BLIPS, TJAW, TTEETH, TLIPS,
        
        # Signal constants
        ZONE_SIGNAL, MFI_FADE, MFI_SQUAT, FDB_TARGET,
        
        # ML constants
        ML_DEFAULT_COLUMNS_TO_KEEP
    )
except ImportError:
    from jgtutils.jgtconstants import (
        VECTOR_AO_FDBS, VECTOR_AO_FDBB, FDBB, FDBS, AO,
        OPEN, LOW, CLOSE, HIGH, DATE,
        JAW, TEETH, LIPS, BJAW, BTEETH, BLIPS, TJAW, TTEETH, TLIPS,
        ZONE_SIGNAL, MFI_FADE, MFI_SQUAT, FDB_TARGET,
        ML_DEFAULT_COLUMNS_TO_KEEP
    )
```

**Special Attention:**
- `jtc.py` has the most complex constants usage
- ML-specific constants may need to be added to jgtcore if missing
- Signal processing constants are critical for trading algorithms

**Test ML pipelines** after migration to ensure feature generation still works.
```

### **PHASE 4: FILE OPERATIONS MIGRATION**

#### **Task 4.1: Migrate jgtpy File Operations**
**Prompt for execution:**
```
Migrate jgtpy from jgtutils.jgtos to jgtcore.os file operations:

**Files with jgtos Dependencies:**  
- `/src/jgtpy/jgtpy/JGTCDS.py`
- `/src/jgtpy/jgtpy/jgtapyhelper.py`
- `/src/jgtpy/jgtpy/JGTChartConfig.py`
- Others with `get_data_path()`, `ensure_directory_exists()` usage

**Migration Pattern:**
```python
# OLD
from jgtutils.jgtos import get_data_path, ensure_directory_exists, mk_fullpath

# NEW  
try:
    from jgtcore.os import ensure_directory_exists
    from jgtcore.filesystem import get_data_path, mk_fullpath  # May need custom implementation
except ImportError:
    from jgtutils.jgtos import get_data_path, ensure_directory_exists, mk_fullpath
```

**Key Functions to Migrate:**
- `get_data_path()` - Data directory management
- `ensure_directory_exists()` - Directory creation (✅ Available in jgtcore.os)
- `mk_fullpath()` - File path construction
- `get_pov_local_data_filename()` - Local data filename generation

**Note:** Some functions may not exist in jgtcore yet and may need implementation.

**Validation:** Test data file access and path generation functionality.
```

#### **Task 4.2: Migrate jgtml File Operations**  
**Prompt for execution:**
```
Migrate jgtml from jgtutils.jgtos to jgtcore.os file operations:

**Files with jgtos Dependencies:**
- `/src/jgtml/jgtml/mldatahelper.py` 
- Files using `get_data_path()`, `tlid_dt_to_string()`

**Migration Pattern:**
```python
# OLD
from jgtutils.jgtos import get_data_path, tlid_dt_to_string

# NEW
try:
    from jgtcore.os import tlid_dt_to_string  # ✅ Available
    from jgtcore.filesystem import get_data_path  # May need implementation
except ImportError:
    from jgtutils.jgtos import get_data_path, tlid_dt_to_string
```

**Functions Available in jgtcore.os:**
- `tlid_dt_to_string()` ✅
- `ensure_directory_exists()` ✅ 
- TLID range functions ✅

**Functions Needing Implementation:**
- `get_data_path()` - Central data directory management
- Custom jgtml path utilities

**Test data pipeline** functionality after migration.
```

### **PHASE 5: TRADING LOGIC MIGRATION**

#### **Task 5.1: Migrate FX Transaction Logic**
**Prompt for execution:**
```
Migrate both jgtpy and jgtml from jgtutils.FXTransact to jgtcore.fx:

**Files with FXTransact Dependencies:**
- jgtpy: Service layer, trading automation
- jgtml: `/src/jgtml/jgtml/automated_fdb_trading_system.py`, trading orchestrator

**Migration Pattern:**
```python
# OLD
from jgtutils.FXTransact import FXTransactDataHelper as ftdh, FXTransactWrapper as ftw

# NEW - jgtcore has these! ✅
try:
    from jgtcore.fx import FXTransactDataHelper as ftdh, FXTransactWrapper as ftw
except ImportError:
    from jgtutils.FXTransact import FXTransactDataHelper as ftdh, FXTransactWrapper as ftw
```

**Good News:** jgtcore.fx already has these classes migrated!
- `FXTransactDataHelper` ✅
- `FXTransactWrapper` ✅  
- `FXTrade`, `FXOrder` classes ✅
- Legacy aliases `ftdh`, `ftw` ✅

**Priority Files:**
1. Search for `FXTransact` imports across both codebases
2. Replace with jgtcore.fx imports using compatibility pattern
3. Test trading automation functionality

**Validation:** Test trade/order processing with sample data.
```

#### **Task 5.2: Migrate Instrument Properties**
**Prompt for execution:**
```
Migrate jgtml from jgtutils.iprops to jgtcore equivalent:

**Files with iprops Dependencies:**
- jgtml files using `get_pips()` function

**Migration Strategy:**
```python
# OLD
from jgtutils.iprops import get_pips

# NEW - May need implementation in jgtcore
try:
    from jgtcore.instruments import get_pips
except ImportError:
    from jgtutils.iprops import get_pips
```

**Note:** `iprops` functionality may need to be added to jgtcore.instruments module if not present.

**Required Functions:**
- `get_pips()` - Get pip value for instrument
- Other instrument property functions

**Action if Missing:** Add instrument properties module to jgtcore or keep jgtutils dependency for now.
```

### **PHASE 6: DATA TYPE AND COLUMN HELPERS**

#### **Task 6.1: Migrate Column Type Definitions**
**Prompt for execution:**
```
Migrate jgtpy and jgtml from jgtutils column helpers to jgtcore:

**Files with Column Helper Dependencies:**
- jgtpy: `/src/jgtpy/jgtpy/JGTCDS.py`, `/src/jgtpy/jgtpy/JGTIDS.py`
- jgtml: Various data processing files

**Migration Pattern:**
```python
# OLD
from jgtutils.coltypehelper import DTYPE_DEFINITIONS
from jgtutils.colconverthelper import convert_columns

# NEW
try:
    from jgtcore.data import DTYPE_DEFINITIONS, convert_columns
except ImportError:
    from jgtutils.coltypehelper import DTYPE_DEFINITIONS
    from jgtutils.colconverthelper import convert_columns
```

**Key Functionality:**
- `DTYPE_DEFINITIONS` - Pandas DataFrame column type definitions
- Column conversion utilities for data processing

**Action if Missing:** May need to implement data type helpers in jgtcore.data module.

**Validation:** Test DataFrame operations and data type enforcement.
```

### **PHASE 7: SERVICE LAYER AND SCHEDULING**

#### **Task 7.1: Migrate jgtpy Service Layer**
**Prompt for execution:**
```
Migrate jgtpy service layer from jgtutils.timeframe_scheduler to jgtcore:

**Files with Scheduler Dependencies:**
- `/src/jgtpy/jgtpy/service/scheduler.py` (already has fallback logic!)
- `/src/jgtpy/jgtpy/jgtservice.py`

**Current Implementation in scheduler.py:**
```python
# Good - already has fallback pattern!
try:
    from jgtutils.timeframe_scheduler import get_times_by_timeframe_str, get_current_time
    # Use real timeframe scheduling logic
except ImportError:
    logger.warning("Could not import jgtutils.timeframe_scheduler, using fallback logic")
    # Fallback to simplified logic
```

**Migration:**
1. Update to try jgtcore first:
   ```python
   try:
       from jgtcore.timeframe import get_times_by_timeframe_str, get_current_time
   except ImportError:
       try:
           from jgtutils.timeframe_scheduler import get_times_by_timeframe_str, get_current_time  
       except ImportError:
           # Use fallback logic
   ```

2. **Test jgtservice** functionality with new imports.

**Good:** Service layer already has graceful degradation built in!
```

### **PHASE 8: TESTING AND VALIDATION**

#### **Task 8.1: CLI Tool Testing Suite**
**Prompt for execution:**
```
Create comprehensive test suite for all CLI tools after migration:

**jgtpy CLI Tools to Test:**
```bash
# Test each CLI tool's help and basic functionality
cd /src/jgtpy

python -m jgtpy.jgtcli --help
python -m jgtpy.cdscli --help  
python -m jgtpy.jgtapycli --help
python -m jgtpy.JGTADS --help
python -m jgtpy.jgtservice --help

# Test with sample arguments (if available)
python -m jgtpy.jgtcli -i EUR/USD -t D1 --help
```

**jgtml CLI Tools to Test:**
```bash
cd /src/jgtml

python -m jgtml.jgtmlcli --help
python -m jgtml.mlfcli --help
python -m jgtml.ttfcli --help  
python -m jgtml.mxcli --help
python -m jgtml.fdbscan --help

# Test basic functionality
python -m jgtml.jgtmlcli -i EUR/USD -t D1 --help
```

**Expected Results:** All tools should display help correctly and maintain existing CLI interface.

**Document any issues** found during testing for follow-up fixes.
```

#### **Task 8.2: Data Pipeline Testing**
**Prompt for execution:**
```
Test data processing pipelines after jgtcore migration:

**jgtpy Data Processing Tests:**
1. **CDS Pipeline:** Test data loading and processing in JGTCDS
2. **IDS Pipeline:** Test indicator calculations in JGTIDS  
3. **ADS Pipeline:** Test advanced analysis in JGTADS

**jgtml ML Pipeline Tests:**
1. **Feature Generation:** Test TTF (Time-based features) generation
2. **Signal Processing:** Test FDB signal detection
3. **ML Data Preparation:** Test data helper functionality

**Test Script Template:**
```python
# Test basic data processing
try:
    # Test imports work
    import jgtpy
    import jgtml
    
    # Test basic functionality
    from jgtpy import JGTCDS, JGTIDS
    from jgtml import mldatahelper
    
    print("✅ Imports successful")
    
    # Test basic operations (with sample data if available)
    # ...
    
except Exception as e:
    print(f"❌ Error: {e}")
```

**Validation Criteria:**
- All imports work without errors
- Basic data operations function correctly
- Constants are resolved properly
- File operations work as expected
```

#### **Task 8.3: Integration Testing**
**Prompt for execution:**
```
Test integration between jgtcore, jgtutils, jgtpy, and jgtml:

**Integration Test Scenarios:**

1. **Cross-Package Imports:**
   ```python
   # Test all combinations work
   import jgtcore
   import jgtutils  
   import jgtpy
   import jgtml
   
   # Test compatibility layer
   from jgtcore.compatibility import get_compatible_function
   func = get_compatible_function('new_parser')
   ```

2. **Data Flow Testing:**
   - jgtpy → jgtml data pipeline
   - jgtutils → jgtcore function calls
   - Mixed import scenarios

3. **Version Compatibility:**
   ```python
   # Check version compatibility
   import jgtcore, jgtutils, jgtpy, jgtml
   print(f"jgtcore: {jgtcore.__version__}")
   print(f"jgtutils: {jgtutils.version}")  
   print(f"jgtpy: {jgtpy.__version__}")
   print(f"jgtml: {jgtml.__version__}")
   ```

**Service Integration Tests:**
- Test jgtservice with new dependencies
- Test ML automation with jgtcore functions
- Test trading orchestration end-to-end

**Expected Results:** All packages work together seamlessly with no import conflicts or functionality regressions.
```

### **PHASE 9: DEPLOYMENT AND DOCUMENTATION**

#### **Task 9.1: Update Documentation**
**Prompt for execution:**
```
Update documentation across all projects for jgtcore migration:

**Documentation Updates Needed:**

1. **jgtpy README.md:**
   - Update installation instructions to include jgtcore
   - Update import examples to show jgtcore compatibility
   - Add migration notes for existing users

2. **jgtml README.md:**  
   - Update dependencies section
   - Update usage examples
   - Document jgtcore integration benefits

3. **CLI Help Updates:**
   - Ensure all CLI tools show correct help text
   - Update any references to jgtutils in help strings
   - Add version information showing jgtcore integration

**Example Updates:**
```markdown
## Installation

```bash
# New installation with jgtcore
pip install jgtpy jgtcore>=0.2.0

# Migration from existing installation  
pip install --upgrade jgtcore>=0.2.0
```

## Migration Notes

This version includes migration to jgtcore for improved performance and compatibility.
Existing code will continue to work unchanged.
```

**Files to Update:**
- `/src/jgtpy/README.md`
- `/src/jgtml/README.md`
- CLI help strings in Python files
- Any other documentation files
```

#### **Task 9.2: Version Updates and Release Preparation**
**Prompt for execution:**
```
Prepare version updates and releases for jgtcore compatibility:

**Version Strategy:**

1. **jgtpy Version Update:**
   - Current: 0.6.15
   - Suggested: 0.7.0 (minor version bump for jgtcore compatibility)
   - Update in `pyproject.toml` and `__init__.py`

2. **jgtml Version Update:**
   - Current: 0.0.341  
   - Suggested: 0.1.0 (move to stable release with jgtcore)
   - Update in `pyproject.toml` and `__init__.py`

**Dependency Updates:**
```toml
# jgtpy pyproject.toml
dependencies = [
  "jgtcore>=0.2.0",
  "jgtutils>=1.0.11",  # Keep for transition
  # ... other deps
]

# jgtml pyproject.toml  
dependencies = [
  "jgtcore>=0.2.0",
  "jgtpy>=0.7.0",
  "jgtutils",  # Keep for transition
  # ... other deps  
]
```

**Release Notes:**
- Document jgtcore integration
- List any breaking changes (should be minimal)
- Provide migration guidance
- Highlight performance improvements

**Testing Before Release:**
- Run full test suite on all packages
- Validate CLI tools functionality
- Test installation from scratch
- Verify backward compatibility
```

### **PHASE 10: MONITORING AND ROLLBACK PLAN**

#### **Task 10.1: Create Rollback Strategy**
**Prompt for execution:**
```
Create rollback strategy in case of issues with jgtcore migration:

**Rollback Plan:**

1. **Branch Strategy:**
   - Create `pre-jgtcore-migration` branches for both jgtpy and jgtml
   - Tag current versions before migration starts
   - Maintain ability to quickly revert

2. **Dependency Rollback:**
   ```toml
   # Emergency rollback - remove jgtcore dependency
   dependencies = [
     "jgtutils>=1.0.11",  # Back to jgtutils only
     # ... other deps remain same
   ]
   ```

3. **Import Rollback:**
   ```python
   # All imports should have fallback to jgtutils
   try:
       from jgtcore.cli import new_parser
   except ImportError:
       from jgtutils.jgtcommon import new_parser  # Fallback always available
   ```

**Monitoring During Migration:**
- Test each phase thoroughly before proceeding
- Keep detailed logs of what changes were made
- Have test data and scripts ready for validation
- Monitor performance impact

**Success Criteria for Each Phase:**
- All CLI tools work correctly
- No import errors in any module
- Data processing pipelines produce same results
- Performance is equal or better than before

**Rollback Triggers:**
- Any CLI tool stops working
- Data processing errors increase
- Performance degradation > 20%
- User reports of functionality loss
```

---

## 🎯 **EXECUTION PRIORITY**

### **HIGH PRIORITY (Start Immediately):**
1. **Task 1.1 & 1.2** - Update dependencies
2. **Task 2.1 & 2.2** - CLI framework migration  
3. **Task 3.1 & 3.2** - Constants migration

### **MEDIUM PRIORITY (After High Priority Complete):**
4. **Task 4.1 & 4.2** - File operations migration
5. **Task 5.1 & 5.2** - Trading logic migration
6. **Task 8.1 & 8.2** - Testing suites

### **LOW PRIORITY (Polish & Documentation):**
7. **Task 6.1** - Data type helpers
8. **Task 7.1** - Service layer (already has fallbacks)
9. **Task 9.1 & 9.2** - Documentation and versioning
10. **Task 10.1** - Rollback strategy

---

## 📊 **SUCCESS METRICS**

- **✅ 59 Python files** successfully migrated
- **✅ 25+ CLI tools** working correctly 
- **✅ 0 import errors** across both codebases
- **✅ Data pipelines** producing identical results
- **✅ Performance** maintained or improved
- **✅ Backward compatibility** preserved

---

## ⚠️ **CRITICAL NOTES**

1. **Always implement fallback imports** - never break existing functionality
2. **Test thoroughly at each phase** - don't proceed if issues found
3. **Keep rollback options ready** - maintain pre-migration branches
4. **Some functions may need implementation** in jgtcore if missing
5. **Performance testing** - ensure no regressions in data processing
6. **User communication** - document any temporary issues during migration

This plan ensures a systematic, safe migration to jgtcore while maintaining full backward compatibility and functionality.