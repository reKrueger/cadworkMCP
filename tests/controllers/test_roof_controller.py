"""Test Roof Controller"""
import sys, os
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
if PROJECT_ROOT not in sys.path: sys.path.insert(0, PROJECT_ROOT)

from controllers.roof_controller import CRoofController
from tests.helpers.test_helper import TestHelper

class TestRoofController:
    def __init__(self):
        self.controller = CRoofController()
        self.helper = TestHelper()
    
    async def run_all_tests(self) -> list:
        self.helper.print_header("ROOF CONTROLLER TESTS")
        await self.helper.run_test("Roof Test Placeholder", self._placeholder_test)
        return self.helper.test_results
    
    async def run_quick_tests(self) -> list:
        self.helper.print_header("ROOF CONTROLLER - QUICK TESTS")
        await self.helper.run_test("Quick Roof Test", self._placeholder_test)
        return self.helper.test_results
    
    async def _placeholder_test(self): return {"status": "success", "message": "Roof controller loaded"}
    def get_summary(self): return self.helper.get_summary()
    def print_summary(self): self.helper.print_summary()
