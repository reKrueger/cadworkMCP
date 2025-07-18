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
    
    async def create_visual_filter(self, filter_name: str, filter_criteria: Dict[str, Any], 
                                 visual_properties: Dict[str, Any]) -> Dict[str, Any]:
        """
        Create and apply visual filter based on element attributes
        
        Args:
            filter_name: Name for the visual filter
            filter_criteria: Criteria to select elements (like search_elements_by_attributes)
            visual_properties: Visual properties to apply (color, transparency, visibility)
        
        Returns:
            dict: Status of filter creation and application
        """
        try:
            # Validate filter name
            if not isinstance(filter_name, str) or not filter_name.strip():
                return {"status": "error", "message": "filter_name must be a non-empty string"}
            
            # Validate filter criteria
            if not isinstance(filter_criteria, dict) or not filter_criteria:
                return {"status": "error", "message": "filter_criteria must be a non-empty dictionary"}
            
            # Validate visual properties
            if not isinstance(visual_properties, dict) or not visual_properties:
                return {"status": "error", "message": "visual_properties must be a non-empty dictionary"}
            
            # Validate visual properties content
            valid_visual_keys = ["color_id", "transparency", "visibility"]
            validated_visuals: Dict[str, Any] = {}
            
            for key, value in visual_properties.items():
                if key not in valid_visual_keys:
                    return {"status": "error", "message": f"Invalid visual property: {key}. Must be one of: {valid_visual_keys}"}
                
                if key == "color_id":
                    if not isinstance(value, int) or value < 1 or value > 255:
                        return {"status": "error", "message": "color_id must be an integer between 1 and 255"}
                    validated_visuals[key] = value
                    
                elif key == "transparency":
                    if not isinstance(value, int) or value < 0 or value > 100:
                        return {"status": "error", "message": "transparency must be an integer between 0 and 100"}
                    validated_visuals[key] = value
                    
                elif key == "visibility":
                    if not isinstance(value, bool):
                        return {"status": "error", "message": "visibility must be a boolean"}
                    validated_visuals[key] = value
            
            # Validate filter criteria structure (similar to search_elements_by_attributes)
            validated_criteria: Dict[str, Any] = {}
            for key, val in filter_criteria.items():
                if key.startswith("user_attr_"):
                    try:
                        attr_num_str = key.replace("user_attr_", "")
                        attr_num = int(attr_num_str)
                        if attr_num <= 0:
                            return {"status": "error", "message": f"Invalid user attribute number: {attr_num}"}
                        validated_criteria[key] = {"type": "user_attribute", "number": attr_num, "value": str(val)}
                    except (ValueError, TypeError):
                        return {"status": "error", "message": f"Invalid user attribute key format: {key}"}
                        
                elif key in ["name", "material", "group", "comment", "subgroup"]:
                    validated_criteria[key] = {"type": "standard_attribute", "value": str(val)}
                    
                elif key.startswith("dimension_"):
                    dimension_type = key.replace("dimension_", "")
                    if dimension_type not in ["width", "height", "length", "volume", "weight"]:
                        return {"status": "error", "message": f"Invalid dimension type: {dimension_type}"}
                    validated_criteria[key] = {"type": "dimension", "dimension": dimension_type, "value": val}
                    
                else:
                    return {"status": "error", "message": f"Unknown filter criteria key: {key}"}
            
            # Send command
            return self.send_command("create_visual_filter", {
                "filter_name": filter_name.strip(),
                "filter_criteria": validated_criteria,
                "visual_properties": validated_visuals
            })
            
        except Exception as e:
            return {"status": "error", "message": f"create_visual_filter failed: {e}"}
    
    async def apply_color_scheme(self, scheme_name: str, element_ids: List[int] = None, 
                               scheme_basis: str = "material") -> Dict[str, Any]:
        """
        Apply predefined color scheme to elements
        
        Args:
            scheme_name: Name of color scheme ('material_based', 'status_based', 'priority_based', 'custom')
            element_ids: Optional list of element IDs (if None, applies to all visible elements)
            scheme_basis: Basis for coloring ('material', 'group', 'element_type', 'user_attribute')
        
        Returns:
            dict: Status of color scheme application
        """
        try:
            # Validate scheme name
            valid_schemes = ["material_based", "status_based", "priority_based", "element_type_based", 
                           "group_based", "dimension_based", "custom"]
            if scheme_name not in valid_schemes:
                return {"status": "error", "message": f"Invalid scheme_name. Must be one of: {valid_schemes}"}
            
            # Validate element IDs if provided
            validated_ids = None
            if element_ids is not None:
                if not isinstance(element_ids, list):
                    return {"status": "error", "message": "element_ids must be a list if provided"}
                if element_ids:  # Only validate if not empty
                    validated_ids = [self.validate_element_id(eid) for eid in element_ids]
            
            # Validate scheme basis
            valid_basis = ["material", "group", "element_type", "user_attribute", "dimension", "status"]
            if scheme_basis not in valid_basis:
                return {"status": "error", "message": f"Invalid scheme_basis. Must be one of: {valid_basis}"}
            
            # Build command arguments
            args: Dict[str, Any] = {
                "scheme_name": scheme_name,
                "scheme_basis": scheme_basis
            }
            
            if validated_ids is not None:
                args["element_ids"] = validated_ids
            
            # Send command
            return self.send_command("apply_color_scheme", args)
            
        except Exception as e:
            return {"status": "error", "message": f"apply_color_scheme failed: {e}"}
