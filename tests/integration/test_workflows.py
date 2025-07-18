"""
Integration Workflow Tests
=========================

End-to-end tests that combine multiple operations in realistic workflows.
"""

import sys
import os
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from helpers.base_test import BaseCadworkTest
from helpers.test_data import TEST_BEAM_DATA, TEST_PANEL_DATA
from controllers.element_controller import ElementController
from controllers.geometry_controller import GeometryController  
from controllers.visualization_controller import CVisualizationController


class TestWorkflows(BaseCadworkTest):
    """Test complete workflows that combine multiple operations"""
    
    def __init__(self, use_mock: bool = False):
        super().__init__(use_mock=use_mock)
        self.element_ctrl = ElementController()
        self.geometry_ctrl = GeometryController()
        self.viz_ctrl = CVisualizationController()
    
    async def test_create_and_modify_beam_workflow(self):
        """Test complete beam creation and modification workflow"""
        workflow_results = {}
        
        # Step 1: Create beam
        create_result = await self.element_ctrl.create_beam(**TEST_BEAM_DATA)
        element_id = self.assert_element_id(create_result, "create_beam")
        workflow_results["created_element_id"] = element_id
        
        # Step 2: Get element info
        info_result = await self.geometry_ctrl.get_element_info(element_id)
        self.assert_success(info_result, "get_element_info")
        workflow_results["element_info"] = info_result
        
        # Step 3: Set color
        color_result = await self.viz_ctrl.set_color([element_id], 2)  # Green
        self.assert_success(color_result, "set_color")
        workflow_results["color_set"] = True
        
        # Step 4: Move element
        move_vector = [500, 0, 0]
        move_result = await self.element_ctrl.move_element([element_id], move_vector)
        self.assert_success(move_result, "move_element")
        workflow_results["moved_by"] = move_vector
        
        # Step 5: Copy element
        copy_vector = [0, 1000, 0]
        copy_result = await self.element_ctrl.copy_elements([element_id], copy_vector)
        self.assert_success(copy_result, "copy_elements")
        
        # Track copied elements if returned
        if "element_ids" in copy_result:
            for copied_id in copy_result["element_ids"]:
                self.track_element(copied_id)
            workflow_results["copied_element_ids"] = copy_result["element_ids"]
        
        return workflow_results
    
    async def test_multi_element_creation_workflow(self):
        """Test creating multiple different element types"""
        created_elements = []
        
        # Create beam
        beam_result = await self.element_ctrl.create_beam(**TEST_BEAM_DATA)
        beam_id = self.assert_element_id(beam_result, "create_beam")
        created_elements.append(("beam", beam_id))
        
        # Create panel
        panel_result = await self.element_ctrl.create_panel(**TEST_PANEL_DATA)
        panel_id = self.assert_element_id(panel_result, "create_panel")
        created_elements.append(("panel", panel_id))
        
        # Create circular beam
        circular_result = await self.element_ctrl.create_circular_beam_points(
            diameter=200, p1=[2000, 0, 0], p2=[3000, 0, 0]
        )
        circular_id = self.assert_element_id(circular_result, "create_circular_beam")
        created_elements.append(("circular_beam", circular_id))
        
        return {
            "created_elements": created_elements,
            "total_count": len(created_elements)
        }
    
    async def test_visualization_workflow(self):
        """Test visualization operations workflow"""
        # Create test elements
        beam_result = await self.element_ctrl.create_beam(**TEST_BEAM_DATA)
        element_id = self.assert_element_id(beam_result, "create_beam_for_viz")
        
        workflow_steps = []
        
        # Step 1: Set initial color (Red)
        color_result = await self.viz_ctrl.set_color([element_id], 1)
        self.assert_success(color_result, "set_color_red")
        workflow_steps.append("color_red")
        
        # Step 2: Set transparency
        transparency_result = await self.viz_ctrl.set_transparency([element_id], 50)
        self.assert_success(transparency_result, "set_transparency")
        workflow_steps.append("transparency_50")
        
        # Step 3: Hide element
        hide_result = await self.viz_ctrl.set_visibility([element_id], False)
        self.assert_success(hide_result, "hide_element")
        workflow_steps.append("hidden")
        
        # Step 4: Show element again
        show_result = await self.viz_ctrl.set_visibility([element_id], True)
        self.assert_success(show_result, "show_element")
        workflow_steps.append("visible")
        
        # Step 5: Change color (Blue)
        blue_result = await self.viz_ctrl.set_color([element_id], 3)
        self.assert_success(blue_result, "set_color_blue")
        workflow_steps.append("color_blue")
        
        return {
            "element_id": element_id,
            "workflow_steps": workflow_steps,
            "total_steps": len(workflow_steps)
        }
    
    async def test_geometry_analysis_workflow(self):
        """Test geometry analysis workflow"""
        # Create test element
        beam_result = await self.element_ctrl.create_beam(**TEST_BEAM_DATA)
        element_id = self.assert_element_id(beam_result, "create_beam_for_geometry")
        
        geometry_data = {}
        
        # Get all dimensions
        width_result = await self.geometry_ctrl.get_element_width(element_id)
        self.assert_success(width_result, "get_width")
        geometry_data["width"] = width_result.get("width")
        
        height_result = await self.geometry_ctrl.get_element_height(element_id)
        self.assert_success(height_result, "get_height")
        geometry_data["height"] = height_result.get("height")
        
        length_result = await self.geometry_ctrl.get_element_length(element_id)
        self.assert_success(length_result, "get_length")
        geometry_data["length"] = length_result.get("length")
        
        # Get volume and weight
        volume_result = await self.geometry_ctrl.get_element_volume(element_id)
        self.assert_success(volume_result, "get_volume")
        geometry_data["volume"] = volume_result.get("volume")
        
        weight_result = await self.geometry_ctrl.get_element_weight(element_id)
        self.assert_success(weight_result, "get_weight")
        geometry_data["weight"] = weight_result.get("weight")
        
        # Get points
        p1_result = await self.geometry_ctrl.get_element_p1(element_id)
        self.assert_success(p1_result, "get_p1")
        geometry_data["p1"] = p1_result.get("point")
        
        p2_result = await self.geometry_ctrl.get_element_p2(element_id)
        self.assert_success(p2_result, "get_p2")
        geometry_data["p2"] = p2_result.get("point")
        
        # Get center of gravity
        cog_result = await self.geometry_ctrl.get_center_of_gravity(element_id)
        self.assert_success(cog_result, "get_center_of_gravity")
        geometry_data["center_of_gravity"] = cog_result.get("center_of_gravity")
        
        return {
            "element_id": element_id,
            "geometry_data": geometry_data,
            "analyzed_properties": len(geometry_data)
        }
    
    async def test_bulk_operations_workflow(self):
        """Test bulk operations on multiple elements"""
        # Create multiple elements
        element_ids = []
        
        for i in range(3):
            beam_data = TEST_BEAM_DATA.copy()
            beam_data["p1"][0] = i * 1500  # Offset each beam
            beam_data["p2"][0] = (i * 1500) + 1000
            
            result = await self.element_ctrl.create_beam(**beam_data)
            element_id = self.assert_element_id(result, f"create_beam_{i}")
            element_ids.append(element_id)
        
        # Bulk color operation
        color_result = await self.viz_ctrl.set_color(element_ids, 4)  # Yellow
        self.assert_success(color_result, "bulk_set_color")
        
        # Bulk transparency operation
        transparency_result = await self.viz_ctrl.set_transparency(element_ids, 25)
        self.assert_success(transparency_result, "bulk_set_transparency")
        
        # Bulk move operation
        move_vector = [0, 500, 100]
        move_result = await self.element_ctrl.move_element(element_ids, move_vector)
        self.assert_success(move_result, "bulk_move")
        
        return {
            "element_ids": element_ids,
            "bulk_operations": ["color", "transparency", "move"],
            "element_count": len(element_ids)
        }
