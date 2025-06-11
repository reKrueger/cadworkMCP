"""
Base controller with common functionality
"""
from typing import Dict, Any
from core.connection import get_connection
from core.logging import log_info, log_error

class BaseController:
    """Base class for all controllers with common functionality"""
    
    def __init__(self, controller_name: str):
        self.controller_name = controller_name
    
    def send_command(self, operation: str, args: Dict[str, Any] = None) -> Dict[str, Any]:
        """Send command to Cadwork and handle common error cases"""
        try:
            connection = get_connection()
            response = connection.send_command(operation, args or {})
            
            if response.get("status") == "ok":
                log_info(f"{self.controller_name}: {operation} completed successfully")
            else:
                log_error(f"{self.controller_name}: {operation} failed - {response.get('message')}")
            
            return response
            
        except ConnectionError as e:
            log_error(f"{self.controller_name}: Connection error - {e}")
            return {"status": "error", "message": f"Connection failed: {e}"}
        except TimeoutError as e:
            log_error(f"{self.controller_name}: Timeout error - {e}")
            return {"status": "error", "message": f"Operation timed out: {e}"}
        except Exception as e:
            log_error(f"{self.controller_name}: Unexpected error - {e}")
            return {"status": "error", "message": f"Unexpected error: {e}"}
    
    def validate_required_args(self, args: Dict[str, Any], required: list) -> None:
        """Validate that all required arguments are present"""
        missing = [key for key in required if key not in args]
        if missing:
            raise ValueError(f"Missing required arguments: {missing}")
    
    def validate_element_id(self, element_id: Any) -> int:
        """Validate and convert element ID"""
        try:
            id_val = int(element_id)
            if id_val < 0:
                raise ValueError(f"Element ID must be non-negative, got: {id_val}")
            return id_val
        except (ValueError, TypeError):
            raise ValueError(f"Invalid element ID: {element_id}")
