"""
Global Mock System
==================

Global mock system that can be activated for all controllers.
"""

from typing import Dict, Any, Optional
from helpers.cadwork_mock import MockCadworkConnection

# Global mock state
_mock_enabled = False
_mock_connection: Optional[MockCadworkConnection] = None

def enable_mock():
    """Enable mock mode globally"""
    global _mock_enabled, _mock_connection
    _mock_enabled = True
    _mock_connection = MockCadworkConnection()
    print("Mock mode enabled globally")

def disable_mock():
    """Disable mock mode globally"""
    global _mock_enabled, _mock_connection
    _mock_enabled = False
    _mock_connection = None
    print("Mock mode disabled")

def is_mock_enabled() -> bool:
    """Check if mock mode is enabled"""
    return _mock_enabled

def get_mock_connection() -> Optional[MockCadworkConnection]:
    """Get the global mock connection"""
    return _mock_connection

def mock_send_command(operation: str, args: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    """Send command using mock connection"""
    if _mock_connection:
        return _mock_connection.send_command(operation, args)
    else:
        return {"status": "error", "message": "Mock connection not available"}
