#!/usr/bin/env python3
"""Test improved validation in JGTTracer"""

from jgtcore import JGTTracer

def test_validation():
    """Test input validation in JGTTracer."""
    print("🔧 Testing JGTTracer validation improvements...")
    
    # Test valid input
    try:
        tracer = JGTTracer("jgtpy", "test_operation")
        print("✅ Valid input accepted")
    except Exception as e:
        print(f"❌ Valid input rejected: {e}")
    
    # Test invalid package name
    try:
        tracer = JGTTracer("", "test_operation")
        print("❌ Empty package name should be rejected")
    except ValueError as e:
        print(f"✅ Empty package name correctly rejected: {e}")
    
    # Test invalid operation type  
    try:
        tracer = JGTTracer("jgtpy", None)
        print("❌ None operation type should be rejected")
    except ValueError as e:
        print(f"✅ None operation type correctly rejected: {e}")
    
    # Test unknown package (should warn but not fail)
    try:
        tracer = JGTTracer("unknown_package", "test_operation")
        print("✅ Unknown package generates warning but allows creation")
    except Exception as e:
        print(f"❌ Unknown package should warn but not fail: {e}")

if __name__ == "__main__":
    test_validation()