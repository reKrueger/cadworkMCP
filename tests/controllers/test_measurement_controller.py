"""Test Measurement Controller"""
import sys, os
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
if PROJECT_ROOT not in sys.path: sys.path.insert(0, PROJECT_ROOT)

from controllers.measurement_controller import CMeasurementController
from tests.helpers.test_helper import TestHelper

class TestMeasurementController:
    def __init__(self):
        self.controller = CMeasurementController()
        self.helper = TestHelper()
    
    async def run_all_tests(self) -> list:
        self.helper.print_header("MEASUREMENT CONTROLLER TESTS")
        await self.helper.run_test("Measure Distance", self.controller.measure_distance, [0,0,0], [1000,0,0])
        await self.helper.run_test("Measure Angle", self.controller.measure_angle, [1,0,0], [0,1,0])
        return self.helper.test_results
    
    async def run_quick_tests(self) -> list:
        self.helper.print_header("MEASUREMENT CONTROLLER - QUICK TESTS")
        await self.helper.run_test("Quick Distance", self.controller.measure_distance, [0,0,0], [100,0,0])
        return self.helper.test_results
    
    def get_summary(self): return self.helper.get_summary()
    def print_summary(self): self.helper.print_summary()
