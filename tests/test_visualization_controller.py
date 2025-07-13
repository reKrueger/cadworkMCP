"""
Visualization Controller Tests
Tests für Farben, Transparenz und Display-Management
"""
import asyncio
import sys
import os

# Add project root to path
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, PROJECT_ROOT)

from tests.test_config import TestSuite, assert_ok, assert_error, assert_has_key
from controllers.visualization_controller import CVisualizationController
from controllers.element_controller import ElementController

class VisualizationControllerTests(TestSuite):
    """Test suite für Visualization Controller"""
    
    def __init__(self):
        super().__init__("Visualization Controller Tests")
        self.controller = CVisualizationController()
        self.element_controller = ElementController()
        self.element_ids = []
    
    def setup(self):
        """Setup vor allen Tests"""
        self.log("Setting up Visualization Controller tests...")
        # Erstelle Test-Element für Visualization-Tests
        try:
            result = asyncio.run(self.element_controller.create_beam([0, 0, 0], [1000, 0, 0], 60, 120))
            if result.get("status") == "ok" and "element_id" in result:
                self.element_ids.append(result["element_id"])
                self.log(f"Created test element: {result['element_id']}")
        except Exception as e:
            self.log(f"Could not create test element: {e}")
    
    def teardown(self):
        """Cleanup nach allen Tests"""
        self.log("Cleaning up Visualization Controller tests...")
        # Test-Elemente löschen
        if self.element_ids:
            try:
                asyncio.run(self.element_controller.delete_elements(self.element_ids))
                self.log(f"Deleted {len(self.element_ids)} test elements")
            except Exception as e:
                self.log(f"Could not delete test elements: {e}")
    
    def get_test_element(self):
        """Hilfsmethode um Test-Element zu bekommen"""
        if self.element_ids:
            return self.element_ids[0]
        else:
            # Fallback: erstelle neues Element
            result = asyncio.run(self.element_controller.create_beam([0, 0, 100], [1000, 0, 100], 60, 120))
            if result.get("status") == "ok" and "element_id" in result:
                element_id = result["element_id"]
                self.element_ids.append(element_id)
                return element_id
            return None
    
    def test_set_color_valid(self):
        """Test set_color mit gültigem Element und Farbe"""
        element_id = self.get_test_element()
        if not element_id:
            return {"status": "skip", "message": "No test element available"}
        
        result = asyncio.run(self.controller.set_color([element_id], 5))  # Blau
        assert_ok(result)
        assert_has_key(result, "message")
        self.log(f"Set color to blue for element {element_id}")
        return result
    
    def test_set_color_invalid_color(self):
        """Test set_color mit ungültiger Farb-ID"""
        element_id = self.get_test_element()
        if not element_id:
            return {"status": "skip", "message": "No test element available"}
        
        result = asyncio.run(self.controller.set_color([element_id], 999))  # Ungültige Farbe
        assert_error(result)
        assert_has_key(result, "message")
        self.log(f"Invalid color ID rejected: {result.get('message')}")
        return result    
    def test_set_transparency_valid(self):
        """Test set_transparency mit gültigem Wert"""
        element_id = self.get_test_element()
        if not element_id:
            return {"status": "skip", "message": "No test element available"}
        
        result = asyncio.run(self.controller.set_transparency([element_id], 50))  # 50% transparent
        assert_ok(result)
        assert_has_key(result, "message")
        self.log(f"Set transparency to 50% for element {element_id}")
        return result
    
    def test_set_transparency_invalid(self):
        """Test set_transparency mit ungültigem Wert"""
        element_id = self.get_test_element()
        if not element_id:
            return {"status": "skip", "message": "No test element available"}
        
        result = asyncio.run(self.controller.set_transparency([element_id], 150))  # > 100%
        assert_error(result)
        assert_has_key(result, "message")
        self.log(f"Invalid transparency rejected: {result.get('message')}")
        return result
    
    def test_set_visibility_show(self):
        """Test set_visibility - Element sichtbar machen"""
        element_id = self.get_test_element()
        if not element_id:
            return {"status": "skip", "message": "No test element available"}
        
        result = asyncio.run(self.controller.set_visibility([element_id], True))
        assert_ok(result)
        assert_has_key(result, "message")
        self.log(f"Made element {element_id} visible")
        return result
    
    def test_set_visibility_hide(self):
        """Test set_visibility - Element ausblenden"""
        element_id = self.get_test_element()
        if not element_id:
            return {"status": "skip", "message": "No test element available"}
        
        result = asyncio.run(self.controller.set_visibility([element_id], False))
        assert_ok(result)
        assert_has_key(result, "message")
        self.log(f"Hidden element {element_id}")
        return result
    
    def test_get_color(self):
        """Test get_color - Farbe eines Elements abfragen"""
        element_id = self.get_test_element()
        if not element_id:
            return {"status": "skip", "message": "No test element available"}
        
        # Erst Farbe setzen
        asyncio.run(self.controller.set_color([element_id], 3))  # Rot
        
        # Dann abfragen
        result = asyncio.run(self.controller.get_color(element_id))
        assert_ok(result)
        assert_has_key(result, "color_id")
        self.log(f"Got color for element {element_id}: {result.get('color_id')}")
        return result
    
    def test_get_transparency(self):
        """Test get_transparency - Transparenz eines Elements abfragen"""
        element_id = self.get_test_element()
        if not element_id:
            return {"status": "skip", "message": "No test element available"}
        
        # Erst Transparenz setzen
        asyncio.run(self.controller.set_transparency([element_id], 25))  # 25%
        
        # Dann abfragen
        result = asyncio.run(self.controller.get_transparency(element_id))
        assert_ok(result)
        assert_has_key(result, "transparency")
        self.log(f"Got transparency for element {element_id}: {result.get('transparency')}%")
        return result
    
    def test_show_all_elements(self):
        """Test show_all_elements - Alle Elemente sichtbar machen"""
        result = asyncio.run(self.controller.show_all_elements())
        assert_ok(result)
        assert_has_key(result, "message")
        self.log(f"Show all elements: {result.get('message')}")
        return result
    
    def test_hide_all_elements(self):
        """Test hide_all_elements - Alle Elemente ausblenden"""
        result = asyncio.run(self.controller.hide_all_elements())
        assert_ok(result)
        assert_has_key(result, "message")
        self.log(f"Hide all elements: {result.get('message')}")
        return result
    
    def test_refresh_display(self):
        """Test refresh_display - Display aktualisieren"""
        result = asyncio.run(self.controller.refresh_display())
        assert_ok(result)
        assert_has_key(result, "message")
        self.log(f"Refresh display: {result.get('message')}")
        return result
    
    def test_get_visible_element_count(self):
        """Test get_visible_element_count - Anzahl sichtbarer Elemente"""
        result = asyncio.run(self.controller.get_visible_element_count())
        assert_ok(result)
        assert_has_key(result, "visible_elements")
        assert_has_key(result, "total_elements")
        self.log(f"Visible elements: {result.get('visible_elements')}/{result.get('total_elements')}")
        return result
    
    def test_visualization_workflow(self):
        """Test kompletter Visualization-Workflow"""
        element_id = self.get_test_element()
        if not element_id:
            return {"status": "skip", "message": "No test element available"}
        
        # 1. Farbe setzen
        color_result = asyncio.run(self.controller.set_color([element_id], 6))  # Gelb
        assert_ok(color_result)
        
        # 2. Transparenz setzen  
        transparency_result = asyncio.run(self.controller.set_transparency([element_id], 30))
        assert_ok(transparency_result)
        
        # 3. Element verstecken
        hide_result = asyncio.run(self.controller.set_visibility([element_id], False))
        assert_ok(hide_result)
        
        # 4. Element wieder zeigen
        show_result = asyncio.run(self.controller.set_visibility([element_id], True))
        assert_ok(show_result)
        
        # 5. Display aktualisieren
        refresh_result = asyncio.run(self.controller.refresh_display())
        assert_ok(refresh_result)
        
        self.log("Complete visualization workflow tested successfully")
        return {
            "color": color_result,
            "transparency": transparency_result,
            "hide": hide_result,
            "show": show_result,
            "refresh": refresh_result
        }

if __name__ == "__main__":
    # Run tests
    suite = VisualizationControllerTests()
    summary = suite.run_all_tests()
    
    print(f"\n{summary['suite_name']}: {summary['passed']}/{summary['total_tests']} passed ({summary['success_rate']:.1f}%)")
    if summary['failed'] > 0:
        print("Failed tests:")
        for result in summary['results']:
            if not result.success:
                print(f"  - {result.test_name}: {result.message}")
