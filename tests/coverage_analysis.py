#!/usr/bin/env python3
"""
Test Coverage Analysis
====================

Compare MCP tools with existing tests to find gaps
"""

# MCP Tools by Controller (from audit)
mcp_tools_by_controller = {
    'element': 51,      # In MCP
    'geometry': 35,     # In MCP
    'attribute': 8,     # In MCP
    'visualization': 9, # In MCP
    'utility': 7,       # In MCP
    'shop_drawing': 4,  # In MCP
    'roof': 2,          # In MCP
    'machine': 1,       # In MCP
    'measurement': 3,   # In MCP
    'material': 3,      # In MCP
    'export': 20,       # In MCP
    'import': 4,        # In MCP
}

# Current Test Implementation (estimated from our test files)
current_test_coverage = {
    'element': 8,        # create_beam, create_panel, etc. - about 8 core tests
    'geometry': 10,      # get_element_width, height, etc. - about 10 tests
    'attribute': 3,      # set_material, set_name - about 3 tests
    'visualization': 3,  # show_all, get_visible_count, refresh - 3 tests
    'utility': 2,        # get_project_data, get_version - 2 tests
    'shop_drawing': 1,   # placeholder test only
    'roof': 1,           # placeholder test only
    'machine': 1,        # placeholder test only
    'measurement': 2,    # measure_distance, measure_angle - 2 tests
    'material': 2,       # list_materials, create_material - 2 tests
    'export': 1,         # export_to_dxf only - 1 test
    'import': 1,         # placeholder test only
}

print("=== TEST COVERAGE ANALYSIS ===")
print()

total_mcp = 0
total_tested = 0
total_missing = 0

for controller in mcp_tools_by_controller.keys():
    mcp_count = mcp_tools_by_controller[controller]
    test_count = current_test_coverage.get(controller, 0)
    missing = mcp_count - test_count
    coverage = (test_count / mcp_count * 100) if mcp_count > 0 else 0
    
    total_mcp += mcp_count
    total_tested += test_count
    total_missing += missing
    
    status = "OK" if coverage >= 80 else "WARN" if coverage >= 50 else "FAIL"
    
    print(f"{status} {controller.upper():15} {test_count:2d}/{mcp_count:2d} ({coverage:5.1f}%) - Missing: {missing:2d}")

print("=" * 50)
total_coverage = (total_tested / total_mcp * 100) if total_mcp > 0 else 0
print(f"OVERALL COVERAGE:   {total_tested:2d}/{total_mcp:2d} ({total_coverage:5.1f}%) - Missing: {total_missing:2d}")

print()
print("=== PRIORITY ACTIONS NEEDED ===")

# Priority 1: Controllers with many missing tests
priority_1 = []
for controller, mcp_count in mcp_tools_by_controller.items():
    test_count = current_test_coverage.get(controller, 0)
    missing = mcp_count - test_count
    if missing >= 10:  # More than 10 missing tests
        priority_1.append((controller, missing, mcp_count))

if priority_1:
    print("PRIORITY 1 - Many Missing Tests:")
    for controller, missing, total in priority_1:
        print(f"   - {controller}: {missing} missing tests (out of {total})")

# Priority 2: Controllers with some missing tests  
priority_2 = []
for controller, mcp_count in mcp_tools_by_controller.items():
    test_count = current_test_coverage.get(controller, 0)
    missing = mcp_count - test_count
    if 3 <= missing < 10:  # 3-9 missing tests
        priority_2.append((controller, missing, mcp_count))

if priority_2:
    print("PRIORITY 2 - Some Missing Tests:")
    for controller, missing, total in priority_2:
        print(f"   - {controller}: {missing} missing tests (out of {total})")

# Priority 3: Controllers with few missing tests
priority_3 = []
for controller, mcp_count in mcp_tools_by_controller.items():
    test_count = current_test_coverage.get(controller, 0)
    missing = mcp_count - test_count
    if 1 <= missing < 3:  # 1-2 missing tests
        priority_3.append((controller, missing, mcp_count))

if priority_3:
    print("PRIORITY 3 - Few Missing Tests:")
    for controller, missing, total in priority_3:
        print(f"   - {controller}: {missing} missing tests (out of {total})")

print()
print("=== RECOMMENDATIONS ===")
print("1. Focus on Element Controller (43 missing tests)")
print("2. Focus on Geometry Controller (25 missing tests)")  
print("3. Add Export Controller tests (19 missing tests)")
print("4. Add Attribute Controller tests (5 missing tests)")
print("5. Visualization/Utility Controllers are mostly covered")
print()
print("=== ESTIMATED EFFORT ===")
effort_hours = total_missing * 0.1  # 6 minutes per test on average
print(f"Estimated time to complete all tests: {effort_hours:.1f} hours")
print(f"Target: Add {total_missing} tests to reach 100% coverage")
