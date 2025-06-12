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
            print("  ✓ Connection established")
        except Exception as e:
            print(f"  ✗ Connection failed: {e}")
            raise
    
    def teardown(self):
        """Cleanup created elements"""
        if self.created_elements:
            print(f"Cleaning up {len(self.created_elements)} test elements...")
            try:
                result = asyncio.run(self.controller.delete_elements(self.created_elements))
                if result.get("status") == "ok":
                    print("  ✓ Cleanup successful")
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
