"""
Advanced Attribute Controller Tests
===================================

Tests for advanced AttributeController functionality - clearing and copying attributes.
"""

import sys
import os
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from helpers.base_test import BaseCadworkTest
from controllers.attribute_controller import AttributeController


class TestAdvancedAttributeController(BaseCadworkTest):
    """Test advanced attribute management operations"""
    
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
    
    async def test_clear_user_attribute_basic(self):
        """Test clearing user-defined attribute"""
        try:
            # Clear user attribute with mock element IDs
            element_ids = [1, 2, 3]
            attribute_number = 5
            
            result = await self.attribute_ctrl.clear_user_attribute(element_ids, attribute_number)
            
            if result and "status" in result:
                self.log_success(f"Clear user attribute {attribute_number} completed with status: {result['status']}")
            else:
                self.log_info(f"Clear user attribute result: {result}")
                
        except Exception as e:
            self.log_error(f"Clear user attribute failed: {e}")
    
    async def test_copy_attributes_basic(self):
        """Test copying attributes between elements"""
        try:
            # Copy attributes from source to targets with mock element IDs
            source_element_id = 1
            target_element_ids = [2, 3, 4]
            
            result = await self.attribute_ctrl.copy_attributes(
                source_element_id, target_element_ids, 
                copy_user_attributes=True, copy_standard_attributes=True
            )
            
            if result and "status" in result:
                self.log_success(f"Copy attributes from {source_element_id} to {len(target_element_ids)} elements completed with status: {result['status']}")
            else:
                self.log_info(f"Copy attributes result: {result}")
                
        except Exception as e:
            self.log_error(f"Copy attributes failed: {e}")
    
    async def test_copy_attributes_user_only(self):
        """Test copying only user attributes"""
        try:
            result = await self.attribute_ctrl.copy_attributes(
                1, [2, 3], copy_user_attributes=True, copy_standard_attributes=False
            )
            
            if result and "status" in result:
                self.log_success(f"Copy user attributes only completed with status: {result['status']}")
            else:
                self.log_info(f"Copy user attributes only result: {result}")
                
        except Exception as e:
            self.log_error(f"Copy user attributes only failed: {e}")
    
    async def test_copy_attributes_standard_only(self):
        """Test copying only standard attributes"""
        try:
            result = await self.attribute_ctrl.copy_attributes(
                1, [2, 3], copy_user_attributes=False, copy_standard_attributes=True
            )
            
            if result and "status" in result:
                self.log_success(f"Copy standard attributes only completed with status: {result['status']}")
            else:
                self.log_info(f"Copy standard attributes only result: {result}")
                
        except Exception as e:
            self.log_error(f"Copy standard attributes only failed: {e}")
    
    async def test_clear_attribute_empty_list(self):
        """Test error handling for empty element list"""
        try:
            await self.attribute_ctrl.clear_user_attribute([], 1)
            self.log_error("Should have failed with empty element list")
        except ValueError as e:
            self.log_success(f"Correctly caught error for empty list: {e}")
        except Exception as e:
            self.log_info(f"Unexpected exception: {e}")
    
    async def test_clear_attribute_invalid_number(self):
        """Test error handling for invalid attribute number"""
        try:
            await self.attribute_ctrl.clear_user_attribute([1], 0)
            self.log_error("Should have failed with invalid attribute number")
        except ValueError as e:
            self.log_success(f"Correctly caught error for invalid attribute number: {e}")
        except Exception as e:
            self.log_info(f"Unexpected exception: {e}")
    
    async def test_copy_attributes_empty_targets(self):
        """Test error handling for empty target list"""
        try:
            await self.attribute_ctrl.copy_attributes(1, [])
            self.log_error("Should have failed with empty target list")
        except ValueError as e:
            self.log_success(f"Correctly caught error for empty target list: {e}")
        except Exception as e:
            self.log_info(f"Unexpected exception: {e}")
    
    async def test_copy_attributes_no_flags(self):
        """Test error handling when no attribute types are selected"""
        try:
            await self.attribute_ctrl.copy_attributes(
                1, [2], copy_user_attributes=False, copy_standard_attributes=False
            )
            self.log_error("Should have failed with no attribute types selected")
        except ValueError as e:
            self.log_success(f"Correctly caught error for no flags: {e}")
        except Exception as e:
            self.log_info(f"Unexpected exception: {e}")
    
    async def test_copy_attributes_invalid_source(self):
        """Test error handling for invalid source element ID"""
        try:
            await self.attribute_ctrl.copy_attributes(-1, [2, 3])
            self.log_error("Should have failed with invalid source element ID")
        except ValueError as e:
            self.log_success(f"Correctly caught error for invalid source ID: {e}")
        except Exception as e:
            self.log_info(f"Unexpected exception: {e}")
    
    async def run_all_tests(self):
        """Run all advanced attribute tests"""
        self.log_info("Starting Advanced Attribute Controller Tests...")
        
        await self.test_clear_user_attribute_basic()
        await self.test_copy_attributes_basic()
        await self.test_copy_attributes_user_only()
        await self.test_copy_attributes_standard_only()
        await self.test_clear_attribute_empty_list()
        await self.test_clear_attribute_invalid_number()
        await self.test_copy_attributes_empty_targets()
        await self.test_copy_attributes_no_flags()
        await self.test_copy_attributes_invalid_source()
        
        self.log_info("Advanced Attribute Controller Tests completed!")
