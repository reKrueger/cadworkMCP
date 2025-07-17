"""
Material controller for material management operations
"""
from typing import Dict, Any, Optional
from .base_controller import BaseController

class CMaterialController(BaseController):
    """Controller for material management operations"""
    
    def __init__(self) -> None:
        super().__init__("MaterialController")
    
    async def create_material(self, material_name: str, density: Optional[float] = None, 
                             thermal_conductivity: Optional[float] = None, 
                             elastic_modulus: Optional[float] = None,
                             color_id: Optional[int] = None) -> Dict[str, Any]:
        """Create a new material with specified properties"""
        try:
            # Validate material name
            if not isinstance(material_name, str) or not material_name.strip():
                return {"status": "error", "message": "material_name must be a non-empty string"}
            
            # Prepare material data
            material_data: Dict[str, Any] = {
                "material_name": material_name.strip()
            }
            
            # Validate and add optional properties
            if density is not None:
                if not isinstance(density, (int, float)) or density <= 0:
                    return {"status": "error", "message": "density must be a positive number (kg/m³)"}
                material_data["density"] = float(density)
            
            if thermal_conductivity is not None:
                if not isinstance(thermal_conductivity, (int, float)) or thermal_conductivity < 0:
                    return {"status": "error", "message": "thermal_conductivity must be a non-negative number (W/mK)"}
                material_data["thermal_conductivity"] = float(thermal_conductivity)
            
            if elastic_modulus is not None:
                if not isinstance(elastic_modulus, (int, float)) or elastic_modulus <= 0:
                    return {"status": "error", "message": "elastic_modulus must be a positive number (N/mm²)"}
                material_data["elastic_modulus"] = float(elastic_modulus)
            
            if color_id is not None:
                if not isinstance(color_id, int) or color_id < 1 or color_id > 255:
                    return {"status": "error", "message": "color_id must be an integer between 1 and 255"}
                material_data["color_id"] = color_id
            
            return self.send_command("create_material", material_data)
            
        except Exception as e:
            return {"status": "error", "message": f"create_material failed: {e}"}
    
    async def get_material_properties(self, material_name: str) -> Dict[str, Any]:
        """Get properties of an existing material"""
        try:
            if not isinstance(material_name, str) or not material_name.strip():
                return {"status": "error", "message": "material_name must be a non-empty string"}
            
            return self.send_command("get_material_properties", {"material_name": material_name.strip()})
            
        except Exception as e:
            return {"status": "error", "message": f"get_material_properties failed: {e}"}
    
    async def list_available_materials(self) -> Dict[str, Any]:
        """List all available materials in the project"""
        try:
            return self.send_command("list_available_materials", {})
            
        except Exception as e:
            return {"status": "error", "message": f"list_available_materials failed: {e}"}
    
    async def set_material_density(self, material_name: str, density: float) -> Dict[str, Any]:
        """Set the density of an existing material"""
        try:
            if not isinstance(material_name, str) or not material_name.strip():
                return {"status": "error", "message": "material_name must be a non-empty string"}
            
            if not isinstance(density, (int, float)) or density <= 0:
                return {"status": "error", "message": "density must be a positive number (kg/m³)"}
            
            return self.send_command("set_material_density", {
                "material_name": material_name.strip(),
                "density": float(density)
            })
            
        except Exception as e:
            return {"status": "error", "message": f"set_material_density failed: {e}"}
    
    async def set_material_thermal_properties(self, material_name: str, 
                                            thermal_conductivity: float) -> Dict[str, Any]:
        """Set thermal properties of an existing material"""
        try:
            if not isinstance(material_name, str) or not material_name.strip():
                return {"status": "error", "message": "material_name must be a non-empty string"}
            
            if not isinstance(thermal_conductivity, (int, float)) or thermal_conductivity < 0:
                return {"status": "error", "message": "thermal_conductivity must be a non-negative number (W/mK)"}
            
            return self.send_command("set_material_thermal_properties", {
                "material_name": material_name.strip(),
                "thermal_conductivity": float(thermal_conductivity)
            })
            
        except Exception as e:
            return {"status": "error", "message": f"set_material_thermal_properties failed: {e}"}