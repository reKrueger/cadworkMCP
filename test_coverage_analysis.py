"""
Analyse der Test-Abdeckung für alle MCP-Tools
"""
import re
import os

def extract_mcp_tools_from_main():
    """Extrahiert alle MCP-Tools aus main.py"""
    main_path = "C:/cadworkMCP/main.py"
    
    with open(main_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Finde alle @mcp.tool Definitionen mit Namen
    pattern = r'@mcp\.tool\(\s*name="([^"]+)"'
    matches = re.findall(pattern, content)
    
    return sorted(matches)

def extract_test_functions():
    """Extrahiert alle Test-Funktionen aus den Test-Dateien"""
    test_dir = "C:/cadworkMCP/tests"
    test_files = [
        "test_element_controller.py",
        "test_geometry_controller.py", 
        "test_attribute_controller.py",
        "test_system.py"
    ]
    
    all_tests = {}
    
    for test_file in test_files:
        file_path = os.path.join(test_dir, test_file)
        
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Finde alle test_ Funktionen
        pattern = r'def (test_[^(]+)\('
        matches = re.findall(pattern, content)
        
        all_tests[test_file] = sorted(matches)
    
    return all_tests

def analyze_coverage():
    """Analysiert die Test-Abdeckung"""
    print("="*80)
    print(" CADWORK MCP TEST COVERAGE ANALYSE ".center(80))
    print("="*80)
    
    # MCP Tools extrahieren
    mcp_tools = extract_mcp_tools_from_main()
    print(f"\nIMPLEMENTIERTE MCP-TOOLS: {len(mcp_tools)}")
    print("-" * 50)
    
    categories = {
        "Element Creation": [],
        "Element Management": [],
        "Geometry": [], 
        "Attributes": [],
        "System": []
    }
    
    for tool in mcp_tools:
        if tool.startswith("create_"):
            categories["Element Creation"].append(tool)
        elif tool in ["get_active_element_ids", "get_all_element_ids", "get_visible_element_ids", 
                      "get_user_element_ids", "get_element_info", "delete_elements", 
                      "copy_elements", "move_element"]:
            categories["Element Management"].append(tool)
        elif tool.startswith("get_element_") or tool.startswith("get_center_") or tool.startswith("get_minimum_") or tool.startswith("get_total_") or tool.startswith("rotate_") or tool.startswith("apply_") or tool.startswith("invert_"):
            categories["Geometry"].append(tool)
        elif "attribute" in tool or tool.startswith("set_") or tool.startswith("list_"):
            categories["Attributes"].append(tool)
        else:
            categories["System"].append(tool)
    
    for category, tools in categories.items():
        if tools:
            print(f"\n{category}: {len(tools)} Tools")
            for tool in tools:
                print(f"  OK {tool}")
    
    # Test-Funktionen extrahieren
    test_functions = extract_test_functions()
    total_tests = sum(len(tests) for tests in test_functions.values())
    
    print(f"\nTEST-FUNKTIONEN: {total_tests}")
    print("-" * 50)
    
    for test_file, tests in test_functions.items():
        controller_name = test_file.replace("test_", "").replace("_controller.py", "").title()
        print(f"\n{controller_name} Controller: {len(tests)} Tests")
        for test in tests:
            print(f"  TEST {test}")
    
    # Coverage-Analyse
    print(f"\nCOVERAGE-ANALYSE")
    print("-" * 50)
    
    # Mapping Test-Namen zu MCP-Tool-Namen
    tested_tools = set()
    untested_tools = set(mcp_tools)
    
    for test_file, tests in test_functions.items():
        for test in tests:
            # Einfache Mapping-Strategie
            test_clean = test.replace("test_", "")
            
            # Direkte Übereinstimmungen finden
            for tool in mcp_tools:
                if tool in test_clean or test_clean in tool:
                    tested_tools.add(tool)
                    untested_tools.discard(tool)
    
    # Manuelle Zuordnungen für komplexere Mappings
    manual_mappings = {
        "test_get_all_element_ids": "get_all_element_ids",
        "test_get_active_element_ids": "get_active_element_ids", 
        "test_get_visible_element_ids": "get_visible_element_ids",
        "test_copy_elements": "copy_elements",
        "test_move_element": "move_element",
        "test_invalid_element_id": "get_element_info",  # Error test
        "test_invalid_beam_parameters": "create_beam",  # Error test
    }
    
    for test_name, tool_name in manual_mappings.items():
        if tool_name in mcp_tools:
            tested_tools.add(tool_name)
            untested_tools.discard(tool_name)
    
    print(f"OK Getestete Tools: {len(tested_tools)}/{len(mcp_tools)} ({len(tested_tools)/len(mcp_tools)*100:.1f}%)")
    print(f"WARN Nicht getestete Tools: {len(untested_tools)}")
    
    if untested_tools:
        print(f"\nFEHLENDE TESTS:")
        for tool in sorted(untested_tools):
            print(f"  FEHLT {tool}")
    
    print(f"\nZUSAMMENFASSUNG")
    print("-" * 50)
    print(f"MCP-Tools implementiert: {len(mcp_tools)}")
    print(f"Test-Funktionen erstellt: {total_tests}")
    print(f"Tools mit Tests: {len(tested_tools)}")
    print(f"Coverage: {len(tested_tools)/len(mcp_tools)*100:.1f}%")
    
    print("="*80)
    
    return {
        "total_tools": len(mcp_tools),
        "total_tests": total_tests,
        "tested_tools": len(tested_tools),
        "coverage_percent": len(tested_tools)/len(mcp_tools)*100,
        "untested_tools": list(untested_tools),
        "all_tools": mcp_tools,
        "categories": categories
    }

if __name__ == "__main__":
    result = analyze_coverage()
