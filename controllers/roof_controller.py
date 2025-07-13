"""
Roof Controller für Cadwork MCP Server
Verwaltet Dach-spezifische CAD-Funktionen für Zimmerei und Dachbau
"""
from .base_controller import BaseController

class CRoofController(BaseController):
    """Controller für Roof/Dach-Operationen"""
    
    def __init__(self):
        super().__init__("RoofController")
    
    async def get_roof_surfaces(self, aElementIds: list) -> dict:
        """
        Ruft Dachflächen-Informationen für angegebene Elemente ab
        
        Analysiert Dach-Elemente und gibt detaillierte Informationen über
        Dachflächen, Neigungen, Orientierungen und geometrische Eigenschaften zurück.
        
        Args:
            aElementIds: Liste von Element-IDs die als Dach-Elemente analysiert werden sollen
        
        Returns:
            dict: Detaillierte Dachflächen-Informationen (Neigungen, Orientierungen, Flächen)
        """
        try:
            # Element-IDs validieren
            lValidatedIds = []
            for lId in aElementIds:
                lValidatedIds.append(self.validate_element_id(lId))
            
            if not lValidatedIds:
                return {"status": "error", "message": "No valid element IDs provided"}
            
            # Command senden
            return self.send_command("get_roof_surfaces", {
                "element_ids": lValidatedIds
            })
            
        except Exception as e:
            return {"status": "error", "message": f"get_roof_surfaces failed: {e}"}
    
    async def calculate_roof_area(self, aRoofElementIds: list) -> dict:
        """
        Berechnet die Gesamtdachfläche für angegebene Dach-Elemente
        
        Führt spezielle Dachflächen-Berechnungen durch, die Neigungen,
        Überstände und komplexe Dachgeometrien berücksichtigen.
        
        Args:
            aRoofElementIds: Liste von Dach-Element-IDs für Flächenberechnung
        
        Returns:
            dict: Dachflächen-Berechnungen (Grundfläche, geneigte Fläche, Faktoren)
        """
        try:
            # Element-IDs validieren
            lValidatedIds = []
            for lId in aRoofElementIds:
                lValidatedIds.append(self.validate_element_id(lId))
            
            if not lValidatedIds:
                return {"status": "error", "message": "No valid roof element IDs provided"}
            
            # Command senden
            return self.send_command("calculate_roof_area", {
                "roof_element_ids": lValidatedIds
            })
            
        except Exception as e:
            return {"status": "error", "message": f"calculate_roof_area failed: {e}"}
