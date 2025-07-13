"""
Utility Controller für Cadwork MCP Server
Verwaltet Display-Refresh, Ausgabe-Funktionen und System-Utilities
"""
from .base_controller import BaseController

class CUtilityController(BaseController):
    """Controller für Utility-Operationen"""
    
    def __init__(self):
        super().__init__("UtilityController")
    
    async def disable_auto_display_refresh(self) -> dict:
        """
        Deaktiviert die automatische Display-Aktualisierung
        
        Wichtig für Performance bei vielen aufeinanderfolgenden Operationen.
        Sollte nach den Operationen wieder mit enable_auto_display_refresh() aktiviert werden.
        
        Returns:
            dict: Status der Operation
        """
        try:
            # Command senden
            return self.send_command("disable_auto_display_refresh", {})
            
        except Exception as e:
            return {"status": "error", "message": f"disable_auto_display_refresh failed: {e}"}
    
    async def enable_auto_display_refresh(self) -> dict:
        """
        Aktiviert die automatische Display-Aktualisierung wieder
        
        Sollte nach Batch-Operationen aufgerufen werden, um die normale
        Anzeige-Aktualisierung zu reaktivieren.
        
        Returns:
            dict: Status der Operation
        """
        try:
            # Command senden  
            return self.send_command("enable_auto_display_refresh", {})
            
        except Exception as e:
            return {"status": "error", "message": f"enable_auto_display_refresh failed: {e}"}
    
    async def print_error(self, aMessage: str) -> dict:
        """
        Gibt eine Fehlermeldung in Cadwork aus
        
        Args:
            aMessage: Fehlermeldung die in Cadwork angezeigt werden soll
        
        Returns:
            dict: Status der Operation
        """
        try:
            # Validierung
            if not isinstance(aMessage, str) or not aMessage.strip():
                return {"status": "error", "message": "message must be a non-empty string"}
            
            # Command senden
            return self.send_command("print_error", {
                "message": aMessage.strip()
            })
            
        except Exception as e:
            return {"status": "error", "message": f"print_error failed: {e}"}
    
    async def print_warning(self, aMessage: str) -> dict:
        """
        Gibt eine Warnmeldung in Cadwork aus
        
        Args:
            aMessage: Warnmeldung die in Cadwork angezeigt werden soll
        
        Returns:
            dict: Status der Operation
        """
        try:
            # Validierung
            if not isinstance(aMessage, str) or not aMessage.strip():
                return {"status": "error", "message": "message must be a non-empty string"}
            
            # Command senden
            return self.send_command("print_warning", {
                "message": aMessage.strip()
            })
            
        except Exception as e:
            return {"status": "error", "message": f"print_warning failed: {e}"}
    
    async def get_3d_file_path(self) -> dict:
        """
        Ruft den Pfad der aktuell geöffneten 3D-Datei ab
        
        Returns:
            dict: Dateipfad und Datei-Informationen
        """
        try:
            # Command senden
            return self.send_command("get_3d_file_path", {})
            
        except Exception as e:
            return {"status": "error", "message": f"get_3d_file_path failed: {e}"}
    
    async def get_project_data(self) -> dict:
        """
        Ruft allgemeine Projektdaten ab
        
        Returns:
            dict: Projekt-Informationen wie Name, Pfad, etc.
        """
        try:
            # Command senden
            return self.send_command("get_project_data", {})
            
        except Exception as e:
            return {"status": "error", "message": f"get_project_data failed: {e}"}
