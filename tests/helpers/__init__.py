"""
Test Helper Package
==================

Contains helper classes and utilities for Cadwork MCP testing.
"""

from .base_test import BaseCadworkTest, TestResult
from .cadwork_mock import MockCadworkConnection
from .global_mock import enable_mock, disable_mock, is_mock_enabled, mock_send_command
from .test_data import TEST_BEAM_DATA, TEST_PANEL_DATA, BEAM_VARIATIONS, TEST_MATERIALS

__all__ = [
    'BaseCadworkTest', 
    'TestResult',
    'MockCadworkConnection',
    'enable_mock',
    'disable_mock', 
    'is_mock_enabled',
    'mock_send_command',
    'TEST_BEAM_DATA',
    'TEST_PANEL_DATA',
    'BEAM_VARIATIONS',
    'TEST_MATERIALS'
]
