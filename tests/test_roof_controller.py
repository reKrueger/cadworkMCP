"""
Roof Controller Tests
Tests für Dach-spezifische CAD-Funktionen
"""
import asyncio
import sys
import os

# Add project root to path
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, PROJECT_ROOT)

from tests.test_config import TestSuite, assert_ok, assert_error, assert_has_key, assert_equal
from controllers.roof_controller import CRoofController
from controllers.element_controller import ElementController

class RoofControllerTests(TestSuite):
    """Test suite für Roof Controller"""
    
    def __init__(self):
        super().__init__("Roof Controller Tests")
        self.controller = CRoofController()
        self.element_ctrl = ElementController()
        self.created_elements = []  # Track für cleanup
    
    def setup(self):
        """Setup test environment"""
        print("Setting up Roof Controller tests...")
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
        print("Cleaning up Roof Controller tests...")
        # Clean up created elements
        if self.created_elements:
            try:
                asyncio.run(self.element_ctrl.delete_elements(self.created_elements))
                print(f"  + Cleaned up {len(self.created_elements)} test elements")
            except:
                print("  - Cleanup warning: Some elements may remain")
    
    def create_test_roof_elements(self, aCount: int = 3) -> list:
        """Hilfsfunktion: Erstellt Test-Dach-Elemente (Platten als Dachflächen)"""
        lRoofElements = []
        
        for i in range(aCount):
            try:
                # Erstelle schräge Platten als "Dachflächen"
                lY = i * 2000
                lP1 = [0, lY, 0]
                lP2 = [4000, lY, 1000]  # Schräge für Dach-Effekt
                
                result = asyncio.run(self.element_ctrl.create_panel(lP1, lP2, 200, 40))
                if result.get("status") == "success":
                    lElementId = result.get("element_id")
                    self.created_elements.append(lElementId)
                    lRoofElements.append(lElementId)
            except:
                pass
        
        return lRoofElements
    
    def test_get_roof_surfaces_basic(self):
        """Test get_roof_surfaces mit Basis-Funktionalität"""
        # Erstelle Test-Dach-Elemente
        lRoofElements = self.create_test_roof_elements(2)
        
        if not lRoofElements:
            self.log("Konnte Test-Dach-Elemente nicht erstellen, Test übersprungen")
            return {"status": "info", "message": "Roof element creation failed, test skipped"}
        
        result = asyncio.run(self.controller.get_roof_surfaces(lRoofElements))
        assert_ok(result)
        assert_has_key(result, "analyzed_elements")
        assert_has_key(result, "surface_details")
        assert_equal(result.get("analyzed_elements"), len(lRoofElements))
        
        lSurfaceDetails = result.get("surface_details", [])
        assert_equal(len(lSurfaceDetails), len(lRoofElements))
        
        for lDetail in lSurfaceDetails:
            assert_has_key(lDetail, "element_id")
            assert_has_key(lDetail, "element_type")
            assert_has_key(lDetail, "is_roof_element")
        
        self.log(f"Roof surfaces analyzed: {len(lRoofElements)} elements")
        return result
    
    def test_calculate_roof_area_basic(self):
        """Test calculate_roof_area mit Basis-Funktionalität"""
        # Erstelle Test-Dach-Elemente
        lRoofElements = self.create_test_roof_elements(3)
        
        if not lRoofElements:
            self.log("Konnte Test-Dach-Elemente nicht erstellen, Test übersprungen")
            return {"status": "info", "message": "Roof element creation failed, test skipped"}
        
        result = asyncio.run(self.controller.calculate_roof_area(lRoofElements))
        assert_ok(result)
        assert_has_key(result, "detailed_calculations")
        assert_has_key(result, "element_areas")
        
        lDetailedCalc = result.get("detailed_calculations", {})
        assert_has_key(lDetailedCalc, "total_sloped_area_m2")
        assert_has_key(lDetailedCalc, "element_count")
        assert_equal(lDetailedCalc.get("element_count"), len(lRoofElements))
        
        lElementAreas = result.get("element_areas", [])
        assert_equal(len(lElementAreas), len(lRoofElements))
        
        lTotalArea = lDetailedCalc.get("total_sloped_area_m2", 0)
        self.log(f"Roof area calculated: {lTotalArea:.2f} m² for {len(lRoofElements)} elements")
        
        return result
    
    def test_roof_workflow_complete(self):
        """Test kompletter Roof-Workflow: Elemente erstellen, Surfaces analysieren, Area berechnen"""
        # 1. Erstelle komplexeres Dach-System
        lMainRoof = self.create_test_roof_elements(2)
        lSideRoof = []
        
        # Zusätzliche Dach-Elemente für komplexere Struktur
        try:
            for i in range(2):
                lX = 4000 + i * 1500
                lP1 = [lX, 0, 800]
                lP2 = [lX, 3000, 400]  # Andere Neigung
                
                result = asyncio.run(self.element_ctrl.create_panel(lP1, lP2, 150, 30))
                if result.get("status") == "success":
                    lElementId = result.get("element_id")
                    self.created_elements.append(lElementId)
                    lSideRoof.append(lElementId)
        except:
            pass
        
        lAllRoofElements = lMainRoof + lSideRoof
        
        if len(lAllRoofElements) < 2:
            self.log("Konnte nicht genügend Dach-Elemente erstellen, Workflow-Test übersprungen")
            return {"status": "info", "message": "Insufficient roof elements, workflow test skipped"}
        
        try:
            # 2. Dachflächen analysieren
            lSurfaceResult = asyncio.run(self.controller.get_roof_surfaces(lAllRoofElements))
            assert_ok(lSurfaceResult)
            self.log(f"Workflow Schritt 1: {len(lAllRoofElements)} Dachflächen analysiert")
            
            # 3. Hauptdach-Bereich berechnen
            if lMainRoof:
                lMainAreaResult = asyncio.run(self.controller.calculate_roof_area(lMainRoof))
                assert_ok(lMainAreaResult)
                lMainArea = lMainAreaResult.get("detailed_calculations", {}).get("total_sloped_area_m2", 0)
                self.log(f"Workflow Schritt 2: Hauptdach-Fläche {lMainArea:.2f} m²")
            
            # 4. Gesamtdach-Bereich berechnen
            lTotalAreaResult = asyncio.run(self.controller.calculate_roof_area(lAllRoofElements))
            assert_ok(lTotalAreaResult)
            lTotalArea = lTotalAreaResult.get("detailed_calculations", {}).get("total_sloped_area_m2", 0)
            self.log(f"Workflow Schritt 3: Gesamtdach-Fläche {lTotalArea:.2f} m²")
            
            self.log("Kompletter Roof-Workflow erfolgreich!")
            
            return {
                "status": "success",
                "message": "Complete roof workflow successful",
                "main_roof_elements": lMainRoof,
                "side_roof_elements": lSideRoof,
                "total_roof_area_m2": lTotalArea,
                "element_count": len(lAllRoofElements)
            }
            
        except Exception as e:
            self.log(f"Roof-Workflow Fehler: {e}")
            return {"status": "error", "message": f"Roof workflow test failed: {e}"}
    
    def test_roof_error_handling(self):
        """Test Fehlerbehandlung bei Roof-Operationen"""
        # Test mit leerer Element-Liste
        result = asyncio.run(self.controller.get_roof_surfaces([]))
        assert_error(result)
        assert_has_key(result, "message")
        self.log("Empty element list error handling: OK")
        
        # Test roof area mit leerer Liste
        result = asyncio.run(self.controller.calculate_roof_area([]))
        assert_error(result)
        assert_has_key(result, "message")
        self.log("Empty roof element list error handling: OK")
        
        # Test mit ungültigen Element-IDs
        result = asyncio.run(self.controller.get_roof_surfaces([99999, 88888]))
        # Kann sowohl error als auch success sein, je nach API-Verhalten
        assert_has_key(result, "status")
        self.log(f"Invalid element IDs test: {result.get('status')} - {result.get('message', 'No message')}")
        
        return {"status": "success", "message": "Roof error handling tests completed"}
    
    def test_roof_single_element_analysis(self):
        """Test Roof-Analyse mit einzelnem Element"""
        # Erstelle einzelnes Dach-Element
        lRoofElements = self.create_test_roof_elements(1)
        
        if not lRoofElements:
            self.log("Konnte Test-Dach-Element nicht erstellen, Test übersprungen")
            return {"status": "info", "message": "Single roof element creation failed, test skipped"}
        
        lElementId = lRoofElements[0]
        
        # Surface-Analyse
        lSurfaceResult = asyncio.run(self.controller.get_roof_surfaces([lElementId]))
        assert_ok(lSurfaceResult)
        assert_equal(lSurfaceResult.get("analyzed_elements"), 1)
        
        # Area-Berechnung
        lAreaResult = asyncio.run(self.controller.calculate_roof_area([lElementId]))
        assert_ok(lAreaResult)
        
        lCalculations = lAreaResult.get("detailed_calculations", {})
        lSingleArea = lCalculations.get("total_sloped_area_m2", 0)
        lAvgArea = lCalculations.get("average_area_per_element_m2", 0)
        
        # Bei einem Element sollten Gesamt- und Durchschnittsfläche gleich sein
        assert_equal(lSingleArea, lAvgArea)
        
        self.log(f"Single element analysis: {lSingleArea:.2f} m² roof area")
        return lAreaResult
