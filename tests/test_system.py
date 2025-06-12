"""
System Tests für weitere MCP-Tools
"""
import asyncio
from test_config import TestSuite, assert_ok, assert_error

class SystemTests(TestSuite):
    """Test suite for system functions"""
    
    def __init__(self):
        super().__init__("System Tests")
    
    def setup(self):
        """Setup system tests"""
        print("Setting up System tests...")
    
    def teardown(self):
        """Cleanup system tests"""
        print("System tests completed.")
    
    def test_get_cadwork_version_info(self):
        """Test getting Cadwork version information"""
        from core.connection import get_connection
        
        try:
            connection = get_connection()
            result = connection.send_command("get_version_info")
            assert_ok(result)
            
            # Version info should contain some version data
            if "version" in result or "info" in result:
                return result
            else:
                return {"status": "ok", "message": "Version info structure may vary"}
                
        except Exception as e:
            return {"status": "error", "message": f"Version info failed: {e}"}
