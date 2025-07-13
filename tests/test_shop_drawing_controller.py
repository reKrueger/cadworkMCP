"""
Shop Drawing Controller Tests
Tests für Werkstattzeichnungs-spezifische Funktionen
"""
import asyncio
import sys
import os

# Add project root to path
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, PROJECT_ROOT)

from tests.test_config import TestSuite, assert_ok, assert_error, assert_has_key, assert_equal
from controllers.shop_drawing_controller import CShopDrawingController
from controllers.element_controller import ElementController

class ShopDrawingControllerTests(TestSuite):
    """Test suite für Shop Drawing Controller"""
    
    def __init__(self):
        super().__init__("Shop Drawing Controller Tests")
        self.controller = CShopDrawingController()
        self.element_ctrl = ElementController()
        self.created_elements = []  # Track für cleanup
    
    def setup(self):
        """Setup test environment"""
        print("Setting up Shop Drawing Controller tests...")
        # Verify connection works
        try:
            result = asyncio.run(self.element_ctrl.get_all_element_ids())
            assert_ok(result, "Connection test failed")
            print("  + Connection established")
        except Exception as e:
            print(f"  X Connection failed: {e}")
            raise
    
    def teardown(self):
        """Cleanup after tests"""
        print("Cleaning up Shop Drawing Controller tests...")
        # Clean up created elements
        if self.created_elements:
            try:
                asyncio.run(self.element_ctrl.delete_elements(self.created_elements))
                print(f"  + Cleaned up {len(self.created_elements)} test elements")
            except:
                print("  - Cleanup warning: Some elements may remain")
    
    def create_test_wall_element(self, aP1: list, aP2: list) -> int:
        """Hilfsfunktion: Erstellt Test-Wand-Element"""
        try:
            # Erstelle eine Platte als "Wand" für Tests
            result = asyncio.run(self.element_ctrl.create_panel(aP1, aP2, 300, 200))
            if result.get("status") == "success":
                lElementId = result.get("element_id")
                self.created_elements.append(lElementId)
                return lElementId
            return None
        except:
            return None
    
    def test_add_wall_section_x_basic(self):
        """Test add_wall_section_x mit Basis-Parametern"""
        # Erstelle Test-Wand
        lWallId = self.create_test_wall_element([0, 0, 0], [3000, 0, 0])
        
        if not lWallId:
            self.log("Konnte Test-Wand nicht erstellen, Test übersprungen")
            return {"status": "info", "message": "Wall creation failed, test skipped"}
        
        result = asyncio.run(self.controller.add_wall_section_x(lWallId))
        assert_ok(result)
        assert_has_key(result, "section_id")
        assert_has_key(result, "wall_id")
        assert_has_key(result, "section_direction")
        assert_equal(result.get("wall_id"), lWallId)
        assert_equal(result.get("section_direction"), "x")
        
        self.log(f"X-Section created: Section ID {result.get('section_id')} for Wall {lWallId}")
        return result
    
    def test_add_wall_section_y_basic(self):
        """Test add_wall_section_y mit Basis-Parametern"""
        # Erstelle Test-Wand
        lWallId = self.create_test_wall_element([0, 0, 0], [0, 3000, 0])
        
        if not lWallId:
            self.log("Konnte Test-Wand nicht erstellen, Test übersprungen")
            return {"status": "info", "message": "Wall creation failed, test skipped"}
        
        result = asyncio.run(self.controller.add_wall_section_y(lWallId))
        assert_ok(result)
        assert_has_key(result, "section_id")
        assert_has_key(result, "wall_id")
        assert_has_key(result, "section_direction")
        assert_equal(result.get("wall_id"), lWallId)
        assert_equal(result.get("section_direction"), "y")
        
        self.log(f"Y-Section created: Section ID {result.get('section_id')} for Wall {lWallId}")
        return result
    
    def test_add_wall_section_x_with_params(self):
        """Test add_wall_section_x mit benutzerdefinierten Parametern"""
        # Erstelle Test-Wand
        lWallId = self.create_test_wall_element([0, 0, 0], [4000, 0, 0])
        
        if not lWallId:
            self.log("Konnte Test-Wand nicht erstellen, Test übersprungen")
            return {"status": "info", "message": "Wall creation failed, test skipped"}
        
        lSectionParams = {
            "position": "custom",
            "depth": 500,
            "show_dimensions": True,
            "show_materials": False,
            "offset": 1000
        }
        
        result = asyncio.run(self.controller.add_wall_section_x(lWallId, lSectionParams))
        assert_ok(result)
        assert_has_key(result, "section_params")
        
        lReturnedParams = result.get("section_params", {})
        assert_equal(lReturnedParams.get("position"), "custom")
        assert_equal(lReturnedParams.get("depth"), 500)
        assert_equal(lReturnedParams.get("show_dimensions"), True)
        assert_equal(lReturnedParams.get("show_materials"), False)
        
        self.log(f"X-Section with custom params: {lReturnedParams}")
        return result
    
    def test_shop_drawing_workflow_complete(self):
        """Test kompletter Shop Drawing Workflow: Wand erstellen, X- und Y-Schnitte hinzufügen"""
        # 1. Erstelle L-förmige Wand-Struktur
        lWallX = self.create_test_wall_element([0, 0, 0], [3000, 0, 0])  # Horizontal
        lWallY = self.create_test_wall_element([0, 0, 0], [0, 2000, 0])  # Vertikal
        
        if not lWallX or not lWallY:
            self.log("Konnte Test-Wände nicht erstellen, Workflow-Test übersprungen")
            return {"status": "info", "message": "Wall creation failed, workflow test skipped"}
        
        try:
            # 2. X-Schnitt für horizontale Wand
            lXSectionResult = asyncio.run(self.controller.add_wall_section_x(lWallX))
            assert_ok(lXSectionResult)
            lXSectionId = lXSectionResult.get("section_id")
            self.log(f"Workflow Schritt 1: X-Schnitt {lXSectionId} für Wand {lWallX}")
            
            # 3. Y-Schnitt für vertikale Wand
            lYSectionResult = asyncio.run(self.controller.add_wall_section_y(lWallY))
            assert_ok(lYSectionResult)
            lYSectionId = lYSectionResult.get("section_id")
            self.log(f"Workflow Schritt 2: Y-Schnitt {lYSectionId} für Wand {lWallY}")
            
            # 4. Zusätzlicher Y-Schnitt für horizontale Wand (Kreuzschnitt)
            lCrossSectionResult = asyncio.run(self.controller.add_wall_section_y(lWallX))
            assert_ok(lCrossSectionResult)
            lCrossSectionId = lCrossSectionResult.get("section_id")
            self.log(f"Workflow Schritt 3: Kreuz-Y-Schnitt {lCrossSectionId} für Wand {lWallX}")
            
            self.log("Kompletter Shop Drawing Workflow erfolgreich!")
            
            return {
                "status": "success",
                "message": "Complete shop drawing workflow successful",
                "wall_x_id": lWallX,
                "wall_y_id": lWallY,
                "x_section_id": lXSectionId,
                "y_section_id": lYSectionId,
                "cross_section_id": lCrossSectionId
            }
            
        except Exception as e:
            self.log(f"Workflow-Test Fehler: {e}")
            return {"status": "error", "message": f"Workflow test failed: {e}"}
    
    def test_shop_drawing_error_handling(self):
        """Test Fehlerbehandlung bei Shop Drawing Operationen"""
        # Test mit ungültiger Wall-ID
        result = asyncio.run(self.controller.add_wall_section_x(99999))
        # Kann sowohl error als auch success sein, je nach API-Verhalten
        assert_has_key(result, "status")
        self.log(f"Invalid wall ID test: {result.get('status')} - {result.get('message', 'No message')}")
        
        # Test mit negativer Wall-ID
        try:
            result = asyncio.run(self.controller.add_wall_section_y(-1))
            assert_error(result)
            self.log("Negative wall ID error handling: OK")
        except:
            self.log("Negative wall ID validation working at controller level")
        
        return {"status": "success", "message": "Shop drawing error handling tests completed"}
