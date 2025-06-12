"""
Attribute controller for attribute operations
"""
from typing import Dict, Any, List
from .base_controller import BaseController

class AttributeController(BaseController):
    """Controller for attribute operations"""
    
    def __init__(self):
        super().__init__("AttributeController")
    
    async def get_standard_attributes(self, element_ids: List[int]) -> Dict[str, Any]:
        """Get standard attributes for elements"""
        if not isinstance(element_ids, list):
            raise ValueError("element_ids must be a list")
        
        # Validate all element IDs
        validated_ids = [self.validate_element_id(eid) for eid in element_ids]
        
        return self.send_command("get_standard_attributes", {"element_ids": validated_ids})
    
    async def get_user_attributes(self, element_ids: List[int], 
                                 attribute_numbers: List[int]) -> Dict[str, Any]:
        """Get user attributes for elements"""
        if not isinstance(element_ids, list):
            raise ValueError("element_ids must be a list")
        if not isinstance(attribute_numbers, list):
            raise ValueError("attribute_numbers must be a list")
        
        # Validate element IDs
        validated_ids = [self.validate_element_id(eid) for eid in element_ids]
        
        # Validate attribute numbers
        validated_attrs = []
        for num in attribute_numbers:
            try:
                attr_num = int(num)
                if attr_num <= 0:
                    raise ValueError(f"Attribute number must be positive: {attr_num}")
                validated_attrs.append(attr_num)
            except (ValueError, TypeError):
                raise ValueError(f"Invalid attribute number: {num}")
        
        return self.send_command("get_user_attributes", {
            "element_ids": validated_ids,
            "attribute_numbers": validated_attrs
        })
    
    async def list_defined_user_attributes(self) -> Dict[str, Any]:
        """List all defined user attributes"""
        return self.send_command("list_defined_user_attributes")
    
    # --- ATTRIBUTE SETTERS ---
    
    async def set_name(self, element_ids: List[int], name: str) -> Dict[str, Any]:
        """Set name for elements"""
        if not isinstance(element_ids, list):
            raise ValueError("element_ids must be a list")
        if not isinstance(name, str):
            raise ValueError("name must be a string")
        
        # Validate all element IDs
        validated_ids = [self.validate_element_id(eid) for eid in element_ids]
        
        return self.send_command("set_name", {
            "element_ids": validated_ids,
            "name": str(name)
        })
    
    async def set_material(self, element_ids: List[int], material: str) -> Dict[str, Any]:
        """Set material for elements"""
        if not isinstance(element_ids, list):
            raise ValueError("element_ids must be a list")
        if not isinstance(material, str):
            raise ValueError("material must be a string")
        
        # Validate all element IDs
        validated_ids = [self.validate_element_id(eid) for eid in element_ids]
        
        return self.send_command("set_material", {
            "element_ids": validated_ids,
            "material": str(material)
        })
