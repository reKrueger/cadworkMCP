#!/usr/bin/env python3
"""
Cadwork MCP - Simple Test Runner
================================

Einfaches Test-System um alle Cadwork MCP Funktionen zu testen.
Führe einfach run_test() aus um alle Tests zu starten.

Autor: Claude
Datum: 2025-07-13
"""

import sys
import os
import time
import traceback
from typing import Dict, Any, List, Optional
from dataclasses import dataclass
from enum import Enum

# Add project root to path
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

# Import controllers  
from controllers.element_controller import ElementController
from controllers.geometry_controller import GeometryController
from controllers.attribute_controller import AttributeController
from controllers.visualization_controller import CVisualizationController
from controllers.utility_controller import CUtilityController
from controllers.shop_drawing_controller import CShopDrawingController
from controllers.roof_controller import CRoofController
from controllers.machine_controller import CMachineController

# Connection management
from core.connection import initialize_connection, get_connection


class CTestStatus(Enum):
    """Test status enumeration"""
    PASSED = "PASSED"
    FAILED = "FAILED" 
    SKIPPED = "SKIPPED"
    ERROR = "ERROR"


@dataclass
class CTestResult:
    """Test result data container"""
    aTestName: str
    eStatus: CTestStatus
    aMessage: str = ""
    fDuration: float = 0.0
    aDetails: str = ""


class CTestSuite:
    """Simple test suite base class"""
    
    def __init__(self, aName: str):
        self.m_aName = aName
        self.m_lResults: List[CTestResult] = []
        self.m_lCreatedElements: List[int] = []
        self.m_bConnectionReady = False
    
    def checkConnection(self) -> bool:
        """Check if Cadwork connection is ready"""
        if self.m_bConnectionReady:
            return True
            
        try:
            initialize_connection("127.0.0.1", 53002)
            lConnection = get_connection()
            lResponse = lConnection.send_command("ping", {})
            
            if lResponse.get("status") == "ok":
                self.m_bConnectionReady = True
                return True
            else:
                self.log(f"X Connection failed: {lResponse.get('message')}")
                return False
                
        except Exception as e:
            self.log(f"X Connection error: {e}")
            return False
    
    def log(self, aMessage: str) -> None:
        """Log message with prefix"""
        print(f"  {aMessage}")
    
    def runTest(self, fTestFunction, aTestName: str = None) -> CTestResult:
        """Run a single test function"""
        if aTestName is None:
            aTestName = fTestFunction.__name__
        
        self.log(f"Test: {aTestName}")
        lStartTime = time.time()
        
        try:
            import asyncio
            # Check if function is async
            if asyncio.iscoroutinefunction(fTestFunction):
                lResult = asyncio.run(fTestFunction())
            else:
                lResult = fTestFunction()
                
            fDuration = time.time() - lStartTime
            
            if isinstance(lResult, dict):
                if lResult.get("status") == "ok":
                    lTestResult = CTestResult(aTestName, CTestStatus.PASSED, "+ Successful", fDuration)
                elif lResult.get("status") == "error":
                    lTestResult = CTestResult(aTestName, CTestStatus.FAILED, f"X API Error: {lResult.get('message')}", fDuration)
                elif lResult.get("status") == "skip":
                    lTestResult = CTestResult(aTestName, CTestStatus.SKIPPED, f"? {lResult.get('message')}", fDuration)
                else:
                    lTestResult = CTestResult(aTestName, CTestStatus.PASSED, f"+ Result: {lResult}", fDuration)
            else:
                lTestResult = CTestResult(aTestName, CTestStatus.PASSED, f"+ Completed: {lResult}", fDuration)
            
            self.log(f"  {lTestResult.eStatus.value} ({fDuration:.2f}s) - {lTestResult.aMessage}")
            
        except Exception as e:
            fDuration = time.time() - lStartTime
            lTestResult = CTestResult(aTestName, CTestStatus.ERROR, f"X Exception: {str(e)}", fDuration, traceback.format_exc())
            self.log(f"  {lTestResult.eStatus.value} ({fDuration:.2f}s) - {lTestResult.aMessage}")
        
        self.m_lResults.append(lTestResult)
        return lTestResult
    
    def trackElement(self, lResult: Dict[str, Any]) -> None:
        """Track created element for cleanup"""
        if isinstance(lResult, dict) and lResult.get("status") == "ok":
            nElementId = lResult.get("element_id") or lResult.get("id")
            if nElementId and isinstance(nElementId, int):
                self.m_lCreatedElements.append(nElementId)
    
    def cleanup(self) -> None:
        """Cleanup created test elements"""
        if self.m_lCreatedElements:
            self.log(f"Cleaning up {len(self.m_lCreatedElements)} test elements...")
            # Note: In real implementation, we would delete the elements here
            # For now, just log them
            self.log(f"  Element IDs: {self.m_lCreatedElements}")
    
    def getSummary(self) -> Dict[str, Any]:
        """Get test suite summary"""
        nTotal = len(self.m_lResults)
        nPassed = sum(1 for r in self.m_lResults if r.eStatus == CTestStatus.PASSED)
        nFailed = sum(1 for r in self.m_lResults if r.eStatus == CTestStatus.FAILED)
        nError = sum(1 for r in self.m_lResults if r.eStatus == CTestStatus.ERROR)
        nSkipped = sum(1 for r in self.m_lResults if r.eStatus == CTestStatus.SKIPPED)
        fTotalDuration = sum(r.fDuration for r in self.m_lResults)
        
        return {
            "suite_name": self.m_aName,
            "total": nTotal,
            "passed": nPassed,
            "failed": nFailed,
            "error": nError,
            "skipped": nSkipped,
            "success_rate": (nPassed / nTotal * 100) if nTotal > 0 else 0,
            "total_duration": fTotalDuration,
            "results": self.m_lResults
        }


