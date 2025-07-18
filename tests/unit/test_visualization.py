"""
Visualization Controller Tests
=============================

Tests for VisualizationController - colors, visibility, transparency.
"""

import sys
import os
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from helpers.base_test import BaseCadworkTest
from helpers.test_data import TEST_BEAM_DATA
from controllers.element_controller import ElementController
from controllers.visualization_controller import CVisualizationController


class TestVisualizationController(BaseCadworkTest):
    """Test visualization and display operations"""
    
    def __init__(self):
        super().__init__()
        self.element_ctrl = ElementController()
        self.viz_ctrl = CVisualizationController()
    
    async def test_show_all_elements(self):
        """Test showing all elements"""
        result = await self.viz_ctrl.show_all_elements()
        self.assert_success(result, "show_all_elements")
        
        return {
            "visible_count": result.get("visible_count", 0)
        }
    
    async def test_hide_all_elements(self):
        """Test hiding all elements"""
        result = await self.viz_ctrl.hide_all_elements()
        self.assert_success(result, "hide_all_elements")
        
        return {
            "hidden_count": result.get("hidden_count", 0)
        }
    
    async def test_get_visible_element_count(self):
        """Test getting visible element count"""
        result = await self.viz_ctrl.get_visible_element_count()
        self.assert_success(result, "get_visible_element_count")
        
        return {
            "visible_count": result.get("visible_count", 0),
            "total_count": result.get("total_count", 0)
        }
    
    async def test_set_element_color(self):
        """Test setting element color"""
        # Create test element
        create_result = await self.element_ctrl.create_beam(**TEST_BEAM_DATA)
        element_id = self.assert_element_id(create_result, "create_beam_for_color")
        
        # Set color (red = color_id 1)
        color_result = await self.viz_ctrl.set_color([element_id], 1)
        self.assert_success(color_result, "set_color")
        
        return {
            "element_id": element_id,
            "color_id": 1,
            "color_result": color_result
        }
    
    async def test_set_element_visibility(self):
        """Test setting element visibility"""
        # Create test element
        create_result = await self.element_ctrl.create_beam(**TEST_BEAM_DATA)
        element_id = self.assert_element_id(create_result, "create_beam_for_visibility")
        
        # Hide element
        hide_result = await self.viz_ctrl.set_visibility([element_id], False)
        self.assert_success(hide_result, "set_visibility_false")
        
        # Show element again
        show_result = await self.viz_ctrl.set_visibility([element_id], True)
        self.assert_success(show_result, "set_visibility_true")
        
        return {
            "element_id": element_id,
            "hide_result": hide_result,
            "show_result": show_result
        }
    
    async def test_set_element_transparency(self):
        """Test setting element transparency"""
        # Create test element
        create_result = await self.element_ctrl.create_beam(**TEST_BEAM_DATA)
        element_id = self.assert_element_id(create_result, "create_beam_for_transparency")
        
        # Set transparency to 50%
        transparency_result = await self.viz_ctrl.set_transparency([element_id], 50)
        self.assert_success(transparency_result, "set_transparency")
        
        return {
            "element_id": element_id,
            "transparency": 50,
            "transparency_result": transparency_result
        }
    
    async def test_get_element_color(self):
        """Test getting element color"""
        # Create test element
        create_result = await self.element_ctrl.create_beam(**TEST_BEAM_DATA)
        element_id = self.assert_element_id(create_result, "create_beam_for_get_color")
        
        # Set a specific color first
        await self.viz_ctrl.set_color([element_id], 2)  # Green
        
        # Get color
        color_result = await self.viz_ctrl.get_color(element_id)
        self.assert_success(color_result, "get_color")
        
        return {
            "element_id": element_id,
            "color_info": color_result
        }
    
    async def test_refresh_display(self):
        """Test refreshing display"""
        result = await self.viz_ctrl.refresh_display()
        self.assert_success(result, "refresh_display")
        
        return result
