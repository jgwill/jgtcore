#!/usr/bin/env python3
"""
Real JGTTracer integration test with actual Langfuse/CoaiaPy
Tests the JGTTracer implementation with live tracing infrastructure.
"""

import os
import sys

def test_jgttracer_basic_functionality():
    """Test basic JGTTracer functionality without external dependencies"""
    print("🔧 Testing JGTTracer basic functionality...")
    
    try:
        from jgtcore import JGTTracer, is_tracing_enabled, get_tracing_config
        print("✅ JGTTracer imports successful")
    except ImportError as e:
        print(f"❌ Import failed: {e}")
        return False
    
    # Test tracer initialization
    try:
        tracer = JGTTracer("jgtpy", "test_operation")
        print("✅ JGTTracer initialization successful")
    except Exception as e:
        print(f"❌ JGTTracer initialization failed: {e}")
        return False
    
    # Test configuration loading
    try:
        config = get_tracing_config()
        print(f"✅ Tracing config loaded: {type(config)}")
        print(f"   Config keys: {list(config.keys()) if config else 'None'}")
    except Exception as e:
        print(f"❌ Config loading failed: {e}")
        return False
    
    # Test tracing enabled check
    try:
        enabled = is_tracing_enabled()
        print(f"✅ Tracing enabled check: {enabled}")
    except Exception as e:
        print(f"❌ Tracing enabled check failed: {e}")
        return False
    
    return True

def test_jgttracer_with_coaiapy():
    """Test JGTTracer with actual CoaiaPy integration"""
    print("\n🔧 Testing JGTTracer with CoaiaPy integration...")
    
    # Check if CoaiaPy is available
    try:
        import coaiapy
        from coaiapy.cofuse import add_trace, add_observation
        print("✅ CoaiaPy is available")
        coaiapy_available = True
    except ImportError:
        print("⚠️  CoaiaPy not available - testing fallback behavior")
        coaiapy_available = False
    
    # Test with configuration
    try:
        from jgtcore import JGTTracer
        tracer = JGTTracer("jgtcore", "integration_test")
        print("✅ JGTTracer initialized with CoaiaPy context")
    except Exception as e:
        print(f"❌ JGTTracer with CoaiaPy failed: {e}")
        return False
    
    # Test basic operations
    try:
        if coaiapy_available:
            # Test with actual tracing
            trace_id = tracer.start_operation("test_real_trace", {"test": True})
            print(f"✅ Started trace operation: {trace_id}")
            
            obs_id = tracer.add_step("test_step", {"input": "test"}, {"output": "success"})
            print(f"✅ Added observation: {obs_id}")
            
            completion_result = tracer.complete_operation({"status": "completed"})
            print(f"✅ Completed operation: {completion_result}")
        else:
            # Test fallback behavior
            trace_id = tracer.start_operation("test_fallback_trace", {"test": True})
            obs_id = tracer.add_step("test_step", {"input": "test"}, {"output": "success"})
            completion_result = tracer.complete_operation({"status": "completed"})
            print(f"✅ Fallback operations completed: trace={trace_id}, obs={obs_id}, complete={completion_result}")
    except Exception as e:
        print(f"❌ Operation testing failed: {e}")
        return False
    
    return True

def test_jgttracer_context_manager():
    """Test JGTTracer context manager functionality"""
    print("\n🔧 Testing JGTTracer context manager...")
    
    try:
        from jgtcore import JGTTracer
        tracer = JGTTracer("jgtcore", "context_test")
        
        with tracer.trace_operation("context_test_operation", {"test": True}) as trace_id:
            print(f"✅ Context manager started: {trace_id}")
            tracer.add_step("context_step", {"step": 1}, {"result": "success"})
            print("✅ Added step within context")
        
        print("✅ Context manager completed successfully")
        return True
    except Exception as e:
        print(f"❌ Context manager test failed: {e}")
        return False

