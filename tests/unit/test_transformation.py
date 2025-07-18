"""
Transformation Controller Tests
==============================

Tests for CTransformationController - element rotation and scaling.
"""

import sys
import os
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from helpers.base_test import BaseCadworkTest
from helpers.test_data import TEST_BEAM_DATA, TEST_PANEL_DATA
from controllers.transformation_controller import CTransformationController
from controllers.element_controller import ElementController


class TestTransformationController(BaseCadworkTest):
    """Test element transformation operations"""
    
    def __init__(self, use_mock: bool = False):
        super().__init__(use_mock=use_mock)
        self.transformation_ctrl = CTransformationController()
        self.element_ctrl = ElementController()
    
    def log_success(self, message: str):
        """Log success message"""
        print(f"SUCCESS: {message}")
    
    def log_error(self, message: str):
        """Log error message"""
        print(f"ERROR: {message}")
    
    def log_info(self, message: str):
        """Log info message"""
        print(f"INFO: {message}")
    
    async def test_rotate_elements_basic(self):
        """Test basic element rotation"""
        try:
            # Rotate around Z-axis by 90 degrees with mock element ID
            origin = [0.0, 0.0, 0.0]
            rotation_axis = [0.0, 0.0, 1.0]  # Z-axis
            rotation_angle = 90.0  # degrees
            
            result = await self.transformation_ctrl.rotate_elements(
                [1], origin, rotation_axis, rotation_angle
            )
            
            if result and "status" in result:
                self.log_success(f"Rotation completed with status: {result['status']}")
            else:
                self.log_info(f"Rotation result: {result}")
                
        except Exception as e:
            self.log_error(f"Rotation failed: {e}")
    
    async def test_apply_global_scale_basic(self):
        """Test basic element scaling"""
        try:
            # Scale by factor 2.0 around origin with mock element ID
            scale_factor = 2.0
            origin = [0.0, 0.0, 0.0]
            
            result = await self.transformation_ctrl.apply_global_scale(
                [1], scale_factor, origin
            )
            
            if result and "status" in result:
                self.log_success(f"Scaling completed with status: {result['status']}")
            else:
                self.log_info(f"Scaling result: {result}")
                
        except Exception as e:
            self.log_error(f"Scaling failed: {e}")

    
    async def test_rotate_empty_list(self):
        """Test error handling for empty element list"""
        try:
            await self.transformation_ctrl.rotate_elements(
                [], [0.0, 0.0, 0.0], [0.0, 0.0, 1.0], 90.0
            )
            self.log_error("Should have failed with empty element list")
        except ValueError as e:
            self.log_success(f"Correctly caught error for empty list: {e}")
    
    async def test_rotate_zero_axis(self):
        """Test error handling for zero rotation axis"""
        beam_result = await self.element_ctrl.create_beam(**TEST_BEAM_DATA)
        beam_id = self.assert_element_id(beam_result, "create_beam")
        
        try:
            await self.transformation_ctrl.rotate_elements(
                [beam_id], [0.0, 0.0, 0.0], [0.0, 0.0, 0.0], 90.0
            )
            self.log_error("Should have failed with zero rotation axis")
        except ValueError as e:
            self.log_success(f"Correctly caught error for zero axis: {e}")
    
    async def test_scale_negative_factor(self):
        """Test error handling for negative scale factor"""
        beam_result = await self.element_ctrl.create_beam(**TEST_BEAM_DATA)
        beam_id = self.assert_element_id(beam_result, "create_beam")
        
        try:
            await self.transformation_ctrl.apply_global_scale(
                [beam_id], -1.0, [0.0, 0.0, 0.0]
            )
            self.log_error("Should have failed with negative scale factor")
        except ValueError as e:
            self.log_success(f"Correctly caught error for negative scale: {e}")
    
    async def run_all_tests(self):
        """Run all transformation tests"""
        self.log_info("Starting Transformation Controller Tests...")
        
        await self.test_rotate_elements_basic()
        await self.test_apply_global_scale_basic()
        await self.test_rotate_empty_list()
        await self.test_rotate_zero_axis()
        await self.test_scale_negative_factor()
        
        self.log_info("Transformation Controller Tests completed!")
