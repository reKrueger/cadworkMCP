#!/usr/bin/env python3
"""
Cadwork MCP Test Runner
======================

Clean, simple test runner for all Cadwork MCP tests.
Supports unit tests, integration tests, and various execution modes.

Usage:
    python run_test.py                    # Run all tests
    python run_test.py --quick            # Run quick tests only
    python run_test.py --unit             # Run unit tests only
    python run_test.py --integration      # Run integration tests only
    python run_test.py --controller=name  # Run specific controller tests
    python run_test.py --verbose          # Verbose output
    python run_test.py --mock             # Use mock (no Cadwork needed)
"""

import sys
import os
import asyncio
import argparse
import time
import importlib
from typing import List, Dict, Any
from pathlib import Path

# Add project root to path
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from tests.helpers.base_test import TestResult


class TestRunner:
    """Main test runner class"""
    
    def __init__(self, verbose: bool = False, mock: bool = False):
        self.verbose = verbose
        self.mock = mock
        self.results: List[TestResult] = []
        self.start_time = time.time()
        
    def print_header(self, title: str):
        """Print formatted header"""
        print("=" * 80)
        print(f"{title:^80}")
        print("=" * 80)
        
    def print_section(self, title: str):
        """Print section header"""
        print(f"\n[{title.upper()}]")
        print("=" * 50)
    
    async def discover_and_run_tests(self, test_path: str, pattern: str = "test_*.py") -> List[TestResult]:
        """Discover and run all tests in a directory"""
        test_results = []
        test_dir = Path(__file__).parent / test_path
        
        if not test_dir.exists():
            print(f"Warning: Test directory {test_dir} does not exist")
            return test_results
            
        # Find all test files
        test_files = list(test_dir.glob(pattern))
        
        for test_file in test_files:
            if test_file.name.startswith('__'):
                continue
                
            module_name = f"tests.{test_path}.{test_file.stem}"
            test_results.extend(await self.run_test_module(module_name))
        
        return test_results
    
    async def run_test_module(self, module_name: str) -> List[TestResult]:
        """Run all tests in a specific module"""
        results = []
        
        try:
            # Import the test module
            module = importlib.import_module(module_name)
            
            # Find all test classes
            test_classes = [
                getattr(module, name) for name in dir(module)
                if name.startswith('Test') and isinstance(getattr(module, name), type)
            ]
            
            for test_class in test_classes:
                results.extend(await self.run_test_class(test_class))
                
        except Exception as e:
            # Module failed to import or run
            results.append(TestResult(
                name=f"Module {module_name}",
                status="ERROR",
                message=f"Failed to run module: {e}",
                execution_time=0.0
            ))
            
        return results
    
    async def run_test_class(self, test_class) -> List[TestResult]:
        """Run all test methods in a test class"""
        results = []
        
        try:
            # Create test instance with mock flag
            if hasattr(test_class, '__init__'):
                # Check if constructor accepts use_mock parameter
                import inspect
                sig = inspect.signature(test_class.__init__)
                if 'use_mock' in sig.parameters:
                    test_instance = test_class(use_mock=self.mock)
                else:
                    test_instance = test_class()
            else:
                test_instance = test_class()
            
            # Find all test methods
            test_methods = [
                getattr(test_instance, method_name) 
                for method_name in dir(test_instance)
                if method_name.startswith('test_')
            ]
            
            for test_method in test_methods:
                test_name = f"{test_class.__name__}.{test_method.__name__}"
                result = await test_instance.run_test(test_method, test_name)
                results.append(result)
                
                # Print immediate feedback
                status_icon = "+" if result.status == "PASSED" else "-"
                print(f"  {status_icon} {test_name} - {result.status}")
                if result.status != "PASSED" and self.verbose:
                    print(f"    {result.message}")
                    
        except Exception as e:
            results.append(TestResult(
                name=f"Class {test_class.__name__}",
                status="ERROR",
                message=f"Failed to run test class: {e}",
                execution_time=0.0
            ))
            
        return results
    
    async def run_quick_tests(self) -> List[TestResult]:
        """Run essential quick tests only"""
        self.print_section("Quick Tests (Essential Only)")
        
        # Just run connection tests for quick check
        return await self.discover_and_run_tests("unit", "test_connection.py")
    
    async def run_unit_tests(self) -> List[TestResult]:
        """Run all unit tests"""
        self.print_section("Unit Tests")
        return await self.discover_and_run_tests("unit")
    
    async def run_integration_tests(self) -> List[TestResult]:
        """Run all integration tests"""
        self.print_section("Integration Tests") 
        return await self.discover_and_run_tests("integration")
    
    async def run_all_tests(self) -> List[TestResult]:
        """Run all tests"""
        results = []
        results.extend(await self.run_unit_tests())
        results.extend(await self.run_integration_tests())
        return results
    
    def print_summary(self, results: List[TestResult]):
        """Print comprehensive test summary"""
        total = len(results)
        passed = len([r for r in results if r.status == "PASSED"])
        failed = len([r for r in results if r.status == "FAILED"])
        errors = len([r for r in results if r.status == "ERROR"])
        
        success_rate = (passed / total * 100) if total > 0 else 0
        total_time = time.time() - self.start_time
        avg_time = sum(r.execution_time for r in results) / total if total > 0 else 0
        
        self.print_header("TEST SUMMARY")
        
        print(f"Tests Total:      {total}")
        print(f"Tests Passed:     {passed}")
        print(f"Tests Failed:     {failed}")
        print(f"Tests Errors:     {errors}")
        print(f"Success Rate:     {success_rate:.1f}%")
        print(f"Total Time:       {total_time:.2f}s")
        print(f"Average Time:     {avg_time:.3f}s per test")
        
        # Show failed tests
        failed_tests = [r for r in results if r.status in ["FAILED", "ERROR"]]
        if failed_tests:
            print(f"\nFAILED/ERROR TESTS ({len(failed_tests)}):")
            print("-" * 50)
            for test in failed_tests[:10]:  # Show first 10
                print(f"{test.status}: {test.name}")
                print(f"    {test.message}")
                if self.verbose and test.details:
                    print(f"    Details: {test.details}")
                print()
        
        # Status and recommendations
        if success_rate >= 90:
            status = "EXCELLENT"
            print(f"\nStatus: {status} - All systems working well!")
        elif success_rate >= 70:
            status = "GOOD" 
            print(f"\nStatus: {status} - Minor issues to investigate")
        elif success_rate >= 50:
            status = "PARTIAL"
            print(f"\nStatus: {status} - Some issues detected")
        else:
            status = "FAILED"
            print(f"\nStatus: {status} - Major issues detected")
            print("Recommendation: Check Cadwork connection and MCP Bridge")
        
        return success_rate >= 50