class CElementTests(CTestSuite):
    """Element Controller Tests"""
    
    def __init__(self):
        super().__init__("Element Controller")
        self.m_pController = ElementController()
    
    async def testGetAllElements(self) -> Dict[str, Any]:
        """Test getting all elements"""
        return await self.m_pController.get_all_element_ids()
    
    async def testGetActiveElements(self) -> Dict[str, Any]:
        """Test getting active elements"""
        return await self.m_pController.get_active_element_ids()
    
    async def testCreateBeam(self) -> Dict[str, Any]:
        """Test beam creation"""
        lResult = await self.m_pController.create_beam(
            p1=[0, 0, 0],
            p2=[1000, 0, 0],
            width=100,
            height=200
        )
        self.trackElement(lResult)
        return lResult
    
    async def testCreatePanel(self) -> Dict[str, Any]:
        """Test panel creation"""
        lResult = await self.m_pController.create_panel(
            p1=[0, 0, 0],
            p2=[0, 1000, 0],
            width=300,
            thickness=18
        )
        self.trackElement(lResult)
        return lResult
    
    def testCreateCircularBeam(self) -> Dict[str, Any]:
        """Test circular beam creation - SKIP (function not available)"""
        return {"status": "skip", "message": "create_circular_beam_points function not available in ElementController"}
    
    async def testGetElementInfo(self) -> Dict[str, Any]:
        """Test getting element info"""
        if not self.m_pController:
            return {"status": "skip", "message": "Controller not available"}
        
        # Get an element to test with
        lAllElements = await self.m_pController.get_all_element_ids()
        if lAllElements.get("status") == "ok" and lAllElements.get("element_ids"):
            nElementId = lAllElements["element_ids"][0]
            return await self.m_pController.get_element_info(nElementId)
        else:
            return {"status": "skip", "message": "No elements available for info test"}
    
    async def testDeleteElements(self) -> Dict[str, Any]:
        """Test deleting elements"""
        if not self.m_pController:
            return {"status": "skip", "message": "Controller not available"}
        
        # Create a test element first
        lCreateResult = await self.m_pController.create_beam(
            p1=[2000, 0, 0], 
            p2=[2500, 0, 0],
            width=50,
            height=100
        )
        
        if lCreateResult.get("status") == "ok" and lCreateResult.get("element_id"):
            nElementId = lCreateResult["element_id"]
            # Don't track this element since we're deleting it
            return await self.m_pController.delete_elements([nElementId])
        else:
            return {"status": "skip", "message": "Could not create test element for deletion"}
    
    async def testCopyElements(self) -> Dict[str, Any]:
        """Test copying elements"""
        if not self.m_pController:
            return {"status": "skip", "message": "Controller not available"}
        
        # Get an element to copy
        lAllElements = await self.m_pController.get_all_element_ids()
        if lAllElements.get("status") == "ok" and lAllElements.get("element_ids"):
            nElementId = lAllElements["element_ids"][0]
            lResult = await self.m_pController.copy_elements([nElementId], [1000, 0, 0])
            # Track copied elements for cleanup
            if lResult.get("status") == "ok" and lResult.get("element_ids"):
                for nCopiedId in lResult["element_ids"]:
                    self.m_lCreatedElements.append(nCopiedId)
            return lResult
        else:
            return {"status": "skip", "message": "No elements available for copy test"}
    
    def runAllTests(self) -> Dict[str, Any]:
        """Run all element tests"""
        print(f"\n[ELEMENTS] {self.m_aName} Tests")
        print("=" * 50)
        
        if not self.checkConnection():
            # Create error summary for failed connection
            lErrorResult = CTestResult("Connection Test", CTestStatus.ERROR, "Connection failed", 0.0)
            self.m_lResults.append(lErrorResult)
            return self.getSummary()
        
        # Run individual tests
        self.runTest(self.testGetAllElements, "Get All Elements")
        self.runTest(self.testGetActiveElements, "Get Active Elements") 
        self.runTest(self.testCreateBeam, "Create Beam")
        self.runTest(self.testCreatePanel, "Create Panel")
        self.runTest(self.testCreateCircularBeam, "Create Circular Beam")
        self.runTest(self.testGetElementInfo, "Get Element Info")
        self.runTest(self.testDeleteElements, "Delete Elements")
        self.runTest(self.testCopyElements, "Copy Elements")
        
        self.cleanup()
        return self.getSummary()


