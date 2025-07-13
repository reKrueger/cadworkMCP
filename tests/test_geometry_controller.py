"""
Geometry Controller Tests
"""
import asyncio
from test_config import TestSuite, assert_ok, assert_error, TEST_POINTS

# Import controllers
from controllers.geometry_controller import GeometryController
from controllers.element_controller import ElementController

class GeometryControllerTests(TestSuite):
    """Test suite for Geometry Controller functions"""
    
    def __init__(self):
        super().__init__("Geometry Controller Tests")
        self.geometry_ctrl = GeometryController()
        self.element_ctrl = ElementController()
        self.test_element_id = None
        self.test_elements = []
    
    def setup(self):
        """Setup test environment with test elements"""
        print("Setting up Geometry Controller tests...")
        try:
            # Create a test beam for geometry operations
            result = asyncio.run(self.element_ctrl.create_beam(
                TEST_POINTS["origin"], 
                TEST_POINTS["x_1000"], 
                200.0, 
                400.0
            ))
            if result.get("status") == "ok" and "element_id" in result:
                self.test_element_id = result["element_id"]
                self.test_elements.append(self.test_element_id)
                print(f"  + Created test element {self.test_element_id}")
            else:
                raise Exception(f"Failed to create test element: {result}")
                
            # Create second element for distance tests
            result2 = asyncio.run(self.element_ctrl.create_beam(
                [2000, 0, 0], 
                [3000, 0, 0], 
                150.0, 
                300.0
            ))
            if result2.get("status") == "ok" and "element_id" in result2:
                self.test_elements.append(result2["element_id"])
                print(f"  + Created second test element {result2['element_id']}")
                
        except Exception as e:
            print(f"  X Setup failed: {e}")
            raise
    
    def teardown(self):
        """Cleanup test elements"""
        if self.test_elements:
            print(f"Cleaning up {len(self.test_elements)} geometry test elements...")
            try:
                result = asyncio.run(self.element_ctrl.delete_elements(self.test_elements))
                if result.get("status") == "ok":
                    print("  + Geometry cleanup successful")
                else:
                    print(f"  ! Geometry cleanup warning: {result.get('message')}")
            except Exception as e:
                print(f"  ! Geometry cleanup error: {e}")
    
    # === BASIC DIMENSION TESTS ===
    
    def test_get_element_width(self):
        """Test getting element width"""
        result = asyncio.run(self.geometry_ctrl.get_element_width(self.test_element_id))
        assert_ok(result)
        assert "width" in result
        # Should be 200.0 from setup
        expected_width = 200.0
        actual_width = result["width"]
        if abs(actual_width - expected_width) > 0.1:
            raise AssertionError(f"Expected width {expected_width}, got {actual_width}")
        return result
    
    def test_get_element_height(self):
        """Test getting element height"""
        result = asyncio.run(self.geometry_ctrl.get_element_height(self.test_element_id))
        assert_ok(result)
        assert "height" in result
        # Should be 400.0 from setup
        expected_height = 400.0
        actual_height = result["height"]
        if abs(actual_height - expected_height) > 0.1:
            raise AssertionError(f"Expected height {expected_height}, got {actual_height}")
        return result
    
    def test_get_element_length(self):
        """Test getting element length"""
        result = asyncio.run(self.geometry_ctrl.get_element_length(self.test_element_id))
        assert_ok(result)
        assert "length" in result
        # Should be 1000.0 from setup (distance between origin and x_1000)
        expected_length = 1000.0
        actual_length = result["length"]
        if abs(actual_length - expected_length) > 0.1:
            raise AssertionError(f"Expected length {expected_length}, got {actual_length}")
        return result
    
    def test_get_element_volume(self):
        """Test getting element volume"""
        result = asyncio.run(self.geometry_ctrl.get_element_volume(self.test_element_id))
        assert_ok(result)
        assert "volume" in result
        # Should be 200 * 400 * 1000 = 80,000,000 mm³
        expected_volume = 80000000.0
        actual_volume = result["volume"]
        if abs(actual_volume - expected_volume) > 1000.0:  # Allow 1000mm³ tolerance
            raise AssertionError(f"Expected volume ~{expected_volume}, got {actual_volume}")
        return result
    
    def test_get_element_weight(self):
        """Test getting element weight"""
        result = asyncio.run(self.geometry_ctrl.get_element_weight(self.test_element_id))
        assert_ok(result)
        assert "weight" in result
        # Weight depends on material density, just check it's positive
        weight = result["weight"]
        if weight <= 0:
            raise AssertionError(f"Expected positive weight, got {weight}")
        return result
    # === COORDINATE SYSTEM TESTS ===
    
    def test_get_element_xl(self):
        """Test getting XL vector (length direction)"""
        result = asyncio.run(self.geometry_ctrl.get_element_xl(self.test_element_id))
        assert_ok(result)
        assert "xl_vector" in result
        return result
    
    def test_get_element_yl(self):
        """Test getting YL vector (width direction)"""
        result = asyncio.run(self.geometry_ctrl.get_element_yl(self.test_element_id))
        assert_ok(result)
        assert "yl_vector" in result
        return result
    
    def test_get_element_zl(self):
        """Test getting ZL vector (height direction)"""
        result = asyncio.run(self.geometry_ctrl.get_element_zl(self.test_element_id))
        assert_ok(result)
        assert "zl_vector" in result
        return result
    
    def test_get_element_p1(self):
        """Test getting P1 point (start point)"""
        result = asyncio.run(self.geometry_ctrl.get_element_p1(self.test_element_id))
        assert_ok(result)
        assert "p1" in result
        # Should be close to origin from setup
        p1 = result["p1"]
        if not isinstance(p1, list) or len(p1) != 3:
            raise AssertionError(f"Expected [x,y,z] list, got {p1}")
        return result
    
    def test_get_element_p2(self):
        """Test getting P2 point (end point)"""
        result = asyncio.run(self.geometry_ctrl.get_element_p2(self.test_element_id))
        assert_ok(result)
        assert "p2" in result
        p2 = result["p2"]
        if not isinstance(p2, list) or len(p2) != 3:
            raise AssertionError(f"Expected [x,y,z] list, got {p2}")
        return result
    
    def test_get_element_p3(self):
        """Test getting P3 point (orientation point)"""
        result = asyncio.run(self.geometry_ctrl.get_element_p3(self.test_element_id))
        assert_ok(result)
        assert "p3" in result
        return result
    
    # === CENTER OF GRAVITY TESTS ===
    
    def test_get_center_of_gravity(self):
        """Test getting center of gravity for single element"""
        result = asyncio.run(self.geometry_ctrl.get_center_of_gravity(self.test_element_id))
        assert_ok(result)
        assert "center_of_gravity" in result
        cog = result["center_of_gravity"]
        if not isinstance(cog, list) or len(cog) != 3:
            raise AssertionError(f"Expected [x,y,z] list, got {cog}")
        return result
    
    def test_get_center_of_gravity_for_list(self):
        """Test getting combined center of gravity for multiple elements"""
        result = asyncio.run(self.geometry_ctrl.get_center_of_gravity_for_list(self.test_elements))
        assert_ok(result)
        assert "center_of_gravity" in result
        return result
    
    # === VERTICES AND GEOMETRY ANALYSIS ===
    
    def test_get_element_vertices(self):
        """Test getting element vertices"""
        result = asyncio.run(self.geometry_ctrl.get_element_vertices(self.test_element_id))
        assert_ok(result)
        assert "vertices" in result
        vertices = result["vertices"]
        if not isinstance(vertices, list):
            raise AssertionError(f"Expected list of vertices, got {type(vertices)}")
        # A beam should have 8 vertices (box shape)
        if len(vertices) < 4:  # At least 4 vertices for any 3D element
            raise AssertionError(f"Expected at least 4 vertices, got {len(vertices)}")
        return result
    
    def test_get_minimum_distance_between_elements(self):
        """Test getting minimum distance between elements"""
        if len(self.test_elements) < 2:
            return {"status": "error", "message": "Need at least 2 elements for distance test"}
        
        result = asyncio.run(self.geometry_ctrl.get_minimum_distance_between_elements(
            self.test_elements[0], 
            self.test_elements[1]
        ))
        assert_ok(result)
        assert "distance" in result
        distance = result["distance"]
        if distance < 0:
            raise AssertionError(f"Expected non-negative distance, got {distance}")
        return result
    
    # === SURFACE AREA TESTS ===
    
    def test_get_element_reference_face_area(self):
        """Test getting reference face area"""
        result = asyncio.run(self.geometry_ctrl.get_element_reference_face_area(self.test_element_id))
        assert_ok(result)
        assert "area" in result
        area = result["area"]
        if area <= 0:
            raise AssertionError(f"Expected positive area, got {area}")
        return result
    
    def test_get_total_area_of_all_faces(self):
        """Test getting total surface area"""
        result = asyncio.run(self.geometry_ctrl.get_total_area_of_all_faces(self.test_element_id))
        assert_ok(result)
        assert "total_area" in result
        total_area = result["total_area"]
        if total_area <= 0:
            raise AssertionError(f"Expected positive total area, got {total_area}")
        return result
    
    # === ERROR HANDLING TESTS ===
    
    def test_invalid_element_geometry(self):
        """Test geometry functions with invalid element ID"""
        result = asyncio.run(self.geometry_ctrl.get_element_width(-1))
        assert_error(result)
        return result
    
    # === TRANSFORMATION TESTS ===
    
    def test_rotate_elements(self):
        """Test element rotation"""
        if not self.test_elements:
            return {"status": "error", "message": "No test elements available"}
        
        result = asyncio.run(self.geometry_ctrl.rotate_elements(
            [self.test_element_id],
            [500, 0, 0],    # origin point
            [0, 0, 1],      # rotation axis (Z-axis)
            45.0            # 45 degrees
        ))
        assert_ok(result)
        return result
    
    def test_apply_global_scale(self):
        """Test global scaling"""
        if not self.test_elements:
            return {"status": "error", "message": "No test elements available"}
        
        result = asyncio.run(self.geometry_ctrl.apply_global_scale(
            [self.test_element_id],
            1.5,            # scale factor 1.5x
            [0, 0, 0]       # origin point
        ))
        assert_ok(result)
        return result
    
    def test_invert_model(self):
        """Test model inversion/mirroring"""
        if not self.test_elements:
            return {"status": "error", "message": "No test elements available"}
        
        result = asyncio.run(self.geometry_ctrl.invert_model([self.test_element_id]))
        assert_ok(result)
        return result
    
    def test_rotate_height_axis_90(self):
        """Test 90 degree height axis rotation"""
        if not self.test_elements:
            return {"status": "error", "message": "No test elements available"}
        
        result = asyncio.run(self.geometry_ctrl.rotate_height_axis_90([self.test_element_id]))
        assert_ok(result)
        return result
    
    def test_rotate_length_axis_90(self):
        """Test 90 degree length axis rotation"""  
        if not self.test_elements:
            return {"status": "error", "message": "No test elements available"}
        
        result = asyncio.run(self.geometry_ctrl.rotate_length_axis_90([self.test_element_id]))
        assert_ok(result)
        return result
    
    def test_get_element_facets(self):
        """Test getting element facets"""
        result = asyncio.run(self.geometry_ctrl.get_element_facets(self.test_element_id))
        assert_ok(result)
        assert "facets" in result
        return result
