"""
Test Configuration and Utilities
"""
import sys
import os
from typing import Dict, Any, List
import time

# Add project root to path
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

class TestResult:
    """Test result container"""
    def __init__(self, test_name: str, success: bool, message: str = "", duration: float = 0.0):
        self.test_name = test_name
        self.success = success
        self.message = message
        self.duration = duration
        self.timestamp = time.time()

class TestSuite:
    """Base test suite class"""
    def __init__(self, name: str):
        self.name = name
        self.results: List[TestResult] = []
        self.setup_done = False
    
    def log(self, message: str):
        """Log a message during testing"""
        print(f"  {message}")
    
    def setup(self):
        """Override in subclasses for setup"""
        pass
    
    def teardown(self):
        """Override in subclasses for cleanup"""
        pass
    
    def run_test(self, test_func, test_name: str = None) -> TestResult:
        """Run a single test function"""
        if not self.setup_done:
            self.setup()
            self.setup_done = True
            
        if test_name is None:
            test_name = test_func.__name__
            
        print(f"Running {test_name}...")
        start_time = time.time()
        
        try:
            result = test_func()
            duration = time.time() - start_time
            
            if isinstance(result, dict) and result.get("status") == "ok":
                test_result = TestResult(test_name, True, "PASSED", duration)
                print(f"  + PASSED ({duration:.2f}s)")
            elif isinstance(result, dict) and result.get("status") == "error":
                test_result = TestResult(test_name, False, f"API Error: {result.get('message')}", duration)
                print(f"  X FAILED: {result.get('message')} ({duration:.2f}s)")
            else:
                test_result = TestResult(test_name, True, f"Unexpected result: {result}", duration)
                print(f"  ? UNCLEAR: {result} ({duration:.2f}s)")
                
        except Exception as e:
            duration = time.time() - start_time
            test_result = TestResult(test_name, False, f"Exception: {str(e)}", duration)
            print(f"  X FAILED: {str(e)} ({duration:.2f}s)")
        
        self.results.append(test_result)
        return test_result
    
    def run_all_tests(self) -> Dict[str, Any]:
        """Run all test methods (methods starting with 'test_')"""
        test_methods = [method for method in dir(self) if method.startswith('test_')]
        
        print(f"\n=== Running {self.name} ===")
        for method_name in test_methods:
            method = getattr(self, method_name)
            self.run_test(method, method_name)
        
        self.teardown()
        return self.get_summary()
    
    def get_summary(self) -> Dict[str, Any]:
        """Get test summary"""
        total = len(self.results)
        passed = sum(1 for r in self.results if r.success)
        failed = total - passed
        total_duration = sum(r.duration for r in self.results)
        
        return {
            "suite_name": self.name,
            "total_tests": total,
            "passed": passed,
            "failed": failed,
            "success_rate": (passed / total * 100) if total > 0 else 0,
            "total_duration": total_duration,
            "results": self.results
        }

def assert_ok(result: Dict[str, Any], message: str = ""):
    """Assert that result status is 'ok'"""
    if not isinstance(result, dict):
        raise AssertionError(f"Expected dict result, got {type(result)}: {result}")
    if result.get("status") != "ok":
        raise AssertionError(f"Expected status 'ok', got '{result.get('status')}': {result.get('message', '')} {message}")

def assert_error(result: Dict[str, Any], message: str = ""):
    """Assert that result status is 'error'"""
    if not isinstance(result, dict):
        raise AssertionError(f"Expected dict result, got {type(result)}: {result}")
    if result.get("status") != "error":
        raise AssertionError(f"Expected status 'error', got '{result.get('status')}' {message}")

def assert_has_key(result: Dict[str, Any], key: str, message: str = ""):
    """Assert that result has specific key"""
    if key not in result:
        raise AssertionError(f"Expected key '{key}' in result {message}")

def assert_element_id(result: Dict[str, Any], message: str = ""):
    """Assert that result contains valid element_id"""
    assert_ok(result)
    assert_has_key(result, "element_id")
    element_id = result["element_id"]
    if not isinstance(element_id, int) or element_id <= 0:
        raise AssertionError(f"Expected positive integer element_id, got {element_id} {message}")

def assert_equal(actual, expected, message: str = ""):
    """Assert that two values are equal"""
    if actual != expected:
        raise AssertionError(f"Expected {expected}, got {actual} {message}")

def assert_in(item, container, message: str = ""):
    """Assert that item is in container"""
    if item not in container:
        raise AssertionError(f"Expected {item} to be in {container} {message}")

def assert_list_equal(actual, expected, message: str = ""):
    """Assert that two lists are equal"""
    if actual != expected:
        raise AssertionError(f"Expected list {expected}, got {actual} {message}")

# Test data containers
TEST_POINTS = {
    "origin": [0, 0, 0],
    "x_1000": [1000, 0, 0],
    "y_1000": [0, 1000, 0],
    "z_1000": [0, 0, 1000],
    "xy_1000": [1000, 1000, 0],
    "xyz_1000": [1000, 1000, 1000]
}

TEST_VECTORS = {
    "x_unit": [1, 0, 0],
    "y_unit": [0, 1, 0], 
    "z_unit": [0, 0, 1],
    "x_neg": [-1, 0, 0],
    "y_neg": [0, -1, 0],
    "z_neg": [0, 0, -1]
}

TEST_MATERIALS = [
    "C24",
    "BSH GL24h", 
    "OSB 18mm",
    "S355",
    "C30/37"
]

TEST_NAMES = [
    "Test_Balken",
    "Test_Platte", 
    "Test_Stütze",
    "Test_Unterzug"
]