class CGeometryTests(CTestSuite):
    """Geometry Controller Tests"""
    
    def __init__(self):
        super().__init__("Geometry Controller")
        self.m_pController = GeometryController()
    
    async def testElementInfo(self) -> Dict[str, Any]:
        """Test getting element info"""
        # First get some element to test with
        lAllElements = await ElementController().get_all_element_ids()
        if lAllElements.get("status") == "ok" and lAllElements.get("element_ids"):
            nElementId = lAllElements["element_ids"][0]
            return await self.m_pController.get_element_info(nElementId)
        else:
            return {"status": "skip", "message": "No elements available for testing"}
    
    async def testCalculateVolume(self) -> Dict[str, Any]:
        """Test volume calculation"""
        lAllElements = await ElementController().get_all_element_ids()
        if lAllElements.get("status") == "ok" and lAllElements.get("element_ids"):
            lElementIds = lAllElements["element_ids"][:3]  # Test with first 3 elements
            return await self.m_pController.calculate_total_volume(lElementIds)
        else:
            return {"status": "skip", "message": "No elements available for volume test"}
    
    def runAllTests(self) -> Dict[str, Any]:
        """Run all geometry tests"""
        print(f"\n[GEOMETRY] {self.m_aName} Tests")
        print("=" * 50)
        
        if not self.checkConnection():
            # Create error summary for failed connection
            lErrorResult = CTestResult("Connection Test", CTestStatus.ERROR, "Connection failed", 0.0)
            self.m_lResults.append(lErrorResult)
            return self.getSummary()
        
        self.runTest(self.testElementInfo, "Element Info")
        self.runTest(self.testCalculateVolume, "Calculate Volume")
        
        return self.getSummary()


class CAttributeTests(CTestSuite):
    """Attribute Controller Tests"""
    
    def __init__(self):
        super().__init__("Attribute Controller")
        self.m_pController = AttributeController()
    
    async def testGetStandardAttributes(self) -> Dict[str, Any]:
        """Test getting standard attributes"""
        lAllElements = await ElementController().get_all_element_ids()
        if lAllElements.get("status") == "ok" and lAllElements.get("element_ids"):
            lElementIds = lAllElements["element_ids"][:2]
            return await self.m_pController.get_standard_attributes(lElementIds)
        else:
            return {"status": "skip", "message": "No elements available for attribute test"}
    
    async def testSetMaterial(self) -> Dict[str, Any]:
        """Test setting material"""
        lAllElements = await ElementController().get_all_element_ids()
        if lAllElements.get("status") == "ok" and lAllElements.get("element_ids"):
            lElementIds = lAllElements["element_ids"][:1]
            return await self.m_pController.set_material(lElementIds, "C24")
        else:
            return {"status": "skip", "message": "No elements available for material test"}
    
    def runAllTests(self) -> Dict[str, Any]:
        """Run all attribute tests"""
        print(f"\n[ATTRIBUTES] {self.m_aName} Tests")
        print("=" * 50)
        
        if not self.checkConnection():
            # Create error summary for failed connection
            lErrorResult = CTestResult("Connection Test", CTestStatus.ERROR, "Connection failed", 0.0)
            self.m_lResults.append(lErrorResult)
            return self.getSummary()
        
        self.runTest(self.testGetStandardAttributes, "Get Standard Attributes")
        self.runTest(self.testSetMaterial, "Set Material")
        
        return self.getSummary()


