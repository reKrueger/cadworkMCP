"""Test Shop Drawing Controller"""
import sys, os
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
if PROJECT_ROOT not in sys.path: sys.path.insert(0, PROJECT_ROOT)

from controllers.shop_drawing_controller import CShopDrawingController
from tests.helpers.test_helper import TestHelper

class TestShopDrawingController:
    def __init__(self):
        self.controller = CShopDrawingController()
        self.helper = TestHelper()
    
    async def run_all_tests(self) -> list:
        self.helper.print_header("SHOP DRAWING CONTROLLER TESTS")
        await self.helper.run_test("Shop Drawing Test Placeholder", self._placeholder_test)
        return self.helper.test_results
    
    async def run_quick_tests(self) -> list:
        self.helper.print_header("SHOP DRAWING CONTROLLER - QUICK TESTS")
        await self.helper.run_test("Quick Shop Drawing Test", self._placeholder_test)
        return self.helper.test_results
    
    async def _placeholder_test(self): return {"status": "success", "message": "Shop drawing controller loaded"}
    def get_summary(self): return self.helper.get_summary()
    def print_summary(self): self.helper.print_summary()
