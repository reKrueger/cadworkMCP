#!/usr/bin/env python3
"""
Working Cadwork MCP Test Runner
==============================
"""

import sys
import os
import time
import asyncio

# Add project root to path
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from core.connection import CadworkConnection

def print_header(title: str) -> None:
    """Print formatted header"""
    print("=" * 80)
    print(f"{title:^80}")
    print("=" * 80)

def print_section(title: str) -> None:
    """Print section header"""
    print(f"\n[{title.upper()}]")
    print("=" * 50)

async def run_working_tests():
    """Run tests using direct connection"""
    print_header("CADWORK MCP WORKING TESTS")
    
    conn = CadworkConnection()
    
    tests_passed = 0
    tests_failed = 0
    tests_total = 0
    failed_tests = []
    
    start_time = time.time()
    
    print_section("Connection & Basic Tests")
    
    # Test 1: Get all elements
    tests_total += 1
    try:
        result = conn.send_command("get_all_element_ids")
        if result.get("status") in ["success", "ok"]:
            element_count = len(result.get("element_ids", []))
            print(f"  + Get All Elements - PASSED ({element_count} elements)")
            tests_passed += 1
        else:
            print(f"  - Get All Elements - FAILED: {result}")
            tests_failed += 1
            failed_tests.append(("Get All Elements", str(result)))
    except Exception as e:
        print(f"  - Get All Elements - ERROR: {e}")
        tests_failed += 1
        failed_tests.append(("Get All Elements", str(e)))
    
    # Test 2: Create beam
    tests_total += 1
    try:
        result = conn.send_command("create_beam", {
            "p1": [0, 0, 0],
            "p2": [1000, 0, 0], 
            "width": 200,
            "height": 300
        })
        if result.get("status") in ["success", "ok"]:
            element_id = result.get("element_id")
            print(f"  + Create Beam - PASSED (ID: {element_id})")
            tests_passed += 1
            
            # Test 3: Get element info  
            tests_total += 1
            try:
                info_result = conn.send_command("get_element_info", {"element_id": element_id})
                if info_result.get("status") in ["success", "ok"]:
                    width = info_result.get("width", "Unknown")
                    height = info_result.get("height", "Unknown")
                    print(f"  + Get Element Info - PASSED (W:{width}mm, H:{height}mm)")
                    tests_passed += 1
                else:
                    print(f"  - Get Element Info - FAILED: {info_result}")
                    tests_failed += 1
                    failed_tests.append(("Get Element Info", str(info_result)))
            except Exception as e:
                print(f"  - Get Element Info - ERROR: {e}")
                tests_failed += 1
                failed_tests.append(("Get Element Info", str(e)))
            
            # Test 4: Delete element (cleanup)
            tests_total += 1
            try:
                del_result = conn.send_command("delete_elements", {"element_ids": [element_id]})
                if del_result.get("status") in ["success", "ok"]:
                    print(f"  + Delete Element - PASSED (Cleanup successful)")
                    tests_passed += 1
                else:
                    print(f"  - Delete Element - FAILED: {del_result}")
                    tests_failed += 1
                    failed_tests.append(("Delete Element", str(del_result)))
            except Exception as e:
                print(f"  - Delete Element - ERROR: {e}")
                tests_failed += 1
                failed_tests.append(("Delete Element", str(e)))
                
        else:
            print(f"  - Create Beam - FAILED: {result}")
            tests_failed += 1
            failed_tests.append(("Create Beam", str(result)))
    except Exception as e:
        print(f"  - Create Beam - ERROR: {e}")
        tests_failed += 1
        failed_tests.append(("Create Beam", str(e)))
    
    # Test 5: Create panel
    tests_total += 1
    try:
        result = conn.send_command("create_panel", {
            "p1": [2000, 0, 0],
            "p2": [3000, 0, 0],
            "width": 2000,
            "thickness": 20
        })
        if result.get("status") in ["success", "ok"]:
            element_id = result.get("element_id")
            print(f"  + Create Panel - PASSED (ID: {element_id})")
            tests_passed += 1
            
            # Cleanup panel
            try:
                conn.send_command("delete_elements", {"element_ids": [element_id]})
            except:
                pass
                
        else:
            print(f"  - Create Panel - FAILED: {result}")
            tests_failed += 1
            failed_tests.append(("Create Panel", str(result)))
    except Exception as e:
        print(f"  - Create Panel - ERROR: {e}")
        tests_failed += 1
        failed_tests.append(("Create Panel", str(e)))
    
    # Test 6: Visualization test
    tests_total += 1
    try:
        result = conn.send_command("show_all_elements")
        if result.get("status") in ["success", "ok"]:
            processed = result.get("processed_count", "Unknown")
            print(f"  + Show All Elements - PASSED ({processed} elements processed)")
            tests_passed += 1
        else:
            print(f"  - Show All Elements - FAILED: {result}")
            tests_failed += 1
            failed_tests.append(("Show All Elements", str(result)))
    except Exception as e:
        print(f"  - Show All Elements - ERROR: {e}")
        tests_failed += 1
        failed_tests.append(("Show All Elements", str(e)))
    
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
            print(f"FAILED {test_name}: {error_msg}")
    
    # Status assessment
    if success_rate >= 90:
        status = "EXCELLENT"
        recommendation = "All systems working perfectly!"
    elif success_rate >= 70:
        status = "GOOD"
        recommendation = "Minor issues detected, but overall functional."
    elif success_rate >= 50:
        status = "PARTIAL"
        recommendation = "Some functionality working, investigate failed tests."
    else:
        status = "FAILED"
        recommendation = "Major issues detected. Check Cadwork connection."
    
    print(f"\nSTATUS: {status}")
    print(f"RECOMMENDATION: {recommendation}")
    
    return success_rate >= 50

if __name__ == "__main__":
    print("Cadwork MCP Working Test Runner")
    print("Cadwork 3D is running and MCP Bridge is started!")
    print()
    
    try:
        success = asyncio.run(run_working_tests())
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\nTests interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\nTest runner error: {e}")
        sys.exit(1)
