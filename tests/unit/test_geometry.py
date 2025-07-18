"""
Geometry Controller Tests
========================

Tests for GeometryController - element dimensions, transformations, and geometry operations.
"""

import sys
import os
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from helpers.base_test import BaseCadworkTest
from helpers.test_data import TEST_BEAM_DATA
from controllers.element_controller import ElementController
from controllers.geometry_controller import GeometryController


class TestGeometryController(BaseCadworkTest):
    """Test geometry operations and measurements"""
    
    def __init__(self):
        super().__init__()
        self.element_ctrl = ElementController()
        self.geometry_ctrl = GeometryController()
    
    async def test_get_element_info(self):
        """Test getting element information"""
        # Create test element
        result = await self.element_ctrl.create_beam(**TEST_BEAM_DATA)
        element_id = self.assert_element_id(result, "create_beam_for_info")
        
        # Get element info
        info_result = await self.geometry_ctrl.get_element_info(element_id)
        self.assert_success(info_result, "get_element_info")
        
        return {
            "element_id": element_id,
            "element_info": info_result
        }
    
    async def test_check_collisions(self):
        """Test collision detection between elements"""
        # Create two overlapping beams for collision test
        beam1_data = {
            "p1": [0.0, 0.0, 0.0],
            "p2": [1000.0, 0.0, 0.0],
            "width": 100.0,
            "height": 100.0
        }
        beam2_data = {
            "p1": [500.0, -50.0, 0.0],
            "p2": [1500.0, -50.0, 0.0],
            "width": 100.0,
            "height": 100.0
        }
        
        # Create test elements
        result1 = await self.element_ctrl.create_beam(**beam1_data)
        element_id1 = self.assert_element_id(result1, "create_beam_for_collision_1")
        
        result2 = await self.element_ctrl.create_beam(**beam2_data)
        element_id2 = self.assert_element_id(result2, "create_beam_for_collision_2")
        
        # Test collision detection
        collision_result = await self.geometry_ctrl.check_collisions([element_id1, element_id2], 0.1)
        self.assert_success(collision_result, "check_collisions")
        
        # Test with invalid input
        invalid_result = await self.geometry_ctrl.check_collisions([element_id1], 0.1)
        self.assert_error(invalid_result, "check_collisions_insufficient_elements")
        
        # Test with negative tolerance
        negative_result = await self.geometry_ctrl.check_collisions([element_id1, element_id2], -1.0)
        self.assert_error(negative_result, "check_collisions_negative_tolerance")
        
        return {
            "element_ids": [element_id1, element_id2],
            "collision_result": collision_result
        }
    
    async def test_validate_joints(self):
        """Test joint validation between elements"""
        # Create two connecting beams
        beam1_data = {
            "p1": [0.0, 0.0, 0.0],
            "p2": [1000.0, 0.0, 0.0],
            "width": 120.0,
            "height": 200.0
        }
        beam2_data = {
            "p1": [1000.0, 0.0, 0.0],
            "p2": [1000.0, 1000.0, 0.0],
            "width": 120.0,
            "height": 200.0
        }
        
        # Create test elements
        result1 = await self.element_ctrl.create_beam(**beam1_data)
        element_id1 = self.assert_element_id(result1, "create_beam_for_joint_1")
        
        result2 = await self.element_ctrl.create_beam(**beam2_data)
        element_id2 = self.assert_element_id(result2, "create_beam_for_joint_2")
        
        # Test basic joint validation
        basic_result = await self.geometry_ctrl.validate_joints(
            element_ids=[element_id1, element_id2]
        )
        self.assert_success(basic_result, "validate_joints_basic")
        
        # Test with specific joint type and load conditions
        load_conditions = {
            "normal_force": 5000.0,  # 5 kN
            "shear_force": 2000.0,   # 2 kN
            "load_duration": "permanent"
        }
        
        advanced_result = await self.geometry_ctrl.validate_joints(
            element_ids=[element_id1, element_id2],
            joint_type="mortise_tenon",
            load_conditions=load_conditions,
            safety_factor=2.5,
            wood_grade="C30"
        )
        self.assert_success(advanced_result, "validate_joints_advanced")
        
        # Test invalid parameters
        invalid_joint_type_result = await self.geometry_ctrl.validate_joints(
            element_ids=[element_id1, element_id2],
            joint_type="invalid_joint"
        )
        self.assert_error(invalid_joint_type_result, "validate_joints_invalid_type")
        
        invalid_safety_result = await self.geometry_ctrl.validate_joints(
            element_ids=[element_id1, element_id2],
            safety_factor=-1.0
        )
        self.assert_error(invalid_safety_result, "validate_joints_invalid_safety")
        
        insufficient_elements_result = await self.geometry_ctrl.validate_joints(
            element_ids=[element_id1]
        )
        self.assert_error(insufficient_elements_result, "validate_joints_insufficient_elements")
        
        return {
            "element_ids": [element_id1, element_id2],
            "joint_results": [basic_result, advanced_result]
        }
    
    async def test_get_element_dimensions(self):
        """Test getting element dimensions"""
        # Create test element
        result = await self.element_ctrl.create_beam(**TEST_BEAM_DATA)
        element_id = self.assert_element_id(result, "create_beam_for_dimensions")
        
        # Get dimensions
        width_result = await self.geometry_ctrl.get_element_width(element_id)
        height_result = await self.geometry_ctrl.get_element_height(element_id)
        length_result = await self.geometry_ctrl.get_element_length(element_id)
        
        self.assert_success(width_result, "get_element_width")
        self.assert_success(height_result, "get_element_height") 
        self.assert_success(length_result, "get_element_length")
        
        return {
            "element_id": element_id,
            "width": width_result.get("width"),
            "height": height_result.get("height"),
            "length": length_result.get("length")
        }
    
    async def test_get_element_volume_weight(self):
        """Test getting element volume and weight"""
        # Create test element
        result = await self.element_ctrl.create_beam(**TEST_BEAM_DATA)
        element_id = self.assert_element_id(result, "create_beam_for_volume")
        
        # Get volume and weight
        volume_result = await self.geometry_ctrl.get_element_volume(element_id)
        weight_result = await self.geometry_ctrl.get_element_weight(element_id)
        
        self.assert_success(volume_result, "get_element_volume")
        self.assert_success(weight_result, "get_element_weight")
        
        return {
            "element_id": element_id,
            "volume": volume_result.get("volume"),
            "weight": weight_result.get("weight")
        }
    
    async def test_get_element_points(self):
        """Test getting element points (P1, P2, P3)"""
        # Create test element
        result = await self.element_ctrl.create_beam(**TEST_BEAM_DATA)
        element_id = self.assert_element_id(result, "create_beam_for_points")
        
        # Get points
        p1_result = await self.geometry_ctrl.get_element_p1(element_id)
        p2_result = await self.geometry_ctrl.get_element_p2(element_id)
        
        self.assert_success(p1_result, "get_element_p1")
        self.assert_success(p2_result, "get_element_p2")
        
        return {
            "element_id": element_id,
            "p1": p1_result.get("point"),
            "p2": p2_result.get("point")
        }
    
    async def test_get_bounding_box(self):
        """Test getting element bounding box"""
        # Create test element
        result = await self.element_ctrl.create_beam(**TEST_BEAM_DATA)
        element_id = self.assert_element_id(result, "create_beam_for_bbox")
        
        # Get bounding box
        bbox_result = await self.geometry_ctrl.get_bounding_box(element_id)
        self.assert_success(bbox_result, "get_bounding_box")
        
        return {
            "element_id": element_id,
            "bounding_box": bbox_result.get("bounding_box")
        }
    
    async def test_get_center_of_gravity(self):
        """Test getting element center of gravity"""
        # Create test element
        result = await self.element_ctrl.create_beam(**TEST_BEAM_DATA)
        element_id = self.assert_element_id(result, "create_beam_for_cog")
        
        # Get center of gravity
        cog_result = await self.geometry_ctrl.get_center_of_gravity(element_id)
        self.assert_success(cog_result, "get_center_of_gravity")
        
        return {
            "element_id": element_id,
            "center_of_gravity": cog_result.get("center_of_gravity")
        }
    
    async def test_scale_elements(self):
        """Test scaling elements"""
        # Create test element
        result = await self.element_ctrl.create_beam(**TEST_BEAM_DATA)
        element_id = self.assert_element_id(result, "create_beam_for_scale")
        
        # Scale element by factor 1.5
        scale_result = await self.geometry_ctrl.scale_elements([element_id], 1.5)
        self.assert_success(scale_result, "scale_elements")
        
        return {
            "element_id": element_id,
            "scale_factor": 1.5,
            "scale_result": scale_result
        }
    
    async def test_move_elements(self):
        """Test moving elements"""
        # Create test element
        result = await self.element_ctrl.create_beam(**TEST_BEAM_DATA)
        element_id = self.assert_element_id(result, "create_beam_for_move")
        
        # Move element
        move_vector = [500, 300, 100]
        move_result = await self.element_ctrl.move_element([element_id], move_vector)
        self.assert_success(move_result, "move_element")
        
        return {
            "element_id": element_id,
            "move_vector": move_vector,
            "move_result": move_result
        }
