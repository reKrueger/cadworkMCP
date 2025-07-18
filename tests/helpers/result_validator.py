"""
Result Validator Class
=====================

Validates and analyzes results from Cadwork MCP function calls.
Provides standardized validation patterns and error analysis.
"""

from typing import Dict, Any, List, Optional, Union, Set
import re


class ResultValidator:
    """
    Validates results from Cadwork MCP function calls.
    Provides standardized validation patterns and detailed error analysis.
    """
    
    def __init__(self):
        self.validation_cache: Dict[str, Any] = {}
    
    def validate_basic_response(self, response: Any) -> Dict[str, Any]:
        """
        Validate basic response structure
        
        Args:
            response: Response from Cadwork API
            
        Returns:
            Validation result with details
        """
        result = {
            "is_valid": False,
            "errors": [],
            "warnings": [],
            "details": {}
        }
        
        # Check if response exists
        if response is None:
            result["errors"].append("Response is None")
            return result
        
        # Check if response is dict
        if not isinstance(response, dict):
            result["errors"].append(f"Response is not dict, got {type(response)}")
            return result
        
        # Check for status field
        if "status" not in response:
            result["errors"].append("Missing 'status' field in response")
            return result
        
        # Check status value
        status = response.get("status")
        if status not in ["success", "error", "warning"]:
            result["warnings"].append(f"Unexpected status value: {status}")
        
        # If success, mark as valid
        if status == "success":
            result["is_valid"] = True
        else:
            result["errors"].append(f"Status is '{status}', not 'success'")
        
        # Store response details
        result["details"]["response_keys"] = list(response.keys())
        result["details"]["status"] = status
        result["details"]["message"] = response.get("message", "")
        
        return result
    
    def validate_element_creation(self, response: Dict[str, Any]) -> Dict[str, Any]:
        """Validate element creation response"""
        result = self.validate_basic_response(response)
        
        if result["is_valid"]:
            # Check for element_id
            if "element_id" not in response:
                result["errors"].append("Missing 'element_id' in successful creation response")
                result["is_valid"] = False
            else:
                element_id = response["element_id"]
                if not isinstance(element_id, int) or element_id <= 0:
                    result["errors"].append(f"Invalid element_id: {element_id}")
                    result["is_valid"] = False
                else:
                    result["details"]["element_id"] = element_id
        
        return result
    
    def validate_element_list(self, response: Dict[str, Any], 
                            expected_key: str = "element_ids") -> Dict[str, Any]:
        """Validate response containing list of element IDs"""
        result = self.validate_basic_response(response)
        
        if result["is_valid"]:
            if expected_key not in response:
                result["errors"].append(f"Missing '{expected_key}' in response")
                result["is_valid"] = False
            else:
                element_list = response[expected_key]
                if not isinstance(element_list, list):
                    result["errors"].append(f"'{expected_key}' is not a list")
                    result["is_valid"] = False
                else:
                    # Validate element IDs
                    invalid_ids = [id for id in element_list if not isinstance(id, int) or id <= 0]
                    if invalid_ids:
                        result["warnings"].append(f"Invalid element IDs found: {invalid_ids}")
                    
                    result["details"]["element_count"] = len(element_list)
                    result["details"]["element_ids"] = element_list[:10]  # First 10 for display
                    
                    if len(element_list) == 0:
                        result["warnings"].append("Element list is empty")
        
        return result
    
    def validate_geometric_data(self, response: Dict[str, Any]) -> Dict[str, Any]:
        """Validate geometric data response (dimensions, coordinates, etc.)"""
        result = self.validate_basic_response(response)
        
        if result["is_valid"]:
            geometric_fields = ["width", "height", "length", "volume", "weight", 
                              "p1", "p2", "p3", "xl", "yl", "zl"]
            
            found_fields = []
            for field in geometric_fields:
                if field in response:
                    found_fields.append(field)
                    value = response[field]
                    
                    # Validate coordinate arrays
                    if field in ["p1", "p2", "p3", "xl", "yl", "zl"]:
                        if not isinstance(value, list) or len(value) != 3:
                            result["warnings"].append(f"Invalid coordinate format for {field}: {value}")
                        else:
                            # Check if coordinates are reasonable
                            if any(abs(coord) > 1000000 for coord in value):
                                result["warnings"].append(f"Very large coordinates in {field}: {value}")
                    
                    # Validate dimensions
                    elif field in ["width", "height", "length"]:
                        if not isinstance(value, (int, float)) or value <= 0:
                            result["warnings"].append(f"Invalid dimension {field}: {value}")
                        elif value > 50000:  # > 50m
                            result["warnings"].append(f"Very large dimension {field}: {value}mm")
                    
                    # Validate volume/weight
                    elif field in ["volume", "weight"]:
                        if not isinstance(value, (int, float)) or value < 0:
                            result["warnings"].append(f"Invalid {field}: {value}")
            
            result["details"]["geometric_fields"] = found_fields
        
        return result
    
    def validate_attribute_data(self, response: Dict[str, Any]) -> Dict[str, Any]:
        """Validate attribute data response"""
        result = self.validate_basic_response(response)
        
        if result["is_valid"]:
            attribute_fields = ["name", "material", "group", "subgroup", "comment", 
                              "color", "transparency", "visible"]
            
            found_attributes = {}
            for field in attribute_fields:
                if field in response:
                    value = response[field]
                    found_attributes[field] = value
                    
                    # Validate specific attribute types
                    if field == "color" and isinstance(value, int):
                        if not (1 <= value <= 255):
                            result["warnings"].append(f"Color ID out of range: {value}")
                    
                    elif field == "transparency" and isinstance(value, int):
                        if not (0 <= value <= 100):
                            result["warnings"].append(f"Transparency out of range: {value}")
                    
                    elif field == "visible" and not isinstance(value, bool):
                        result["warnings"].append(f"Visibility should be boolean: {value}")
            
            result["details"]["attributes"] = found_attributes
        
        return result
    
    def validate_statistics_data(self, response: Dict[str, Any]) -> Dict[str, Any]:
        """Validate statistics/count data response"""
        result = self.validate_basic_response(response)
        
        if result["is_valid"]:
            # Look for count fields
            count_fields = [k for k in response.keys() if "count" in k.lower() or "total" in k.lower()]
            percentage_fields = [k for k in response.keys() if "percentage" in k.lower() or "rate" in k.lower()]
            
            for field in count_fields:
                value = response[field]
                if not isinstance(value, int) or value < 0:
                    result["warnings"].append(f"Invalid count value {field}: {value}")
            
            for field in percentage_fields:
                value = response[field]
                if not isinstance(value, (int, float)) or not (0 <= value <= 100):
                    result["warnings"].append(f"Invalid percentage {field}: {value}")
            
            result["details"]["count_fields"] = count_fields
            result["details"]["percentage_fields"] = percentage_fields
        
        return result
    
    def validate_export_result(self, response: Dict[str, Any]) -> Dict[str, Any]:
        """Validate export operation result"""
        result = self.validate_basic_response(response)
        
        if result["is_valid"]:
            # Check for export-specific fields
            export_fields = ["file_path", "exported_elements", "export_format", 
                           "file_size", "export_time"]
            
            found_export_data = {}
            for field in export_fields:
                if field in response:
                    found_export_data[field] = response[field]
            
            # Validate file path if present
            if "file_path" in response:
                file_path = response["file_path"]
                if not isinstance(file_path, str) or not file_path:
                    result["warnings"].append(f"Invalid file_path: {file_path}")
            
            # Validate exported elements count
            if "exported_elements" in response:
                count = response["exported_elements"]
                if not isinstance(count, int) or count < 0:
                    result["warnings"].append(f"Invalid exported_elements count: {count}")
            
            result["details"]["export_data"] = found_export_data
        
        return result
    
    def analyze_error_response(self, response: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze error response for common issues"""
        analysis = {
            "error_type": "unknown",
            "likely_cause": "unknown",
            "suggestions": []
        }
        
        if not isinstance(response, dict):
            analysis["error_type"] = "invalid_response_type"
            analysis["likely_cause"] = f"Expected dict, got {type(response)}"
            analysis["suggestions"].append("Check API connection and response format")
            return analysis
        
        message = str(response.get("message", "")).lower()
        
        # Common error patterns
        if "connection" in message or "not connected" in message:
            analysis["error_type"] = "connection_error"
            analysis["likely_cause"] = "Cadwork bridge not connected"
            analysis["suggestions"].extend([
                "Start Cadwork 3D application",
                "Start MCP Bridge in Cadwork",
                "Check bridge connection status"
            ])
        
        elif "element" in message and "not found" in message:
            analysis["error_type"] = "element_not_found"
            analysis["likely_cause"] = "Element ID does not exist"
            analysis["suggestions"].extend([
                "Verify element ID exists",
                "Check if element was deleted",
                "Use get_all_element_ids() to verify"
            ])
        
        elif "parameter" in message or "argument" in message:
            analysis["error_type"] = "parameter_error"
            analysis["likely_cause"] = "Invalid function parameters"
            analysis["suggestions"].extend([
                "Check parameter types and values",
                "Verify coordinate format [x,y,z]",
                "Check dimension values > 0"
            ])
        
        elif "permission" in message or "access" in message:
            analysis["error_type"] = "permission_error"
            analysis["likely_cause"] = "Insufficient permissions"
            analysis["suggestions"].append("Check file/directory permissions")
        
        elif "timeout" in message:
            analysis["error_type"] = "timeout_error"
            analysis["likely_cause"] = "Operation took too long"
            analysis["suggestions"].extend([
                "Reduce operation complexity",
                "Check system performance",
                "Increase timeout if possible"
            ])
        
        return analysis
    
    def get_validation_summary(self, validation_results: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Get summary of multiple validation results"""
        total = len(validation_results)
        valid = len([r for r in validation_results if r.get("is_valid", False)])
        invalid = total - valid
        
        all_errors = []
        all_warnings = []
        
        for result in validation_results:
            all_errors.extend(result.get("errors", []))
            all_warnings.extend(result.get("warnings", []))
        
        # Count unique errors/warnings
        unique_errors = list(set(all_errors))
        unique_warnings = list(set(all_warnings))
        
        return {
            "total_validations": total,
            "valid_count": valid,
            "invalid_count": invalid,
            "success_rate": (valid / total * 100) if total > 0 else 0,
            "total_errors": len(all_errors),
            "unique_errors": unique_errors,
            "total_warnings": len(all_warnings),
            "unique_warnings": unique_warnings
        }
