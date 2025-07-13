"""
Main Test Runner
"""
import sys
import os
import time
from typing import List, Dict, Any

# Add project root to path
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, PROJECT_ROOT)

from tests.test_config import TestResult
from tests.test_element_controller import ElementControllerTests
from tests.test_geometry_controller import GeometryControllerTests
from tests.test_attribute_controller import AttributeControllerTests
from tests.test_visualization_controller import VisualizationControllerTests
from tests.test_utility_controller import UtilityControllerTests
from tests.test_system import SystemTests

def print_separator(char="=", length=80):
    """Print a separator line"""
    print(char * length)

def print_header(title: str):
    """Print a formatted header"""
    print_separator()
    print(f" {title} ".center(80))
    print_separator()

def print_summary_table(summaries: List[Dict[str, Any]]):
    """Print a formatted summary table"""
    print("\n" + "="*80)
    print(" TEST SUMMARY ".center(80))
    print("="*80)
    
    # Table header
    print(f"{'Suite':<30} {'Total':<8} {'Passed':<8} {'Failed':<8} {'Success':<10} {'Time':<8}")
    print("-" * 80)
    
    # Table rows
    total_tests = 0
    total_passed = 0
    total_failed = 0
    total_time = 0.0
    
    for summary in summaries:
        suite_name = summary["suite_name"]
        total = summary["total_tests"]
        passed = summary["passed"]
        failed = summary["failed"]
        success_rate = summary["success_rate"]
        duration = summary["total_duration"]
        
        total_tests += total
        total_passed += passed
        total_failed += failed
        total_time += duration
        
        print(f"{suite_name:<30} {total:<8} {passed:<8} {failed:<8} {success_rate:>6.1f}%   {duration:>6.2f}s")
    
    # Total row
    print("-" * 80)
    overall_success = (total_passed / total_tests * 100) if total_tests > 0 else 0
    print(f"{'TOTAL':<30} {total_tests:<8} {total_passed:<8} {total_failed:<8} {overall_success:>6.1f}%   {total_time:>6.2f}s")
    print("="*80)

def print_failed_tests(summaries: List[Dict[str, Any]]):
    """Print details of failed tests"""
    failed_tests = []
    
    for summary in summaries:
        for result in summary["results"]:
            if not result.success:
                failed_tests.append((summary["suite_name"], result))
    
    if failed_tests:
        print("\n" + "="*80)
        print(" FAILED TESTS DETAILS ".center(80))
        print("="*80)
        
        for suite_name, result in failed_tests:
            print(f"\n[{suite_name}] {result.test_name}")
            print(f"  Error: {result.message}")
            print(f"  Duration: {result.duration:.2f}s")
        
        print("="*80)

def run_connection_test():
    """Test if Cadwork connection is available"""
    print_header("CADWORK CONNECTION TEST")
    
    try:
        # Import bridge to test connection
        from core.connection import get_connection
        
        print("Testing bridge connection...")
        connection = get_connection()
        result = connection.send_command("ping")
        
        if result.get("status") == "ok":
            print("+ Bridge connection successful")
            return True
        else:
            print(f"X Bridge connection failed: {result.get('message')}")
            return False
            
    except Exception as e:
        print(f"X Connection test failed: {e}")
        print("\nPlease ensure:")
        print("1. Cadwork 3D is running")
        print("2. Bridge is started (run start.txt in Cadwork Python console)")
        print("3. Bridge is listening on port 53002")
        return False

def run_all_tests(skip_connection_test=False):
    """Run all test suites"""
    start_time = time.time()
    
    print_header("CADWORK MCP SERVER TEST SUITE")
    print(f"Start Time: {time.strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"Python: {sys.version.split()[0]}")
    print(f"Project Root: {PROJECT_ROOT}")
    
    # Connection test
    if not skip_connection_test:
        if not run_connection_test():
            print("\nX Skipping tests due to connection failure")
            print("Use --skip-connection to run tests without connection check")
            return False
    
    # Initialize test suites
    test_suites = [
        ElementControllerTests(),
        GeometryControllerTests(), 
        AttributeControllerTests(),
        VisualizationControllerTests(),
        UtilityControllerTests(),
        SystemTests()
    ]
    
    # Run all test suites
    summaries = []
    for suite in test_suites:
        try:
            summary = suite.run_all_tests()
            summaries.append(summary)
        except KeyboardInterrupt:
            print(f"\nX Tests interrupted during {suite.name}")
            break
        except Exception as e:
            print(f"\nX Test suite {suite.name} crashed: {e}")
            # Create error summary
            error_summary = {
                "suite_name": suite.name,
                "total_tests": 1,
                "passed": 0,
                "failed": 1,
                "success_rate": 0.0,
                "total_duration": 0.0,
                "results": [TestResult(f"{suite.name}_crash", False, str(e), 0.0)]
            }
            summaries.append(error_summary)
    
    # Print results
    if summaries:
        print_summary_table(summaries)
        print_failed_tests(summaries)
        
        total_duration = time.time() - start_time
        total_tests = sum(s["total_tests"] for s in summaries)
        total_passed = sum(s["passed"] for s in summaries)
        
        print(f"\nTotal Execution Time: {total_duration:.2f} seconds")
        print(f"Tests Per Second: {total_tests/total_duration:.1f}")
        
        if total_passed == total_tests:
            print("\n[SUCCESS] ALL TESTS PASSED!")
            return True
        else:
            print(f"\n[WARNING] {total_tests - total_passed} TESTS FAILED")
            return False
    else:
        print("\nX No test results available")
        return False

def main():
    """Main entry point"""
    import argparse
    
    parser = argparse.ArgumentParser(description="Cadwork MCP Server Test Suite")
    parser.add_argument("--skip-connection", action="store_true", 
                       help="Skip connection test (useful for testing without Cadwork)")
    parser.add_argument("--suite", choices=["element", "geometry", "attribute", "visualization", "utility", "system"], 
                       help="Run only specific test suite")
    
    args = parser.parse_args()
    
    if args.suite:
        # Run specific suite
        suite_map = {
            "element": ElementControllerTests,
            "geometry": GeometryControllerTests,
            "attribute": AttributeControllerTests,
            "visualization": VisualizationControllerTests,
            "utility": UtilityControllerTests,
            "system": SystemTests
        }
        
        suite_class = suite_map[args.suite]
        suite = suite_class()
        
        if not args.skip_connection and not run_connection_test():
            print("Connection test failed. Use --skip-connection to run anyway.")
            return
        
        summary = suite.run_all_tests()
        print_summary_table([summary])
        print_failed_tests([summary])
    else:
        # Run all tests
        success = run_all_tests(args.skip_connection)
        sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()
