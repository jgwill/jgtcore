#!/usr/bin/env python3
"""
Simple test to debug environment loading
"""

import os
import sys
import json

def test_direct_env_loading():
    """Test direct environment loading."""
    print("🔧 Testing direct environment loading...")
    
    # Test the _load_env_file function directly
    sys.path.insert(0, '/src/jgtcore')
    from jgtcore.core import _load_env_file
    
    print(f"Current working directory: {os.getcwd()}")
    
    # Try loading from different paths
    env_paths = [
        ".env.caishen",
        "/src/.env.caishen",
        os.path.expanduser("~/.env.caishen")
    ]
    
    for path in env_paths:
        print(f"Checking path: {path}")
        if os.path.exists(path):
            print(f"✅ Found: {path}")
            break
        else:
            print(f"❌ Not found: {path}")
    
    # Load the file
    print("\nLoading .env.caishen...")
    _load_env_file(".env.caishen")
    
    # Check if variables are loaded
    langfuse_keys = ['LANGFUSE_SECRET_KEY', 'LANGFUSE_PUBLIC_KEY', 'LANGFUSE_HOST']
    for key in langfuse_keys:
        value = os.getenv(key)
        if value:
            print(f"✅ {key}: {value[:20]}...")
        else:
            print(f"❌ {key}: Not loaded")

if __name__ == "__main__":
    test_direct_env_loading()