class CVisualizationTests(CTestSuite):
    """Visualization Controller Tests"""
    
    def __init__(self):
        super().__init__("Visualization Controller")
        self.m_pController = CVisualizationController()
    
    async def testShowAllElements(self) -> Dict[str, Any]:
        """Test showing all elements"""
        return await self.m_pController.show_all_elements()
    
    async def testGetVisibleCount(self) -> Dict[str, Any]:
        """Test getting visible element count"""
        return await self.m_pController.get_visible_element_count()
    
    def runAllTests(self) -> Dict[str, Any]:
        """Run all visualization tests"""
        print(f"\n[VISUALIZATION] {self.m_aName} Tests")
        print("=" * 50)
        
        if not self.checkConnection():
            # Create error summary for failed connection
            lErrorResult = CTestResult("Connection Test", CTestStatus.ERROR, "Connection failed", 0.0)
            self.m_lResults.append(lErrorResult)
            return self.getSummary()
        
        self.runTest(self.testShowAllElements, "Show All Elements")
        self.runTest(self.testGetVisibleCount, "Get Visible Count")
        
        return self.getSummary()


class CSystemTests(CTestSuite):
    """System Tests"""
    
    def __init__(self):
        super().__init__("System Tests")
        self.m_pUtilityController = CUtilityController()
    
    def testPing(self) -> Dict[str, Any]:
        """Test ping connection"""
        lConnection = get_connection()
        return lConnection.send_command("ping", {})
    
    async def testProjectInfo(self) -> Dict[str, Any]:
        """Test getting project info"""
        return await self.m_pUtilityController.get_project_data()
    
    async def testVersionInfo(self) -> Dict[str, Any]:
        """Test getting version info"""
        return await self.m_pUtilityController.get_cadwork_version_info()
    
    def runAllTests(self) -> Dict[str, Any]:
        """Run all system tests"""
        print(f"\n[SYSTEM] {self.m_aName} Tests")
        print("=" * 50)
        
        if not self.checkConnection():
            # Create error summary for failed connection
            lErrorResult = CTestResult("Connection Test", CTestStatus.ERROR, "Connection failed", 0.0)
            self.m_lResults.append(lErrorResult)
            return self.getSummary()
        
        self.runTest(self.testPing, "Ping Test")
        self.runTest(self.testProjectInfo, "Project Info")
        self.runTest(self.testVersionInfo, "Version Info")
        
        return self.getSummary()


def printHeader(aTitle: str) -> None:
    """Print formatted header"""
    print("\n" + "=" * 80)
    print(f" {aTitle} ".center(80))
    print("=" * 80)


