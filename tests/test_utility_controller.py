"""
Utility Controller Tests
Tests für Performance- und Ausgabe-Funktionen
"""
import asyncio
import sys
import os

# Add project root to path
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, PROJECT_ROOT)

from tests.test_config import TestSuite, assert_ok, assert_error, assert_has_key
from controllers.utility_controller import CUtilityController

class UtilityControllerTests(TestSuite):
    """Test suite für Utility Controller"""
    
    def __init__(self):
        super().__init__("Utility Controller Tests")
        self.controller = CUtilityController()
    
    def setup(self):
        """Setup vor allen Tests"""
        self.log("Setting up Utility Controller tests...")
    
    def teardown(self):
        """Cleanup nach allen Tests"""
        self.log("Cleaning up Utility Controller tests...")
    
    def test_disable_auto_display_refresh(self):
        """Test disable_auto_display_refresh"""
        result = asyncio.run(self.controller.disable_auto_display_refresh())
        assert_ok(result)
        assert_has_key(result, "message")
        self.log(f"Display refresh disabled: {result.get('message')}")
        return result
    
    def test_enable_auto_display_refresh(self):
        """Test enable_auto_display_refresh"""
        result = asyncio.run(self.controller.enable_auto_display_refresh())
        assert_ok(result)
        assert_has_key(result, "message")
        self.log(f"Display refresh enabled: {result.get('message')}")
        return result
    
    def test_print_error_valid_message(self):
        """Test print_error mit gültiger Nachricht"""
        lTestMessage = "Test error message from unit tests"
        result = asyncio.run(self.controller.print_error(lTestMessage))
        assert_ok(result)
        assert_has_key(result, "message")
        self.log(f"Error message printed: {lTestMessage}")
        return result
    
    def test_print_error_empty_message(self):
        """Test print_error mit leerer Nachricht"""
        result = asyncio.run(self.controller.print_error(""))
        assert_error(result)
        assert_has_key(result, "message")
        self.log(f"Empty message rejected: {result.get('message')}")
        return result
    
    def test_print_error_invalid_type(self):
        """Test print_error mit ungültigem Typ"""
        result = asyncio.run(self.controller.print_error(123))
        assert_error(result)
        assert_has_key(result, "message")
        self.log(f"Invalid type rejected: {result.get('message')}")
        return result
    
    def test_print_warning_valid_message(self):
        """Test print_warning mit gültiger Nachricht"""
        lTestMessage = "Test warning message from unit tests"
        result = asyncio.run(self.controller.print_warning(lTestMessage))
        assert_ok(result)
        assert_has_key(result, "message")
        self.log(f"Warning message printed: {lTestMessage}")
        return result
    
    def test_print_warning_whitespace_message(self):
        """Test print_warning mit Whitespace-Nachricht"""
        lTestMessage = "   Test warning with whitespace   "
        result = asyncio.run(self.controller.print_warning(lTestMessage))
        assert_ok(result)
        assert_has_key(result, "message")
        self.log(f"Whitespace message handled: {lTestMessage.strip()}")
        return result
    
    def test_get_3d_file_path(self):
        """Test get_3d_file_path"""
        result = asyncio.run(self.controller.get_3d_file_path())
        # Kann ok oder error sein, je nachdem ob Datei geöffnet ist
        assert_has_key(result, "status")
        assert_has_key(result, "message")
        self.log(f"3D file path result: {result.get('message')}")
        return result
    
    def test_get_project_data(self):
        """Test get_project_data"""
        result = asyncio.run(self.controller.get_project_data())
        # Kann ok oder error sein, je nachdem ob Projekt geladen ist
        assert_has_key(result, "status")
        assert_has_key(result, "message")
        self.log(f"Project data result: {result.get('message')}")
        return result
    
    def test_display_refresh_workflow(self):
        """Test kompletter Display-Refresh Workflow"""
        # Disable auto refresh
        disable_result = asyncio.run(self.controller.disable_auto_display_refresh())
        assert_ok(disable_result)
        
        # Print info message
        info_result = asyncio.run(self.controller.print_warning("Auto refresh disabled for testing"))
        assert_ok(info_result)
        
        # Enable auto refresh
        enable_result = asyncio.run(self.controller.enable_auto_display_refresh())
        assert_ok(enable_result)
        
        # Print completion message
        complete_result = asyncio.run(self.controller.print_warning("Auto refresh re-enabled"))
        assert_ok(complete_result)
        
        self.log("Complete display refresh workflow tested successfully")
        return {
            "disable": disable_result,
            "info": info_result, 
            "enable": enable_result,
            "complete": complete_result
        }

if __name__ == "__main__":
    # Run tests
    suite = UtilityControllerTests()
    summary = suite.run_all_tests()
    
    print(f"\n{summary['suite_name']}: {summary['passed']}/{summary['total_tests']} passed ({summary['success_rate']:.1f}%)")
    if summary['failed'] > 0:
        print("Failed tests:")
        for result in summary['results']:
            if not result.success:
                print(f"  - {result.test_name}: {result.message}")
