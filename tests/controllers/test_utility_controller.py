"""Test Utility Controller"""
import sys, os
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
if PROJECT_ROOT not in sys.path: sys.path.insert(0, PROJECT_ROOT)

from controllers.utility_controller import CUtilityController
from tests.helpers.test_helper import TestHelper

class TestUtilityController:
    def __init__(self):
        self.controller = CUtilityController()
        self.helper = TestHelper()
    
    async def run_all_tests(self) -> list:
        self.helper.print_header("UTILITY CONTROLLER TESTS")
        await self.helper.run_test("Get Project Data", self.controller.get_project_data)
        await self.helper.run_test("Get Cadwork Version", self.controller.get_cadwork_version_info)
        return self.helper.test_results
    
    async def run_quick_tests(self) -> list:
        self.helper.print_header("UTILITY CONTROLLER - QUICK TESTS")
        await self.helper.run_test("Quick Version Check", self.controller.get_cadwork_version_info)
        return self.helper.test_results
    
    def get_summary(self): return self.helper.get_summary()
    def print_summary(self): self.helper.print_summary()
