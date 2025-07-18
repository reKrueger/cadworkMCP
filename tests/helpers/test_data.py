"""
Test Data and Fixtures
======================

Standard test data for consistent testing across all test modules.
"""

# Standard test points for elements
TEST_BEAM_DATA = {
    'p1': [0, 0, 0],
    'p2': [1000, 0, 0], 
    'width': 200,
    'height': 300
}

TEST_PANEL_DATA = {
    'p1': [0, 0, 0],
    'p2': [1000, 0, 0],
    'width': 200,
    'thickness': 20
}

TEST_SURFACE_DATA = {
    'vertices': [
        [0, 0, 0],
        [1000, 0, 0],
        [1000, 1000, 0],
        [0, 1000, 0]
    ]
}

# Different beam configurations for testing
BEAM_VARIATIONS = [
    {'p1': [0, 0, 0], 'p2': [500, 0, 0], 'width': 100, 'height': 150},
    {'p1': [0, 0, 0], 'p2': [2000, 0, 0], 'width': 300, 'height': 400},
    {'p1': [0, 0, 0], 'p2': [0, 1000, 0], 'width': 80, 'height': 200}
]

# Test materials
TEST_MATERIALS = [
    "Wood",
    "Steel", 
    "Concrete",
    "Generic"
]

# Performance test parameters
PERFORMANCE_LIMITS = {
    'single_element_creation': 1.0,  # seconds
    'bulk_element_creation': 5.0,    # seconds for 10 elements
    'element_query': 0.5,            # seconds
    'element_modification': 1.0      # seconds
}
