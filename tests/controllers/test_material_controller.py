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
    
    async def run_material_workflow_tests(self) -> list:
        """Run comprehensive material workflow tests"""
        self.helper.print_header("MATERIAL CONTROLLER - WORKFLOW TESTS")
        
        # Test 1: Create multiple materials with different properties
        materials_to_create = [
            {"name": "Oak", "density": 700.0, "thermal_conductivity": 0.17, "elastic_modulus": 11000.0, "color_id": 5},
            {"name": "Pine", "density": 520.0, "thermal_conductivity": 0.13, "elastic_modulus": 9000.0, "color_id": 10},
            {"name": "Steel", "density": 7850.0, "thermal_conductivity": 50.0, "elastic_modulus": 210000.0, "color_id": 15}
        ]
        
        created_materials = []
        for mat_config in materials_to_create:
            result = await self.helper.run_test(
                f"Create Material {mat_config['name']}",
                self.controller.create_material,
                mat_config["name"],
                mat_config["density"],
                mat_config["thermal_conductivity"],
                mat_config["elastic_modulus"],
                mat_config["color_id"]
            )
            if result.status == "PASSED":
                created_materials.append(mat_config["name"])
        
        # Test 2: Batch material property retrieval
        for material_name in created_materials:
            await self.helper.run_test(
                f"Get Properties for {material_name}",
                self.controller.get_material_properties,
                material_name
            )
        
        # Test 3: Material property updates
        if "Oak" in created_materials:
            await self.helper.run_test(
                "Update Oak Density",
                self.controller.set_material_density,
                "Oak",
                750.0  # Updated density
            )
            
            await self.helper.run_test(
                "Update Oak Thermal Properties",
                self.controller.set_material_thermal_properties,
                "Oak",
                0.19  # Updated thermal conductivity
            )
        
        # Test 4: Material validation with extreme values
        extreme_test_cases = [
            ("Very High Density", "TestExtreme1", 15000.0, 1.0, 50000.0, 25),
            ("Very Low Values", "TestExtreme2", 100.0, 0.01, 1000.0, 1),
        ]
        
        for test_name, mat_name, density, thermal, elastic, color in extreme_test_cases:
            await self.helper.run_test(
                test_name,
                self.controller.create_material,
                mat_name,
                density,
                thermal,
                elastic,
                color
            )
        
        # Test 5: Material error handling
        error_test_cases = [
            ("Empty Name", "", 500.0, 0.1, 8000.0, 5),
            ("Negative Density", "ErrorTest1", -100.0, 0.1, 8000.0, 5),
            ("Invalid Color ID", "ErrorTest2", 500.0, 0.1, 8000.0, 300),  # > 255
            ("Zero Elastic Modulus", "ErrorTest3", 500.0, 0.1, 0.0, 5)
        ]
        
        error_handling_score = 0
        for test_name, mat_name, density, thermal, elastic, color in error_test_cases:
            result = await self.helper.run_test(
                f"Error Handling: {test_name}",
                self.controller.create_material,
                mat_name,
                density,
                thermal,
                elastic,
                color
            )
            # Should fail with error
            if result.status == "FAILED" or "error" in result.message.lower():
                error_handling_score += 1
        
        await self.helper.run_test(
            "Material Error Handling Summary",
            self._summarize_error_handling,
            error_handling_score,
            len(error_test_cases)
        )
        
        return self.helper.test_results
    
    async def _summarize_error_handling(self, errors_caught, total_errors):
        """Summarize error handling results"""
        success_rate = errors_caught / total_errors if total_errors > 0 else 0
        if success_rate >= 0.75:
            return {"status": "success", "message": f"Error handling excellent: {errors_caught}/{total_errors} errors caught"}
        elif success_rate >= 0.5:
            return {"status": "success", "message": f"Error handling good: {errors_caught}/{total_errors} errors caught"}
        else:
            return {"status": "error", "message": f"Error handling needs improvement: only {errors_caught}/{total_errors} errors caught"}
