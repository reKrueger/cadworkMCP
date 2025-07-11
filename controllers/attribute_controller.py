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
    
    async def set_group(self, aElementIds: list, aGroup: str) -> dict:
        """
        Setzt die Gruppe für eine Liste von Elementen
        
        Args:
            aElementIds: Liste der Element-IDs
            aGroup: Gruppen-Name (String)
        
        Returns:
            dict: Status der Operation
        """
        try:
            # Validierung
            if not isinstance(aElementIds, list) or not aElementIds:
                return {"status": "error", "message": "element_ids must be a non-empty list"}
            
            lValidatedIds = [self.validate_element_id(lId) for lId in aElementIds]
            
            if not isinstance(aGroup, str):
                return {"status": "error", "message": "group must be a string"}
            
            # Command senden
            return self.send_command("set_group", {
                "element_ids": lValidatedIds,
                "group": aGroup
            })
            
        except Exception as e:
            return {"status": "error", "message": f"set_group failed: {e}"}
    
    async def set_comment(self, aElementIds: list, aComment: str) -> dict:
        """
        Setzt den Kommentar für eine Liste von Elementen
        
        Args:
            aElementIds: Liste der Element-IDs
            aComment: Kommentar-Text (String)
        
        Returns:
            dict: Status der Operation
        """
        try:
            # Validierung
            if not isinstance(aElementIds, list) or not aElementIds:
                return {"status": "error", "message": "element_ids must be a non-empty list"}
            
            lValidatedIds = [self.validate_element_id(lId) for lId in aElementIds]
            
            if not isinstance(aComment, str):
                return {"status": "error", "message": "comment must be a string"}
            
            # Command senden
            return self.send_command("set_comment", {
                "element_ids": lValidatedIds,
                "comment": aComment
            })
            
        except Exception as e:
            return {"status": "error", "message": f"set_comment failed: {e}"}
    
    async def set_subgroup(self, aElementIds: list, aSubgroup: str) -> dict:
        """
        Setzt die Untergruppe für eine Liste von Elementen
        
        Args:
            aElementIds: Liste der Element-IDs
            aSubgroup: Untergruppen-Name (String)
        
        Returns:
            dict: Status der Operation
        """
        try:
            # Validierung
            if not isinstance(aElementIds, list) or not aElementIds:
                return {"status": "error", "message": "element_ids must be a non-empty list"}
            
            lValidatedIds = [self.validate_element_id(lId) for lId in aElementIds]
            
            if not isinstance(aSubgroup, str):
                return {"status": "error", "message": "subgroup must be a string"}
            
            # Command senden
            return self.send_command("set_subgroup", {
                "element_ids": lValidatedIds,
                "subgroup": aSubgroup
            })
            
        except Exception as e:
            return {"status": "error", "message": f"set_subgroup failed: {e}"}
