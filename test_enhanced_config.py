#!/usr/bin/env python3
"""
Test enhanced configuration with tracing section
"""

import os
import sys
import json

def test_enhanced_config_loading():
    """Test loading enhanced config with tracing section."""
    print("🔧 Testing enhanced configuration loading...")
    
    # Change to examples directory to test config loading
    examples_dir = os.path.join(os.path.dirname(__file__), 'examples')
    config_path = os.path.join(examples_dir, 'enhanced_config.json')
    
    print(f"Testing config from: {config_path}")
    
    try:
        # Test reading config directly
        with open(config_path, 'r') as f:
            config = json.load(f)
        
        print("✅ Enhanced config loaded successfully")
        print(f"📋 Tracing section: {json.dumps(config.get('tracing', {}), indent=2)}")
        
        # Test with jgtcore config loading
        from jgtcore import readconfig, get_tracing_config
        
        # Load config from file
        jgt_config = readconfig(config_file=config_path)
        print(f"✅ JGT config loaded: connection={jgt_config.get('connection')}")
        
        # Test tracing config with environment resolution
        tracing_config = get_tracing_config(jgt_config)
        print(f"✅ Tracing config with env resolution:")
        print(json.dumps(tracing_config, indent=2))
        
        return True
        
    except Exception as e:
        print(f"❌ Failed to test enhanced config: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    print("🚀 Enhanced Configuration Test")
    print("=" * 40)
    
    success = test_enhanced_config_loading()
    
    if success:
        print("\n🎉 Enhanced configuration test passed!")
    else:
        print("\n❌ Enhanced configuration test failed!")
        sys.exit(1)