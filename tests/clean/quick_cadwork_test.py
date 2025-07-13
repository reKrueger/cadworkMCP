#!/usr/bin/env python3
"""
Quick Fixed Test - Only working functions
"""

import sys
import os
import time
import asyncio
from typing import Dict, Any

# Add project root to path
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from controllers.element_controller import ElementController
from core.connection import initialize_connection, get_connection

async def test_create_beam():
    """Test creating a beam"""
    controller = ElementController()
    result = await controller.create_beam(
        p1=[0, 0, 0],
        p2=[1000, 0, 0],
        width=100,
        height=200
    )
    return result

async def test_get_all_elements():
    """Test getting all elements"""
    controller = ElementController()
    result = await controller.get_all_element_ids()
    return result

async def quick_test():
    """Run a quick test with working Cadwork connection"""
    print("=" * 60)
    print(" QUICK CADWORK CONNECTION TEST ".center(60))
    print("=" * 60)
    
    # Test connection
    try:
        initialize_connection("127.0.0.1", 53002)
        conn = get_connection()
        ping_result = conn.send_command("ping", {})
        print(f"Ping: {ping_result}")
        
        if ping_result.get("status") != "ok":
            print("X Connection failed")
            return
            
        print("+ Connection successful!")
        
        # Test beam creation
        print("\nTesting beam creation...")
        beam_result = await test_create_beam()
        print(f"Create Beam: {beam_result}")
        
        # Test getting elements
        print("\nTesting get all elements...")
        elements_result = await test_get_all_elements()
        print(f"Get Elements: {elements_result}")
        
        print("\n" + "=" * 60)
        print("QUICK TEST COMPLETED!")
        
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(quick_test())
