"""
MCP (Model Context Protocol) Server

Provides tool discovery and invocation for AI agents.
"""

from app.mcp.server import MCPServer
from app.mcp.tools import get_tools

__all__ = ["MCPServer", "get_tools"]

