"""
Advanced Visualization Controller Tests
=======================================

Tests for advanced VisualizationController functionality - filters and color schemes.
"""

import sys
import os
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from helpers.base_test import BaseCadworkTest
from controllers.visualization_controller import CVisualizationController


class TestAdvancedVisualizationController(BaseCadworkTest):
    """Test advanced visualization operations"""
    
    def __init__(self, use_mock: bool = False):
        super().__init__(use_mock=use_mock)
        self.visualization_ctrl = CVisualizationController()
    
    def log_success(self, message: str):
        """Log success message"""
        print(f"SUCCESS: {message}")
    
    def log_error(self, message: str):
        """Log error message"""
        print(f"ERROR: {message}")
    
    def log_info(self, message: str):
        """Log info message"""
        print(f"INFO: {message}")
    
    async def test_create_visual_filter_basic(self):
        """Test basic visual filter creation"""
        try:
            # Create filter for GL24h materials with red color
            filter_criteria = {
                "material": "GL24h",
                "group": "Structural"
            }
            
            visual_properties = {
                "color_id": 1,  # Red
                "transparency": 0,
                "visibility": True
            }
            
            result = await self.visualization_ctrl.create_visual_filter(
                "GL24h_Structural_Filter", filter_criteria, visual_properties
            )
            
            if result and "status" in result:
                self.log_success(f"Visual filter creation completed with status: {result['status']}")
                if "affected_elements" in result:
                    self.log_info(f"Filter applied to {result['affected_elements']} elements")
            else:
                self.log_info(f"Visual filter result: {result}")
                
        except Exception as e:
            self.log_error(f"Visual filter creation failed: {e}")
    
    async def test_create_visual_filter_user_attributes(self):
        """Test visual filter with user attributes"""
        try:
            # Filter for high priority elements
            filter_criteria = {
                "user_attr_101": "PROJECT-2025",
                "user_attr_104": "HIGH-PRIORITY"
            }
            
            visual_properties = {
                "color_id": 2,  # Orange for high priority
                "transparency": 25
            }
            
            result = await self.visualization_ctrl.create_visual_filter(
                "High_Priority_Filter", filter_criteria, visual_properties
            )
            
            if result and "status" in result:
                self.log_success(f"User attribute filter completed with status: {result['status']}")
            else:
                self.log_info(f"User attribute filter result: {result}")
                
        except Exception as e:
            self.log_error(f"User attribute filter failed: {e}")
    
    async def test_create_visual_filter_dimensions(self):
        """Test visual filter with dimensions"""
        try:
            # Filter for large elements
            filter_criteria = {
                "dimension_width": {"operator": ">=", "value": 200},
                "dimension_length": {"operator": ">=", "value": 6000}
            }
            
            visual_properties = {
                "color_id": 3,  # Blue for large elements
                "visibility": True
            }
            
            result = await self.visualization_ctrl.create_visual_filter(
                "Large_Elements_Filter", filter_criteria, visual_properties
            )
            
            if result and "status" in result:
                self.log_success(f"Dimension filter completed with status: {result['status']}")
            else:
                self.log_info(f"Dimension filter result: {result}")
                
        except Exception as e:
            self.log_error(f"Dimension filter failed: {e}")
    
    async def test_apply_color_scheme_material_based(self):
        """Test material-based color scheme"""
        try:
            result = await self.visualization_ctrl.apply_color_scheme(
                "material_based", element_ids=None, scheme_basis="material"
            )
            
            if result and "status" in result:
                self.log_success(f"Material color scheme completed with status: {result['status']}")
                if "color_mapping" in result:
                    self.log_info(f"Applied colors: {result['color_mapping']}")
            else:
                self.log_info(f"Material color scheme result: {result}")
                
        except Exception as e:
            self.log_error(f"Material color scheme failed: {e}")
    
    async def test_apply_color_scheme_element_type(self):
        """Test element type-based color scheme"""
        try:
            element_ids = [1, 2, 3, 4, 5]
            
            result = await self.visualization_ctrl.apply_color_scheme(
                "element_type_based", element_ids=element_ids, scheme_basis="element_type"
            )
            
            if result and "status" in result:
                self.log_success(f"Element type color scheme completed with status: {result['status']}")
            else:
                self.log_info(f"Element type color scheme result: {result}")
                
        except Exception as e:
            self.log_error(f"Element type color scheme failed: {e}")
    
    async def test_apply_color_scheme_status_based(self):
        """Test status-based color scheme"""
        try:
            result = await self.visualization_ctrl.apply_color_scheme(
                "status_based", scheme_basis="user_attribute"
            )
            
            if result and "status" in result:
                self.log_success(f"Status color scheme completed with status: {result['status']}")
            else:
                self.log_info(f"Status color scheme result: {result}")
                
        except Exception as e:
            self.log_error(f"Status color scheme failed: {e}")
    
    async def test_visual_filter_empty_name(self):
        """Test error handling for empty filter name"""
        try:
            await self.visualization_ctrl.create_visual_filter(
                "", {"material": "GL24h"}, {"color_id": 1}
            )
            self.log_error("Should have failed with empty filter name")
        except ValueError as e:
            self.log_success(f"Correctly caught error for empty name: {e}")
        except Exception as e:
            self.log_info(f"Unexpected exception: {e}")
    
    async def test_visual_filter_empty_criteria(self):
        """Test error handling for empty filter criteria"""
        try:
            await self.visualization_ctrl.create_visual_filter(
                "Test_Filter", {}, {"color_id": 1}
            )
            self.log_error("Should have failed with empty criteria")
        except ValueError as e:
            self.log_success(f"Correctly caught error for empty criteria: {e}")
        except Exception as e:
            self.log_info(f"Unexpected exception: {e}")
    
    async def test_visual_filter_invalid_color(self):
        """Test error handling for invalid color ID"""
        try:
            await self.visualization_ctrl.create_visual_filter(
                "Test_Filter", {"material": "GL24h"}, {"color_id": 300}
            )
            self.log_error("Should have failed with invalid color ID")
        except ValueError as e:
            self.log_success(f"Correctly caught error for invalid color: {e}")
        except Exception as e:
            self.log_info(f"Unexpected exception: {e}")
    
    async def test_visual_filter_invalid_transparency(self):
        """Test error handling for invalid transparency"""
        try:
            await self.visualization_ctrl.create_visual_filter(
                "Test_Filter", {"material": "GL24h"}, {"transparency": 150}
            )
            self.log_error("Should have failed with invalid transparency")
        except ValueError as e:
            self.log_success(f"Correctly caught error for invalid transparency: {e}")
        except Exception as e:
            self.log_info(f"Unexpected exception: {e}")
    
    async def test_color_scheme_invalid_scheme(self):
        """Test error handling for invalid color scheme"""
        try:
            await self.visualization_ctrl.apply_color_scheme("invalid_scheme")
            self.log_error("Should have failed with invalid scheme")
        except ValueError as e:
            self.log_success(f"Correctly caught error for invalid scheme: {e}")
        except Exception as e:
            self.log_info(f"Unexpected exception: {e}")
    
    async def test_color_scheme_invalid_basis(self):
        """Test error handling for invalid scheme basis"""
        try:
            await self.visualization_ctrl.apply_color_scheme(
                "material_based", scheme_basis="invalid_basis"
            )
            self.log_error("Should have failed with invalid basis")
        except ValueError as e:
            self.log_success(f"Correctly caught error for invalid basis: {e}")
        except Exception as e:
            self.log_info(f"Unexpected exception: {e}")
    
    async def test_color_scheme_invalid_element_ids(self):
        """Test error handling for invalid element IDs type"""
        try:
            await self.visualization_ctrl.apply_color_scheme(
                "material_based", element_ids="not_a_list"
            )
            self.log_error("Should have failed with invalid element IDs type")
        except ValueError as e:
            self.log_success(f"Correctly caught error for invalid element IDs: {e}")
        except Exception as e:
            self.log_info(f"Unexpected exception: {e}")
    
    async def run_all_tests(self):
        """Run all advanced visualization tests"""
        self.log_info("Starting Advanced Visualization Controller Tests...")
        
        await self.test_create_visual_filter_basic()
        await self.test_create_visual_filter_user_attributes()
        await self.test_create_visual_filter_dimensions()
        await self.test_apply_color_scheme_material_based()
        await self.test_apply_color_scheme_element_type()
        await self.test_apply_color_scheme_status_based()
        await self.test_visual_filter_empty_name()
        await self.test_visual_filter_empty_criteria()
        await self.test_visual_filter_invalid_color()
        await self.test_visual_filter_invalid_transparency()
        await self.test_color_scheme_invalid_scheme()
        await self.test_color_scheme_invalid_basis()
        await self.test_color_scheme_invalid_element_ids()
        
        self.log_info("Advanced Visualization Controller Tests completed!")