def test_environment_variable_resolution():
    """Test environment variable resolution in tracing config"""
    print("\n🔧 Testing environment variable resolution...")
    
    try:
        from jgtcore.core import _resolve_env_variables
        
        # Test basic resolution
        test_config = {
            "langfuse": {
                "secret_key": "${TEST_SECRET_KEY}",
                "host": "https://test.com"
            }
        }
        
        # Set test environment variable
        os.environ["TEST_SECRET_KEY"] = "test_secret_value"
        
        resolved = _resolve_env_variables(test_config)
        expected_value = "test_secret_value"
        actual_value = resolved["langfuse"]["secret_key"]
        
        if actual_value == expected_value:
            print(f"✅ Environment variable resolution successful: {actual_value}")
        else:
            print(f"❌ Environment resolution failed: expected {expected_value}, got {actual_value}")
            return False
        
        # Clean up
        del os.environ["TEST_SECRET_KEY"]
        return True
    except Exception as e:
        print(f"❌ Environment variable resolution test failed: {e}")
        return False

def test_real_langfuse_integration():
    """Test actual Langfuse integration if credentials available"""
    print("\n🔧 Testing real Langfuse integration...")
    
    # Check if .env.caishen exists
    env_paths = ["/src/.env.caishen", "~/.env.caishen", ".env.caishen"]
    env_file_found = None
    
    for path in env_paths:
        expanded_path = os.path.expanduser(path)
        if os.path.exists(expanded_path):
            env_file_found = expanded_path
            break
    
    if not env_file_found:
        print("⚠️  No .env.caishen file found - skipping real Langfuse test")
        return True
    
    print(f"✅ Found .env.caishen at: {env_file_found}")
    
    try:
        from jgtcore import JGTTracer, is_tracing_enabled
        
        if not is_tracing_enabled():
            print("⚠️  Tracing not enabled - check configuration")
            return True
        
        # Test real integration
        tracer = JGTTracer("jgtcore", "real_langfuse_test")
        
        with tracer.trace_operation("Real_Langfuse_Test", {"test_type": "integration"}) as trace_id:
            tracer.add_step("langfuse_connection_test", 
                          {"connection": "testing"}, 
                          {"status": "connected"})
            
            tracer.add_step("data_processing_simulation",
                          {"data_size": 100},
                          {"processed_records": 100, "success": True})
        
        print(f"✅ Real Langfuse integration test completed successfully!")
        print(f"   Trace ID: {trace_id}")
        
        # Try to get trace URL if available
        try:
            from jgtcore import get_trace_url
            trace_url = get_trace_url(trace_id)
            if trace_url:
                print(f"   🔗 View trace: {trace_url}")
        except:
            pass
        
        return True
    except Exception as e:
        print(f"❌ Real Langfuse integration test failed: {e}")
        return False

def main():
    print("🔍 JGTTracer Integration Test Suite")
    print("=" * 50)
    
    tests = [
        ("Basic Functionality", test_jgttracer_basic_functionality),
        ("CoaiaPy Integration", test_jgttracer_with_coaiapy),
        ("Context Manager", test_jgttracer_context_manager),
        ("Environment Variables", test_environment_variable_resolution),
        ("Real Langfuse", test_real_langfuse_integration)
    ]
    
    results = []
    for test_name, test_func in tests:
        print(f"\n{'='*20} {test_name} {'='*20}")
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"❌ {test_name} failed with exception: {e}")
            results.append((test_name, False))
    
    # Summary
    print(f"\n{'='*50}")
    print("📊 Test Results Summary:")
    passed = 0
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"  {status} {test_name}")
        if result:
            passed += 1
    
    print(f"\n🎯 Overall: {passed}/{len(results)} tests passed")
    
    if passed == len(results):
        print("🎉 All JGTTracer integration tests passed!")
        return True
    else:
        print("⚠️  Some tests failed - JGTTracer needs attention")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)