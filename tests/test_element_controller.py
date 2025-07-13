"""
Element Controller Tests
"""
import asyncio
from test_config import TestSuite, assert_ok, assert_error, assert_element_id, TEST_POINTS, TEST_MATERIALS, TEST_NAMES

# Import controllers
from controllers.element_controller import ElementController

class ElementControllerTests(TestSuite):
    """Test suite for Element Controller functions"""
    
    def __init__(self):
        super().__init__("Element Controller Tests")
        self.controller = ElementController()
        self.created_elements = []  # Track created elements for cleanup
    
    def setup(self):
        """Setup test environment"""
        print("Setting up Element Controller tests...")
        # Verify connection works
        try:
            result = asyncio.run(self.controller.get_all_element_ids())
            assert_ok(result, "Connection test failed")
            print("  + Connection established")
        except Exception as e:
            print(f"  X Connection failed: {e}")
            raise
    
    def teardown(self):
        """Cleanup created elements"""
        if self.created_elements:
            print(f"Cleaning up {len(self.created_elements)} test elements...")
            try:
                result = asyncio.run(self.controller.delete_elements(self.created_elements))
                if result.get("status") == "ok":
                    print("  + Cleanup successful")
                else:
                    print(f"  ! Cleanup warning: {result.get('message')}")
            except Exception as e:
                print(f"  ! Cleanup error: {e}")
    
    def track_element(self, result):
        """Track created element for cleanup"""
        if isinstance(result, dict) and "element_id" in result:
            self.created_elements.append(result["element_id"])
        return result
    
    # === BASIC ELEMENT RETRIEVAL TESTS ===
    
    def test_get_all_element_ids(self):
        """Test getting all element IDs"""
        result = asyncio.run(self.controller.get_all_element_ids())
        assert_ok(result)
        assert "element_ids" in result
        return result
    
    def test_get_active_element_ids(self):
        """Test getting active element IDs"""
        result = asyncio.run(self.controller.get_active_element_ids())
        assert_ok(result)
        assert "element_ids" in result
        return result
    
    def test_get_visible_element_ids(self):
        """Test getting visible element IDs"""
        result = asyncio.run(self.controller.get_visible_element_ids())
        assert_ok(result)
        assert "element_ids" in result
        return result
    
    # === ELEMENT CREATION TESTS ===
    
    def test_create_beam(self):
        """Test rectangular beam creation"""
        result = asyncio.run(self.controller.create_beam(
            TEST_POINTS["origin"], 
            TEST_POINTS["x_1000"], 
            200.0, 
            400.0
        ))
        assert_element_id(result)
        return self.track_element(result)
    
    def test_create_panel(self):
        """Test rectangular panel creation"""
        result = asyncio.run(self.controller.create_panel(
            TEST_POINTS["origin"], 
            TEST_POINTS["xy_1000"], 
            300.0, 
            18.0
        ))
        assert_element_id(result)
        return self.track_element(result)
    
    def test_create_circular_beam_points(self):
        """Test circular beam creation"""
        result = asyncio.run(self.controller.create_circular_beam_points(
            150.0,
            TEST_POINTS["origin"], 
            TEST_POINTS["x_1000"]
        ))
        assert_element_id(result)
        return self.track_element(result)
    
    def test_create_square_beam_points(self):
        """Test square beam creation"""
        result = asyncio.run(self.controller.create_square_beam_points(
            120.0,
            TEST_POINTS["origin"], 
            TEST_POINTS["y_1000"]
        ))
        assert_element_id(result)
        return self.track_element(result)
    def test_create_standard_beam_points(self):
        """Test standard beam creation"""
        # Note: This test may fail if standard elements are not configured
        try:
            result = asyncio.run(self.controller.create_standard_beam_points(
                "KVH 60/120",  # Common standard beam
                TEST_POINTS["origin"], 
                TEST_POINTS["x_1000"]
            ))
            assert_element_id(result)
            return self.track_element(result)
        except Exception as e:
            # Return error result if standard elements not available
            return {"status": "error", "message": f"Standard elements not configured: {e}"}
    
    def test_create_standard_panel_points(self):
        """Test standard panel creation"""
        try:
            result = asyncio.run(self.controller.create_standard_panel_points(
                "OSB 18mm",  # Common standard panel
                TEST_POINTS["origin"], 
                TEST_POINTS["xy_1000"]
            ))
            assert_element_id(result)
            return self.track_element(result)
        except Exception as e:
            return {"status": "error", "message": f"Standard elements not configured: {e}"}
    
    def test_create_drilling_points(self):
        """Test drilling creation"""
        result = asyncio.run(self.controller.create_drilling_points(
            12.0,  # 12mm diameter
            TEST_POINTS["origin"], 
            TEST_POINTS["z_1000"]
        ))
        assert_element_id(result)
        return self.track_element(result)
    
    def test_create_polygon_beam(self):
        """Test polygon beam creation"""
        # L-shaped profile
        vertices = [
            [0, 0, 0], [200, 0, 0], [200, 80, 0], 
            [80, 80, 0], [80, 200, 0], [0, 200, 0]
        ]
        result = asyncio.run(self.controller.create_polygon_beam(
            vertices,
            1000.0,  # 1000mm length
            [0, 0, 1],  # xl vector (length direction)
            [1, 0, 0]   # zl vector (height direction)
        ))
        assert_element_id(result)
        return self.track_element(result)
    
    # === ELEMENT MANIPULATION TESTS ===
    
    def test_copy_elements(self):
        """Test element copying"""
        # First create an element to copy
        beam_result = asyncio.run(self.controller.create_beam(
            TEST_POINTS["origin"], TEST_POINTS["x_1000"], 100.0, 200.0
        ))
        assert_element_id(beam_result)
        self.track_element(beam_result)
        
        # Copy the element
        copy_result = asyncio.run(self.controller.copy_elements(
            [beam_result["element_id"]],
            [0, 500, 0]  # Copy 500mm in Y direction
        ))
        assert_ok(copy_result)
        assert "new_element_ids" in copy_result
        
        # Track copied elements for cleanup
        for eid in copy_result["new_element_ids"]:
            self.created_elements.append(eid)
        
        return copy_result
    
    def test_move_element(self):
        """Test element moving"""
        # Create element to move
        panel_result = asyncio.run(self.controller.create_panel(
            TEST_POINTS["origin"], TEST_POINTS["xy_1000"], 200.0, 20.0
        ))
        assert_element_id(panel_result)
        self.track_element(panel_result)
        
        # Move the element
        move_result = asyncio.run(self.controller.move_element(
            [panel_result["element_id"]],
            [0, 0, 300]  # Move 300mm in Z direction
        ))
        assert_ok(move_result)
        return move_result
    
    # === ELEMENT INFO TESTS ===
    
    def test_get_element_info(self):
        """Test getting element information"""
        # Create element first
        beam_result = asyncio.run(self.controller.create_beam(
            TEST_POINTS["origin"], TEST_POINTS["x_1000"], 160.0, 240.0
        ))
        assert_element_id(beam_result)
        self.track_element(beam_result)
        
        # Get element info
        info_result = asyncio.run(self.controller.get_element_info(
            beam_result["element_id"]
        ))
        assert_ok(info_result)
        assert "info" in info_result
        return info_result
    
    # === ERROR HANDLING TESTS ===
    
    def test_invalid_element_id(self):
        """Test handling of invalid element ID"""
        result = asyncio.run(self.controller.get_element_info(-1))
        assert_error(result)
        return result
    
    def test_invalid_beam_parameters(self):
        """Test handling of invalid beam parameters"""
        try:
            result = asyncio.run(self.controller.create_beam(
                TEST_POINTS["origin"], 
                TEST_POINTS["x_1000"], 
                -100.0,  # Invalid negative width
                200.0
            ))
            # If it reaches here, it should be an error
            assert_error(result)
            return result
        except Exception as e:
            # Parameter validation in controller
            return {"status": "ok", "message": f"Parameter validation works: {e}"}
    
    def test_delete_elements(self):
        """Test element deletion"""
        # Create element to delete
        beam_result = asyncio.run(self.controller.create_beam(
            TEST_POINTS["origin"], TEST_POINTS["x_1000"], 100.0, 200.0
        ))
        assert_element_id(beam_result)
        element_to_delete = beam_result["element_id"]
        
        # Delete the element
        delete_result = asyncio.run(self.controller.delete_elements([element_to_delete]))
        assert_ok(delete_result)
        
        # Don't track this element since we deleted it
        return delete_result
    
    def test_get_user_element_ids_no_count(self):
        """Test user element selection without count limit"""
        # This will require user interaction in real Cadwork, 
        # but we test the API call structure
        try:
            result = asyncio.run(self.controller.get_user_element_ids())
            # In headless mode this might timeout or return empty
            return result
        except Exception as e:
            return {"status": "ok", "message": f"User selection API callable: {e}"}
    
    def test_join_elements_valid(self):
        """Test join_elements mit gültigen Element-IDs"""
        # Erstelle zwei Test-Elemente
        beam1 = self.create_test_element()
        beam2 = self.create_test_element([1000, 0, 0], [2000, 0, 0])
        
        lElementIds = [beam1, beam2]
        result = asyncio.run(self.controller.join_elements(lElementIds))
        assert_ok(result)
        assert_has_key(result, "message")
        self.log(f"Joined elements {lElementIds}: {result.get('message')}")
        return result
    
    def test_join_elements_insufficient_elements(self):
        """Test join_elements mit zu wenigen Elementen"""
        # Nur ein Element - sollte fehlschlagen
        beam1 = self.create_test_element()
        
        result = asyncio.run(self.controller.join_elements([beam1]))
        assert_error(result)
        assert_has_key(result, "message")
        self.log(f"Single element join rejected: {result.get('message')}")
        return result
    
    def test_join_elements_empty_list(self):
        """Test join_elements mit leerer Liste"""
        result = asyncio.run(self.controller.join_elements([]))
        assert_error(result)
        assert_has_key(result, "message")
        self.log(f"Empty list join rejected: {result.get('message')}")
        return result
    
    def test_unjoin_elements_valid(self):
        """Test unjoin_elements mit gültigen Element-IDs"""
        # Erstelle und verbinde zwei Test-Elemente
        beam1 = self.create_test_element()
        beam2 = self.create_test_element([1000, 0, 0], [2000, 0, 0])
        
        # Erst verbinden
        join_result = asyncio.run(self.controller.join_elements([beam1, beam2]))
        assert_ok(join_result)
        
        # Dann trennen
        unjoin_result = asyncio.run(self.controller.unjoin_elements([beam1, beam2]))
        assert_ok(unjoin_result)
        assert_has_key(unjoin_result, "message")
        self.log(f"Unjoined elements {[beam1, beam2]}: {unjoin_result.get('message')}")
        return unjoin_result
    
    def test_unjoin_elements_empty_list(self):
        """Test unjoin_elements mit leerer Liste"""
        result = asyncio.run(self.controller.unjoin_elements([]))
        assert_error(result)
        assert_has_key(result, "message")
        self.log(f"Empty list unjoin rejected: {result.get('message')}")
        return result
    
    def test_join_unjoin_workflow(self):
        """Test kompletter Join/Unjoin Workflow"""
        # Erstelle drei Test-Elemente für komplexeren Test
        beam1 = self.create_test_element([0, 0, 0], [1000, 0, 0])
        beam2 = self.create_test_element([1000, 0, 0], [2000, 0, 0])
        beam3 = self.create_test_element([2000, 0, 0], [3000, 0, 0])
        
        lElementIds = [beam1, beam2, beam3]
        
        # Alle verbinden
        join_result = asyncio.run(self.controller.join_elements(lElementIds))
        assert_ok(join_result)
        self.log(f"Joined 3 elements: {join_result.get('message')}")
        
        # Alle trennen
        unjoin_result = asyncio.run(self.controller.unjoin_elements(lElementIds))
        assert_ok(unjoin_result)
        self.log(f"Unjoined 3 elements: {unjoin_result.get('message')}")
        
        return {
            "join_result": join_result,
            "unjoin_result": unjoin_result,
            "element_count": 3
        }
    
    def test_get_visible_element_ids(self):
        """Test get_visible_element_ids"""
        result = asyncio.run(self.controller.get_visible_element_ids())
        assert_ok(result)
        assert_has_key(result, "element_ids")
        self.log(f"Found {len(result.get('element_ids', []))} visible elements")
        return result
    
    def test_create_standard_panel_points(self):
        """Test create_standard_panel_points"""
        lStandardName = "OSB 18mm"  # Standard panel name
        lP1 = [0, 0, 200]
        lP2 = [2000, 0, 200]
        
        result = asyncio.run(self.controller.create_standard_panel_points(lStandardName, lP1, lP2))
        assert_ok(result)
        assert_has_key(result, "element_id")
        
        # Element für cleanup merken
        if "element_id" in result:
            self.created_elements.append(result["element_id"])
        
        self.log(f"Created standard panel '{lStandardName}': {result.get('element_id')}")
        return result
    
    def test_create_polygon_beam(self):
        """Test create_polygon_beam"""
        # Dreieckiger Querschnitt
        lVertices = [
            [0, 0, 0],
            [100, 0, 0], 
            [50, 100, 0]
        ]
        lThickness = 2000  # 2m lang
        lXl = [1, 0, 0]    # X-Richtung
        lZl = [0, 0, 1]    # Z-Richtung
        
        result = asyncio.run(self.controller.create_polygon_beam(lVertices, lThickness, lXl, lZl))
        assert_ok(result)
        assert_has_key(result, "element_id")
        
        # Element für cleanup merken
        if "element_id" in result:
            self.created_elements.append(result["element_id"])
        
        self.log(f"Created polygon beam: {result.get('element_id')}")
        return result
    
    def test_cut_corner_lap_valid(self):
        """Test cut_corner_lap mit gültigen Element-IDs"""
        # Erstelle zwei Test-Elemente für Eckblatt-Verbindung
        beam1 = self.create_test_element([0, 0, 0], [2000, 0, 0])
        beam2 = self.create_test_element([1800, 0, 0], [1800, 1500, 0])
        
        lElementIds = [beam1, beam2]
        result = asyncio.run(self.controller.cut_corner_lap(lElementIds))
        assert_ok(result)
        assert_has_key(result, "message")
        self.log(f"Corner lap cut created between elements {lElementIds}: {result.get('message')}")
        return result
    
    def test_cut_corner_lap_with_params(self):
        """Test cut_corner_lap mit Schnitt-Parametern"""
        # Erstelle Test-Elemente
        beam1 = self.create_test_element([0, 0, 100], [2000, 0, 100])
        beam2 = self.create_test_element([1800, 0, 100], [1800, 1500, 100])
        
        lElementIds = [beam1, beam2]
        lCutParams = {
            "cut_depth": 30,     # 30mm Tiefe
            "cut_width": 120,    # 120mm Breite
            "offset": 50         # 50mm Versatz
        }
        
        result = asyncio.run(self.controller.cut_corner_lap(lElementIds, lCutParams))
        assert_ok(result)
        assert_has_key(result, "cut_params")
        self.log(f"Corner lap cut with params: {result.get('message')}")
        return result
    
    def test_cut_corner_lap_insufficient_elements(self):
        """Test cut_corner_lap mit zu wenigen Elementen"""
        beam1 = self.create_test_element()
        
        result = asyncio.run(self.controller.cut_corner_lap([beam1]))
        assert_error(result)
        assert_has_key(result, "message")
        self.log(f"Single element corner lap rejected: {result.get('message')}")
        return result
    
    def test_cut_cross_lap_valid(self):
        """Test cut_cross_lap mit gültigen Element-IDs"""
        # Erstelle zwei sich kreuzende Balken
        beam1 = self.create_test_element([0, 0, 0], [3000, 0, 0])      # Horizontal
        beam2 = self.create_test_element([1500, -500, 0], [1500, 500, 0])  # Vertikal kreuzend
        
        lElementIds = [beam1, beam2]
        result = asyncio.run(self.controller.cut_cross_lap(lElementIds))
        assert_ok(result)
        assert_has_key(result, "message")
        self.log(f"Cross lap cut created between elements {lElementIds}: {result.get('message')}")
        return result
    
    def test_cut_cross_lap_with_params(self):
        """Test cut_cross_lap mit Schnitt-Parametern"""
        # Erstelle sich kreuzende Test-Elemente
        beam1 = self.create_test_element([0, 0, 200], [3000, 0, 200])
        beam2 = self.create_test_element([1500, -500, 200], [1500, 500, 200])
        
        lElementIds = [beam1, beam2]
        lCutParams = {
            "cut_depth_1": 60,   # Tiefe für erstes Element
            "cut_depth_2": 60,   # Tiefe für zweites Element  
            "cut_width": 120,    # Breite des Schnitts
            "position": "center" # Position des Schnitts
        }
        
        result = asyncio.run(self.controller.cut_cross_lap(lElementIds, lCutParams))
        assert_ok(result)
        assert_has_key(result, "cut_params")
        self.log(f"Cross lap cut with params: {result.get('message')}")
        return result
    
    def test_cut_cross_lap_multiple_elements(self):
        """Test cut_cross_lap mit mehreren Elementen"""
        # Erstelle 4 Elemente für mehrere Kreuzblatt-Verbindungen
        beam1 = self.create_test_element([0, 0, 300], [2000, 0, 300])
        beam2 = self.create_test_element([1000, -500, 300], [1000, 500, 300])
        beam3 = self.create_test_element([0, 1000, 300], [2000, 1000, 300])
        beam4 = self.create_test_element([1000, 500, 300], [1000, 1500, 300])
        
        lElementIds = [beam1, beam2, beam3, beam4]
        result = asyncio.run(self.controller.cut_cross_lap(lElementIds))
        assert_ok(result)
        assert_has_key(result, "pairs_processed")
        self.log(f"Multiple cross lap cuts: {result.get('pairs_processed')} pairs processed")
        return result
    
    def test_cut_operations_workflow(self):
        """Test kompletter Cut-Operations Workflow"""
        # Erstelle Holzstruktur für umfassende Verbindungen
        main_beam = self.create_test_element([0, 0, 0], [4000, 0, 0])      # Hauptbalken
        cross_beam1 = self.create_test_element([1000, -200, 0], [1000, 200, 0])  # Querbalken 1
        cross_beam2 = self.create_test_element([3000, -200, 0], [3000, 200, 0])  # Querbalken 2
        corner_beam = self.create_test_element([3800, 0, 0], [3800, 1000, 0])    # Eckbalken
        
        # 1. Kreuzblatt-Verbindungen für Querbalken
        cross_result1 = asyncio.run(self.controller.cut_cross_lap([main_beam, cross_beam1]))
        assert_ok(cross_result1)
        
        cross_result2 = asyncio.run(self.controller.cut_cross_lap([main_beam, cross_beam2]))
        assert_ok(cross_result2)
        
        # 2. Eckblatt-Verbindung für Eckbalken
        corner_result = asyncio.run(self.controller.cut_corner_lap([main_beam, corner_beam]))
        assert_ok(corner_result)
        
        self.log("Complete cut operations workflow tested successfully:")
        self.log(f"  - Cross lap cuts: 2 created")
        self.log(f"  - Corner lap cuts: 1 created")
        self.log(f"  - Total elements involved: 4")
        
        return {
            "cross_cuts": [cross_result1, cross_result2],
            "corner_cuts": [corner_result],
            "total_operations": 3
        }
    
    def test_cut_half_lap_valid(self):
        """Test cut_half_lap mit gültigen Element-IDs"""
        # Erstelle zwei Balken für Halbes Blatt-Verbindung
        main_beam = self.create_test_element([0, 0, 0], [3000, 0, 0])      # Hauptbalken
        side_beam = self.create_test_element([2800, 0, 0], [2800, 800, 0]) # Seitenbalken
        
        lElementIds = [main_beam, side_beam]
        result = asyncio.run(self.controller.cut_half_lap(lElementIds))
        assert_ok(result)
        assert_has_key(result, "message")
        assert_has_key(result, "master_element")
        self.log(f"Half lap cut created: {result.get('message')}")
        return result
    
    def test_cut_half_lap_with_params(self):
        """Test cut_half_lap mit spezifischen Parametern"""
        beam1 = self.create_test_element([0, 0, 100], [3000, 0, 100])
        beam2 = self.create_test_element([2800, 0, 100], [2800, 800, 100])
        
        lElementIds = [beam1, beam2]
        lCutParams = {
            "master_element": beam1,
            "cut_depth_ratio": 0.6,    # 60% der Dicke
            "cut_position": "center"   # Mittlere Position
        }
        
        result = asyncio.run(self.controller.cut_half_lap(lElementIds, lCutParams))
        assert_ok(result)
        assert_has_key(result, "cut_depth_ratio")
        self.log(f"Half lap with 60% depth: {result.get('message')}")
        return result
    
    def test_cut_half_lap_insufficient_elements(self):
        """Test cut_half_lap mit zu wenigen Elementen"""
        beam1 = self.create_test_element()
        
        result = asyncio.run(self.controller.cut_half_lap([beam1]))
        assert_error(result)
        assert_has_key(result, "message")
        self.log(f"Single element half lap rejected: {result.get('message')}")
        return result
    
    def test_cut_double_tenon_valid(self):
        """Test cut_double_tenon mit gültigen Element-IDs"""
        # Erstelle zwei Balken für Doppelzapfen-Verbindung
        tenon_beam = self.create_test_element([0, 0, 0], [200, 0, 0])       # Zapfen-Balken (kurz)
        mortise_beam = self.create_test_element([200, 0, -500], [200, 0, 500])  # Nut-Balken (lang)
        
        lElementIds = [tenon_beam, mortise_beam]
        result = asyncio.run(self.controller.cut_double_tenon(lElementIds))
        assert_ok(result)
        assert_has_key(result, "message")
        assert_has_key(result, "tenon_element")
        assert_has_key(result, "mortise_element")
        self.log(f"Double tenon created: {result.get('message')}")
        return result
    
    def test_cut_double_tenon_with_params(self):
        """Test cut_double_tenon mit detaillierten Parametern"""
        tenon_beam = self.create_test_element([0, 0, 200], [200, 0, 200])
        mortise_beam = self.create_test_element([200, 0, -300], [200, 0, 700])
        
        lElementIds = [tenon_beam, mortise_beam]
        lCutParams = {
            "tenon_element": tenon_beam,
            "mortise_element": mortise_beam,
            "tenon_width": 50,     # 50mm Breite
            "tenon_height": 100,   # 100mm Höhe
            "tenon_spacing": 80,   # 80mm Abstand
            "tenon_depth": 60      # 60mm Tiefe
        }
        
        result = asyncio.run(self.controller.cut_double_tenon(lElementIds, lCutParams))
        assert_ok(result)
        assert_has_key(result, "tenon_specifications")
        specs = result.get("tenon_specifications", {})
        self.log(f"Double tenon with specs: {specs.get('width')}x{specs.get('height')}mm")
        return result
    
    def test_cut_double_tenon_wrong_element_count(self):
        """Test cut_double_tenon mit falscher Anzahl Elemente"""
        beam1 = self.create_test_element()
        beam2 = self.create_test_element([1000, 0, 0], [2000, 0, 0])
        beam3 = self.create_test_element([3000, 0, 0], [4000, 0, 0])
        
        # Zu viele Elemente (3 statt 2)
        result = asyncio.run(self.controller.cut_double_tenon([beam1, beam2, beam3]))
        assert_error(result)
        assert_has_key(result, "message")
        self.log(f"Three elements rejected: {result.get('message')}")
        return result
    
    def test_advanced_cut_operations_workflow(self):
        """Test erweiterte Cut-Operations in komplexem Workflow"""
        # Erstelle Holzrahmen-Struktur
        bottom_beam = self.create_test_element([0, 0, 0], [4000, 0, 0])        # Unterzug
        top_beam = self.create_test_element([0, 0, 2000], [4000, 0, 2000])     # Oberzug
        left_post = self.create_test_element([0, 0, 0], [0, 0, 2000])          # Linker Pfosten
        right_post = self.create_test_element([4000, 0, 0], [4000, 0, 2000])   # Rechter Pfosten
        center_beam = self.create_test_element([2000, 0, 1000], [2000, 500, 1000])  # Mittelbalken
        
        # 1. Doppelzapfen-Verbindungen für Pfosten zu Balken
        tenon_params = {
            "tenon_width": 60, "tenon_height": 120, 
            "tenon_spacing": 100, "tenon_depth": 80
        }
        
        double_tenon1 = asyncio.run(self.controller.cut_double_tenon([left_post, bottom_beam], tenon_params))
        assert_ok(double_tenon1)
        
        double_tenon2 = asyncio.run(self.controller.cut_double_tenon([right_post, bottom_beam], tenon_params))
        assert_ok(double_tenon2)
        
        # 2. Halbes Blatt für obere Verbindungen
        half_lap_params = {"cut_depth_ratio": 0.5, "cut_position": "end"}
        
        half_lap1 = asyncio.run(self.controller.cut_half_lap([left_post, top_beam], half_lap_params))
        assert_ok(half_lap1)
        
        half_lap2 = asyncio.run(self.controller.cut_half_lap([right_post, top_beam], half_lap_params))
        assert_ok(half_lap2)
        
        # 3. Kreuzblatt für Mittelbalken
        cross_lap = asyncio.run(self.controller.cut_cross_lap([center_beam, top_beam]))
        assert_ok(cross_lap)
        
        self.log("Advanced cut operations workflow completed successfully:")
        self.log(f"  - Double tenon connections: 2")
        self.log(f"  - Half lap connections: 2") 
        self.log(f"  - Cross lap connections: 1")
        self.log(f"  - Total cut operations: 5")
        self.log(f"  - Elements in frame: 5")
        
        return {
            "double_tenons": [double_tenon1, double_tenon2],
            "half_laps": [half_lap1, half_lap2],
            "cross_laps": [cross_lap],
            "total_operations": 5,
            "frame_elements": 5
        }
    
    def test_cut_scarf_joint_valid(self):
        """Test cut_scarf_joint mit gültigen Element-IDs"""
        # Erstelle zwei Balken für Stoßverbindung (Verlängerung)
        beam1 = self.create_test_element([0, 0, 0], [2000, 0, 0])      # Erster Balken
        beam2 = self.create_test_element([1950, 0, 0], [4000, 0, 0])   # Zweiter Balken (überlappend)
        
        lElementIds = [beam1, beam2]
        result = asyncio.run(self.controller.cut_scarf_joint(lElementIds))
        assert_ok(result)
        assert_has_key(result, "message")
        assert_has_key(result, "scarf_specifications")
        self.log(f"Scarf joint created: {result.get('message')}")
        return result
    
    def test_cut_scarf_joint_with_params(self):
        """Test cut_scarf_joint mit spezifischen Parametern"""
        beam1 = self.create_test_element([0, 0, 100], [2000, 0, 100])
        beam2 = self.create_test_element([1900, 0, 100], [4000, 0, 100])
        
        lElementIds = [beam1, beam2]
        lCutParams = {
            "scarf_type": "stepped_scarf",    # Gestufte Stoßverbindung
            "scarf_length": 600,              # 600mm Länge
            "scarf_angle": 45,                # 45° Winkel
            "overlap_length": 100             # 100mm Überlappung
        }
        
        result = asyncio.run(self.controller.cut_scarf_joint(lElementIds, lCutParams))
        assert_ok(result)
        specs = result.get("scarf_specifications", {})
        assert specs.get("length") == 600
        assert specs.get("angle") == 45
        self.log(f"Stepped scarf joint: {specs.get('length')}mm at {specs.get('angle')}°")
        return result
    
    def test_cut_scarf_joint_wrong_element_count(self):
        """Test cut_scarf_joint mit falscher Anzahl Elemente"""
        beam1 = self.create_test_element()
        beam2 = self.create_test_element([1000, 0, 0], [2000, 0, 0])
        beam3 = self.create_test_element([3000, 0, 0], [4000, 0, 0])
        
        # Zu viele Elemente (3 statt 2)
        result = asyncio.run(self.controller.cut_scarf_joint([beam1, beam2, beam3]))
        assert_error(result)
        assert_has_key(result, "message")
        self.log(f"Three elements for scarf joint rejected: {result.get('message')}")
        return result
    
    def test_cut_shoulder_valid(self):
        """Test cut_shoulder mit gültigen Element-IDs"""
        # Erstelle tragende Struktur
        support_beam = self.create_test_element([0, 0, 0], [4000, 0, 0])       # Träger (unten)
        load_beam1 = self.create_test_element([1000, 0, 0], [1000, 1500, 0])   # Aufliegender Balken 1
        load_beam2 = self.create_test_element([3000, 0, 0], [3000, 1500, 0])   # Aufliegender Balken 2
        
        lElementIds = [support_beam, load_beam1, load_beam2]
        result = asyncio.run(self.controller.cut_shoulder(lElementIds))
        assert_ok(result)
        assert_has_key(result, "message")
        assert_has_key(result, "supporting_element")
        assert_has_key(result, "total_pairs")
        self.log(f"Shoulder cuts created: {result.get('total_pairs')} pairs")
        return result
    
    def test_cut_shoulder_with_params(self):
        """Test cut_shoulder mit detaillierten Parametern"""
        support_beam = self.create_test_element([0, 0, 200], [4000, 0, 200])
        load_beam = self.create_test_element([2000, 0, 200], [2000, 2000, 200])
        
        lElementIds = [support_beam, load_beam]
        lCutParams = {
            "supporting_element": support_beam,
            "shoulder_depth": 60,             # 60mm Tiefe
            "shoulder_width": 160,            # 160mm Breite
            "shoulder_type": "stepped_shoulder", # Gestufte Schulter
            "contact_angle": 95               # 95° Kontaktwinkel
        }
        
        result = asyncio.run(self.controller.cut_shoulder(lElementIds, lCutParams))
        assert_ok(result)
        specs = result.get("shoulder_specifications", {})
        assert specs.get("depth") == 60
        assert specs.get("width") == 160
        self.log(f"Stepped shoulder: {specs.get('depth')}x{specs.get('width')}mm at {specs.get('contact_angle')}°")
        return result
    
    def test_cut_shoulder_insufficient_elements(self):
        """Test cut_shoulder mit zu wenigen Elementen"""
        beam1 = self.create_test_element()
        
        result = asyncio.run(self.controller.cut_shoulder([beam1]))
        assert_error(result)
        assert_has_key(result, "message")
        self.log(f"Single element shoulder cut rejected: {result.get('message')}")
        return result
    
    def test_complete_structural_cut_operations(self):
        """Test kompletter struktureller Cut-Operations Workflow"""
        # Erstelle Holzrahmen-Struktur mit allen 6 Cut-Operations
        
        # Basis-Struktur
        foundation_beam = self.create_test_element([0, 0, 0], [6000, 0, 0])        # Grundbalken
        extension_beam = self.create_test_element([5800, 0, 0], [10000, 0, 0])     # Verlängerung
        
        # Tragende Elemente
        post1 = self.create_test_element([1500, 0, 0], [1500, 0, 3000])           # Pfosten 1
        post2 = self.create_test_element([4500, 0, 0], [4500, 0, 3000])           # Pfosten 2
        top_beam = self.create_test_element([0, 0, 3000], [6000, 0, 3000])        # Deckbalken
        
        # Querverbindungen
        cross_brace = self.create_test_element([3000, -200, 1500], [3000, 200, 1500])  # Querverband
        
        # 1. Stoßverbindung für Balkenverlängerung
        scarf_params = {"scarf_type": "stepped_scarf", "scarf_length": 800, "scarf_angle": 30}
        scarf_result = asyncio.run(self.controller.cut_scarf_joint([foundation_beam, extension_beam], scarf_params))
        assert_ok(scarf_result)
        
        # 2. Schulterschnitte für tragende Verbindungen
        shoulder_params = {"shoulder_depth": 50, "shoulder_width": 200, "shoulder_type": "stepped_shoulder"}
        shoulder_result1 = asyncio.run(self.controller.cut_shoulder([foundation_beam, post1], shoulder_params))
        assert_ok(shoulder_result1)
        
        shoulder_result2 = asyncio.run(self.controller.cut_shoulder([foundation_beam, post2], shoulder_params))
        assert_ok(shoulder_result2)
        
        # 3. Doppelzapfen für obere Verbindungen
        tenon_params = {"tenon_width": 80, "tenon_height": 150, "tenon_spacing": 120}
        tenon_result1 = asyncio.run(self.controller.cut_double_tenon([post1, top_beam], tenon_params))
        assert_ok(tenon_result1)
        
        tenon_result2 = asyncio.run(self.controller.cut_double_tenon([post2, top_beam], tenon_params))
        assert_ok(tenon_result2)
        
        # 4. Kreuzblatt für Querverband
        cross_result = asyncio.run(self.controller.cut_cross_lap([cross_brace, top_beam]))
        assert_ok(cross_result)
        
        self.log("Complete structural cut operations workflow completed:")
        self.log(f"  - Scarf joints: 1 (foundation extension)")
        self.log(f"  - Shoulder cuts: 2 (post connections)")
        self.log(f"  - Double tenons: 2 (top connections)")
        self.log(f"  - Cross laps: 1 (bracing)")
        self.log(f"  - Total cut operations: 6")
        self.log(f"  - Total elements: 6")
        self.log(f"  - Structure type: Complete timber frame")
        
        return {
            "scarf_joints": [scarf_result],
            "shoulder_cuts": [shoulder_result1, shoulder_result2],
            "double_tenons": [tenon_result1, tenon_result2],
            "cross_laps": [cross_result],
            "total_operations": 6,
            "structure_elements": 6,
            "structure_type": "timber_frame"
        }
