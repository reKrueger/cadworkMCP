"""
Extended Attribute Controller Tests
===================================

Tests for extended AttributeController functionality - user attributes and display names.
"""

import sys
import os
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from helpers.base_test import BaseCadworkTest
from controllers.attribute_controller import AttributeController


class TestExtendedAttributeController(BaseCadworkTest):
    """Test extended attribute management operations"""
    
    def __init__(self, use_mock: bool = False):
        super().__init__(use_mock=use_mock)
        self.attribute_ctrl = AttributeController()
    
    def log_success(self, message: str):
        """Log success message"""
        print(f"SUCCESS: {message}")
    
    def log_error(self, message: str):
        """Log error message"""
        print(f"ERROR: {message}")
    
    def log_info(self, message: str):
        """Log info message"""
        print(f"INFO: {message}")
    
    async def test_set_user_attribute_basic(self):
        """Test setting user-defined attribute"""
        try:
            # Set user attribute with mock element ID
            element_ids = [1, 2]
            attribute_number = 1
            attribute_value = "Custom Value 123"
            
            result = await self.attribute_ctrl.set_user_attribute(
                element_ids, attribute_number, attribute_value
            )
            
            if result and "status" in result:
                self.log_success(f"Set user attribute {attribute_number} completed with status: {result['status']}")
            else:
                self.log_info(f"Set user attribute result: {result}")
                
        except Exception as e:
            self.log_error(f"Set user attribute failed: {e}")
    
    async def test_get_attribute_display_name_basic(self):
        """Test getting attribute display name"""
        try:
            # Get display name for attribute number 1
            attribute_number = 1
            
            result = await self.attribute_ctrl.get_element_attribute_display_name(attribute_number)
            
            if result and "status" in result:
                self.log_success(f"Get attribute display name completed with status: {result['status']}")
                if "display_name" in result:
                    self.log_info(f"Attribute {attribute_number} display name: {result['display_name']}")
            else:
                self.log_info(f"Get attribute display name result: {result}")
                
        except Exception as e:
            self.log_error(f"Get attribute display name failed: {e}")
    
    async def test_set_user_attribute_empty_list(self):
        """Test error handling for empty element list"""
        try:
            await self.attribute_ctrl.set_user_attribute([], 1, "test value")
            self.log_error("Should have failed with empty element list")
        except ValueError as e:
            self.log_success(f"Correctly caught error for empty list: {e}")
        except Exception as e:
            self.log_info(f"Unexpected exception: {e}")
    
    async def test_set_user_attribute_invalid_number(self):
        """Test error handling for invalid attribute number"""
        try:
            await self.attribute_ctrl.set_user_attribute([1], 0, "test value")
            self.log_error("Should have failed with invalid attribute number")
        except ValueError as e:
            self.log_success(f"Correctly caught error for invalid attribute number: {e}")
        except Exception as e:
            self.log_info(f"Unexpected exception: {e}")
    
    async def test_set_user_attribute_non_string_value(self):
        """Test error handling for non-string attribute value"""
        try:
            await self.attribute_ctrl.set_user_attribute([1], 1, 123)
            self.log_error("Should have failed with non-string value")
        except ValueError as e:
            self.log_success(f"Correctly caught error for non-string value: {e}")
        except Exception as e:
            self.log_info(f"Unexpected exception: {e}")
    
    async def test_get_display_name_invalid_number(self):
        """Test error handling for invalid attribute number"""
        try:
            await self.attribute_ctrl.get_element_attribute_display_name(-1)
            self.log_error("Should have failed with invalid attribute number")
        except ValueError as e:
            self.log_success(f"Correctly caught error for invalid attribute number: {e}")
        except Exception as e:
            self.log_info(f"Unexpected exception: {e}")
    
    async def run_all_tests(self):
        """Run all extended attribute tests"""
        self.log_info("Starting Extended Attribute Controller Tests...")
        
        await self.test_set_user_attribute_basic()
        await self.test_get_attribute_display_name_basic()
        await self.test_set_user_attribute_empty_list()
        await self.test_set_user_attribute_invalid_number()
        await self.test_set_user_attribute_non_string_value()
        await self.test_get_display_name_invalid_number()
        
        self.log_info("Extended Attribute Controller Tests completed!")
