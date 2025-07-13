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
    
    async def join_elements(self, aElementIds: list) -> dict:
        """
        Verbindet Elemente miteinander (Join)
        
        Args:
            aElementIds: Liste der Element-IDs die verbunden werden sollen (mindestens 2)
        
        Returns:
            dict: Status der Verbindungs-Operation
        """
        try:
            # Validierung
            if not isinstance(aElementIds, list) or len(aElementIds) < 2:
                return {"status": "error", "message": "At least 2 element IDs required for joining"}
            
            lValidatedIds = [self.validate_element_id(lId) for lId in aElementIds]
            
            # Command senden
            return self.send_command("join_elements", {
                "element_ids": lValidatedIds
            })
            
        except Exception as e:
            return {"status": "error", "message": f"join_elements failed: {e}"}
    
    async def unjoin_elements(self, aElementIds: list) -> dict:
        """
        Trennt verbundene Elemente (Unjoin)
        
        Args:
            aElementIds: Liste der Element-IDs deren Verbindungen getrennt werden sollen
        
        Returns:
            dict: Status der Trennungs-Operation
        """
        try:
            # Validierung
            if not isinstance(aElementIds, list) or not aElementIds:
                return {"status": "error", "message": "element_ids must be a non-empty list"}
            
            lValidatedIds = [self.validate_element_id(lId) for lId in aElementIds]
            
            # Command senden
            return self.send_command("unjoin_elements", {
                "element_ids": lValidatedIds
            })
            
        except Exception as e:
            return {"status": "error", "message": f"unjoin_elements failed: {e}"}
    
    async def cut_corner_lap(self, aElementIds: list, aCutParams: dict = None) -> dict:
        """
        Erstellt Eckblatt-Verbindung zwischen Elementen
        
        Args:
            aElementIds: Liste der Element-IDs für Eckblatt-Verbindung (mindestens 2)
            aCutParams: Optionale Schnitt-Parameter (Tiefe, Breite, etc.)
        
        Returns:
            dict: Status der Eckblatt-Operation
        """
        try:
            # Validierung
            if not isinstance(aElementIds, list) or len(aElementIds) < 2:
                return {"status": "error", "message": "At least 2 element IDs required for corner lap cut"}
            
            lValidatedIds = [self.validate_element_id(lId) for lId in aElementIds]
            
            # Standard-Parameter wenn nicht angegeben
            if aCutParams is None:
                aCutParams = {}
            
            # Command senden
            return self.send_command("cut_corner_lap", {
                "element_ids": lValidatedIds,
                "cut_params": aCutParams
            })
            
        except Exception as e:
            return {"status": "error", "message": f"cut_corner_lap failed: {e}"}
    
    async def cut_cross_lap(self, aElementIds: list, aCutParams: dict = None) -> dict:
        """
        Erstellt Kreuzblatt-Verbindung zwischen Elementen
        
        Args:
            aElementIds: Liste der Element-IDs für Kreuzblatt-Verbindung (mindestens 2)
            aCutParams: Optionale Schnitt-Parameter (Tiefe, Breite, Position, etc.)
        
        Returns:
            dict: Status der Kreuzblatt-Operation
        """
        try:
            # Validierung
            if not isinstance(aElementIds, list) or len(aElementIds) < 2:
                return {"status": "error", "message": "At least 2 element IDs required for cross lap cut"}
            
            lValidatedIds = [self.validate_element_id(lId) for lId in aElementIds]
            
            # Standard-Parameter wenn nicht angegeben
            if aCutParams is None:
                aCutParams = {}
            
            # Command senden
            return self.send_command("cut_cross_lap", {
                "element_ids": lValidatedIds,
                "cut_params": aCutParams
            })
            
        except Exception as e:
            return {"status": "error", "message": f"cut_cross_lap failed: {e}"}
    
    async def cut_half_lap(self, aElementIds: list, aCutParams: dict = None) -> dict:
        """
        Erstellt Halbes Blatt-Verbindung zwischen Elementen
        
        Bei dieser Verbindung wird nur ein Element zur Hälfte seiner Dicke geschnitten,
        während das andere Element vollständig durchgeschnitten wird.
        
        Args:
            aElementIds: Liste der Element-IDs für Halbes Blatt (mindestens 2)
            aCutParams: Optionale Schnitt-Parameter (cut_depth, master_element, etc.)
        
        Returns:
            dict: Status der Halbes Blatt-Operation
        """
        try:
            # Validierung
            if not isinstance(aElementIds, list) or len(aElementIds) < 2:
                return {"status": "error", "message": "At least 2 element IDs required for half lap cut"}
            
            lValidatedIds = [self.validate_element_id(lId) for lId in aElementIds]
            
            # Standard-Parameter wenn nicht angegeben
            if aCutParams is None:
                aCutParams = {
                    "master_element": lValidatedIds[0],  # Erstes Element als Master
                    "cut_depth_ratio": 0.5,             # 50% der Elementdicke
                    "cut_position": "end"                # Position des Schnitts
                }
            
            # Command senden
            return self.send_command("cut_half_lap", {
                "element_ids": lValidatedIds,
                "cut_params": aCutParams
            })
            
        except Exception as e:
            return {"status": "error", "message": f"cut_half_lap failed: {e}"}
    
    async def cut_double_tenon(self, aElementIds: list, aCutParams: dict = None) -> dict:
        """
        Erstellt Doppelzapfen-Verbindung zwischen Elementen
        
        Diese Verbindung erstellt zwei parallele Zapfen an einem Element
        und entsprechende Nuten am anderen Element.
        
        Args:
            aElementIds: Liste der Element-IDs für Doppelzapfen (genau 2 Elemente)
            aCutParams: Optionale Schnitt-Parameter (tenon_width, tenon_height, spacing, etc.)
        
        Returns:
            dict: Status der Doppelzapfen-Operation
        """
        try:
            # Validierung
            if not isinstance(aElementIds, list) or len(aElementIds) != 2:
                return {"status": "error", "message": "Exactly 2 element IDs required for double tenon cut"}
            
            lValidatedIds = [self.validate_element_id(lId) for lId in aElementIds]
            
            # Standard-Parameter wenn nicht angegeben
            if aCutParams is None:
                aCutParams = {
                    "tenon_element": lValidatedIds[0],    # Element mit Zapfen
                    "mortise_element": lValidatedIds[1],  # Element mit Nuten
                    "tenon_width": 40,                    # Breite der Zapfen (mm)
                    "tenon_height": 80,                   # Höhe der Zapfen (mm)
                    "tenon_spacing": 60,                  # Abstand zwischen Zapfen (mm)
                    "tenon_depth": 50                     # Tiefe der Zapfen (mm)
                }
            
            # Command senden
            return self.send_command("cut_double_tenon", {
                "element_ids": lValidatedIds,
                "cut_params": aCutParams
            })
            
        except Exception as e:
            return {"status": "error", "message": f"cut_double_tenon failed: {e}"}
    
    async def cut_scarf_joint(self, aElementIds: list, aCutParams: dict = None) -> dict:
        """
        Erstellt Stoßverbindung zwischen Elementen
        
        Stoßverbindungen werden verwendet um Balken zu verlängern oder
        zwei Balken nahtlos miteinander zu verbinden.
        
        Args:
            aElementIds: Liste der Element-IDs für Stoßverbindung (genau 2 Elemente)
            aCutParams: Optionale Schnitt-Parameter (scarf_type, scarf_length, angle, etc.)
        
        Returns:
            dict: Status der Stoßverbindung-Operation
        """
        try:
            # Validierung
            if not isinstance(aElementIds, list) or len(aElementIds) != 2:
                return {"status": "error", "message": "Exactly 2 element IDs required for scarf joint"}
            
            lValidatedIds = [self.validate_element_id(lId) for lId in aElementIds]
            
            # Standard-Parameter wenn nicht angegeben
            if aCutParams is None:
                aCutParams = {
                    "scarf_type": "plain_scarf",        # Art der Stoßverbindung
                    "scarf_length": 400,                # Länge der Stoßverbindung (mm)
                    "scarf_angle": 30,                  # Winkel des Schnitts (Grad)
                    "element_1": lValidatedIds[0],      # Erstes Element
                    "element_2": lValidatedIds[1],      # Zweites Element
                    "overlap_length": 50                # Überlappungslänge (mm)
                }
            
            # Command senden
            return self.send_command("cut_scarf_joint", {
                "element_ids": lValidatedIds,
                "cut_params": aCutParams
            })
            
        except Exception as e:
            return {"status": "error", "message": f"cut_scarf_joint failed: {e}"}
    
    async def cut_shoulder(self, aElementIds: list, aCutParams: dict = None) -> dict:
        """
        Erstellt Schulterschnitt zwischen Elementen
        
        Schulterschnitte werden für tragende Verbindungen verwendet,
        bei denen ein Element auf einem anderen aufliegt.
        
        Args:
            aElementIds: Liste der Element-IDs für Schulterschnitt (mindestens 2)
            aCutParams: Optionale Schnitt-Parameter (shoulder_depth, shoulder_width, etc.)
        
        Returns:
            dict: Status der Schulterschnitt-Operation
        """
        try:
            # Validierung
            if not isinstance(aElementIds, list) or len(aElementIds) < 2:
                return {"status": "error", "message": "At least 2 element IDs required for shoulder cut"}
            
            lValidatedIds = [self.validate_element_id(lId) for lId in aElementIds]
            
            # Standard-Parameter wenn nicht angegeben
            if aCutParams is None:
                aCutParams = {
                    "supporting_element": lValidatedIds[0],   # Tragendes Element (unten)
                    "supported_element": lValidatedIds[1],    # Getragenes Element (oben)
                    "shoulder_depth": 40,                     # Tiefe der Schulter (mm)
                    "shoulder_width": 120,                    # Breite der Schulter (mm)
                    "shoulder_type": "simple_shoulder",       # Art des Schulterschnitts
                    "contact_angle": 90                       # Kontaktwinkel (Grad)
                }
            
            # Command senden
            return self.send_command("cut_shoulder", {
                "element_ids": lValidatedIds,
                "cut_params": aCutParams
            })
            
        except Exception as e:
            return {"status": "error", "message": f"cut_shoulder failed: {e}"}
    
    async def create_auxiliary_beam_points(self, aP1: list, aP2: list, aP3: list = None) -> dict:
        """
        Erstellt ein Hilfs-Balkenelement zwischen zwei Punkten
        
        Hilfselemente werden für Konstruktionszwecke verwendet und können später
        in reguläre Balken konvertiert werden.
        
        Args:
            aP1: Startpunkt [x, y, z] in mm
            aP2: Endpunkt [x, y, z] in mm  
            aP3: Optionaler Orientierungspunkt [x, y, z] in mm
        
        Returns:
            dict: Element-ID und Informationen über das erstellte Hilfselement
        """
        try:
            # Punkte validieren
            lP1 = self.validate_point_3d(aP1, "p1")
            lP2 = self.validate_point_3d(aP2, "p2")
            lP3 = self.validate_point_3d(aP3, "p3") if aP3 is not None else None
            
            # Command senden
            return self.send_command("create_auxiliary_beam_points", {
                "p1": lP1,
                "p2": lP2,
                "p3": lP3
            })
            
        except Exception as e:
            return {"status": "error", "message": f"create_auxiliary_beam_points failed: {e}"}
    
    async def convert_beam_to_panel(self, aElementIds: list) -> dict:
        """
        Konvertiert Balken-Elemente zu Platten-Elementen
        
        Die Geometrie wird dabei entsprechend angepasst. Breite wird zur Dicke,
        Höhe wird zur Breite der resultierenden Platte.
        
        Args:
            aElementIds: Liste von Element-IDs die konvertiert werden sollen
        
        Returns:
            dict: Informationen über die Konvertierung und neue Element-IDs
        """
        try:
            # Element-IDs validieren
            lValidatedIds = []
            for lId in aElementIds:
                lValidatedIds.append(self.validate_element_id(lId))
            
            if not lValidatedIds:
                return {"status": "error", "message": "No valid element IDs provided"}
            
            # Command senden
            return self.send_command("convert_beam_to_panel", {
                "element_ids": lValidatedIds
            })
            
        except Exception as e:
            return {"status": "error", "message": f"convert_beam_to_panel failed: {e}"}
    
    async def convert_panel_to_beam(self, aElementIds: list) -> dict:
        """
        Konvertiert Platten-Elemente zu Balken-Elementen
        
        Die Geometrie wird dabei entsprechend angepasst. Dicke wird zur Breite,
        Breite wird zur Höhe des resultierenden Balkens.
        
        Args:
            aElementIds: Liste von Element-IDs die konvertiert werden sollen
        
        Returns:
            dict: Informationen über die Konvertierung und neue Element-IDs
        """
        try:
            # Element-IDs validieren
            lValidatedIds = []
            for lId in aElementIds:
                lValidatedIds.append(self.validate_element_id(lId))
            
            if not lValidatedIds:
                return {"status": "error", "message": "No valid element IDs provided"}
            
            # Command senden
            return self.send_command("convert_panel_to_beam", {
                "element_ids": lValidatedIds
            })
            
        except Exception as e:
            return {"status": "error", "message": f"convert_panel_to_beam failed: {e}"}
    
    async def convert_auxiliary_to_beam(self, aElementIds: list) -> dict:
        """
        Konvertiert Auxiliary-Elemente zu regulären Balken-Elementen
        
        Hilfselemente werden zu vollwertigen Balken mit allen Eigenschaften
        konvertiert. Geometrie bleibt dabei erhalten.
        
        Args:
            aElementIds: Liste von Auxiliary Element-IDs die konvertiert werden sollen
        
        Returns:
            dict: Informationen über die Konvertierung und neue Element-IDs
        """
        try:
            # Element-IDs validieren
            lValidatedIds = []
            for lId in aElementIds:
                lValidatedIds.append(self.validate_element_id(lId))
            
            if not lValidatedIds:
                return {"status": "error", "message": "No valid element IDs provided"}
            
            # Command senden
            return self.send_command("convert_auxiliary_to_beam", {
                "element_ids": lValidatedIds
            })
            
        except Exception as e:
            return {"status": "error", "message": f"convert_auxiliary_to_beam failed: {e}"}
    
    async def create_auto_container_from_standard(self, aElementIds: list, aContainerName: str) -> dict:
        """
        Erstellt automatisch einen Container aus Standard-Elementen
        
        Container sind Baugruppen die mehrere Elemente zusammenfassen.
        Useful für Organisation komplexer Strukturen und Bauteile.
        
        Args:
            aElementIds: Liste von Element-IDs die in den Container sollen
            aContainerName: Name des zu erstellenden Containers
        
        Returns:
            dict: Container-ID und Informationen über erstellten Container
        """
        try:
            # Element-IDs validieren
            lValidatedIds = []
            for lId in aElementIds:
                lValidatedIds.append(self.validate_element_id(lId))
            
            if not lValidatedIds:
                return {"status": "error", "message": "No valid element IDs provided"}
            
            # Container-Name validieren
            if not isinstance(aContainerName, str) or not aContainerName.strip():
                return {"status": "error", "message": "Container name must be a non-empty string"}
            
            # Command senden
            return self.send_command("create_auto_container_from_standard", {
                "element_ids": lValidatedIds,
                "container_name": aContainerName.strip()
            })
            
        except Exception as e:
            return {"status": "error", "message": f"create_auto_container_from_standard failed: {e}"}
    
    async def get_container_content_elements(self, aContainerId: int) -> dict:
        """
        Ruft alle Elemente eines Containers ab
        
        Gibt eine Liste aller Element-IDs zurück, die in dem angegebenen
        Container enthalten sind.
        
        Args:
            aContainerId: ID des Containers dessen Inhalt abgerufen werden soll
        
        Returns:
            dict: Liste der Element-IDs und Container-Informationen
        """
        try:
            # Container-ID validieren
            lValidatedId = self.validate_element_id(aContainerId)
            
            # Command senden
            return self.send_command("get_container_content_elements", {
                "container_id": lValidatedId
            })
            
        except Exception as e:
            return {"status": "error", "message": f"get_container_content_elements failed: {e}"}
