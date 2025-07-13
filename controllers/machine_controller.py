"""
Machine Controller für Cadwork MCP Server
Verwaltet CNC- und fertigungsspezifische Funktionen für Produktionsplanung
"""
from .base_controller import BaseController

class CMachineController(BaseController):
    """Controller für Machine/CNC-Operationen"""
    
    def __init__(self) -> None:
        super().__init__("MachineController")
    
    async def check_production_list_discrepancies(self, aProductionListId: int) -> dict:
        """
        Überprüft Produktionslisten auf Unstimmigkeiten und Konflikte
        
        Analysiert Produktionslisten auf mögliche Probleme wie fehlende Elemente,
        inkonsistente Maße, Materialfehler oder CNC-Bearbeitungskonflikte.
        Essentiell für qualitätsgesicherte Fertigung.
        
        Args:
            aProductionListId: ID der Produktionsliste die überprüft werden soll
        
        Returns:
            dict: Detaillierte Analyse mit gefundenen Unstimmigkeiten und Empfehlungen
        """
        try:
            # Production List ID validieren
            if not isinstance(aProductionListId, int) or aProductionListId <= 0:
                return {"status": "error", "message": "Production list ID must be a positive integer"}
            
            # Command senden
            return self.send_command("check_production_list_discrepancies", {
                "production_list_id": aProductionListId
            })
            
        except Exception as e:
            return {"status": "error", "message": f"check_production_list_discrepancies failed: {e}"}
