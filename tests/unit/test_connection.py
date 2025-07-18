"""
Connection Tests
===============

Tests for basic Cadwork connection and bridge functionality.
"""

import sys
import os
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from helpers.base_test import BaseCadworkTest
from core.connection import initialize_connection, get_connection
import socket


class TestConnection(BaseCadworkTest):
    """Test basic connection functionality"""
    
    def __init__(self, use_mock: bool = False):
        super().__init__(use_mock=use_mock)
    
    async def test_bridge_port_listening(self):
        """Test that MCP Bridge is listening on port 53002"""
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            result = sock.connect_ex(('127.0.0.1', 53002))
            if result != 0:
                raise AssertionError("MCP Bridge not listening on port 53002")
        finally:
            sock.close()
        return {"port_53002": "listening"}
    
    async def test_connection_initialization(self):
        """Test connection initialization"""
        initialize_connection()
        connection = get_connection()
        
        if connection is None:
            raise AssertionError("Connection not initialized")
        
        return {"connection": "initialized"}
    
    async def test_ping_command(self):
        """Test basic ping command"""
        if self.use_mock:
            from helpers.global_mock import mock_send_command
            response = mock_send_command("ping")
        else:
            connection = get_connection()
            response = connection.send_command("ping")
        
        self.assert_success(response, "ping")
        return response
    
    async def test_get_all_elements(self):
        """Test getting all elements from Cadwork"""
        if self.use_mock:
            from helpers.global_mock import mock_send_command
            response = mock_send_command("get_all_element_ids")
        else:
            connection = get_connection()
            response = connection.send_command("get_all_element_ids")
        
        element_ids = self.assert_element_list(response, "get_all_element_ids")
        
        return {
            "total_elements": len(element_ids),
            "element_ids": element_ids[:5]  # Show first 5 elements
        }
