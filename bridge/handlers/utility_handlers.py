"""
Utility Handler für Cadwork Bridge
Verarbeitet Display-Refresh und System-Utilities
"""

def handle_disable_auto_display_refresh(aParams: dict) -> dict:
    """Deaktiviert automatische Display-Aktualisierung"""
    try:
        import utility_controller as uc
        
        # Cadwork API aufrufen
        uc.disable_auto_display_refresh()
        
        return {
            "status": "success",
            "message": "Auto display refresh disabled",
            "operation": "disable_auto_display_refresh",
            "note": "Remember to enable it again after batch operations"
        }
        
    except Exception as e:
        return {"status": "error", "message": f"disable_auto_display_refresh failed: {e}"}

def handle_enable_auto_display_refresh(aParams: dict) -> dict:
    """Aktiviert automatische Display-Aktualisierung"""
    try:
        import utility_controller as uc
        
        # Cadwork API aufrufen
        uc.enable_auto_display_refresh()
        
        return {
            "status": "success",
            "message": "Auto display refresh enabled",
            "operation": "enable_auto_display_refresh"
        }
        
    except Exception as e:
        return {"status": "error", "message": f"enable_auto_display_refresh failed: {e}"}

def handle_print_error(aParams: dict) -> dict:
    """Gibt Fehlermeldung in Cadwork aus"""
    try:
        import utility_controller as uc
        
        lMessage = aParams.get("message")
        
        if not lMessage:
            return {"status": "error", "message": "No message provided"}
        
        # Cadwork API aufrufen
        uc.print_error(lMessage)
        
        return {
            "status": "success",
            "message": f"Error message displayed in Cadwork: '{lMessage}'",
            "displayed_message": lMessage,
            "operation": "print_error"
        }
        
    except Exception as e:
        return {"status": "error", "message": f"print_error failed: {e}"}

def handle_print_warning(aParams: dict) -> dict:
    """Gibt Warnmeldung in Cadwork aus"""
    try:
        import utility_controller as uc
        
        lMessage = aParams.get("message")
        
        if not lMessage:
            return {"status": "error", "message": "No message provided"}
        
        # Cadwork API aufrufen
        uc.print_warning(lMessage)
        
        return {
            "status": "success",
            "message": f"Warning message displayed in Cadwork: '{lMessage}'",
            "displayed_message": lMessage,
            "operation": "print_warning"
        }
        
    except Exception as e:
        return {"status": "error", "message": f"print_warning failed: {e}"}

def handle_get_3d_file_path(aParams: dict) -> dict:
    """Ruft Pfad der 3D-Datei ab"""
    try:
        import utility_controller as uc
        
        # Cadwork API aufrufen
        lFilePath = uc.get_3d_file_path()
        
        # Pfad-Informationen extrahieren
        import os
        lFileName = os.path.basename(lFilePath) if lFilePath else ""
        lDirectory = os.path.dirname(lFilePath) if lFilePath else ""
        lFileExists = os.path.exists(lFilePath) if lFilePath else False
        
        return {
            "status": "success",
            "file_path": lFilePath,
            "file_name": lFileName,
            "directory": lDirectory,
            "file_exists": lFileExists,
            "operation": "get_3d_file_path"
        }
        
    except Exception as e:
        return {"status": "error", "message": f"get_3d_file_path failed: {e}"}

def handle_get_project_data(aParams: dict) -> dict:
    """Ruft Projektdaten ab"""
    try:
        import utility_controller as uc
        
        # Cadwork API aufrufen
        lProjectData = uc.get_project_data()
        
        return {
            "status": "success",
            "project_data": lProjectData,
            "operation": "get_project_data"
        }
        
    except Exception as e:
        return {"status": "error", "message": f"get_project_data failed: {e}"}

def handle_get_cadwork_version_info(aParams: dict) -> dict:
    """Ruft Cadwork Versionsinformationen ab"""
    try:
        import utility_controller as uc
        
        # Cadwork API aufrufen
        lVersionInfo = uc.get_cadwork_version_info()
        
        return {
            "status": "success",
            "version_info": lVersionInfo,
            "operation": "get_cadwork_version_info"
        }
        
    except Exception as e:
        return {"status": "error", "message": f"get_cadwork_version_info failed: {e}"}
