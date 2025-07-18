"""
Performance Tests
================

Tests for performance and timing of operations.
"""

import sys
import os
import time
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from helpers.base_test import BaseCadworkTest
from helpers.test_data import TEST_BEAM_DATA, PERFORMANCE_LIMITS
from controllers.element_controller import ElementController


class TestPerformance(BaseCadworkTest):
    """Test performance and timing of operations"""
    
    def __init__(self, use_mock: bool = False):
        super().__init__(use_mock=use_mock)
        self.element_ctrl = ElementController()
    
    async def test_single_element_creation_performance(self):
        """Test single element creation performance"""
        start_time = time.time()
        
        result = await self.element_ctrl.create_beam(**TEST_BEAM_DATA)
        element_id = self.assert_element_id(result, "create_beam_performance")
        
        creation_time = time.time() - start_time
        time_limit = PERFORMANCE_LIMITS["single_element_creation"]
        
        # Performance assertion
        if creation_time > time_limit:
            raise AssertionError(f"Element creation too slow: {creation_time:.3f}s > {time_limit}s")
        
        return {
            "element_id": element_id,
            "creation_time": creation_time,
            "time_limit": time_limit,
            "performance_ratio": creation_time / time_limit
        }
    
    async def test_bulk_element_creation_performance(self):
        """Test bulk element creation performance"""
        element_count = 5  # Reduced for mock testing
        start_time = time.time()
        
        created_elements = []
        for i in range(element_count):
            beam_data = TEST_BEAM_DATA.copy()
            beam_data["p1"][0] = i * 1200  # Offset each beam
            beam_data["p2"][0] = (i * 1200) + 1000
            
            result = await self.element_ctrl.create_beam(**beam_data)
            element_id = self.assert_element_id(result, f"bulk_beam_{i}")
            created_elements.append(element_id)
        
        total_time = time.time() - start_time
        avg_time = total_time / element_count
        time_limit = PERFORMANCE_LIMITS["bulk_element_creation"]
        
        # Performance assertion
        if total_time > time_limit:
            raise AssertionError(f"Bulk creation too slow: {total_time:.3f}s > {time_limit}s")
        
        return {
            "element_ids": created_elements,
            "element_count": element_count,
            "total_time": total_time,
            "average_time": avg_time,
            "time_limit": time_limit,
            "elements_per_second": element_count / total_time
        }
    
    async def test_element_query_performance(self):
        """Test element query performance"""
        # Create a test element first
        create_result = await self.element_ctrl.create_beam(**TEST_BEAM_DATA)
        element_id = self.assert_element_id(create_result, "create_beam_for_query")
        
        start_time = time.time()
        
        # Query all elements
        result = await self.element_ctrl.get_all_element_ids()
        element_ids = self.assert_element_list(result, "get_all_element_ids")
        
        query_time = time.time() - start_time
        time_limit = PERFORMANCE_LIMITS["element_query"]
        
        # Performance assertion
        if query_time > time_limit:
            raise AssertionError(f"Element query too slow: {query_time:.3f}s > {time_limit}s")
        
        return {
            "query_time": query_time,
            "time_limit": time_limit,
            "element_count": len(element_ids),
            "elements_per_second": len(element_ids) / query_time if query_time > 0 else 0
        }
    
    async def test_stress_test_rapid_operations(self):
        """Test rapid successive operations"""
        operations = []
        start_time = time.time()
        
        # Rapid creation
        for i in range(3):
            op_start = time.time()
            
            beam_data = TEST_BEAM_DATA.copy()
            beam_data["p1"][0] = i * 800
            beam_data["p2"][0] = (i * 800) + 600
            
            result = await self.element_ctrl.create_beam(**beam_data)
            element_id = self.assert_element_id(result, f"stress_beam_{i}")
            
            op_time = time.time() - op_start
            operations.append({
                "operation": f"create_beam_{i}",
                "time": op_time,
                "element_id": element_id
            })
        
        total_time = time.time() - start_time
        avg_operation_time = total_time / len(operations)
        
        return {
            "operations": operations,
            "total_operations": len(operations),
            "total_time": total_time,
            "average_operation_time": avg_operation_time,
            "operations_per_second": len(operations) / total_time
        }
