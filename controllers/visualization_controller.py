"""
Visualization Controller for Cadwork MCP Server
Manages colors, transparency and visibility of elements
"""
from typing import Dict, Any, List
from .base_controller import BaseController

class CVisualizationController(BaseController):
    """Controller for visualization operations"""
    
    def __init__(self) -> None:
        super().__init__("VisualizationController")
    
    async def set_color(self, element_ids: List[int], color_id: int) -> Dict[str, Any]:
        """
        Set color for a list of elements
        
        Args:
            element_ids: List of element IDs
            color_id: Color ID (1-255, see Cadwork color palette)
        
        Returns:
            dict: Status of operation
        """
        try:
            # Validation
            if not isinstance(element_ids, list) or not element_ids:
                return {"status": "error", "message": "element_ids must be a non-empty list"}
            
            validated_ids = [self.validate_element_id(eid) for eid in element_ids]
            
            if not isinstance(color_id, int) or color_id < 1 or color_id > 255:
                return {"status": "error", "message": "color_id must be an integer between 1 and 255"}
            
            # Send command
            return self.send_command("set_color", {
                "element_ids": validated_ids,
                "color_id": color_id
            })
            
        except Exception as e:
            return {"status": "error", "message": f"set_color failed: {e}"}
    
    async def set_visibility(self, element_ids: List[int], visible: bool) -> Dict[str, Any]:
        """
        Set visibility for a list of elements
        
        Args:
            element_ids: List of element IDs  
            visible: True = visible, False = hidden
        
        Returns:
            dict: Status of operation
        """
        try:
            # Validation
            if not isinstance(element_ids, list) or not element_ids:
                return {"status": "error", "message": "element_ids must be a non-empty list"}
            
            validated_ids = [self.validate_element_id(eid) for eid in element_ids]
            
            if not isinstance(visible, bool):
                return {"status": "error", "message": "visible must be a boolean (True/False)"}
            
            # Send command
            return self.send_command("set_visibility", {
                "element_ids": validated_ids,
                "visible": visible
            })
            
        except Exception as e:
            return {"status": "error", "message": f"set_visibility failed: {e}"}
    
    async def set_transparency(self, element_ids: List[int], transparency: int) -> Dict[str, Any]:
        """
        Set transparency for a list of elements
        
        Args:
            element_ids: List of element IDs
            transparency: Transparency value (0-100, 0=opaque, 100=fully transparent)
        
        Returns:
            dict: Status of operation
        """
        try:
            # Validation
            if not isinstance(element_ids, list) or not element_ids:
                return {"status": "error", "message": "element_ids must be a non-empty list"}
            
            validated_ids = [self.validate_element_id(eid) for eid in element_ids]
            
            if not isinstance(transparency, int) or transparency < 0 or transparency > 100:
                return {"status": "error", "message": "transparency must be an integer between 0 and 100"}
            
            # Send command
            return self.send_command("set_transparency", {
                "element_ids": validated_ids,
                "transparency": transparency
            })
            
        except Exception as e:
            return {"status": "error", "message": f"set_transparency failed: {e}"}
    
    async def get_color(self, element_id: int) -> Dict[str, Any]:
        """
        Get color of an element
        
        Args:
            element_id: Element ID
        
        Returns:
            dict: Color ID and color information
        """
        try:
            # Validation
            validated_id = self.validate_element_id(element_id)
            
            # Send command
            return self.send_command("get_color", {
                "element_id": validated_id
            })
            
        except Exception as e:
            return {"status": "error", "message": f"get_color failed: {e}"}
    
    async def get_transparency(self, element_id: int) -> Dict[str, Any]:
        """
        Get transparency of an element
        
        Args:
            element_id: Element ID
        
        Returns:
            dict: Transparency value (0-100)
        """
        try:
            # Validation
            validated_id = self.validate_element_id(element_id)
            
            # Send command
            return self.send_command("get_transparency", {
                "element_id": validated_id
            })
            
        except Exception as e:
            return {"status": "error", "message": f"get_transparency failed: {e}"}
    
    async def show_all_elements(self) -> Dict[str, Any]:
        """
        Make all elements in the model visible
        
        Returns:
            dict: Status of operation with count of affected elements
        """
        try:
            # Send command
            return self.send_command("show_all_elements", {})
            
        except Exception as e:
            return {"status": "error", "message": f"show_all_elements failed: {e}"}
    
    async def hide_all_elements(self) -> Dict[str, Any]:
        """
        Hide all elements in the model
        
        Returns:
            dict: Status of operation with count of affected elements
        """
        try:
            # Send command
            return self.send_command("hide_all_elements", {})
            
        except Exception as e:
            return {"status": "error", "message": f"hide_all_elements failed: {e}"}
    
    async def refresh_display(self) -> Dict[str, Any]:
        """
        Refresh display/viewport after changes
        
        Returns:
            dict: Status of display refresh
        """
        try:
            # Send command
            return self.send_command("refresh_display", {})
            
        except Exception as e:
            return {"status": "error", "message": f"refresh_display failed: {e}"}
    
    async def get_visible_element_count(self) -> Dict[str, Any]:
        """
        Get count of currently visible elements
        
        Returns:
            dict: Count of visible elements + statistics
        """
        try:
            # Send command
            return self.send_command("get_visible_element_count", {})
            
        except Exception as e:
            return {"status": "error", "message": f"get_visible_element_count failed: {e}"}
