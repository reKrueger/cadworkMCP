"""
Utility operation handlers
"""
from typing import Dict, Any

def handle_ping(args: Dict[str, Any]) -> Dict[str, Any]:
    """Handle ping command"""
    return {"status": "ok", "message": "pong"}

def handle_get_version_info(args: Dict[str, Any]) -> Dict[str, Any]:
    """Handle get version info command"""
    try:
        # Import here to avoid import-time errors
        import utility_controller as uc
        cw_version = str(uc.get_3d_version())
        return {
            "status": "ok", 
            "cw_version": cw_version, 
            "plugin_version": "0.2.0"
        }
    except ImportError as e:
        return {
            "status": "error", 
            "message": f"Failed to import Cadwork modules: {e}"
        }
    except Exception as e:
        return {
            "status": "error", 
            "message": f"Failed to get version info: {e}"
        }

def handle_get_model_name(args: Dict[str, Any]) -> Dict[str, Any]:
    """Handle get model name command"""
    try:
        # Import here to avoid import-time errors
        import utility_controller as uc
        model_name = uc.get_3d_file_name()
        return {
            "status": "ok", 
            "name": model_name or "(unsaved model)"
        }
    except ImportError as e:
        return {
            "status": "error", 
            "message": f"Failed to import Cadwork modules: {e}"
        }
    except Exception as e:
        return {
            "status": "error", 
            "message": f"Failed to get model name: {e}"
        }
