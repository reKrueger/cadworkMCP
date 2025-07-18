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
    
    async def run_extended_tests(self) -> list:
        """Run extended material controller tests with 5 new test cases"""
        self.helper.print_header("MATERIAL CONTROLLER EXTENDED TESTS")
        
        # Test 1: Create material with full properties
        await self.helper.run_test(
            "Create Material with Properties", 
            self.controller.create_material,
            "AdvancedWood",
            650.0,  # density kg/m³
            0.15,   # thermal_conductivity W/mK  
            11000.0,  # elastic_modulus N/mm²
            5       # color_id
        )
        
        # Test 2: Get material properties
        await self.helper.run_test(
            "Get Material Properties",
            self.controller.get_material_properties,
            "AdvancedWood"
        )
        
        # Test 3: Set material density
        await self.helper.run_test(
            "Set Material Density",
            self.controller.set_material_density,
            "AdvancedWood",
            700.0
        )
        
        # Test 4: Set thermal properties
        await self.helper.run_test(
            "Set Material Thermal Properties",
            self.controller.set_material_thermal_properties,
            "AdvancedWood",
            0.18
        )
        
        # Test 5: Create material with minimal properties
        await self.helper.run_test(
            "Create Minimal Material",
            self.controller.create_material,
            "SimpleSteel"
        )
        
        return self.helper.test_results
    
    async def run_quick_tests(self) -> list:
        self.helper.print_header("MATERIAL CONTROLLER - QUICK TESTS")
        await self.helper.run_test("Quick Material List", self.controller.list_available_materials)
        return self.helper.test_results
    
    def get_summary(self): return self.helper.get_summary()
    def print_summary(self): self.helper.print_summary()
