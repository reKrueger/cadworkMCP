#!/usr/bin/env python3
"""
Direct Connection Test
"""

import sys
import os
import asyncio

# Add project root to path
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from core.connection import CadworkConnection

async def test_direct_connection():
    """Test direct connection to Cadwork"""
    print("Testing direct connection to Cadwork...")
    
    conn = CadworkConnection()
    
    try:
        # Test basic command
        result = conn.send_command("get_all_element_ids")
        print(f"Connection result: {result}")
        
        if result.get("status") in ["success", "ok"]:
            element_count = len(result.get("element_ids", []))
            print(f"SUCCESS: Connected to Cadwork! Found {element_count} elements")
            return True
        else:
            print(f"FAILED: {result}")
            return False
            
    except Exception as e:
        print(f"CONNECTION ERROR: {e}")
        return False

if __name__ == "__main__":
    success = asyncio.run(test_direct_connection())
    print(f"Connection test: {'PASSED' if success else 'FAILED'}")
