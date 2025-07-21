# bridge/handlers/base_handler.py  
"""
Basis-Handler mit einheitlicher Controller-Nutzung
"""
from typing import Dict, Any
from ..controller_manager import call_cadwork_function

class BaseHandler:
    """Basis-Klasse für alle Handler"""
    
    @staticmethod
    def safe_call(function_name: str, *args, **kwargs) -> Dict[str, Any]:
        """
        Sichere Controller-Aufrufe mit einheitlicher Fehlerbehandlung
        
        Args:
            function_name: Name der Cadwork-Funktion
            *args, **kwargs: Parameter für die Funktion
            
        Returns:
            Standardisierte Response mit status/message/data
        """
        try:
            result = call_cadwork_function(function_name, *args, **kwargs)
            return {
                "status": "success",
                "data": result,
                "function": function_name
            }
        except AttributeError as e:
            return {
                "status": "error",
                "message": f"Function not found: {e}",
                "function": function_name
            }
        except Exception as e:
            return {
                "status": "error", 
                "message": f"API error: {e}",
                "function": function_name
            }

def validate_element_ids(element_ids):
    """Validiert Element-IDs"""
    if not isinstance(element_ids, list):
        raise ValueError("element_ids must be a list")
    if not element_ids:
        raise ValueError("element_ids cannot be empty")
    return [int(eid) for eid in element_ids]
