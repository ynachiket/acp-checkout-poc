"""
MCP Protocol Schemas

JSON-RPC 2.0 based schemas for MCP protocol.
"""

from typing import Optional, List, Dict, Any, Literal
from pydantic import BaseModel, Field


class JSONRPCRequest(BaseModel):
    """JSON-RPC 2.0 request."""
    jsonrpc: Literal["2.0"] = "2.0"
    id: Optional[int | str] = None
    method: str
    params: Optional[Dict[str, Any]] = None


class JSONRPCResponse(BaseModel):
    """JSON-RPC 2.0 response."""
    jsonrpc: Literal["2.0"] = "2.0"
    id: Optional[int | str] = None
    result: Optional[Any] = None
    error: Optional[Dict[str, Any]] = None


class JSONRPCError(BaseModel):
    """JSON-RPC 2.0 error object."""
    code: int
    message: str
    data: Optional[Any] = None


class ToolSchema(BaseModel):
    """MCP Tool definition."""
    name: str
    description: str
    inputSchema: Dict[str, Any] = Field(
        description="JSON Schema describing the tool's input parameters"
    )


class ToolListResponse(BaseModel):
    """Response for tools/list method."""
    tools: List[ToolSchema]


class ToolCallRequest(BaseModel):
    """Request for tools/call method."""
    name: str
    arguments: Dict[str, Any]


class ToolCallResponse(BaseModel):
    """Response for tools/call method."""
    content: List[Dict[str, Any]]
    isError: bool = False

