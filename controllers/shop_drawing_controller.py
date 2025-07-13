"""
Shop Drawing Controller for Cadwork MCP Server
Manages shop drawing-specific functions for production planning
"""
from typing import Dict, Any, Optional
from .base_controller import BaseController

class CShopDrawingController(BaseController):
    """Controller for shop drawing operations"""
    
    def __init__(self) -> None:
        super().__init__("ShopDrawingController")
    
    async def add_wall_section_x(self, wall_id: int, section_params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Add wall section in X-direction
        
        Creates technical section views for shop drawings.
        X-direction means section parallel to X-axis.
        
        Args:
            wall_id: ID of wall element for section
            section_params: Optional parameters for section configuration
                          (position, depth, display options, etc.)
        
        Returns:
            dict: Information about created wall section
        """
        try:
            # Validate wall ID
            validated_id = self.validate_element_id(wall_id)
            
            # Standardize section parameters
            final_section_params = section_params if section_params is not None else {}
            
            # Send command
            return self.send_command("add_wall_section_x", {
                "wall_id": validated_id,
                "section_params": final_section_params
            })
            
        except Exception as e:
            return {"status": "error", "message": f"add_wall_section_x failed: {e}"}
    
    async def add_wall_section_y(self, wall_id: int, section_params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Add wall section in Y-direction
        
        Creates technical section views for shop drawings.
        Y-direction means section parallel to Y-axis.
        
        Args:
            wall_id: ID of wall element for section
            section_params: Optional parameters for section configuration
                          (position, depth, display options, etc.)
        
        Returns:
            dict: Information about created wall section
        """
        try:
            # Validate wall ID
            validated_id = self.validate_element_id(wall_id)
            
            # Standardize section parameters
            final_section_params = section_params if section_params is not None else {}
            
            # Send command
            return self.send_command("add_wall_section_y", {
                "wall_id": validated_id,
                "section_params": final_section_params
            })
            
        except Exception as e:
            return {"status": "error", "message": f"add_wall_section_y failed: {e}"}
