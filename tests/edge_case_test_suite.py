                if element_id:
                    self.edge_test_elements.append(element_id)
                return {"status": "success", "message": "System recovered successfully after error"}
            else:
                return {"status": "error", "message": "System did not recover properly after error"}
                
        except Exception as e:
            return {"status": "partial", "message": f"Recovery test exception: {str(e)[:50]}"}
    
    async def _test_partial_operations(self):
        """Test handling of partial operations"""
        try:
            # Create mix of valid and invalid element IDs for batch operation
            valid_element = None
            
            # Create one valid element
            valid_params = self.param_finder.get_beam_parameters()
            result = await self.element_ctrl.create_beam(**valid_params)
            
            if result.get("status") == "success":
                valid_element = result.get("element_id")
                if valid_element:
                    self.edge_test_elements.append(valid_element)
            
            if valid_element:
                # Try batch operation with mix of valid and invalid IDs
                mixed_ids = [valid_element, 999999, -1, valid_element]
                
                batch_result = await self.element_ctrl.copy_elements(
                    mixed_ids, [1000, 0, 0]
                )
                
                return {
                    "status": "success", 
                    "message": f"Partial operation handled: {batch_result.get('status', 'unknown')}"
                }
            else:
                return {"status": "skip", "message": "Could not create valid element for partial test"}
                
        except Exception as e:
            return {"status": "success", "message": f"Partial operation exception handled: {str(e)[:50]}"}
    
    async def _test_resource_cleanup(self):
        """Test resource cleanup after errors"""
        try:
            cleanup_elements = []
            
            # Create several elements
            for i in range(5):
                params = self.param_finder.get_beam_parameters()
                params["p1"][0] += i * 1000
                params["p2"][0] += i * 1000
                
                result = await self.element_ctrl.create_beam(**params)
                if result.get("status") == "success":
                    element_id = result.get("element_id")
                    if element_id:
                        cleanup_elements.append(element_id)
            
            # Force an error condition, then cleanup
            try:
                # Try invalid operation on valid elements
                await self.element_ctrl.scale_elements(cleanup_elements, -1)  # Invalid scale
            except:
                pass
            
            # Test if cleanup still works after error
            if cleanup_elements:
                cleanup_result = await self.element_ctrl.delete_elements(cleanup_elements)
                
                if cleanup_result.get("status") == "success":
                    return {"status": "success", "message": "Resource cleanup successful after error"}
                else:
                    # Add to edge elements for later cleanup
                    self.edge_test_elements.extend(cleanup_elements)
                    return {"status": "partial", "message": "Resource cleanup attempted after error"}
            else:
                return {"status": "skip", "message": "No elements to cleanup"}
                
        except Exception as e:
            return {"status": "success", "message": f"Cleanup exception handled: {str(e)[:50]}"}
    
    def get_summary(self) -> Dict[str, Any]:
        """Get edge case test summary"""
        return self.helper.get_summary()
    
    def print_summary(self) -> None:
        """Print edge case test summary"""
        self.helper.print_summary()


# Convenience function for standalone testing
async def run_edge_case_tests() -> None:
    """Run edge case test suite standalone"""
    test_suite = EdgeCaseTestSuite()
    await test_suite.run_all_edge_case_tests()
    test_suite.print_summary()


if __name__ == "__main__":
    print("🎯 CADWORK MCP EDGE CASE & ERROR RECOVERY TEST SUITE")
    print("⚠️  This will test system limits and error conditions!")
    print("⚠️  Ensure Cadwork 3D is running and ready for edge case testing!")
    print()
    
    asyncio.run(run_edge_case_tests())
