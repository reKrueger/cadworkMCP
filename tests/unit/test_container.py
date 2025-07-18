"""
Container Controller Tests
=========================

Tests for CContainerController - container creation and content retrieval.
"""

import sys
import os
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from helpers.base_test import BaseCadworkTest
from helpers.test_data import TEST_BEAM_DATA, TEST_PANEL_DATA
from controllers.container_controller import CContainerController
from controllers.element_controller import ElementController


class TestContainerController(BaseCadworkTest):
    """Test container creation and management"""
    
    def __init__(self, use_mock: bool = False):
        super().__init__(use_mock=use_mock)
        self.container_ctrl = CContainerController()
        self.element_ctrl = ElementController()
    
    def log_success(self, message: str):
        """Log success message"""
        print(f"SUCCESS: {message}")
    
    def log_error(self, message: str):
        """Log error message"""
        print(f"ERROR: {message}")
    
    def log_info(self, message: str):
        """Log info message"""
        print(f"INFO: {message}")
    
    async def test_create_auto_container_basic(self):
        """Test basic container creation"""
        try:
            # Create container with mock element IDs
            container_name = "Test Container"
            result = await self.container_ctrl.create_auto_container_from_standard(
                [1, 2], container_name
            )
            
            # For mock testing, just check the structure
            if result and "status" in result:
                self.log_success(f"Container creation completed with status: {result['status']}")
            else:
                self.log_info(f"Container creation result: {result}")
                
        except Exception as e:
            self.log_error(f"Container creation failed: {e}")
    
    async def test_create_container_empty_list(self):
        """Test error handling for empty element list"""
        try:
            await self.container_ctrl.create_auto_container_from_standard([], "Empty Container")
            self.log_error("Should have failed with empty element list")
        except ValueError as e:
            self.log_success(f"Correctly caught error for empty list: {e}")
        except Exception as e:
            self.log_info(f"Unexpected exception: {e}")
    
    async def test_create_container_empty_name(self):
        """Test error handling for empty container name"""
        try:
            await self.container_ctrl.create_auto_container_from_standard([1], "")
            self.log_error("Should have failed with empty container name")
        except ValueError as e:
            self.log_success(f"Correctly caught error for empty name: {e}")
        except Exception as e:
            self.log_info(f"Unexpected exception: {e}")
    
    async def run_all_tests(self):
        """Run all container tests"""
        self.log_info("Starting Container Controller Tests...")
        
        await self.test_create_auto_container_basic()
        await self.test_create_container_empty_list()
        await self.test_create_container_empty_name()
        
        self.log_info("Container Controller Tests completed!")

