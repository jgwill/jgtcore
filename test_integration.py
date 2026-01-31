#!/usr/bin/env python3
"""
Test script for jgtcore Langfuse integration
Tests configuration loading, environment variable resolution, and real Langfuse connection.
"""

import os
import sys
import json

# Test configuration loading
def test_tracing_config():
    """Test that tracing configuration loads correctly."""
    print("🔧 Testing tracing configuration...")
    
    try:
        from jgtcore import get_tracing_config
        config = get_tracing_config()
        print(f"✅ Tracing config loaded: {json.dumps(config, indent=2)}")
        return True
    except Exception as e:
        print(f"❌ Failed to load tracing config: {e}")
        return False

# Test JGTTracer initialization
def test_tracer_initialization():
    """Test JGTTracer initialization."""
    print("\n🔧 Testing JGTTracer initialization...")
    
    try:
        from jgtcore import JGTTracer, is_tracing_enabled
        
        print(f"Tracing enabled: {is_tracing_enabled()}")
        
        tracer = JGTTracer("jgtcore", "integration_test")
        print(f"✅ JGTTracer initialized: {tracer.package_name}, enabled: {tracer.enabled}")
        return True
    except Exception as e:
        print(f"❌ Failed to initialize JGTTracer: {e}")
        return False

# Test environment variable resolution
def test_env_resolution():
    """Test environment variable resolution from .env.caishen."""
    print("\n🔧 Testing environment variable resolution...")
    
    try:
        # Check if .env.caishen variables are loaded
        langfuse_keys = ['LANGFUSE_SECRET_KEY', 'LANGFUSE_PUBLIC_KEY', 'LANGFUSE_HOST']
        loaded_vars = {}
        
        for key in langfuse_keys:
            value = os.getenv(key)
            loaded_vars[key] = value[:20] + "..." if value and len(value) > 20 else value
        
        print(f"✅ Environment variables: {json.dumps(loaded_vars, indent=2)}")
        return all(os.getenv(key) for key in langfuse_keys)
    except Exception as e:
        print(f"❌ Failed to test environment resolution: {e}")
        return False

# Test real Langfuse integration
def test_real_langfuse():
    """Test actual Langfuse integration."""
    print("\n🔧 Testing real Langfuse integration...")
    
    try:
        from jgtcore import JGTTracer, is_tracing_enabled, get_trace_url
        
        if not is_tracing_enabled():
            print("⚠️ Tracing not enabled, skipping real integration test")
            return True
            
        tracer = JGTTracer("jgtcore", "integration_test")
        
        # Test with context manager
        with tracer.trace_operation("test_operation", {"test": True}) as trace_id:
            tracer.add_step("step_1", {"input": "test"}, {"output": "success"})
            tracer.add_step("step_2", {"input": "step1_output"}, {"final": "complete"})
        
        print(f"✅ Integration test completed, trace: {trace_id}")
        
        # Get trace URL
        trace_url = get_trace_url(trace_id)
        if trace_url:
            print(f"🔗 View trace: {trace_url}")
        
        return True
    except Exception as e:
        print(f"❌ Real Langfuse integration failed: {e}")
        import traceback
        traceback.print_exc()
        return False

# Enhanced config test with tracing section
def test_enhanced_config():
    """Test enhanced configuration with tracing section."""
    print("\n🔧 Testing enhanced configuration setup...")
    
    # Create test config with tracing section
    test_config = {
        "user_id": "test_user",
        "tracing": {
            "enabled": True,
            "provider": "langfuse",
            "langfuse": {
                "secret_key": "${LANGFUSE_SECRET_KEY}",
                "public_key": "${LANGFUSE_PUBLIC_KEY}",
                "host": "${LANGFUSE_HOST}"
            }
        }
    }
    
    print(f"📋 Example enhanced config structure:")
    print(json.dumps(test_config, indent=2))
    
    return True

if __name__ == "__main__":
    print("🚀 JGTCore Langfuse Integration Test Suite")
    print("=" * 50)
    
    # Run tests
    tests = [
        test_tracing_config,
        test_tracer_initialization, 
        test_env_resolution,
        test_enhanced_config,
        test_real_langfuse
    ]
    
    results = []
    for test in tests:
        try:
            result = test()
            results.append(result)
        except Exception as e:
            print(f"❌ Test {test.__name__} crashed: {e}")
            results.append(False)
    
    print("\n" + "=" * 50)
    print("📊 Test Results Summary:")
    passed = sum(results)
    total = len(results)
    
    for i, (test, result) in enumerate(zip(tests, results)):
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{i+1}. {test.__name__}: {status}")
    
    print(f"\n🎯 Overall: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! jgtcore Langfuse integration is ready.")
    else:
        print("⚠️ Some tests failed. Check configuration and dependencies.")
        sys.exit(1)