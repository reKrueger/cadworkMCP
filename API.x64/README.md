# MCP Bridge Plugin - Clean Version

Simple Cadwork plugin to start/stop the MCP bridge.

## Files:
- `MCPBridge.py` - Main plugin with GUI
- `plugin_info.xml` - Plugin metadata

## Installation:
Copy the MCPBridge folder to your Cadwork API.x64 directory.

## Usage:
1. Start Cadwork
2. Go to Window → Plugins → MCP Bridge
3. Click "Start Bridge" to execute the MCP server
4. Click "Stop Bridge" to stop it

The plugin executes: `exec(open(r'C:\cadworkMCP\start.txt').read())`
