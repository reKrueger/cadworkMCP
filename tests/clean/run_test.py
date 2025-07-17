#!/usr/bin/env python3
"""
Cadwork MCP Test Runner - Vereinfachte Version
==============================================

Eine einzige test_run() Funktion für alle wichtigen Tests.
Aufgeräumt und übersichtlich.

Verwendung:
    python run_test.py
"""

import sys
import os
import time
import asyncio
from typing import Dict, Any, List

# Add project root to path
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

# Import all controllers
from controllers.element_controller import ElementController
from controllers.geometry_controller import GeometryController
from controllers.attribute_controller import AttributeController
from controllers.visualization_controller import CVisualizationController


def print_header(title: str) -> None:
    """Print formatted header"""
    print("=" * 80)
    print(f"{title:^80}")
    print("=" * 80)


def print_section(title: str) -> None:
    """Print section header"""
    print(f"\n[{title.upper()}]")
    print("=" * 50)


async def test_run() -> bool:
    """
    Haupttest-Funktion - führt alle wichtigen Cadwork MCP Tests aus
    
    Returns:
        bool: True wenn alle Tests erfolgreich, False bei Fehlern
    """
    
    print_header("CADWORK MCP SERVER - SIMPLIFIED TEST RUNNER")
    
    print(f"Start Time: {time.strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"Python: {sys.version.split()[0]}")
    print(f"Project Root: {PROJECT_ROOT}")
    
    # Test statistics
    tests_total = 0
    tests_passed = 0
    tests_failed = 0
    start_time = time.time()
    failed_tests = []
    
    # Element Controller Tests
    print_section("Element Controller Tests")
    
    element_controller = ElementController()
    
    # Get All Elements
    tests_total += 1
    try:
        result = await element_controller.get_all_element_ids()
        if result.get("status") == "ok":
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
    
    # Create Beam
    tests_total += 1
    try:
        result = await element_controller.create_beam(
            p1=[0, 0, 0], p2=[1000, 0, 0], width=200, height=300
        )
        if result.get("status") == "ok":
            print(f"  + Create Beam - PASSED (ID: {result.get('id')})")
            tests_passed += 1
        else:
            print(f"  - Create Beam - FAILED: {result.get('message', 'Unknown error')}")
            tests_failed += 1
            failed_tests.append(("Create Beam", result.get('message', 'Unknown error')))
    except Exception as e:
        print(f"  - Create Beam - ERROR: {e}")
        tests_failed += 1
        failed_tests.append(("Create Beam", str(e)))
    
    # Create Panel
    tests_total += 1
    try:
        result = await element_controller.create_panel(
            p1=[2000, 0, 0], p2=[3000, 0, 0], width=1000, thickness=20
        )
        if result.get("status") == "ok":
            print(f"  + Create Panel - PASSED (ID: {result.get('id')})")
            tests_passed += 1
        else:
            print(f"  - Create Panel - FAILED: {result.get('message', 'Unknown error')}")
            tests_failed += 1
            failed_tests.append(("Create Panel", result.get('message', 'Unknown error')))
    except Exception as e:
        print(f"  - Create Panel - ERROR: {e}")
        tests_failed += 1
        failed_tests.append(("Create Panel", str(e)))
    
    # Create Surface
    tests_total += 1
    try:
        result = await element_controller.create_surface(
            vertices=[[0, 0, 0], [1000, 0, 0], [1000, 1000, 0], [0, 1000, 0]]
        )
        if result.get("status") == "ok":
            print(f"  + Create Surface - PASSED (ID: {result.get('id')})")
            tests_passed += 1
        else:
            print(f"  - Create Surface - FAILED: {result.get('message', 'Unknown error')}")
            tests_failed += 1
            failed_tests.append(("Create Surface", result.get('message', 'Unknown error')))
    except Exception as e:
        print(f"  - Create Surface - ERROR: {e}")
        tests_failed += 1
        failed_tests.append(("Create Surface", str(e)))
    
    # Geometry Controller Tests
    print_section("Geometry Controller Tests")
    
    geometry_controller = GeometryController()
    
    # Get Element Info
    tests_total += 1
    try:
        all_elements = await element_controller.get_all_element_ids()
        if all_elements.get("status") == "ok" and all_elements.get("element_ids"):
            element_id = all_elements["element_ids"][0]
            result = await geometry_controller.get_element_info(element_id)
            if result.get("status") == "ok":
                print(f"  + Get Element Info - PASSED (Element {element_id})")
                tests_passed += 1
            else:
                print(f"  - Get Element Info - FAILED: {result.get('message', 'Unknown error')}")
                tests_failed += 1
                failed_tests.append(("Get Element Info", result.get('message', 'Unknown error')))
        else:
            print("  ! Get Element Info - SKIPPED (No elements available)")
            tests_failed += 1
            failed_tests.append(("Get Element Info", "No elements available"))
    except Exception as e:
        print(f"  - Get Element Info - ERROR: {e}")
        tests_failed += 1
        failed_tests.append(("Get Element Info", str(e)))
    
    # Get Bounding Box
    tests_total += 1
    try:
        all_elements = await element_controller.get_all_element_ids()
        if all_elements.get("status") == "ok" and all_elements.get("element_ids"):
            element_id = all_elements["element_ids"][0]
            result = await geometry_controller.get_bounding_box(element_id)
            if result.get("status") == "ok":
                print(f"  + Get Bounding Box - PASSED (Element {element_id})")
                tests_passed += 1
            else:
                print(f"  - Get Bounding Box - FAILED: {result.get('message', 'Unknown error')}")
                tests_failed += 1
                failed_tests.append(("Get Bounding Box", result.get('message', 'Unknown error')))
        else:
            print("  ! Get Bounding Box - SKIPPED (No elements available)")
            tests_failed += 1
            failed_tests.append(("Get Bounding Box", "No elements available"))
    except Exception as e:
        print(f"  - Get Bounding Box - ERROR: {e}")
        tests_failed += 1
        failed_tests.append(("Get Bounding Box", str(e)))
    
    # Visualization Controller Tests
    print_section("Visualization Controller Tests")
    
    visualization_controller = CVisualizationController()
    
    # Show All Elements
    tests_total += 1
    try:
        result = await visualization_controller.show_all_elements()
        if result.get("status") == "success":
            visible_count = result.get("processed_count", 0)
            print(f"  + Show All Elements - PASSED ({visible_count} elements)")
            tests_passed += 1
        else:
            print(f"  - Show All Elements - FAILED: {result.get('message', 'Unknown error')}")
            tests_failed += 1
            failed_tests.append(("Show All Elements", result.get('message', 'Unknown error')))
    except Exception as e:
        print(f"  - Show All Elements - ERROR: {e}")
        tests_failed += 1
        failed_tests.append(("Show All Elements", str(e)))
    
    # Get Visible Element Count
    tests_total += 1
    try:
        result = await visualization_controller.get_visible_element_count()
        if result.get("status") == "success":
            visible_count = result.get("visible_elements", 0)
            total_count = result.get("total_elements", 0)
            percentage = result.get("visibility_percentage", 0)
            print(f"  + Get Visible Count - PASSED ({visible_count}/{total_count} = {percentage:.1f}%)")
            tests_passed += 1
        else:
            print(f"  - Get Visible Count - FAILED: {result.get('message', 'Unknown error')}")
            tests_failed += 1
            failed_tests.append(("Get Visible Count", result.get('message', 'Unknown error')))
    except Exception as e:
        print(f"  - Get Visible Count - ERROR: {e}")
        tests_failed += 1
        failed_tests.append(("Get Visible Count", str(e)))
    
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
    print(f"Tests per Second: {tests_total/duration:.1f}")
    
    if failed_tests:
        print(f"\nFAILED TESTS ({len(failed_tests)}):")
        print("-" * 50)
        for test_name, error_msg in failed_tests:
            print(f"  {test_name}: {error_msg}")
    
    if tests_failed == 0:
        print("\nALL TESTS PASSED!")
        return True
    else:
        print(f"\n{tests_failed} TESTS FAILED")
        return False


# Backwards compatibility
async def runTest() -> bool:
    """Legacy function name for compatibility"""
    return await test_run()


def main():
    """Entry point when script is run directly"""
    try:
        success = asyncio.run(test_run())
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n\nTests interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n\nUnexpected error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
