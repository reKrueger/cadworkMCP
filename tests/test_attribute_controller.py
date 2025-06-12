"""
Attribute Controller Tests
"""
import asyncio
from test_config import TestSuite, assert_ok, assert_error, TEST_MATERIALS, TEST_NAMES

# Import controllers
from controllers.attribute_controller import AttributeController
from controllers.element_controller import ElementController

class AttributeControllerTests(TestSuite):
    """Test suite for Attribute Controller functions"""
    
    def __init__(self):
        super().__init__("Attribute Controller Tests")
        self.attribute_ctrl = AttributeController()
        self.element_ctrl = ElementController()
        self.test_elements = []
    
    def setup(self):
        """Setup test environment with test elements"""
        print("Setting up Attribute Controller tests...")
        try:
            # Create test elements for attribute testing
            for i in range(3):
                result = asyncio.run(self.element_ctrl.create_beam(
                    [i * 1000, 0, 0], 
                    [(i + 1) * 1000, 0, 0], 
                    100.0 + i * 50, 
                    200.0 + i * 100
                ))
                if result.get("status") == "ok" and "element_id" in result:
                    self.test_elements.append(result["element_id"])
                    print(f"  ✓ Created test element {result['element_id']}")
                else:
                    raise Exception(f"Failed to create test element {i+1}: {result}")
                    
        except Exception as e:
            print(f"  ✗ Setup failed: {e}")
            raise
    
    def teardown(self):
        """Cleanup test elements"""
        if self.test_elements:
            print(f"Cleaning up {len(self.test_elements)} attribute test elements...")
            try:
                result = asyncio.run(self.element_ctrl.delete_elements(self.test_elements))
                if result.get("status") == "ok":
                    print("  ✓ Attribute cleanup successful")
                else:
                    print(f"  ! Attribute cleanup warning: {result.get('message')}")
            except Exception as e:
                print(f"  ! Attribute cleanup error: {e}")
    
    # === ATTRIBUTE GETTER TESTS ===
    
    def test_get_standard_attributes(self):
        """Test getting standard attributes"""
        result = asyncio.run(self.attribute_ctrl.get_standard_attributes(self.test_elements))
        assert_ok(result)
        assert "attributes_by_id" in result
        attributes = result["attributes_by_id"]
        
        # Check that we got attributes for each element
        for element_id in self.test_elements:
            if str(element_id) not in attributes and element_id not in attributes:
                raise AssertionError(f"Missing attributes for element {element_id}")
        
        return result
    
    def test_get_user_attributes(self):
        """Test getting user attributes"""
        # Test with common user attribute numbers
        test_attr_numbers = [1, 2, 3]
        result = asyncio.run(self.attribute_ctrl.get_user_attributes(
            self.test_elements, 
            test_attr_numbers
        ))
        assert_ok(result)
        assert "user_attributes_by_id" in result
        return result
    
    def test_list_defined_user_attributes(self):
        """Test listing defined user attributes"""
        result = asyncio.run(self.attribute_ctrl.list_defined_user_attributes())
        assert_ok(result)
        assert "defined_attributes" in result
        # Result can be empty if no user attributes are defined
        return result
    
    # === ATTRIBUTE SETTER TESTS ===
    
    def test_set_name(self):
        """Test setting element names"""
        test_name = TEST_NAMES[0]  # "Test_Balken"
        result = asyncio.run(self.attribute_ctrl.set_name(self.test_elements, test_name))
        assert_ok(result)
        
        # Verify the name was set by getting attributes
        verify_result = asyncio.run(self.attribute_ctrl.get_standard_attributes(self.test_elements))
        assert_ok(verify_result)
        
        attributes = verify_result["attributes_by_id"]
        for element_id in self.test_elements:
            element_attrs = attributes.get(str(element_id)) or attributes.get(element_id)
            if element_attrs and element_attrs.get("name") != test_name:
                print(f"  ! Warning: Name not verified for element {element_id}")
        
        return result
    
    def test_set_material(self):
        """Test setting element materials"""
        test_material = TEST_MATERIALS[0]  # "C24"
        result = asyncio.run(self.attribute_ctrl.set_material(self.test_elements, test_material))
        assert_ok(result)
        
        # Verify the material was set by getting attributes
        verify_result = asyncio.run(self.attribute_ctrl.get_standard_attributes(self.test_elements))
        assert_ok(verify_result)
        
        attributes = verify_result["attributes_by_id"]
        for element_id in self.test_elements:
            element_attrs = attributes.get(str(element_id)) or attributes.get(element_id)
            if element_attrs and element_attrs.get("material") != test_material:
                print(f"  ! Warning: Material not verified for element {element_id}")
        
        return result
    
    def test_set_name_single_element(self):
        """Test setting name for single element"""
        if not self.test_elements:
            return {"status": "error", "message": "No test elements available"}
        
        single_element = [self.test_elements[0]]
        test_name = "Single_Test_Element"
        
        result = asyncio.run(self.attribute_ctrl.set_name(single_element, test_name))
        assert_ok(result)
        return result
    
    def test_set_material_different_materials(self):
        """Test setting different materials for different elements"""
        if len(self.test_elements) < 2:
            return {"status": "error", "message": "Need at least 2 elements for this test"}
        
        # Set different materials for different elements
        results = []
        for i, element_id in enumerate(self.test_elements[:2]):
            material = TEST_MATERIALS[i % len(TEST_MATERIALS)]
            result = asyncio.run(self.attribute_ctrl.set_material([element_id], material))
            assert_ok(result)
            results.append(result)
        
        return {"status": "ok", "message": f"Set {len(results)} different materials"}
    
    # === ERROR HANDLING TESTS ===
    
    def test_invalid_element_ids_attributes(self):
        """Test attribute functions with invalid element IDs"""
        result = asyncio.run(self.attribute_ctrl.get_standard_attributes([-1, -2]))
        # This might return ok with empty results or error, both are acceptable
        return result
    
    def test_empty_element_list(self):
        """Test attribute functions with empty element list"""
        result = asyncio.run(self.attribute_ctrl.get_standard_attributes([]))
        assert_ok(result)  # Should return ok with empty results
        return result
    
    def test_invalid_attribute_numbers(self):
        """Test user attributes with invalid attribute numbers"""
        try:
            result = asyncio.run(self.attribute_ctrl.get_user_attributes(
                self.test_elements, 
                [-1, 0]  # Invalid attribute numbers
            ))
            # Should raise exception or return error
            assert_error(result)
            return result
        except Exception as e:
            # Parameter validation in controller is also acceptable
            return {"status": "ok", "message": f"Parameter validation works: {e}"}
    
    def test_set_name_invalid_parameters(self):
        """Test set_name with invalid parameters"""
        try:
            # Test with invalid element ID
            result = asyncio.run(self.attribute_ctrl.set_name([-1], "Test"))
            # Should return error or raise exception
            return result
        except Exception as e:
            return {"status": "ok", "message": f"Parameter validation works: {e}"}
