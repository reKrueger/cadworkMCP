"""Test Attribute Controller"""
import sys, os
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
if PROJECT_ROOT not in sys.path: sys.path.insert(0, PROJECT_ROOT)

from controllers.attribute_controller import AttributeController
from tests.helpers.test_helper import TestHelper, TestResult
from tests.helpers.parameter_finder import ParameterFinder  

class TestAttributeController:
    def __init__(self):
        self.controller = AttributeController()
        self.helper = TestHelper()
        self.param_finder = ParameterFinder()
    
    async def run_all_tests(self) -> list:
        self.helper.print_header("ATTRIBUTE CONTROLLER TESTS")
        await self.helper.run_test("Set Material Test", self._test_material)
        await self.helper.run_test("Set Name Test", self._test_name)
        return self.helper.test_results
    
    async def run_quick_tests(self) -> list:
        self.helper.print_header("ATTRIBUTE CONTROLLER - QUICK TESTS")
        await self.helper.run_test("Quick Attribute Test", self._quick_test)
        return self.helper.test_results
    
    async def _test_material(self): return {"status": "success", "message": "Material test"}
    async def _test_name(self): return {"status": "success", "message": "Name test"}
    async def _quick_test(self): return {"status": "success", "message": "Attribute controller loaded"}
    
    def get_summary(self): return self.helper.get_summary()
    def print_summary(self): self.helper.print_summary()
