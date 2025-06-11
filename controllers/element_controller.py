"""
Element controller for element operations
"""
from typing import Dict, Any, List, Optional
from .base_controller import BaseController

class ElementController(BaseController):
    """Controller for element operations"""
    
    def __init__(self):
        super().__init__("ElementController")
    
    async def create_beam(self, p1: list, p2: list, width: float, height: float, 
                         p3: Optional[list] = None) -> Dict[str, Any]:
        """Create a rectangular beam"""
        args = {
            "p1": p1,
            "p2": p2, 
            "width": width,
            "height": height
        }
        if p3 is not None:
            args["p3"] = p3
        
        return self.send_command("create_beam", args)
    
    async def create_panel(self, p1: list, p2: list, width: float, thickness: float,
                          p3: Optional[list] = None) -> Dict[str, Any]:
        """Create a rectangular panel"""
        args = {
            "p1": p1,
            "p2": p2,
            "width": width, 
            "thickness": thickness
        }
        if p3 is not None:
            args["p3"] = p3
        
        return self.send_command("create_panel", args)
    
    async def get_active_element_ids(self) -> Dict[str, Any]:
        """Get active element IDs"""
        return self.send_command("get_active_element_ids")
    
    async def get_all_element_ids(self) -> Dict[str, Any]:
        """Get all element IDs in the model"""
        return self.send_command("get_all_element_ids")
    
    async def get_visible_element_ids(self) -> Dict[str, Any]:
        """Get visible element IDs"""
        return self.send_command("get_visible_element_ids")
    
    async def get_element_info(self, element_id: int) -> Dict[str, Any]:
        """Get element information"""
        element_id = self.validate_element_id(element_id)
        return self.send_command("get_element_info", {"element_id": element_id})
    
    async def delete_elements(self, element_ids: List[int]) -> Dict[str, Any]:
        """Delete elements from the model"""
        if not isinstance(element_ids, list):
            raise ValueError("element_ids must be a list")
        
        # Validate all element IDs
        validated_ids = [self.validate_element_id(eid) for eid in element_ids]
        
        return self.send_command("delete_elements", {"element_ids": validated_ids})
    
    async def copy_elements(self, element_ids: List[int], copy_vector: list) -> Dict[str, Any]:
        """Copy elements with a given vector offset"""
        if not isinstance(element_ids, list):
            raise ValueError("element_ids must be a list")
        if not isinstance(copy_vector, list) or len(copy_vector) != 3:
            raise ValueError("copy_vector must be a list of 3 numbers [x, y, z]")
        
        # Validate all element IDs
        validated_ids = [self.validate_element_id(eid) for eid in element_ids]
        
        return self.send_command("copy_elements", {
            "element_ids": validated_ids,
            "copy_vector": copy_vector
        })
    
    async def move_element(self, element_ids: List[int], move_vector: list) -> Dict[str, Any]:
        """Move elements by a given vector offset"""
        if not isinstance(element_ids, list):
            raise ValueError("element_ids must be a list")
        if not isinstance(move_vector, list) or len(move_vector) != 3:
            raise ValueError("move_vector must be a list of 3 numbers [x, y, z]")
        
        # Validate all element IDs
        validated_ids = [self.validate_element_id(eid) for eid in element_ids]
        
        return self.send_command("move_element", {
            "element_ids": validated_ids,
            "move_vector": move_vector
        })
    
    async def get_user_element_ids(self, count: Optional[int] = None) -> Dict[str, Any]:
        """Get user-selected elements with optional count limit"""
        args = {}
        if count is not None:
            if not isinstance(count, int) or count <= 0:
                raise ValueError("count must be a positive integer")
            args["count"] = count
        
        return self.send_command("get_user_element_ids", args)
