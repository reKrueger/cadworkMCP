"""
Optimization Controller Tests
=============================

Tests for COptimizationController - cutting list optimization and material efficiency.
"""

import sys
import os
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from helpers.base_test import BaseCadworkTest
from helpers.test_data import TEST_BEAM_DATA
from controllers.element_controller import ElementController
from controllers.optimization_controller import COptimizationController


class TestOptimizationController(BaseCadworkTest):
    """Test optimization operations"""
    
    def __init__(self):
        super().__init__()
        self.element_ctrl = ElementController()
        self.optimization_ctrl = COptimizationController()
    
    async def test_optimize_cutting_list_basic(self):
        """Test basic cutting list optimization"""
        # Create test elements with different lengths
        beam1_data = {
            "p1": [0.0, 0.0, 0.0],
            "p2": [1500.0, 0.0, 0.0],  # 1500mm length
            "width": 120.0,
            "height": 200.0
        }
        beam2_data = {
            "p1": [0.0, 0.0, 0.0],
            "p2": [800.0, 0.0, 0.0],   # 800mm length
            "width": 120.0,
            "height": 200.0
        }
        
        # Create test elements
        result1 = await self.element_ctrl.create_beam(**beam1_data)
        element_id1 = self.assert_element_id(result1, "create_beam_for_optimization_1")
        
        result2 = await self.element_ctrl.create_beam(**beam2_data)
        element_id2 = self.assert_element_id(result2, "create_beam_for_optimization_2")
        
        # Test basic optimization
        optimization_result = await self.optimization_ctrl.optimize_cutting_list(
            element_ids=[element_id1, element_id2]
        )
        self.assert_success(optimization_result, "optimize_cutting_list_basic")
        
        return {
            "element_ids": [element_id1, element_id2],
            "optimization_result": optimization_result
        }    
    async def test_optimize_cutting_list_advanced(self):
        """Test advanced cutting list optimization parameters"""
        # Test with custom stock lengths and optimization parameters
        advanced_result = await self.optimization_ctrl.optimize_cutting_list(
            stock_lengths=[3000.0, 4000.0, 6000.0],
            optimization_algorithm="genetic",
            kerf_width=2.5,
            min_offcut_length=150.0,
            max_waste_percentage=3.0,
            priority_mode="cost_reduction"
        )
        self.assert_success(advanced_result, "optimize_cutting_list_advanced")
        
        # Test parameter validation
        invalid_algorithm_result = await self.optimization_ctrl.optimize_cutting_list(
            optimization_algorithm="invalid_algorithm"
        )
        self.assert_error(invalid_algorithm_result, "optimize_cutting_list_invalid_algorithm")
        
        invalid_kerf_result = await self.optimization_ctrl.optimize_cutting_list(
            kerf_width=-1.0  # Negative kerf width
        )
        self.assert_error(invalid_kerf_result, "optimize_cutting_list_invalid_kerf")
        
        invalid_waste_result = await self.optimization_ctrl.optimize_cutting_list(
            max_waste_percentage=150.0  # > 100%
        )
        self.assert_error(invalid_waste_result, "optimize_cutting_list_invalid_waste")
        
        invalid_priority_result = await self.optimization_ctrl.optimize_cutting_list(
            priority_mode="invalid_priority"
        )
        self.assert_error(invalid_priority_result, "optimize_cutting_list_invalid_priority")
        
        return {
            "advanced_tests": "completed",
            "advanced_result": advanced_result
        }
