"""
Geometry controller for geometry operations
"""
from typing import Dict, Any
from .base_controller import BaseController

class GeometryController(BaseController):
    """Controller for geometry operations"""
    
    def __init__(self):
        super().__init__("GeometryController")
    
    async def get_element_width(self, element_id: int) -> Dict[str, Any]:
        """Get element width"""
        element_id = self.validate_element_id(element_id)
        return self.send_command("get_element_width", {"element_id": element_id})
    
    async def get_element_height(self, element_id: int) -> Dict[str, Any]:
        """Get element height"""
        element_id = self.validate_element_id(element_id)
        return self.send_command("get_element_height", {"element_id": element_id})
    
    async def get_element_length(self, element_id: int) -> Dict[str, Any]:
        """Get element length"""
        element_id = self.validate_element_id(element_id)
        return self.send_command("get_element_length", {"element_id": element_id})
    
    async def get_element_volume(self, element_id: int) -> Dict[str, Any]:
        """Get element volume"""
        element_id = self.validate_element_id(element_id)
        return self.send_command("get_element_volume", {"element_id": element_id})
    
    async def get_element_weight(self, element_id: int) -> Dict[str, Any]:
        """Get element weight"""
        element_id = self.validate_element_id(element_id)
        return self.send_command("get_element_weight", {"element_id": element_id})
    
    async def get_element_xl(self, element_id: int) -> Dict[str, Any]:
        """Get element XL vector (length direction)"""
        element_id = self.validate_element_id(element_id)
        return self.send_command("get_element_xl", {"element_id": element_id})
    
    async def get_element_yl(self, element_id: int) -> Dict[str, Any]:
        """Get element YL vector (width direction)"""
        element_id = self.validate_element_id(element_id)
        return self.send_command("get_element_yl", {"element_id": element_id})
    
    async def get_element_zl(self, element_id: int) -> Dict[str, Any]:
        """Get element ZL vector (height direction)"""
        element_id = self.validate_element_id(element_id)
        return self.send_command("get_element_zl", {"element_id": element_id})
    
    async def get_element_p1(self, element_id: int) -> Dict[str, Any]:
        """Get element P1 point (start point)"""
        element_id = self.validate_element_id(element_id)
        return self.send_command("get_element_p1", {"element_id": element_id})
    
    async def get_element_p2(self, element_id: int) -> Dict[str, Any]:
        """Get element P2 point (end point)"""
        element_id = self.validate_element_id(element_id)
        return self.send_command("get_element_p2", {"element_id": element_id})
    
    async def get_element_p3(self, element_id: int) -> Dict[str, Any]:
        """Get element P3 point (orientation point)"""
        element_id = self.validate_element_id(element_id)
        return self.send_command("get_element_p3", {"element_id": element_id})
    
    async def get_center_of_gravity(self, element_id: int) -> Dict[str, Any]:
        """Get center of gravity for a single element"""
        element_id = self.validate_element_id(element_id)
        return self.send_command("get_center_of_gravity", {"element_id": element_id})
    
    async def get_center_of_gravity_for_list(self, element_ids: list) -> Dict[str, Any]:
        """Get center of gravity for multiple elements combined"""
        if not isinstance(element_ids, list):
            raise ValueError("element_ids must be a list")
        
        # Validate all element IDs
        validated_ids = [self.validate_element_id(eid) for eid in element_ids]
        
        return self.send_command("get_center_of_gravity_for_list", {"element_ids": validated_ids})
    
    async def get_element_vertices(self, element_id: int) -> Dict[str, Any]:
        """Get all vertices (corner points) of an element"""
        element_id = self.validate_element_id(element_id)
        return self.send_command("get_element_vertices", {"element_id": element_id})
    
    async def get_minimum_distance_between_elements(self, first_element_id: int, second_element_id: int) -> Dict[str, Any]:
        """Get minimum distance between two elements"""
        first_element_id = self.validate_element_id(first_element_id)
        second_element_id = self.validate_element_id(second_element_id)
        
        return self.send_command("get_minimum_distance_between_elements", {
            "first_element_id": first_element_id,
            "second_element_id": second_element_id
        })
    
    async def get_element_facets(self, element_id: int) -> Dict[str, Any]:
        """Get all facets (faces) of an element"""
        element_id = self.validate_element_id(element_id)
        return self.send_command("get_element_facets", {"element_id": element_id})
    
    async def get_element_reference_face_area(self, element_id: int) -> Dict[str, Any]:
        """Get reference face area of an element"""
        element_id = self.validate_element_id(element_id)
        return self.send_command("get_element_reference_face_area", {"element_id": element_id})
    
    async def get_total_area_of_all_faces(self, element_id: int) -> Dict[str, Any]:
        """Get total surface area of all faces of an element"""
        element_id = self.validate_element_id(element_id)
        return self.send_command("get_total_area_of_all_faces", {"element_id": element_id})
    
    async def rotate_elements(self, element_ids: list, origin: list, rotation_axis: list, rotation_angle: float) -> Dict[str, Any]:
        """Rotate elements around an axis"""
        if not isinstance(element_ids, list):
            raise ValueError("element_ids must be a list")
        if not isinstance(origin, list) or len(origin) != 3:
            raise ValueError("origin must be a list of 3 numbers [x, y, z]")
        if not isinstance(rotation_axis, list) or len(rotation_axis) != 3:
            raise ValueError("rotation_axis must be a list of 3 numbers [x, y, z]")
        if not isinstance(rotation_angle, (int, float)):
            raise ValueError("rotation_angle must be a number")
        
        # Validate all element IDs
        validated_ids = [self.validate_element_id(eid) for eid in element_ids]
        
        return self.send_command("rotate_elements", {
            "element_ids": validated_ids,
            "origin": origin,
            "rotation_axis": rotation_axis,
            "rotation_angle": float(rotation_angle)
        })
    
    async def apply_global_scale(self, element_ids: list, scale: float, origin: list) -> Dict[str, Any]:
        """Apply global scaling to elements"""
        if not isinstance(element_ids, list):
            raise ValueError("element_ids must be a list")
        if not isinstance(scale, (int, float)) or scale <= 0:
            raise ValueError("scale must be a positive number")
        if not isinstance(origin, list) or len(origin) != 3:
            raise ValueError("origin must be a list of 3 numbers [x, y, z]")
        
        # Validate all element IDs
        validated_ids = [self.validate_element_id(eid) for eid in element_ids]
        
        return self.send_command("apply_global_scale", {
            "element_ids": validated_ids,
            "scale": float(scale),
            "origin": origin
        })
    
    async def invert_model(self, element_ids: list) -> Dict[str, Any]:
        """Invert/mirror elements"""
        if not isinstance(element_ids, list):
            raise ValueError("element_ids must be a list")
        
        # Validate all element IDs
        validated_ids = [self.validate_element_id(eid) for eid in element_ids]
        
        return self.send_command("invert_model", {"element_ids": validated_ids})
    
    async def rotate_height_axis_90(self, element_ids: list) -> Dict[str, Any]:
        """Rotate element height axis by 90 degrees"""
        if not isinstance(element_ids, list):
            raise ValueError("element_ids must be a list")
        
        # Validate all element IDs
        validated_ids = [self.validate_element_id(eid) for eid in element_ids]
        
        return self.send_command("rotate_height_axis_90", {"element_ids": validated_ids})
    
    async def rotate_length_axis_90(self, element_ids: list) -> Dict[str, Any]:
        """Rotate element length axis by 90 degrees"""
        if not isinstance(element_ids, list):
            raise ValueError("element_ids must be a list")
        
        # Validate all element IDs
        validated_ids = [self.validate_element_id(eid) for eid in element_ids]
        
        return self.send_command("rotate_length_axis_90", {"element_ids": validated_ids})
    
    async def get_element_type(self, aElementId: int) -> dict:
        """
        Ruft den Typ eines Cadwork-Elements ab
        
        Args:
            aElementId: Element-ID
        
        Returns:
            dict: Element-Typ Information (beam, panel, drilling, etc.)
        """
        try:
            # Validierung
            lValidatedId = self.validate_element_id(aElementId)
            
            # Command senden
            return self.send_command("get_element_type", {
                "element_id": lValidatedId
            })
            
        except Exception as e:
            return {"status": "error", "message": f"get_element_type failed: {e}"}
    
    async def calculate_total_volume(self, aElementIds: list) -> dict:
        """
        Berechnet das Gesamtvolumen einer Liste von Elementen
        
        Args:
            aElementIds: Liste der Element-IDs
        
        Returns:
            dict: Gesamtvolumen in mm³ und anderen Einheiten
        """
        try:
            # Validierung
            if not isinstance(aElementIds, list) or not aElementIds:
                return {"status": "error", "message": "element_ids must be a non-empty list"}
            
            lValidatedIds = [self.validate_element_id(lId) for lId in aElementIds]
            
            # Command senden
            return self.send_command("calculate_total_volume", {
                "element_ids": lValidatedIds
            })
            
        except Exception as e:
            return {"status": "error", "message": f"calculate_total_volume failed: {e}"}
    
    async def calculate_total_weight(self, aElementIds: list) -> dict:
        """
        Berechnet das Gesamtgewicht einer Liste von Elementen
        
        Args:
            aElementIds: Liste der Element-IDs
        
        Returns:
            dict: Gesamtgewicht in kg und anderen Einheiten
        """
        try:
            # Validierung
            if not isinstance(aElementIds, list) or not aElementIds:
                return {"status": "error", "message": "element_ids must be a non-empty list"}
            
            lValidatedIds = [self.validate_element_id(lId) for lId in aElementIds]
            
            # Command senden
            return self.send_command("calculate_total_weight", {
                "element_ids": lValidatedIds
            })
            
        except Exception as e:
            return {"status": "error", "message": f"calculate_total_weight failed: {e}"}
