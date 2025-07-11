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
    
    # --- EXTENDED ELEMENT CREATION ---
    
    async def create_circular_beam_points(self, diameter: float, p1: list, p2: list, p3: list = None) -> Dict[str, Any]:
        """Create circular beam using points. Requires diameter, start point p1, end point p2, optional orientation point p3"""
        return self.send_command("create_circular_beam_points", {
            "diameter": float(diameter),
            "p1": p1,
            "p2": p2, 
            "p3": p3
        })
    
    async def create_square_beam_points(self, width: float, p1: list, p2: list, p3: list = None) -> Dict[str, Any]:
        """Create square beam using points. Requires width, start point p1, end point p2, optional orientation point p3"""
        return self.send_command("create_square_beam_points", {
            "width": float(width),
            "p1": p1,
            "p2": p2,
            "p3": p3
        })
    
    async def create_standard_beam_points(self, standard_element_name: str, p1: list, p2: list, p3: list = None) -> Dict[str, Any]:
        """Create standard beam using points. Requires standard element name, start point p1, end point p2, optional orientation point p3"""
        return self.send_command("create_standard_beam_points", {
            "standard_element_name": str(standard_element_name),
            "p1": p1,
            "p2": p2,
            "p3": p3
        })
    
    async def create_standard_panel_points(self, standard_element_name: str, p1: list, p2: list, p3: list = None) -> Dict[str, Any]:
        """Create standard panel using points. Requires standard element name, start point p1, end point p2, optional orientation point p3"""
        return self.send_command("create_standard_panel_points", {
            "standard_element_name": str(standard_element_name),
            "p1": p1,
            "p2": p2,
            "p3": p3
        })
    
    async def create_drilling_points(self, diameter: float, p1: list, p2: list) -> Dict[str, Any]:
        """Create drilling using points. Requires diameter, start point p1, and end point p2"""
        return self.send_command("create_drilling_points", {
            "diameter": float(diameter),
            "p1": p1,
            "p2": p2
        })
    
    async def create_polygon_beam(self, polygon_vertices: list, thickness: float, xl: list, zl: list) -> Dict[str, Any]:
        """Create polygon beam. Requires polygon vertices, thickness, xl vector (length direction), and zl vector (height direction)"""
        return self.send_command("create_polygon_beam", {
            "polygon_vertices": polygon_vertices,
            "thickness": float(thickness),
            "xl": xl,
            "zl": zl
        })
    
    async def get_elements_by_type(self, aElementType: str) -> dict:
        """
        Findet alle Elemente eines bestimmten Typs im Modell
        
        Args:
            aElementType: Element-Typ ("beam", "panel", "drilling", etc.)
        
        Returns:
            dict: Liste der Element-IDs des angegebenen Typs
        """
        try:
            # Validierung des Element-Typs
            lValidTypes = ["beam", "panel", "drilling", "node", "line", "surface", 
                          "volume", "container", "auxiliary", "text_object", 
                          "dimension", "architectural"]
            
            if not isinstance(aElementType, str) or aElementType not in lValidTypes:
                return {"status": "error", 
                       "message": f"element_type must be one of: {', '.join(lValidTypes)}"}
            
            # Command senden
            return self.send_command("get_elements_by_type", {
                "element_type": aElementType
            })
            
        except Exception as e:
            return {"status": "error", "message": f"get_elements_by_type failed: {e}"}
    
    async def filter_elements_by_material(self, aMaterialName: str) -> dict:
        """
        Filtert alle Elemente nach Material-Name
        
        Args:
            aMaterialName: Material-Name (String)
        
        Returns:
            dict: Liste der Element-IDs mit dem angegebenen Material
        """
        try:
            # Validierung
            if not isinstance(aMaterialName, str):
                return {"status": "error", "message": "material_name must be a string"}
            
            if not aMaterialName.strip():
                return {"status": "error", "message": "material_name cannot be empty"}
            
            # Command senden
            return self.send_command("filter_elements_by_material", {
                "material_name": aMaterialName.strip()
            })
            
        except Exception as e:
            return {"status": "error", "message": f"filter_elements_by_material failed: {e}"}
    
    async def get_elements_in_group(self, aGroupName: str) -> dict:
        """
        Findet alle Elemente in einer bestimmten Gruppe
        
        Args:
            aGroupName: Gruppen-Name (String)
        
        Returns:
            dict: Liste der Element-IDs in der angegebenen Gruppe
        """
        try:
            # Validierung
            if not isinstance(aGroupName, str):
                return {"status": "error", "message": "group_name must be a string"}
            
            if not aGroupName.strip():
                return {"status": "error", "message": "group_name cannot be empty"}
            
            # Command senden
            return self.send_command("get_elements_in_group", {
                "group_name": aGroupName.strip()
            })
            
        except Exception as e:
            return {"status": "error", "message": f"get_elements_in_group failed: {e}"}
    
    async def get_element_count_by_type(self) -> dict:
        """
        Ermittelt die Anzahl aller Elemente pro Typ im Modell
        
        Returns:
            dict: Statistiken über Element-Verteilung nach Typen
        """
        try:
            # Command senden
            return self.send_command("get_element_count_by_type", {})
            
        except Exception as e:
            return {"status": "error", "message": f"get_element_count_by_type failed: {e}"}
    
    async def get_material_statistics(self) -> dict:
        """
        Ermittelt Material-Statistiken des gesamten Modells
        
        Returns:
            dict: Statistiken über Material-Verteilung (welche Materialien, Anzahl, Prozente)
        """
        try:
            # Command senden
            return self.send_command("get_material_statistics", {})
            
        except Exception as e:
            return {"status": "error", "message": f"get_material_statistics failed: {e}"}
    
    async def get_group_statistics(self) -> dict:
        """
        Ermittelt Gruppen-Statistiken des gesamten Modells
        
        Returns:
            dict: Statistiken über Gruppen-Verteilung (welche Gruppen, Anzahl, Prozente)
        """
        try:
            # Command senden
            return self.send_command("get_group_statistics", {})
            
        except Exception as e:
            return {"status": "error", "message": f"get_group_statistics failed: {e}"}
    
    async def duplicate_elements(self, aElementIds: list) -> dict:
        """
        Dupliziert Elemente am gleichen Ort (ohne Versatz)
        
        Args:
            aElementIds: Liste der Element-IDs zum Duplizieren
        
        Returns:
            dict: Liste der neuen Element-IDs der duplizierten Elemente
        """
        try:
            # Validierung
            if not isinstance(aElementIds, list) or not aElementIds:
                return {"status": "error", "message": "element_ids must be a non-empty list"}
            
            lValidatedIds = [self.validate_element_id(lId) for lId in aElementIds]
            
            # Command senden
            return self.send_command("duplicate_elements", {
                "element_ids": lValidatedIds
            })
            
        except Exception as e:
            return {"status": "error", "message": f"duplicate_elements failed: {e}"}
