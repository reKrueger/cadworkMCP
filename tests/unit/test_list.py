"""
List Controller Tests
====================

Tests for CListController - element list generation and reports.
"""

import sys
import os
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from helpers.base_test import BaseCadworkTest
from helpers.test_data import TEST_BEAM_DATA, TEST_PANEL_DATA
from controllers.element_controller import ElementController
from controllers.list_controller import CListController


class TestListController(BaseCadworkTest):
    """Test list generation and report operations"""
    
    def __init__(self):
        super().__init__()
        self.element_ctrl = ElementController()
        self.list_ctrl = CListController()
    
    async def test_create_element_list_basic(self):
        """Test basic element list creation"""
        # Create test elements
        beam_result = await self.element_ctrl.create_beam(**TEST_BEAM_DATA)
        beam_id = self.assert_element_id(beam_result, "create_beam_for_list")
        
        panel_data = {
            "p1": [0.0, 0.0, 0.0],
            "p2": [1000.0, 0.0, 0.0],
            "width": 500.0,
            "thickness": 20.0
        }
        panel_result = await self.element_ctrl.create_panel(**panel_data)
        panel_id = self.assert_element_id(panel_result, "create_panel_for_list")
        
        # Test basic list creation
        list_result = await self.list_ctrl.create_element_list(
            element_ids=[beam_id, panel_id]
        )
        self.assert_success(list_result, "create_element_list_basic")
        
        return {
            "element_ids": [beam_id, panel_id],
            "list_result": list_result
        }
    
    async def test_create_element_list_parameters(self):
        """Test element list with various parameters"""
        # Test parameter validation
        invalid_group_result = await self.list_ctrl.create_element_list(
            group_by="invalid_option"
        )
        self.assert_error(invalid_group_result, "create_element_list_invalid_group")
        
        invalid_sort_result = await self.list_ctrl.create_element_list(
            sort_by="invalid_option"
        )
        self.assert_error(invalid_sort_result, "create_element_list_invalid_sort")
        
        # Test valid parameters
        valid_result = await self.list_ctrl.create_element_list(
            group_by="type",
            sort_by="name",
            include_properties=True,
            include_materials=True,
            include_dimensions=True
        )
        self.assert_success(valid_result, "create_element_list_valid_params")
        
        return {
            "parameter_tests": "completed"
        }
    
    async def test_generate_material_list_basic(self):
        """Test basic material list generation"""
        # Create test elements with different materials
        beam_result = await self.element_ctrl.create_beam(**TEST_BEAM_DATA)
        beam_id = self.assert_element_id(beam_result, "create_beam_for_material_list")
        
        panel_data = {
            "p1": [0.0, 0.0, 0.0],
            "p2": [1000.0, 0.0, 0.0],
            "width": 500.0,
            "thickness": 20.0
        }
        panel_result = await self.element_ctrl.create_panel(**panel_data)
        panel_id = self.assert_element_id(panel_result, "create_panel_for_material_list")
        
        # Test basic material list generation
        material_result = await self.list_ctrl.generate_material_list(
            element_ids=[beam_id, panel_id]
        )
        self.assert_success(material_result, "generate_material_list_basic")
        
        return {
            "element_ids": [beam_id, panel_id],
            "material_result": material_result
        }
    
    async def test_generate_material_list_advanced(self):
        """Test advanced material list parameters"""
        # Test with waste calculation
        waste_result = await self.list_ctrl.generate_material_list(
            include_waste=True,
            waste_factor=0.15,
            group_by_material=True,
            optimization_mode="volume"
        )
        self.assert_success(waste_result, "generate_material_list_with_waste")
        
        # Test parameter validation
        invalid_waste_result = await self.list_ctrl.generate_material_list(
            waste_factor=1.5  # Invalid: > 1.0
        )
        self.assert_error(invalid_waste_result, "generate_material_list_invalid_waste")
        
        invalid_optimization_result = await self.list_ctrl.generate_material_list(
            optimization_mode="invalid_mode"
        )
        self.assert_error(invalid_optimization_result, "generate_material_list_invalid_optimization")
        
        # Test with cost calculation
        cost_result = await self.list_ctrl.generate_material_list(
            include_costs=True,
            cost_database="premium"
        )
        self.assert_success(cost_result, "generate_material_list_with_costs")
        
        return {
            "advanced_tests": "completed",
            "waste_result": waste_result
        }
