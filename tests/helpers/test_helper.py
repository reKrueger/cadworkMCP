"""
Test Helper Class
================

Base helper class providing common functionality for all Cadwork MCP tests.
Includes timing, logging, result formatting and test utilities.
"""

import time
import asyncio
from typing import Dict, Any, List, Optional, Callable, Tuple
from dataclasses import dataclass


@dataclass
class TestResult:
    """Standardized test result structure"""
    name: str
    status: str  # 'PASSED', 'FAILED', 'ERROR', 'SKIPPED'
    message: str
    execution_time: float
    details: Optional[Dict[str, Any]] = None


class TestHelper:
    """
    Base helper class for all Cadwork MCP tests.
    Provides common functionality like timing, formatting, validation.
    """
    
    def __init__(self):
        self.test_results: List[TestResult] = []
        self.start_time: float = 0
        self.current_section: str = ""
    
    def start_timer(self) -> None:
        """Start timing for test execution"""
        self.start_time = time.time()
    
    def get_elapsed_time(self) -> float:
        """Get elapsed time since start_timer() was called"""
        return time.time() - self.start_time
    
    def print_header(self, title: str, char: str = "=") -> None:
        """Print formatted section header"""
        print(f"\n{char * 60}")
        print(f" {title}")
        print(f"{char * 60}")
    
    def print_subheader(self, title: str) -> None:
        """Print formatted subsection header"""
        print(f"\n--- {title} ---")
        self.current_section = title
    
    def print_test_result(self, test_name: str, status: str, message: str = "", 
                         execution_time: Optional[float] = None) -> None:
        """Print formatted test result"""
        status_symbol = {
            'PASSED': '✅',
            'FAILED': '❌', 
            'ERROR': '⚠️',
            'SKIPPED': '⏭️'
        }.get(status, '❓')
        
        time_str = f" ({execution_time:.3f}s)" if execution_time else ""
        msg_str = f" - {message}" if message else ""
        
        print(f"  {status_symbol} {test_name}{time_str}{msg_str}")
    
    async def run_test(self, test_name: str, test_func: Callable, 
                      *args, **kwargs) -> TestResult:
        """
        Run a single test function with timing and error handling
        
        Args:
            test_name: Name of the test
            test_func: Async function to execute
            *args, **kwargs: Arguments for test_func
            
        Returns:
            TestResult with execution details
        """
        start_time = time.time()
        
        try:
            # Execute the test function
            result = await test_func(*args, **kwargs)
            execution_time = time.time() - start_time
            
            # Validate result
            if isinstance(result, dict) and result.get("status") == "success":
                test_result = TestResult(
                    name=test_name,
                    status="PASSED",
                    message=result.get("message", ""),
                    execution_time=execution_time,
                    details=result
                )
                self.print_test_result(test_name, "PASSED", "", execution_time)
            else:
                error_msg = result.get("message", "Unknown error") if isinstance(result, dict) else str(result)
                test_result = TestResult(
                    name=test_name,
                    status="FAILED", 
                    message=error_msg,
                    execution_time=execution_time,
                    details=result if isinstance(result, dict) else None
                )
                self.print_test_result(test_name, "FAILED", error_msg, execution_time)
                
        except Exception as e:
            execution_time = time.time() - start_time
            test_result = TestResult(
                name=test_name,
                status="ERROR",
                message=str(e),
                execution_time=execution_time,
                details=None
            )
            self.print_test_result(test_name, "ERROR", str(e), execution_time)
        
        self.test_results.append(test_result)
        return test_result
    
    async def run_test_batch(self, tests: List[Tuple[str, Callable, tuple, dict]]) -> List[TestResult]:
        """
        Run multiple tests in sequence
        
        Args:
            tests: List of (test_name, test_func, args, kwargs) tuples
            
        Returns:
            List of TestResult objects
        """
        results = []
        for test_name, test_func, args, kwargs in tests:
            result = await self.run_test(test_name, test_func, *args, **kwargs)
            results.append(result)
        return results
    
    def get_summary(self) -> Dict[str, Any]:
        """Get test execution summary"""
        total = len(self.test_results)
        passed = len([r for r in self.test_results if r.status == "PASSED"])
        failed = len([r for r in self.test_results if r.status == "FAILED"])
        errors = len([r for r in self.test_results if r.status == "ERROR"])
        skipped = len([r for r in self.test_results if r.status == "SKIPPED"])
        
        total_time = sum(r.execution_time for r in self.test_results)
        success_rate = (passed / total * 100) if total > 0 else 0
        
        return {
            "total_tests": total,
            "passed": passed,
            "failed": failed,
            "errors": errors,
            "skipped": skipped,
            "success_rate": success_rate,
            "total_execution_time": total_time,
            "tests_per_second": total / total_time if total_time > 0 else 0
        }
    
    def print_summary(self) -> None:
        """Print formatted test summary"""
        summary = self.get_summary()
        
        self.print_header("TEST SUMMARY")
        print(f"Total Tests:      {summary['total_tests']}")
        print(f"Passed:           {summary['passed']} ✅")
        print(f"Failed:           {summary['failed']} ❌")
        print(f"Errors:           {summary['errors']} ⚠️")
        print(f"Skipped:          {summary['skipped']} ⏭️")
        print(f"Success Rate:     {summary['success_rate']:.1f}%")
        print(f"Execution Time:   {summary['total_execution_time']:.2f}s")
        print(f"Tests/Second:     {summary['tests_per_second']:.1f}")
        
        # Print failed tests details
        failed_tests = [r for r in self.test_results if r.status in ["FAILED", "ERROR"]]
        if failed_tests:
            print(f"\n🔍 FAILED TESTS ({len(failed_tests)}):")
            print("-" * 50)
            for test in failed_tests:
                print(f"{test.status}: {test.name}")
                print(f"    Message: {test.message}")
                if test.details:
                    print(f"    Details: {test.details}")
                print()
    
    def clear_results(self) -> None:
        """Clear all test results"""
        self.test_results.clear()
    
    @staticmethod
    def validate_cadwork_response(response: Any, expected_keys: Optional[List[str]] = None) -> bool:
        """
        Validate a typical Cadwork API response
        
        Args:
            response: Response from Cadwork API
            expected_keys: Optional list of expected keys in response
            
        Returns:
            True if response is valid, False otherwise
        """
        if not isinstance(response, dict):
            return False
        
        # Check for success status
        if response.get("status") != "success":
            return False
        
        # Check for expected keys
        if expected_keys:
            for key in expected_keys:
                if key not in response:
                    return False
        
        return True
    
    @staticmethod
    def format_list_output(items: List[Any], max_items: int = 5) -> str:
        """Format list output for readable display"""
        if not items:
            return "[]"
        
        if len(items) <= max_items:
            return str(items)
        else:
            shown = items[:max_items]
            remaining = len(items) - max_items
            return f"{shown}... (+{remaining} more)"
