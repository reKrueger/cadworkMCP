#!/usr/bin/env python3
"""
Simple Cadwork MCP Test Runner
=============================
"""

import sys
import os
import time
import asyncio

# Add project root to path
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

# Import controllers directly
from controllers.element_controller import ElementController
from controllers.geometry_controller import GeometryController
from controllers.attribute_controller import AttributeController
from controllers.visualization_controller import CVisualizationController
from controllers.utility_controller import CUtilityController

def print_header(title: str) -> None:
    """Print formatted header"""
    print("=" * 80)
    print(f"{title:^80}")
    print("=" * 80)

def print_section(title: str) -> None:
    """Print section header"""
    print(f"\n[{title.upper()}]")
    print("=" * 50)

async def run_quick_tests():
    """Run essential quick tests"""
    print_header("CADWORK MCP QUICK TESTS")
    
    # Initialize controllers
    element_ctrl = ElementController()
    geometry_ctrl = GeometryController()
    viz_ctrl = CVisualizationController()
    util_ctrl = CUtilityController()
    
    tests_passed = 0
    tests_failed = 0
    tests_total = 0
    failed_tests = []
    
    start_time = time.time()
    
    print_section("Basic Connection Tests")
    
    # Test 1: Get all elements
    tests_total += 1
    try:
        result = await element_ctrl.get_all_element_ids()
        if result.get("status") == "success":
            element_count = len(result.get("element_ids", []))
            print(f"  + Get All Elements - PASSED ({element_count} elements)")
            tests_passed += 1
        else:
            print(f"  - Get All Elements - FAILED: {result.get('message', 'Unknown error')}")
            tests_failed += 1
            failed_tests.append(("Get All Elements", result.get('message', 'Unknown error')))
    except Exception as e:
        print(f"  - Get All Elements - ERROR: {e}")
        tests_failed += 1
        failed_tests.append(("Get All Elements", str(e)))
    
    # Test 2: Show all elements
    tests_total += 1
    try:
        result = await viz_ctrl.show_all_elements()
        if result.get("status") == "success":
            print(f"  + Show All Elements - PASSED")
            tests_passed += 1
        else:
            print(f"  - Show All Elements - FAILED: {result.get('message', 'Unknown error')}")
            tests_failed += 1
            failed_tests.append(("Show All Elements", result.get('message', 'Unknown error')))
    except Exception as e:
        print(f"  - Show All Elements - ERROR: {e}")
        tests_failed += 1
        failed_tests.append(("Show All Elements", str(e)))
    
    # Test 3: Get version info
    tests_total += 1
    try:
        result = await util_ctrl.get_cadwork_version_info()
        if result.get("status") == "success":
            version = result.get("version", "Unknown")
            print(f"  + Get Version Info - PASSED (Version: {version})")
            tests_passed += 1
        else:
            print(f"  - Get Version Info - FAILED: {result.get('message', 'Unknown error')}")
            tests_failed += 1
            failed_tests.append(("Get Version Info", result.get('message', 'Unknown error')))
    except Exception as e:
        print(f"  - Get Version Info - ERROR: {e}")
        tests_failed += 1
        failed_tests.append(("Get Version Info", str(e)))
    
    print_section("Element Creation Tests")
    
    # Test 4: Create beam
    tests_total += 1
    try:
        result = await element_ctrl.create_beam(
            p1=[0, 0, 0], p2=[1000, 0, 0], width=200, height=300
        )
        if result.get("status") == "success":
            element_id = result.get("element_id")
            print(f"  + Create Beam - PASSED (ID: {element_id})")
            tests_passed += 1
            
            # Test 5: Get element info
            tests_total += 1
            try:
                info_result = await geometry_ctrl.get_element_info(element_id)
                if info_result.get("status") == "success":
                    print(f"  + Get Element Info - PASSED")
                    tests_passed += 1
                else:
                    print(f"  - Get Element Info - FAILED: {info_result.get('message', 'Unknown error')}")
                    tests_failed += 1
                    failed_tests.append(("Get Element Info", info_result.get('message', 'Unknown error')))
            except Exception as e:
                print(f"  - Get Element Info - ERROR: {e}")
                tests_failed += 1
                failed_tests.append(("Get Element Info", str(e)))
            
            # Cleanup: Delete test element
            try:
                await element_ctrl.delete_elements([element_id])
                print(f"  + Cleanup - Test element deleted")
            except Exception as e:
                print(f"  - Cleanup - WARNING: Could not delete test element: {e}")
        else:
            print(f"  - Create Beam - FAILED: {result.get('message', 'Unknown error')}")
            tests_failed += 1
            failed_tests.append(("Create Beam", result.get('message', 'Unknown error')))
    except Exception as e:
        print(f"  - Create Beam - ERROR: {e}")
        tests_failed += 1
        failed_tests.append(("Create Beam", str(e)))
    
    # Summary
    end_time = time.time()
    duration = end_time - start_time
    success_rate = (tests_passed / tests_total * 100) if tests_total > 0 else 0
    
    print_header("TEST SUMMARY")
    
    print(f"Tests Total:      {tests_total}")
    print(f"Tests Passed:     {tests_passed}")
    print(f"Tests Failed:     {tests_failed}")
    print(f"Success Rate:     {success_rate:.1f}%")
    print(f"Execution Time:   {duration:.2f} seconds")
    
    if failed_tests:
        print(f"\nFAILED TESTS ({len(failed_tests)}):")
        print("-" * 50)
        for test_name, error_msg in failed_tests:
            print(f"{test_name}: {error_msg}")
    
    print(f"\nStatus: {'SUCCESS' if success_rate >= 80 else 'PARTIAL' if success_rate >= 50 else 'FAILED'}")
    return success_rate >= 50

if __name__ == "__main__":
    print("Cadwork MCP Quick Test Runner")
    print("Ensure Cadwork 3D is running and MCP Bridge is started!")
    print()
    
    try:
        success = asyncio.run(run_quick_tests())
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\nTests interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\nTest runner error: {e}")
        sys.exit(1)
