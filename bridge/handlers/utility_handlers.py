"""
Utility Handler for Cadwork Bridge
Processes Display-Refresh and System-Utilities
"""
from typing import Dict, Any

def handle_ping(params: Dict[str, Any]) -> Dict[str, Any]:
    """Ping handler for connection testing"""
    return {
        "status": "ok",
        "message": "pong",
        "operation": "ping"
    }

def handle_get_version_info(params: Dict[str, Any]) -> Dict[str, Any]:
    """Get version info handler"""
    return handle_get_cadwork_version_info(params)

def handle_get_model_name(params: Dict[str, Any]) -> Dict[str, Any]:
    """Get model name handler"""
    try:
        import utility_controller as uc
        
        # Try to get the file path and extract model name
        file_path = uc.get_file_path()
        
        if file_path:
            import os
            model_name = os.path.splitext(os.path.basename(file_path))[0]
        else:
            model_name = "Unknown"
        
        return {
            "status": "success",
            "model_name": model_name,
            "operation": "get_model_name"
        }
        
    except Exception as e:
        return {"status": "error", "message": f"get_model_name failed: {e}"}

def handle_disable_auto_display_refresh(params: Dict[str, Any]) -> Dict[str, Any]:
    """Disable automatic display refresh"""
    try:
        import utility_controller as uc
        
        # Call Cadwork API
        uc.disable_auto_display_refresh()
        
        return {
            "status": "success", 
            "message": "Auto display refresh disabled",
            "operation": "disable_auto_display_refresh",
            "note": "Remember to enable it again after batch operations"
        }
        
    except Exception as e:
        return {"status": "error", "message": f"disable_auto_display_refresh failed: {e}"}

def handle_enable_auto_display_refresh(params: Dict[str, Any]) -> Dict[str, Any]:
    """Enable automatic display refresh"""
    try:
        import utility_controller as uc
        
        # Call Cadwork API
        uc.enable_auto_display_refresh()
        
        return {
            "status": "success",
            "message": "Auto display refresh enabled"
        }        
    except Exception as e:
        return {"status": "error", "message": f"enable_auto_display_refresh failed: {e}"}

def handle_print_error(params: Dict[str, Any]) -> Dict[str, Any]:
    """Display error message in Cadwork"""
    try:
        import utility_controller as uc
        
        message = params.get("message")
        
        if not isinstance(message, str) or not message.strip():
            return {"status": "error", "message": "message must be a non-empty string"}
        
        # Call Cadwork API
        uc.print_error(message.strip())
        
        return {
            "status": "success",
            "message": f"Error message displayed: {message}",
            "operation": "print_error"
        }
        
    except Exception as e:
        return {"status": "error", "message": f"print_error failed: {e}"}

def handle_print_warning(params: Dict[str, Any]) -> Dict[str, Any]:
    """Display warning message in Cadwork"""
    try:
        import utility_controller as uc
        
        message = params.get("message")
        
        if not isinstance(message, str) or not message.strip():
            return {"status": "error", "message": "message must be a non-empty string"}
        
        # Call Cadwork API
        uc.print_warning(message.strip())
        
        return {
            "status": "success",
            "message": f"Warning message displayed: {message}",
            "operation": "print_warning"
        }
        
    except Exception as e:
        return {"status": "error", "message": f"print_warning failed: {e}"}

def handle_get_3d_file_path(params: Dict[str, Any]) -> Dict[str, Any]:
    """Get path of currently opened 3D file"""
    try:
        import utility_controller as uc
        
        # Call Cadwork API
        file_path = uc.get_3d_file_path()
        
        return {
            "status": "success",
            "file_path": file_path,
            "operation": "get_3d_file_path"
        }
        
    except Exception as e:
        return {"status": "error", "message": f"get_3d_file_path failed: {e}"}

def handle_get_project_data(params: Dict[str, Any]) -> Dict[str, Any]:
    """Get general project data"""
    try:
        import utility_controller as uc
        
        # Call Cadwork API
        project_data = uc.get_project_data()
        
        return {
            "status": "success",
            "project_data": project_data,
            "operation": "get_project_data"
        }
        
    except Exception as e:
        return {"status": "error", "message": f"get_project_data failed: {e}"}

def handle_get_cadwork_version_info(params: Dict[str, Any]) -> Dict[str, Any]:
    """Get Cadwork version information"""
    try:
        import utility_controller as uc
        
        # Call Cadwork API
        version_info = uc.get_cadwork_version_info()
        
        return {
            "status": "success",
            "version_info": version_info,
            "operation": "get_cadwork_version_info"
        }
        
    except Exception as e:
        return {"status": "error", "message": f"get_cadwork_version_info failed: {e}"}
