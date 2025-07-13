"""
Shop Drawing Controller für Cadwork MCP Server
Verwaltet Werkstattzeichnungs-spezifische Funktionen für Fertigungsplanung
"""
from .base_controller import BaseController

class CShopDrawingController(BaseController):
    """Controller für Shop Drawing Operationen"""
    
    def __init__(self):
        super().__init__("ShopDrawingController")
    
    async def add_wall_section_x(self, aWallId: int, aSectionParams: dict = None) -> dict:
        """
        Fügt einen Wandschnitt in X-Richtung hinzu
        
        Erstellt technische Schnittdarstellungen für Werkstattzeichnungen.
        X-Richtung bedeutet Schnitt parallel zur X-Achse.
        
        Args:
            aWallId: ID des Wand-Elements für den Schnitt
            aSectionParams: Optionale Parameter für Schnitt-Konfiguration
                          (Position, Tiefe, Darstellungsoptionen, etc.)
        
        Returns:
            dict: Informationen über erstellten Wandschnitt
        """
        try:
            # Wall-ID validieren
            lValidatedId = self.validate_element_id(aWallId)
            
            # Section-Parameter standardisieren
            lSectionParams = aSectionParams if aSectionParams is not None else {}
            
            # Command senden
            return self.send_command("add_wall_section_x", {
                "wall_id": lValidatedId,
                "section_params": lSectionParams
            })
            
        except Exception as e:
            return {"status": "error", "message": f"add_wall_section_x failed: {e}"}
    
    async def add_wall_section_y(self, aWallId: int, aSectionParams: dict = None) -> dict:
        """
        Fügt einen Wandschnitt in Y-Richtung hinzu
        
        Erstellt technische Schnittdarstellungen für Werkstattzeichnungen.
        Y-Richtung bedeutet Schnitt parallel zur Y-Achse.
        
        Args:
            aWallId: ID des Wand-Elements für den Schnitt
            aSectionParams: Optionale Parameter für Schnitt-Konfiguration
                          (Position, Tiefe, Darstellungsoptionen, etc.)
        
        Returns:
            dict: Informationen über erstellten Wandschnitt
        """
        try:
            # Wall-ID validieren
            lValidatedId = self.validate_element_id(aWallId)
            
            # Section-Parameter standardisieren
            lSectionParams = aSectionParams if aSectionParams is not None else {}
            
            # Command senden
            return self.send_command("add_wall_section_y", {
                "wall_id": lValidatedId,
                "section_params": lSectionParams
            })
            
        except Exception as e:
            return {"status": "error", "message": f"add_wall_section_y failed: {e}"}
