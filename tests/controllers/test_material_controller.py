"""Test Material Controller"""
import sys, os
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
if PROJECT_ROOT not in sys.path: sys.path.insert(0, PROJECT_ROOT)

from controllers.material_controller import CMaterialController
from tests.helpers.test_helper import TestHelper

class TestMaterialController:
    def __init__(self):
        self.controller = CMaterialController()
        self.helper = TestHelper()
    
    async def run_all_tests(self) -> list:
        self.helper.print_header("MATERIAL CONTROLLER TESTS")
        await self.helper.run_test("List Materials", self.controller.list_available_materials)
        await self.helper.run_test("Create Material", self.controller.create_material, "TestWood")
        return self.helper.test_results
    
    async def run_quick_tests(self) -> list:
        self.helper.print_header("MATERIAL CONTROLLER - QUICK TESTS")
        await self.helper.run_test("Quick Material List", self.controller.list_available_materials)
        return self.helper.test_results
    
    def get_summary(self): return self.helper.get_summary()
    def print_summary(self): self.helper.print_summary()