async def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(description="Cadwork MCP Test Runner")
    parser.add_argument('--quick', action='store_true', help='Run quick tests only')
    parser.add_argument('--unit', action='store_true', help='Run unit tests only')
    parser.add_argument('--integration', action='store_true', help='Run integration tests only')
    parser.add_argument('--controller', type=str, help='Run specific controller tests')
    parser.add_argument('--verbose', '-v', action='store_true', help='Verbose output')
    parser.add_argument('--mock', action='store_true', help='Use mock mode (no Cadwork needed)')
    
    args = parser.parse_args()
    
    runner = TestRunner(verbose=args.verbose, mock=args.mock)
    
    runner.print_header("CADWORK MCP TEST RUNNER")
    
    if args.mock:
        print("Mode: MOCK (No Cadwork connection required)")
    else:
        print("Mode: LIVE (Requires Cadwork 3D and MCP Bridge)")
    
    print(f"Verbose: {args.verbose}")
    print()
    
    try:
        # Run appropriate tests based on arguments
        if args.quick:
            results = await runner.run_quick_tests()
        elif args.unit:
            results = await runner.run_unit_tests()
        elif args.integration:
            results = await runner.run_integration_tests()
        elif args.controller:
            # Run specific controller tests (to be implemented)
            results = await runner.discover_and_run_tests("unit", f"test_{args.controller}.py")
        else:
            results = await runner.run_all_tests()
        
        # Print summary and return appropriate exit code
        success = runner.print_summary(results)
        return 0 if success else 1
        
    except KeyboardInterrupt:
        print("\nTests interrupted by user")
        return 1
    except Exception as e:
        print(f"\nTest runner error: {e}")
        if args.verbose:
            import traceback
            traceback.print_exc()
        return 1


if __name__ == "__main__":
    print("Cadwork MCP Test Runner")
    print("Ensure Cadwork 3D is running and MCP Bridge is started!")
    print()
    
    exit_code = asyncio.run(main())
    sys.exit(exit_code)
