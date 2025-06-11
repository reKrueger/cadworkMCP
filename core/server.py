"""
MCP Server setup and configuration
"""
import os
from contextlib import asynccontextmanager
from typing import AsyncIterator, Dict, Any
from mcp.server.fastmcp import FastMCP
from .connection import initialize_connection, get_connection
from .logging import setup_logging, log_info, log_warning

@asynccontextmanager
async def server_lifespan(server: FastMCP) -> AsyncIterator[Dict[str, Any]]:
    """Manage server lifecycle"""
    # Setup logging
    setup_logging()
    log_info("Starting Cadwork MCP Server...")
    
    # Initialize connection
    host = "127.0.0.1"
    port = int(os.environ.get("CW_PORT", 53002))
    connection = initialize_connection(host, port)
    
    # Test connection
    handshake_ok = connection.test_connection()
    if handshake_ok:
        log_info("Connection to Cadwork established successfully")
    else:
        log_warning("Could not establish connection to Cadwork")
    
    yield {"cadwork_connected": handshake_ok}
    
    # Cleanup
    log_info("Shutting down Cadwork MCP Server...")

def create_mcp_server() -> FastMCP:
    """Create and configure MCP server"""
    return FastMCP(
        "CadworkMCP",
        version="0.2.0",
        description="Enhanced Cadwork 3D integration via Python API",
        lifespan=server_lifespan
    )
