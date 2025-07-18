"""
Element Controller Tests
=======================

Tests for ElementController - creation, deletion, modification and querying.
"""

import sys
import os
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from helpers.base_test import BaseCadworkTest
from helpers.test_data import TEST_BEAM_DATA, TEST_PANEL_DATA, BEAM_VARIATIONS
from controllers.element_controller import ElementController


class TestElementController(BaseCadworkTest):
    """Test element creation, modification and querying"""
    
    def __init__(self, use_mock: bool = False):
        super().__init__(use_mock=use_mock)
        self.element_ctrl = ElementController()
    
    async def test_create_beam_basic(self):
        """Test basic beam creation"""
        result = await self.element_ctrl.create_beam(**TEST_BEAM_DATA)
        element_id = self.assert_element_id(result, "create_beam")
        
        return {
            "element_id": element_id,
            "beam_data": TEST_BEAM_DATA
        }
    
    async def test_create_panel_basic(self):
        """Test basic panel creation"""
        result = await self.element_ctrl.create_panel(**TEST_PANEL_DATA)
        element_id = self.assert_element_id(result, "create_panel")
        
        return {
            "element_id": element_id,
            "panel_data": TEST_PANEL_DATA
        }
    
    async def test_get_all_element_ids(self):
        """Test getting all element IDs"""
        result = await self.element_ctrl.get_all_element_ids()
        element_ids = self.assert_element_list(result, "get_all_element_ids")
        
        return {
            "total_elements": len(element_ids),
            "element_ids_sample": element_ids[:3]  # Show first 3
        }
    
    async def test_create_multiple_beams(self):
        """Test creating multiple beam variations"""
        created_elements = []
        
        for i, beam_data in enumerate(BEAM_VARIATIONS[:3]):  # Test first 3 variations
            result = await self.element_ctrl.create_beam(**beam_data)
            element_id = self.assert_element_id(result, f"create_beam_{i}")
            created_elements.append(element_id)
        
        return {
            "created_count": len(created_elements),
            "element_ids": created_elements
        }
    
    async def test_delete_elements(self):
        """Test element deletion"""
        # First create a test element
        result = await self.element_ctrl.create_beam(**TEST_BEAM_DATA)
        element_id = self.assert_element_id(result, "create_beam_for_deletion")
        
        # Don't track this element since we're testing deletion
        if element_id in self.created_elements:
            self.created_elements.remove(element_id)
        
        # Now delete it
        delete_result = await self.element_ctrl.delete_elements([element_id])
        self.assert_success(delete_result, "delete_elements")
        
        return {
            "deleted_element_id": element_id,
            "delete_result": delete_result
        }
    
    async def test_copy_elements(self):
        """Test element copying"""
        # Create source element
        result = await self.element_ctrl.create_beam(**TEST_BEAM_DATA)
        source_id = self.assert_element_id(result, "create_beam_for_copy")
        
        # Copy element with offset
        copy_vector = [2000, 0, 0]  # Move 2 meters in X direction
        copy_result = await self.element_ctrl.copy_elements([source_id], copy_vector)
        self.assert_success(copy_result, "copy_elements")
        
        # Track copied element if ID is returned
        if "element_ids" in copy_result:
            for copied_id in copy_result["element_ids"]:
                self.track_element(copied_id)
        
        return {
            "source_id": source_id,
            "copy_vector": copy_vector,
            "copy_result": copy_result
        }
    
    async def test_create_beam_with_orientation(self):
        """Test beam creation with orientation point"""
        beam_data = TEST_BEAM_DATA.copy()
        beam_data['p3'] = [0, 0, 100]  # Add orientation point
        
        result = await self.element_ctrl.create_beam(**beam_data)
        element_id = self.assert_element_id(result, "create_beam_with_p3")
        
        return {
            "element_id": element_id,
            "orientation_point": beam_data['p3']
        }
    
    async def test_create_circular_beam(self):
        """Test circular beam creation"""
        result = await self.element_ctrl.create_circular_beam_points(
            diameter=300,
            p1=[0, 0, 0],
            p2=[1500, 0, 0]
        )
        element_id = self.assert_element_id(result, "create_circular_beam")
        
        return {
            "element_id": element_id,
            "diameter": 300
        }
    
    async def test_create_square_beam(self):
        """Test square beam creation"""
        result = await self.element_ctrl.create_square_beam_points(
            width=250,
            p1=[0, 0, 0], 
            p2=[1200, 0, 0]
        )
        element_id = self.assert_element_id(result, "create_square_beam")
        
        return {
            "element_id": element_id,
            "width": 250
        }
