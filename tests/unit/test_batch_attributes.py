"""
Batch Attribute Controller Tests
================================

Tests for batch AttributeController functionality - batch operations and validation.
"""

import sys
import os
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from helpers.base_test import BaseCadworkTest
from controllers.attribute_controller import AttributeController


class TestBatchAttributeController(BaseCadworkTest):
    """Test batch attribute management operations"""
    
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
    
    async def test_batch_set_user_attributes_basic(self):
        """Test batch setting of multiple user attributes"""
        try:
            # Set multiple attributes in one operation
            element_ids = [1, 2, 3]
            attribute_mappings = {
                101: "Project ABC",
                102: "Phase 1", 
                103: "Team Alpha",
                104: "High Priority"
            }
            
            result = await self.attribute_ctrl.batch_set_user_attributes(element_ids, attribute_mappings)
            
            if result and "status" in result:
                self.log_success(f"Batch set {len(attribute_mappings)} attributes for {len(element_ids)} elements with status: {result['status']}")
            else:
                self.log_info(f"Batch set attributes result: {result}")
                
        except Exception as e:
            self.log_error(f"Batch set attributes failed: {e}")
    
    async def test_validate_attribute_consistency_completeness(self):
        """Test attribute completeness validation"""
        try:
            # Check if all elements have required attributes
            element_ids = [1, 2, 3, 4, 5]
            attribute_numbers = [101, 102, 103]
            
            result = await self.attribute_ctrl.validate_attribute_consistency(
                element_ids, attribute_numbers, 
                check_completeness=True, check_uniqueness=False
            )
            
            if result and "status" in result:
                self.log_success(f"Attribute completeness validation completed with status: {result['status']}")
                if "missing_attributes" in result:
                    self.log_info(f"Missing attributes found: {result['missing_attributes']}")
            else:
                self.log_info(f"Completeness validation result: {result}")
                
        except Exception as e:
            self.log_error(f"Completeness validation failed: {e}")
    
    async def test_validate_attribute_consistency_uniqueness(self):
        """Test attribute uniqueness validation"""
        try:
            # Check for duplicate attribute values
            element_ids = [1, 2, 3]
            attribute_numbers = [201, 202]
            
            result = await self.attribute_ctrl.validate_attribute_consistency(
                element_ids, attribute_numbers,
                check_completeness=False, check_uniqueness=True
            )
            
            if result and "status" in result:
                self.log_success(f"Attribute uniqueness validation completed with status: {result['status']}")
                if "duplicate_values" in result:
                    self.log_info(f"Duplicate values found: {result['duplicate_values']}")
            else:
                self.log_info(f"Uniqueness validation result: {result}")
                
        except Exception as e:
            self.log_error(f"Uniqueness validation failed: {e}")
    
    async def test_validate_attribute_consistency_both(self):
        """Test both completeness and uniqueness validation"""
        try:
            result = await self.attribute_ctrl.validate_attribute_consistency(
                [1, 2, 3], [101, 102],
                check_completeness=True, check_uniqueness=True
            )
            
            if result and "status" in result:
                self.log_success(f"Combined validation completed with status: {result['status']}")
            else:
                self.log_info(f"Combined validation result: {result}")
                
        except Exception as e:
            self.log_error(f"Combined validation failed: {e}")
    
    async def test_batch_set_empty_mappings(self):
        """Test error handling for empty attribute mappings"""
        try:
            await self.attribute_ctrl.batch_set_user_attributes([1, 2], {})
            self.log_error("Should have failed with empty mappings")
        except ValueError as e:
            self.log_success(f"Correctly caught error for empty mappings: {e}")
        except Exception as e:
            self.log_info(f"Unexpected exception: {e}")
    
    async def test_batch_set_invalid_attribute_number(self):
        """Test error handling for invalid attribute number in mappings"""
        try:
            await self.attribute_ctrl.batch_set_user_attributes([1], {0: "test"})
            self.log_error("Should have failed with invalid attribute number")
        except ValueError as e:
            self.log_success(f"Correctly caught error for invalid attribute number: {e}")
        except Exception as e:
            self.log_info(f"Unexpected exception: {e}")
    
    async def test_batch_set_non_string_value(self):
        """Test error handling for non-string attribute value"""
        try:
            await self.attribute_ctrl.batch_set_user_attributes([1], {101: 123})
            self.log_error("Should have failed with non-string value")
        except ValueError as e:
            self.log_success(f"Correctly caught error for non-string value: {e}")
        except Exception as e:
            self.log_info(f"Unexpected exception: {e}")
    
    async def test_validate_consistency_empty_elements(self):
        """Test error handling for empty element list"""
        try:
            await self.attribute_ctrl.validate_attribute_consistency([], [101])
            self.log_error("Should have failed with empty element list")
        except ValueError as e:
            self.log_success(f"Correctly caught error for empty elements: {e}")
        except Exception as e:
            self.log_info(f"Unexpected exception: {e}")
    
    async def test_validate_consistency_no_checks(self):
        """Test error handling when no validation checks are enabled"""
        try:
            await self.attribute_ctrl.validate_attribute_consistency(
                [1, 2], [101], check_completeness=False, check_uniqueness=False
            )
            self.log_error("Should have failed with no checks enabled")
        except ValueError as e:
            self.log_success(f"Correctly caught error for no checks: {e}")
        except Exception as e:
            self.log_info(f"Unexpected exception: {e}")
    
    async def test_validate_consistency_invalid_attribute_number(self):
        """Test error handling for invalid attribute number"""
        try:
            await self.attribute_ctrl.validate_attribute_consistency([1], [-1])
            self.log_error("Should have failed with invalid attribute number")
        except ValueError as e:
            self.log_success(f"Correctly caught error for invalid attribute number: {e}")
        except Exception as e:
            self.log_info(f"Unexpected exception: {e}")
    
    async def run_all_tests(self):
        """Run all batch attribute tests"""
        self.log_info("Starting Batch Attribute Controller Tests...")
        
        await self.test_batch_set_user_attributes_basic()
        await self.test_validate_attribute_consistency_completeness()
        await self.test_validate_attribute_consistency_uniqueness()
        await self.test_validate_attribute_consistency_both()
        await self.test_batch_set_empty_mappings()
        await self.test_batch_set_invalid_attribute_number()
        await self.test_batch_set_non_string_value()
        await self.test_validate_consistency_empty_elements()
        await self.test_validate_consistency_no_checks()
        await self.test_validate_consistency_invalid_attribute_number()
        
        self.log_info("Batch Attribute Controller Tests completed!")
