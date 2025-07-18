"""
Business Intelligence Attribute Tests
=====================================

Tests for BI AttributeController functionality - search and reporting.
"""

import sys
import os
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from helpers.base_test import BaseCadworkTest
from controllers.attribute_controller import AttributeController


class TestBIAttributeController(BaseCadworkTest):
    """Test business intelligence attribute operations"""
    
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
    
    async def test_search_elements_standard_attributes(self):
        """Test searching by standard attributes"""
        try:
            # Search for elements with specific material and group
            search_criteria = {
                "material": "GL24h",
                "group": "Structural Beams"
            }
            
            result = await self.attribute_ctrl.search_elements_by_attributes(
                search_criteria, search_mode="AND"
            )
            
            if result and "status" in result:
                self.log_success(f"Standard attribute search completed with status: {result['status']}")
                if "found_elements" in result:
                    self.log_info(f"Found {len(result['found_elements'])} matching elements")
            else:
                self.log_info(f"Standard attribute search result: {result}")
                
        except Exception as e:
            self.log_error(f"Standard attribute search failed: {e}")
    
    async def test_search_elements_user_attributes(self):
        """Test searching by user attributes"""
        try:
            # Search for elements with specific user attributes
            search_criteria = {
                "user_attr_101": "PROJECT-2025",
                "user_attr_102": "PHASE-1"
            }
            
            result = await self.attribute_ctrl.search_elements_by_attributes(
                search_criteria, search_mode="AND"
            )
            
            if result and "status" in result:
                self.log_success(f"User attribute search completed with status: {result['status']}")
            else:
                self.log_info(f"User attribute search result: {result}")
                
        except Exception as e:
            self.log_error(f"User attribute search failed: {e}")
    
    async def test_search_elements_dimensions(self):
        """Test searching by dimensions"""
        try:
            # Search for elements with specific dimensions
            search_criteria = {
                "dimension_width": {"operator": ">=", "value": 100},
                "dimension_height": {"min": 200, "max": 400}
            }
            
            result = await self.attribute_ctrl.search_elements_by_attributes(
                search_criteria, search_mode="AND"
            )
            
            if result and "status" in result:
                self.log_success(f"Dimension search completed with status: {result['status']}")
            else:
                self.log_info(f"Dimension search result: {result}")
                
        except Exception as e:
            self.log_error(f"Dimension search failed: {e}")
    
    async def test_search_elements_or_mode(self):
        """Test OR search mode"""
        try:
            search_criteria = {
                "material": "GL24h",
                "group": "Alternative Group"
            }
            
            result = await self.attribute_ctrl.search_elements_by_attributes(
                search_criteria, search_mode="OR"
            )
            
            if result and "status" in result:
                self.log_success(f"OR mode search completed with status: {result['status']}")
            else:
                self.log_info(f"OR mode search result: {result}")
                
        except Exception as e:
            self.log_error(f"OR mode search failed: {e}")
    
    async def test_export_attribute_report_json(self):
        """Test JSON attribute report export"""
        try:
            element_ids = [1, 2, 3, 4, 5]
            
            result = await self.attribute_ctrl.export_attribute_report(
                element_ids, report_format="JSON",
                include_standard_attributes=True,
                include_user_attributes=True,
                include_dimensions=False
            )
            
            if result and "status" in result:
                self.log_success(f"JSON report export completed with status: {result['status']}")
                if "report_data" in result:
                    self.log_info(f"Report contains data for {len(element_ids)} elements")
            else:
                self.log_info(f"JSON report result: {result}")
                
        except Exception as e:
            self.log_error(f"JSON report export failed: {e}")
    
    async def test_export_attribute_report_csv_grouped(self):
        """Test CSV report with grouping"""
        try:
            element_ids = [1, 2, 3, 4, 5]
            
            result = await self.attribute_ctrl.export_attribute_report(
                element_ids, report_format="CSV",
                include_standard_attributes=True,
                include_user_attributes=True,
                user_attribute_numbers=[101, 102, 103],
                include_dimensions=True,
                group_by="material"
            )
            
            if result and "status" in result:
                self.log_success(f"CSV grouped report completed with status: {result['status']}")
            else:
                self.log_info(f"CSV grouped report result: {result}")
                
        except Exception as e:
            self.log_error(f"CSV grouped report failed: {e}")
    
    async def test_search_empty_criteria(self):
        """Test error handling for empty search criteria"""
        try:
            await self.attribute_ctrl.search_elements_by_attributes({})
            self.log_error("Should have failed with empty criteria")
        except ValueError as e:
            self.log_success(f"Correctly caught error for empty criteria: {e}")
        except Exception as e:
            self.log_info(f"Unexpected exception: {e}")
    
    async def test_search_invalid_mode(self):
        """Test error handling for invalid search mode"""
        try:
            await self.attribute_ctrl.search_elements_by_attributes(
                {"material": "GL24h"}, search_mode="INVALID"
            )
            self.log_error("Should have failed with invalid search mode")
        except ValueError as e:
            self.log_success(f"Correctly caught error for invalid mode: {e}")
        except Exception as e:
            self.log_info(f"Unexpected exception: {e}")
    
    async def test_search_invalid_user_attribute_key(self):
        """Test error handling for invalid user attribute key"""
        try:
            await self.attribute_ctrl.search_elements_by_attributes(
                {"user_attr_invalid": "value"}
            )
            self.log_error("Should have failed with invalid user attribute key")
        except ValueError as e:
            self.log_success(f"Correctly caught error for invalid user attr key: {e}")
        except Exception as e:
            self.log_info(f"Unexpected exception: {e}")
    
    async def test_export_report_empty_elements(self):
        """Test error handling for empty element list"""
        try:
            await self.attribute_ctrl.export_attribute_report([])
            self.log_error("Should have failed with empty element list")
        except ValueError as e:
            self.log_success(f"Correctly caught error for empty elements: {e}")
        except Exception as e:
            self.log_info(f"Unexpected exception: {e}")
    
    async def test_export_report_invalid_format(self):
        """Test error handling for invalid report format"""
        try:
            await self.attribute_ctrl.export_attribute_report(
                [1, 2], report_format="INVALID"
            )
            self.log_error("Should have failed with invalid format")
        except ValueError as e:
            self.log_success(f"Correctly caught error for invalid format: {e}")
        except Exception as e:
            self.log_info(f"Unexpected exception: {e}")
    
    async def test_export_report_no_data_types(self):
        """Test error handling when no data types are included"""
        try:
            await self.attribute_ctrl.export_attribute_report(
                [1, 2], include_standard_attributes=False,
                include_user_attributes=False, include_dimensions=False
            )
            self.log_error("Should have failed with no data types")
        except ValueError as e:
            self.log_success(f"Correctly caught error for no data types: {e}")
        except Exception as e:
            self.log_info(f"Unexpected exception: {e}")
    
    async def run_all_tests(self):
        """Run all BI attribute tests"""
        self.log_info("Starting Business Intelligence Attribute Tests...")
        
        await self.test_search_elements_standard_attributes()
        await self.test_search_elements_user_attributes()
        await self.test_search_elements_dimensions()
        await self.test_search_elements_or_mode()
        await self.test_export_attribute_report_json()
        await self.test_export_attribute_report_csv_grouped()
        await self.test_search_empty_criteria()
        await self.test_search_invalid_mode()
        await self.test_search_invalid_user_attribute_key()
        await self.test_export_report_empty_elements()
        await self.test_export_report_invalid_format()
        await self.test_export_report_no_data_types()
        
        self.log_info("Business Intelligence Attribute Tests completed!")
