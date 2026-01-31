#!/usr/bin/env python3
"""
Usage examples for jgtcore Langfuse integration
Demonstrates how to use JGTTracer in real trading workflows.
"""

import time
import sys
import os

# Add parent directory to path for local import
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from jgtcore import JGTTracer, create_session_tracer, is_tracing_enabled, get_trace_url

def example_basic_tracing():
    """Basic tracing example for a data processing operation."""
    print("📊 Example 1: Basic Operation Tracing")
    
    tracer = JGTTracer("jgtpy", "data_processing")
    
    trace_id = tracer.start_operation("process_market_data", {"symbol": "EURUSD"})
    
    # Simulate processing steps
    tracer.add_step("load_data", {"source": "broker"}, {"records": 1000})
    time.sleep(0.1)  # Simulate work
    
    tracer.add_step("calculate_indicators", {"indicators": ["MA", "RSI"]}, {"success": True})
    time.sleep(0.1)  # Simulate work
    
    tracer.add_step("detect_signals", {"pattern": "FDB"}, {"signals_found": 3})
    
    tracer.complete_operation({"total_signals": 3, "processing_time": "0.3s"})
    
    return trace_id

def example_context_manager():
    """Context manager example for automatic lifecycle management."""
    print("\n📊 Example 2: Context Manager Usage")
    
    tracer = JGTTracer("jgtml", "ml_analysis")
    
    with tracer.trace_operation("feature_engineering", {"timeframe": "H1"}) as trace_id:
        # Feature extraction
        tracer.add_step("extract_features", 
                       input_data={"raw_data": "1000_bars"}, 
                       output_data={"features": 50})
        time.sleep(0.1)  # Simulate work
        
        # Model prediction
        tracer.add_step("ml_prediction", 
                       input_data={"features": 50}, 
                       output_data={"prediction": "BUY", "confidence": 0.85},
                       observation_type="GENERATION")
    
    return trace_id

def example_session_tracing():
    """Example of session-level tracing across multiple packages."""
    print("\n📊 Example 3: Session-Level Multi-Package Tracing")
    
    session_tracer = create_session_tracer("full_trading_workflow")
    
    with session_tracer.trace_operation("trading_session") as session_id:
        # Data phase (would be in jgtpy)
        session_tracer.add_step("data_collection", 
                               {"symbols": ["EURUSD", "GBPUSD"]}, 
                               {"data_quality": "good"})
        time.sleep(0.1)  # Simulate work
        
        # Analysis phase (would be in jgtml) 
        session_tracer.add_step("signal_analysis",
                               {"algorithms": ["FDB", "Alligator"]},
                               {"signals": 5})
        time.sleep(0.1)  # Simulate work
        
        # Decision phase (would be in jgtagentic)
        session_tracer.add_step("agent_decision",
                               {"signals": 5, "risk_level": "medium"},
                               {"action": "place_orders", "orders": 2})
    
    return session_id

def example_error_handling():
    """Example of error handling in tracing."""
    print("\n📊 Example 4: Error Handling")
    
    tracer = JGTTracer("jgtpy", "error_test")
    
    try:
        with tracer.trace_operation("operation_with_error") as trace_id:
            tracer.add_step("step_1", {"input": "data"}, {"output": "success"})
            
            # Simulate an error
            raise ValueError("Simulated error for testing")
            
    except ValueError as e:
        print(f"✅ Error caught and traced: {e}")
    
    return trace_id

if __name__ == "__main__":
    print("🚀 JGTCore Langfuse Integration Usage Examples")
    print("=" * 55)
    
    if is_tracing_enabled():
        print("✅ Tracing is enabled - running live examples")
        
        # Run examples
        trace1 = example_basic_tracing()
        trace2 = example_context_manager()
        trace3 = example_session_tracing()
        trace4 = example_error_handling()
        
        print("\n🔗 Trace URLs:")
        for i, trace_id in enumerate([trace1, trace2, trace3, trace4], 1):
            trace_url = get_trace_url(trace_id)
            if trace_url and trace_id:
                print(f"  {i}. {trace_url}/{trace_id}")
        
    else:
        print("⚠️ Tracing not enabled - running simulation examples")
        
        # Run examples anyway to show the API
        example_basic_tracing()
        example_context_manager()
        example_session_tracing()
        example_error_handling()
        
        print("\n💡 To enable tracing:")
        print("  1. Install CoaiaPy: pip install coaiapy")
        print("  2. Add tracing config to ~/.jgt/config.json")
        print("  3. Set up .env.caishen with Langfuse credentials")
    
    print("\n🎉 All examples completed successfully!")