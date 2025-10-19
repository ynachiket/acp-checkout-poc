"""
MCP Server Implementation

Implements the Model Context Protocol for AI agent tool discovery and invocation.
"""

from typing import Dict, Any, List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.mcp.schemas import JSONRPCRequest, JSONRPCResponse, JSONRPCError, ToolListResponse
from app.mcp.tools import get_tools
from app.mcp.handlers import MCPHandlers


# Create router for MCP endpoints
router = APIRouter(prefix="/mcp", tags=["MCP Protocol"])


@router.post("", response_model=JSONRPCResponse)
@router.post("/", response_model=JSONRPCResponse)
async def mcp_endpoint(
    request: JSONRPCRequest,
    db: Session = Depends(get_db)
):
    """
    MCP JSON-RPC 2.0 endpoint.
    
    Handles:
    - tools/list: Discover available tools
    - tools/call: Invoke a specific tool
    """
    try:
        # Route based on method
        if request.method == "tools/list":
            return handle_tools_list(request)
        
        elif request.method == "tools/call":
            return await handle_tools_call(request, db)
        
        else:
            # Method not found
            return JSONRPCResponse(
                id=request.id,
                error=JSONRPCError(
                    code=-32601,
                    message=f"Method not found: {request.method}"
                ).dict()
            )
    
    except Exception as e:
        # Internal error
        return JSONRPCResponse(
            id=request.id,
            error=JSONRPCError(
                code=-32603,
                message=f"Internal error: {str(e)}"
            ).dict()
        )


def handle_tools_list(request: JSONRPCRequest) -> JSONRPCResponse:
    """
    Handle tools/list request.
    
    Returns list of available tools with their schemas.
    """
    tools = get_tools()
    
    return JSONRPCResponse(
        id=request.id,
        result={
            "tools": [tool.dict() for tool in tools]
        }
    )


async def handle_tools_call(request: JSONRPCRequest, db: Session) -> JSONRPCResponse:
    """
    Handle tools/call request.
    
    Invokes the specified tool with provided arguments.
    """
    if not request.params:
        return JSONRPCResponse(
            id=request.id,
            error=JSONRPCError(
                code=-32602,
                message="Missing params for tools/call"
            ).dict()
        )
    
    tool_name = request.params.get("name")
    arguments = request.params.get("arguments", {})
    
    if not tool_name:
        return JSONRPCResponse(
            id=request.id,
            error=JSONRPCError(
                code=-32602,
                message="Missing tool name in params"
            ).dict()
        )
    
    # Create handlers
    handlers = MCPHandlers(db)
    
    # Route to appropriate handler
    try:
        if tool_name == "search_products":
            result = await handlers.search_products(**arguments)
        
        elif tool_name == "get_product_details":
            result = await handlers.get_product_details(**arguments)
        
        elif tool_name == "create_checkout":
            result = await handlers.create_checkout(**arguments)
        
        elif tool_name == "add_shipping_address":
            result = await handlers.add_shipping_address(**arguments)
        
        elif tool_name == "complete_purchase":
            result = await handlers.complete_purchase(**arguments)
        
        elif tool_name == "get_order_status":
            result = await handlers.get_order_status(**arguments)
        
        else:
            return JSONRPCResponse(
                id=request.id,
                error=JSONRPCError(
                    code=-32601,
                    message=f"Tool not found: {tool_name}"
                ).dict()
            )
        
        # Return success response with proper JSON
        import json
        
        return JSONRPCResponse(
            id=request.id,
            result={
                "content": [
                    {
                        "type": "text",
                        "text": json.dumps(result) if isinstance(result, (dict, list)) else str(result)
                    },
                    {
                        "type": "resource",
                        "resource": {
                            "uri": f"nike://commerce/{tool_name}",
                            "mimeType": "application/json",
                            "text": json.dumps(result)  # Proper JSON serialization
                        }
                    }
                ],
                "isError": "error" in result if isinstance(result, dict) else False
            }
        )
    
    except Exception as e:
        return JSONRPCResponse(
            id=request.id,
            error=JSONRPCError(
                code=-32603,
                message=f"Tool execution error: {str(e)}"
            ).dict()
        )


class MCPServer:
    """
    MCP Server class for managing tool discovery and invocation.
    
    This can be used programmatically or via the FastAPI router.
    """
    
    def __init__(self, db: Session):
        self.db = db
        self.handlers = MCPHandlers(db)
    
    def list_tools(self) -> List[Dict[str, Any]]:
        """List all available tools."""
        tools = get_tools()
        return [tool.dict() for tool in tools]
    
    async def call_tool(self, tool_name: str, arguments: Dict[str, Any]) -> Any:
        """Call a specific tool with arguments."""
        handler_method = getattr(self.handlers, tool_name, None)
        
        if not handler_method:
            raise ValueError(f"Tool not found: {tool_name}")
        
        return await handler_method(**arguments)

