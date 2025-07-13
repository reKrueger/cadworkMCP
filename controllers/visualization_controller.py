"""
Visualization Controller für Cadwork MCP Server
Verwaltet Farben, Transparenz und Sichtbarkeit von Elementen
"""
from .base_controller import BaseController

class CVisualizationController(BaseController):
    """Controller für Visualization-Operationen"""
    
    def __init__(self) -> None:
        super().__init__("VisualizationController")
    
    async def set_color(self, aElementIds: list, aColorId: int) -> dict:
        """
        Setzt die Farbe für eine Liste von Elementen
        
        Args:
            aElementIds: Liste der Element-IDs
            aColorId: Farb-ID (1-255, siehe Cadwork Farbpalette)
        
        Returns:
            dict: Status der Operation
        """
        try:
            # Validierung
            if not isinstance(aElementIds, list) or not aElementIds:
                return {"status": "error", "message": "element_ids must be a non-empty list"}
            
            lValidatedIds = [self.validate_element_id(lId) for lId in aElementIds]
            
            if not isinstance(aColorId, int) or aColorId < 1 or aColorId > 255:
                return {"status": "error", "message": "color_id must be an integer between 1 and 255"}
            
            # Command senden
            return self.send_command("set_color", {
                "element_ids": lValidatedIds,
                "color_id": aColorId
            })
            
        except Exception as e:
            return {"status": "error", "message": f"set_color failed: {e}"}
    
    async def set_visibility(self, aElementIds: list, aVisible: bool) -> dict:
        """
        Setzt die Sichtbarkeit für eine Liste von Elementen
        
        Args:
            aElementIds: Liste der Element-IDs  
            aVisible: True = sichtbar, False = ausgeblendet
        
        Returns:
            dict: Status der Operation
        """
        try:
            # Validierung
            if not isinstance(aElementIds, list) or not aElementIds:
                return {"status": "error", "message": "element_ids must be a non-empty list"}
            
            lValidatedIds = [self.validate_element_id(lId) for lId in aElementIds]
            
            if not isinstance(aVisible, bool):
                return {"status": "error", "message": "visible must be a boolean (True/False)"}
            
            # Command senden
            return self.send_command("set_visibility", {
                "element_ids": lValidatedIds,
                "visible": aVisible
            })
            
        except Exception as e:
            return {"status": "error", "message": f"set_visibility failed: {e}"}
    
    async def set_transparency(self, aElementIds: list, aTransparency: int) -> dict:
        """
        Setzt die Transparenz für eine Liste von Elementen
        
        Args:
            aElementIds: Liste der Element-IDs
            aTransparency: Transparenz-Wert (0-100, 0=undurchsichtig, 100=vollständig transparent)
        
        Returns:
            dict: Status der Operation
        """
        try:
            # Validierung
            if not isinstance(aElementIds, list) or not aElementIds:
                return {"status": "error", "message": "element_ids must be a non-empty list"}
            
            lValidatedIds = [self.validate_element_id(lId) for lId in aElementIds]
            
            if not isinstance(aTransparency, int) or aTransparency < 0 or aTransparency > 100:
                return {"status": "error", "message": "transparency must be an integer between 0 and 100"}
            
            # Command senden
            return self.send_command("set_transparency", {
                "element_ids": lValidatedIds,
                "transparency": aTransparency
            })
            
        except Exception as e:
            return {"status": "error", "message": f"set_transparency failed: {e}"}
    
    async def get_color(self, aElementId: int) -> dict:
        """
        Ruft die Farbe eines Elements ab
        
        Args:
            aElementId: Element-ID
        
        Returns:
            dict: Farb-ID und Farb-Information
        """
        try:
            # Validierung
            lValidatedId = self.validate_element_id(aElementId)
            
            # Command senden
            return self.send_command("get_color", {
                "element_id": lValidatedId
            })
            
        except Exception as e:
            return {"status": "error", "message": f"get_color failed: {e}"}
    
    async def get_transparency(self, aElementId: int) -> dict:
        """
        Ruft die Transparenz eines Elements ab
        
        Args:
            aElementId: Element-ID
        
        Returns:
            dict: Transparenz-Wert (0-100)
        """
        try:
            # Validierung
            lValidatedId = self.validate_element_id(aElementId)
            
            # Command senden
            return self.send_command("get_transparency", {
                "element_id": lValidatedId
            })
            
        except Exception as e:
            return {"status": "error", "message": f"get_transparency failed: {e}"}
    
    async def show_all_elements(self) -> dict:
        """
        Macht alle Elemente im Modell sichtbar
        
        Returns:
            dict: Status der Operation mit Anzahl betroffener Elemente
        """
        try:
            # Command senden
            return self.send_command("show_all_elements", {})
            
        except Exception as e:
            return {"status": "error", "message": f"show_all_elements failed: {e}"}
    
    async def hide_all_elements(self) -> dict:
        """
        Blendet alle Elemente im Modell aus
        
        Returns:
            dict: Status der Operation mit Anzahl betroffener Elemente
        """
        try:
            # Command senden
            return self.send_command("hide_all_elements", {})
            
        except Exception as e:
            return {"status": "error", "message": f"hide_all_elements failed: {e}"}
    
    async def refresh_display(self) -> dict:
        """
        Aktualisiert das Display/Viewport nach Änderungen
        
        Returns:
            dict: Status der Display-Aktualisierung
        """
        try:
            # Command senden
            return self.send_command("refresh_display", {})
            
        except Exception as e:
            return {"status": "error", "message": f"refresh_display failed: {e}"}
    
    async def get_visible_element_count(self) -> dict:
        """
        Ermittelt die Anzahl aktuell sichtbarer Elemente
        
        Returns:
            dict: Anzahl sichtbarer Elemente + Statistiken
        """
        try:
            # Command senden
            return self.send_command("get_visible_element_count", {})
            
        except Exception as e:
            return {"status": "error", "message": f"get_visible_element_count failed: {e}"}
