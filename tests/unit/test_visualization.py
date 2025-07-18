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
    
    async def test_create_assembly_animation(self):
        """Test creating assembly animation"""
        # Create test elements
        beam_result = await self.element_ctrl.create_beam(**TEST_BEAM_DATA)
        beam_id = self.assert_element_id(beam_result, "create_beam_for_animation")
        
        # Test basic animation creation
        animation_result = await self.viz_ctrl.create_assembly_animation(
            element_ids=[beam_id],
            animation_type="sequential",
            duration=5.0
        )
        self.assert_success(animation_result, "create_assembly_animation_basic")
        
        # Test with multiple elements and advanced parameters
        beam2_data = {
            "p1": [1000.0, 0.0, 0.0],
            "p2": [2000.0, 0.0, 0.0],
            "width": 100.0,
            "height": 100.0
        }
        beam2_result = await self.element_ctrl.create_beam(**beam2_data)
        beam2_id = self.assert_element_id(beam2_result, "create_beam_for_animation_2")
        
        advanced_result = await self.viz_ctrl.create_assembly_animation(
            element_ids=[beam_id, beam2_id],
            animation_type="parallel",
            duration=10.0,
            start_delay=1.0,
            element_delay=0.5,
            fade_in=True,
            movement_path="gravity"
        )
        self.assert_success(advanced_result, "create_assembly_animation_advanced")
        
        # Test invalid parameters
        invalid_type_result = await self.viz_ctrl.create_assembly_animation(
            element_ids=[beam_id],
            animation_type="invalid_type"
        )
        self.assert_error(invalid_type_result, "create_assembly_animation_invalid_type")
        
        invalid_duration_result = await self.viz_ctrl.create_assembly_animation(
            element_ids=[beam_id],
            duration=-1.0
        )
        self.assert_error(invalid_duration_result, "create_assembly_animation_invalid_duration")
        
        return {
            "element_ids": [beam_id, beam2_id],
            "animation_results": [animation_result, advanced_result]
        }
    
    async def test_set_camera_position(self):
        """Test setting camera position"""
        # Test basic camera positioning
        basic_result = await self.viz_ctrl.set_camera_position(
            position=[1000.0, 1000.0, 1000.0],
            target=[0.0, 0.0, 0.0]
        )
        self.assert_success(basic_result, "set_camera_position_basic")
        
        # Test with advanced parameters
        advanced_result = await self.viz_ctrl.set_camera_position(
            position=[2000.0, 2000.0, 1500.0],
            target=[500.0, 500.0, 0.0],
            up_vector=[0.0, 0.0, 1.0],
            fov=60.0,
            animate_transition=True,
            transition_duration=3.0,
            camera_name="overview"
        )
        self.assert_success(advanced_result, "set_camera_position_advanced")
        
        # Test invalid parameters
        invalid_position_result = await self.viz_ctrl.set_camera_position(
            position=[1000.0, 1000.0],  # Missing z coordinate
            target=[0.0, 0.0, 0.0]
        )
        self.assert_error(invalid_position_result, "set_camera_position_invalid_position")
        
        invalid_fov_result = await self.viz_ctrl.set_camera_position(
            position=[1000.0, 1000.0, 1000.0],
            target=[0.0, 0.0, 0.0],
            fov=200.0  # Invalid FOV > 180
        )
        self.assert_error(invalid_fov_result, "set_camera_position_invalid_fov")
        
        same_position_target_result = await self.viz_ctrl.set_camera_position(
            position=[1000.0, 1000.0, 1000.0],
            target=[1000.0, 1000.0, 1000.0]  # Same as position
        )
        self.assert_error(same_position_target_result, "set_camera_position_same_point")
        
        return {
            "camera_results": [basic_result, advanced_result]
        }
    
    async def test_create_walkthrough(self):
        """Test creating 3D walkthrough"""
        # Define waypoints for walkthrough
        waypoints = [
            [0.0, 0.0, 1700.0],      # Start position
            [2000.0, 0.0, 1700.0],   # Move forward
            [2000.0, 2000.0, 1700.0], # Turn right
            [0.0, 2000.0, 1700.0],   # Move back
            [0.0, 0.0, 1700.0]       # Return to start
        ]
        
        # Test basic walkthrough creation
        basic_result = await self.viz_ctrl.create_walkthrough(
            waypoints=waypoints,
            duration=20.0
        )
        self.assert_success(basic_result, "create_walkthrough_basic")
        
        # Test with advanced parameters
        advanced_result = await self.viz_ctrl.create_walkthrough(
            waypoints=waypoints,
            duration=30.0,
            camera_height=1800.0,
            movement_speed="smooth",
            include_audio=True,
            output_format="mp4",
            resolution="1920x1080"
        )
        self.assert_success(advanced_result, "create_walkthrough_advanced")
        
        # Test invalid parameters
        invalid_waypoints_result = await self.viz_ctrl.create_walkthrough(
            waypoints=[[0.0, 0.0]]  # Missing waypoints
        )
        self.assert_error(invalid_waypoints_result, "create_walkthrough_invalid_waypoints")
        
        insufficient_waypoints_result = await self.viz_ctrl.create_walkthrough(
            waypoints=[[0.0, 0.0, 0.0]]  # Only one waypoint
        )
        self.assert_error(insufficient_waypoints_result, "create_walkthrough_insufficient_waypoints")
        
        invalid_duration_result = await self.viz_ctrl.create_walkthrough(
            waypoints=waypoints,
            duration=-5.0  # Negative duration
        )
        self.assert_error(invalid_duration_result, "create_walkthrough_invalid_duration")
        
        invalid_resolution_result = await self.viz_ctrl.create_walkthrough(
            waypoints=waypoints,
            resolution="invalid_resolution"
        )
        self.assert_error(invalid_resolution_result, "create_walkthrough_invalid_resolution")
        
        return {
            "waypoints": waypoints,
            "walkthrough_results": [basic_result, advanced_result]
        }