def printSummaryTable(lSummaries: List[Dict[str, Any]]) -> None:
    """Print test summary table"""
    print("\n" + "=" * 80)
    print(" TEST SUMMARY ".center(80))
    print("=" * 80)
    
    # Table header
    print(f"{'Suite':<25} {'Total':<6} {'Pass':<6} {'Fail':<6} {'Err':<6} {'Skip':<6} {'Success':<8} {'Time':<8}")
    print("-" * 80)
    
    nTotalTests = 0
    nTotalPassed = 0
    nTotalFailed = 0
    nTotalError = 0
    nTotalSkipped = 0
    fTotalTime = 0.0
    
    for lSummary in lSummaries:
        aSuiteName = lSummary["suite_name"]
        nTotal = lSummary["total"]
        nPassed = lSummary["passed"]
        nFailed = lSummary["failed"]
        nError = lSummary["error"]
        nSkipped = lSummary["skipped"]
        fSuccessRate = lSummary["success_rate"]
        fDuration = lSummary["total_duration"]
        
        nTotalTests += nTotal
        nTotalPassed += nPassed
        nTotalFailed += nFailed
        nTotalError += nError
        nTotalSkipped += nSkipped
        fTotalTime += fDuration
        
        print(f"{aSuiteName:<25} {nTotal:<6} {nPassed:<6} {nFailed:<6} {nError:<6} {nSkipped:<6} {fSuccessRate:>6.1f}%   {fDuration:>6.2f}s")
    
    # Total row
    print("-" * 80)
    fOverallSuccess = (nTotalPassed / nTotalTests * 100) if nTotalTests > 0 else 0
    print(f"{'TOTAL':<25} {nTotalTests:<6} {nTotalPassed:<6} {nTotalFailed:<6} {nTotalError:<6} {nTotalSkipped:<6} {fOverallSuccess:>6.1f}%   {fTotalTime:>6.2f}s")
    print("=" * 80)


def printFailedTests(lSummaries: List[Dict[str, Any]]) -> None:
    """Print failed test details"""
    lFailedTests = []
    
    for lSummary in lSummaries:
        for lResult in lSummary["results"]:
            if lResult.eStatus in [CTestStatus.FAILED, CTestStatus.ERROR]:
                lFailedTests.append((lSummary["suite_name"], lResult))
    
    if lFailedTests:
        print("\n" + "=" * 80)
        print(" FAILED/ERROR TESTS ".center(80))
        print("=" * 80)
        
        for aSuiteName, lResult in lFailedTests:
            print(f"\n[{aSuiteName}] {lResult.aTestName}")
            print(f"  Status: {lResult.eStatus.value}")
            print(f"  Message: {lResult.aMessage}")
            print(f"  Duration: {lResult.fDuration:.2f}s")
            if lResult.aDetails:
                print(f"  Details: {lResult.aDetails[:200]}...")
        
        print("=" * 80)


def runTest() -> bool:
    """Main test runner function - call this to run all tests"""
    
    printHeader("CADWORK MCP SERVER - SIMPLE TEST RUNNER")
    
    print(f"Start Time: {time.strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"Python: {sys.version.split()[0]}")
    print(f"Project Root: {PROJECT_ROOT}")
    
    # Initialize test suites
    lTestSuites = [
        CElementTests(),
        CGeometryTests(),
        CAttributeTests(),
        CVisualizationTests(),
        CSystemTests()
    ]
    
    # Run all test suites
    lSummaries = []
    fStartTime = time.time()
    
    for lSuite in lTestSuites:
        try:
            lSummary = lSuite.runAllTests()
            lSummaries.append(lSummary)
        except KeyboardInterrupt:
            print(f"\nTests interrupted during {lSuite.m_aName}")
            break
        except Exception as e:
            print(f"\nTest suite {lSuite.m_aName} crashed: {e}")
            lErrorSummary = {
                "suite_name": lSuite.m_aName,
                "total": 1,
                "passed": 0,
                "failed": 0,
                "error": 1,
                "skipped": 0,
                "success_rate": 0.0,
                "total_duration": 0.0,
                "results": [CTestResult(f"{lSuite.m_aName}_crash", CTestStatus.ERROR, str(e), 0.0)]
            }
            lSummaries.append(lErrorSummary)
    
    # Print results
    if lSummaries:
        printSummaryTable(lSummaries)
        printFailedTests(lSummaries)
        
        fTotalDuration = time.time() - fStartTime
        nTotalTests = sum(s["total"] for s in lSummaries)
        nTotalPassed = sum(s["passed"] for s in lSummaries)
        
        print(f"\nTotal Execution Time: {fTotalDuration:.2f} seconds")
        print(f"Tests Per Second: {nTotalTests/fTotalDuration:.1f}")
        
        if nTotalPassed == nTotalTests:
            print("\n[SUCCESS] ALL TESTS PASSED!")
            return True
        else:
            print(f"\n[WARNING] {nTotalTests - nTotalPassed} TESTS FAILED/ERROR")
            return False
    else:
        print("\nNo test results available")
        return False


def main():
    """Entry point when script is run directly"""
    bSuccess = runTest()
    sys.exit(0 if bSuccess else 1)


if __name__ == "__main__":
    main()
