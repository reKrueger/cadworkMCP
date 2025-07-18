"""
Base Test Class for Cadwork MCP Tests
====================================

Provides common functionality for all tests including connection management,
setup/teardown, and common assertions.
"""

import time
import asyncio
from typing import Dict, Any, List, Optional
from dataclasses import dataclass

# Add project root to path
import sys
import os
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from core.connection import initialize_connection, get_connection
from helpers.cadwork_mock import MockCadworkConnection
from helpers.global_mock import enable_mock, disable_mock, is_mock_enabled, mock_send_command


@dataclass
class TestResult:
    """Standardized test result structure"""
    name: str
    status: str  # 'PASSED', 'FAILED', 'ERROR', 'SKIPPED'
    message: str
    execution_time: float
    details: Optional[Dict[str, Any]] = None


class BaseCadworkTest:
    """
    Base class for all Cadwork MCP tests.
    Handles connection management, cleanup, and common functionality.
    """
    
    def __init__(self, use_mock: bool = False):
        self.created_elements: List[int] = []
        self.connection_initialized = False
        self.use_mock = use_mock
        self.mock_connection = None
        
    def setUp(self):
        """Setup test environment"""
        try:
            if self.use_mock:
                # Enable global mock mode
                enable_mock()
                self.connection_initialized = True
                
                # Monkey patch all controllers to use mock
                self._patch_controllers_for_mock()
                return True
            else:
                # Initialize real connection if not already done
                if not self.connection_initialized:
                    initialize_connection()
                    self.connection_initialized = True
                
                # Verify connection works
                connection = get_connection()
                response = connection.send_command("ping")
                if response.get("status") != "ok":
                    raise ConnectionError("Cadwork bridge not responding")
                    
                return True
        except Exception as e:
            print(f"Setup failed: {e}")
            return False
    
    def tearDown(self):
        """Cleanup test environment"""
        # Restore controllers if we patched them
        if self.use_mock:
            self._restore_controllers_from_mock()
            disable_mock()
        
        # Delete any elements we created during testing (only for real connections)
        if self.created_elements and not self.use_mock:
            try:
                from controllers.element_controller import ElementController
                element_ctrl = ElementController()
                asyncio.run(element_ctrl.delete_elements(self.created_elements))
                print(f"Cleaned up {len(self.created_elements)} test elements")
            except Exception as e:
                print(f"Warning: Could not cleanup test elements: {e}")
            finally:
                self.created_elements.clear()
    
    def _patch_controllers_for_mock(self):
        """Patch all controller instances to use mock"""
        self._original_methods = {}
        
        # Patch controllers that exist in this test instance
        for attr_name in dir(self):
            attr = getattr(self, attr_name)
            if hasattr(attr, 'send_command') and hasattr(attr, 'controller_name'):
                # This is a controller, patch its send_command method
                self._original_methods[attr_name] = attr.send_command
                attr.send_command = self._mock_send_command_wrapper
    
    def _restore_controllers_from_mock(self):
        """Restore original controller methods"""
        if hasattr(self, '_original_methods'):
            for attr_name, original_method in self._original_methods.items():
                if hasattr(self, attr_name):
                    controller = getattr(self, attr_name)
                    controller.send_command = original_method
    
    def _mock_send_command_wrapper(self, operation: str, args: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Wrapper for mock send_command"""
        return mock_send_command(operation, args)
    
    def track_element(self, element_id: int):
        """Track an element for cleanup"""
        if element_id and element_id not in self.created_elements:
            self.created_elements.append(element_id)
    
    def assert_success(self, result: Dict[str, Any], operation: str = "operation") -> bool:
        """Assert that a Cadwork operation was successful"""
        if not isinstance(result, dict):
            raise AssertionError(f"{operation} returned non-dict: {result}")
        
        status = result.get("status")
        if status in ["ok", "success"]:
            return True
        elif status == "error":
            message = result.get("message", "Unknown error")
            raise AssertionError(f"{operation} failed: {message}")
        else:
            raise AssertionError(f"{operation} returned unexpected status: {status}")
    
    def assert_element_id(self, result: Dict[str, Any], operation: str = "operation") -> int:
        """Assert that result contains a valid element ID and track it"""
        self.assert_success(result, operation)
        
        element_id = result.get("element_id")
        if not element_id or not isinstance(element_id, int) or element_id <= 0:
            raise AssertionError(f"{operation} did not return valid element_id: {element_id}")
        
        self.track_element(element_id)
        return element_id
    
    def assert_element_list(self, result: Dict[str, Any], operation: str = "operation") -> List[int]:
        """Assert that result contains a list of element IDs"""
        self.assert_success(result, operation)
        
        element_ids = result.get("element_ids", [])
        if not isinstance(element_ids, list):
            raise AssertionError(f"{operation} did not return element_ids list: {element_ids}")
        
        return element_ids
    
    async def run_test(self, test_func, test_name: str) -> TestResult:
        """Run a single test function with timing and error handling"""
        start_time = time.time()
        
        try:
            # Setup
            if not self.setUp():
                return TestResult(
                    name=test_name,
                    status="ERROR", 
                    message="Test setup failed",
                    execution_time=time.time() - start_time
                )
            
            # Temporarily replace connection if using mock
            original_send_command = None
            if self.use_mock and hasattr(self, 'element_ctrl'):
                # Monkey patch the controller's send_command method
                if hasattr(self.element_ctrl, 'send_command'):
                    original_send_command = self.element_ctrl.send_command
                    self.element_ctrl.send_command = self._mock_send_command
            
            # Run test
            if asyncio.iscoroutinefunction(test_func):
                result = await test_func()
            else:
                result = test_func()
            
            # Restore original method
            if original_send_command and hasattr(self, 'element_ctrl'):
                self.element_ctrl.send_command = original_send_command
            
            # Test passed
            execution_time = time.time() - start_time
            return TestResult(
                name=test_name,
                status="PASSED",
                message="Test completed successfully",
                execution_time=execution_time,
                details=result if isinstance(result, dict) else None
            )
            
        except AssertionError as e:
            return TestResult(
                name=test_name,
                status="FAILED",
                message=str(e),
                execution_time=time.time() - start_time
            )
        except Exception as e:
            return TestResult(
                name=test_name,
                status="ERROR", 
                message=f"Unexpected error: {e}",
                execution_time=time.time() - start_time
            )
        finally:
            # Always cleanup (but only if not using mock)
            if not self.use_mock:
                self.tearDown()
    
    def _mock_send_command(self, operation: str, args: Dict[str, Any] = None) -> Dict[str, Any]:
        """Mock send_command method for controllers"""
        return self.mock_connection.send_command(operation, args)


class MockCadworkTest(BaseCadworkTest):
    """
    Mock version of BaseCadworkTest for testing without Cadwork connection
    """
    
    def setUp(self):
        """Mock setup - always succeeds"""
        self.connection_initialized = True
        return True
    
    def mock_response(self, operation: str, success: bool = True, **kwargs) -> Dict[str, Any]:
        """Generate mock response"""
        if success:
            response = {"status": "ok"}
            
            # Add operation-specific mock data
            if operation == "get_all_element_ids":
                response["element_ids"] = [12345, 67890]
            elif operation.startswith("create_"):
                response["element_id"] = 99999
            elif operation == "get_element_info":
                response.update({
                    "width": 200,
                    "height": 300, 
                    "length": 1000,
                    "material": "Wood"
                })
            
            response.update(kwargs)
            return response
        else:
            return {"status": "error", "message": "Mock operation failed"}
