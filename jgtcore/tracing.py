#!/usr/bin/env python3
"""
jgtcore.tracing - Unified tracing infrastructure for JGT ecosystem
Provides Langfuse integration through CoaiaPy with fail-safe design.
"""

import os
import json
import uuid
import datetime
from typing import Any, Dict, Optional, List
from contextlib import contextmanager

# Import from jgtcore
from .core import get_tracing_config

# Optional CoaiaPy import with fallback
try:
    from coaiapy.cofuse import add_trace, add_observation, add_observations_batch
    COAIAPY_AVAILABLE = True
except ImportError:
    COAIAPY_AVAILABLE = False

# Configuration constants
DEFAULT_BATCH_SIZE = 50
DEFAULT_TIMEOUT_MS = 5000
DEFAULT_SESSION_PREFIX = "jgt_session"
DEFAULT_PROJECT_NAME = "jgt-trading-ecosystem"

# Valid JGT package names
VALID_PACKAGES = {"jgtcore", "jgtpy", "jgtml", "jgtagentic", "jgt_session"}


class JGTTracer:
    """
    Unified tracing infrastructure for JGT ecosystem.
    Provides Langfuse observability through CoaiaPy with fail-safe design.
    """
    
    def __init__(self, package_name: str, operation_type: str):
        """
        Initialize JGT tracer for a specific package and operation.
        
        Args:
            package_name: Name of JGT package (jgtpy, jgtml, jgtagentic)
            operation_type: Type of operation (data_refresh, signal_analysis, etc.)
            
        Raises:
            ValueError: If package_name is not a valid JGT package
        """
        # Input validation
        if not package_name or not isinstance(package_name, str):
            raise ValueError("package_name must be a non-empty string")
        if not operation_type or not isinstance(operation_type, str):
            raise ValueError("operation_type must be a non-empty string")
        
        # Validate package name (with warning for unknown packages)
        if package_name not in VALID_PACKAGES:
            print(f"Warning: Unknown package '{package_name}'. Known packages: {', '.join(sorted(VALID_PACKAGES))}")
        
        self.package_name = package_name
        self.operation_type = operation_type
        self.trace_id = None
        self.session_id = None
        self.current_trace = None
        self.observations = []
        
        # Load tracing configuration
        self.config = self._load_tracing_config()
        self.enabled = self.config.get("enabled", True) and COAIAPY_AVAILABLE
        
        if not self.enabled and not COAIAPY_AVAILABLE:
            print(f"Info: CoaiaPy not available, tracing disabled for {package_name}")
    
    def _load_tracing_config(self) -> Dict[str, Any]:
        """Load tracing configuration with defaults."""
        try:
            config = get_tracing_config()
            defaults = {
                "enabled": True,
                "project_name": DEFAULT_PROJECT_NAME,
                "session_prefix": DEFAULT_SESSION_PREFIX,
                "environment": "development",
                "batch_size": DEFAULT_BATCH_SIZE,
                "timeout_ms": DEFAULT_TIMEOUT_MS,
                "fail_silent": True,
                "trace_levels": ["INFO", "WARNING", "ERROR"],
                "excluded_packages": []
            }
            
            # Merge with defaults
            for key, default_value in defaults.items():
                if key not in config:
                    config[key] = default_value
            
            return config
        except Exception as e:
            print(f"Warning: Error loading tracing config, using defaults: {e}")
            return {"enabled": False, "fail_silent": True}
    
    def _safe_execute(self, operation, *args, **kwargs):
        """Execute tracing operation with fail-safe error handling."""
        if not self.enabled:
            return None
            
        try:
            return operation(*args, **kwargs)
        except Exception as e:
            if not self.config.get("fail_silent", True):
                print(f"Tracing error in {self.package_name}: {e}")
            return None
    
    def start_operation(self, name: str, input_data: Any = None, metadata: Dict[str, Any] = None) -> str:
        """
        Start a new trading operation trace.
        
        Args:
            name: Operation name (e.g., "PDS refresh EURUSD M15")
            input_data: Input data for the operation
            metadata: Additional metadata
            
        Returns:
            Trace ID if successful, None if tracing disabled/failed
        """
        if not self.enabled:
            return None
            
        # Generate trace and session IDs
        self.trace_id = str(uuid.uuid4())
        self.session_id = f"{self.config['session_prefix']}_{int(datetime.datetime.now().timestamp())}"
        
        # Build trace metadata
        trace_metadata = {
            "package": self.package_name,
            "operation_type": self.operation_type,
            "environment": self.config.get("environment", "development"),
            "session_id": self.session_id
        }
        
        if metadata:
            trace_metadata.update(metadata)
        
        # Create trace
        result = self._safe_execute(
            add_trace,
            trace_id=self.trace_id,
            session_id=self.session_id,
            name=f"{self.package_name}:{self.operation_type}:{name}",
            input_data=input_data,
            metadata=trace_metadata
        )
        
        if result:
            print(f"🔍 Trace started: {self.package_name}:{name} [{self.trace_id[:8]}...]")
            
        return self.trace_id
    
    def add_step(self, step_name: str, input_data: Any = None, output_data: Any = None, 
                 metadata: Dict[str, Any] = None, observation_type: str = "EVENT") -> str:
        """
        Add an observation step to the current trace.
        
        Args:
            step_name: Name of the processing step
            input_data: Input data for this step
            output_data: Output data from this step
            metadata: Additional step metadata
            observation_type: Type of observation (EVENT, SPAN, GENERATION)
            
        Returns:
            Observation ID if successful, None if failed
        """
        if not self.enabled or not self.trace_id:
            return None
            
        observation_id = str(uuid.uuid4())
        
        # Build observation metadata
        obs_metadata = {
            "step_type": step_name,
            "package": self.package_name,
            "operation": self.operation_type
        }
        
        if metadata:
            obs_metadata.update(metadata)
        
        # Create observation
        result = self._safe_execute(
            add_observation,
            observation_id=observation_id,
            trace_id=self.trace_id,
            observation_type=observation_type,
            name=f"{self.package_name}:{step_name}",
            input_data=input_data,
            output_data=output_data,
            metadata=obs_metadata
        )
        
        if result:
            self.observations.append({
                "id": observation_id,
                "name": step_name,
                "type": observation_type
            })
            
        return observation_id
    
    def complete_operation(self, output_data: Any = None, metadata: Dict[str, Any] = None) -> bool:
        """
        Complete the current operation and finalize the trace.
        
        Args:
            output_data: Final output data
            metadata: Final metadata
            
        Returns:
            True if successful, False if failed
        """
        if not self.enabled or not self.trace_id:
            return False
            
        # Add completion observation
        completion_metadata = {
            "operation_completed": True,
            "total_observations": len(self.observations),
            "trace_duration": "calculated_by_langfuse"
        }
        
        if metadata:
            completion_metadata.update(metadata)
        
        result = self.add_step(
            "operation_complete",
            input_data={"observations_summary": self.observations},
            output_data=output_data,
            metadata=completion_metadata,
            observation_type="EVENT"
        )
        
        if result:
            print(f"✅ Trace completed: {self.package_name} [{self.trace_id[:8]}...] with {len(self.observations)} steps")
            
        return result is not None
    
    @contextmanager
    def trace_operation(self, name: str, input_data: Any = None, metadata: Dict[str, Any] = None):
        """
        Context manager for automatic trace lifecycle management.
        
        Args:
            name: Operation name
            input_data: Input data
            metadata: Operation metadata
            
        Usage:
            with tracer.trace_operation("PDS_refresh", {"symbol": "EURUSD"}) as trace_id:
                # Do work
                tracer.add_step("data_fetch", input_data, output_data)
                # Context manager handles completion automatically
        """
        trace_id = self.start_operation(name, input_data, metadata)
        try:
            yield trace_id
        except Exception as e:
            # Add error observation
            self.add_step(
                "operation_error",
                input_data={"error_type": type(e).__name__},
                output_data={"error_message": str(e)},
                metadata={"operation_failed": True}
            )
            raise
        finally:
            # Always complete the trace
            self.complete_operation(
                metadata={"context_manager": True}
            )


# Utility Functions

def create_session_tracer(session_name: str) -> JGTTracer:
    """Create a session-level tracer for multi-package workflows."""
    return JGTTracer("jgt_session", session_name)

def get_trace_url(trace_id: str) -> Optional[str]:
    """Get Langfuse URL for a specific trace."""
    try:
        config = get_tracing_config()
        base_url = config.get("langfuse", {}).get("trace_url")
        if base_url and trace_id:
            return f"{base_url}/{trace_id}"
    except:
        pass
    return None

def is_tracing_enabled() -> bool:
    """Check if tracing is enabled and available."""
    try:
        config = get_tracing_config()
        return config.get("enabled", False) and COAIAPY_AVAILABLE
    except:
        return False