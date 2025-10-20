"""
MCP Tool Definitions

Defines all commerce tools available to AI agents.
"""

from typing import List, Dict, Any
from app.mcp.schemas import ToolSchema


def get_tools() -> List[ToolSchema]:
    """
    Get all available MCP tools.
    
    Returns:
        List of tool definitions with schemas
    """
    return [
        ToolSchema(
            name="search_products",
            description="Search products by keywords, category, or price range. Returns a list of matching products with details.",
            inputSchema={
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "Search keywords (e.g., 'Air Max', 'running shoes', 'basketball')"
                    },
                    "category": {
                        "type": "string",
                        "description": "Filter by category (e.g., 'Shoes', 'Apparel', 'Equipment')",
                        "enum": ["Shoes", "Apparel", "Equipment"]
                    },
                    "price_max": {
                        "type": "number",
                        "description": "Maximum price filter in USD"
                    },
                    "limit": {
                        "type": "number",
                        "description": "Maximum number of results to return",
                        "default": 10
                    }
                },
                "required": ["query"]
            }
        ),
        
        ToolSchema(
            name="get_product_details",
            description="Get detailed information about a specific product by GTIN (Global Trade Item Number).",
            inputSchema={
                "type": "object",
                "properties": {
                    "gtin": {
                        "type": "string",
                        "description": "Product GTIN (8-14 digit number)",
                        "pattern": "^[0-9]{8,14}$"
                    }
                },
                "required": ["gtin"]
            }
        ),
        
        ToolSchema(
            name="create_checkout",
            description="Create a checkout session with selected products. Returns a session ID and initial pricing.",
            inputSchema={
                "type": "object",
                "properties": {
                    "items": {
                        "type": "array",
                        "description": "Products to add to cart",
                        "items": {
                            "type": "object",
                            "properties": {
                                "gtin": {"type": "string", "description": "Product GTIN"},
                                "quantity": {"type": "number", "description": "Quantity to purchase", "minimum": 1}
                            },
                            "required": ["gtin", "quantity"]
                        }
                    },
                    "buyer_email": {
                        "type": "string",
                        "description": "Customer email address",
                        "format": "email"
                    }
                },
                "required": ["items"]
            }
        ),
        
        ToolSchema(
            name="add_shipping_address",
            description="Add shipping address to checkout session and calculate shipping options and tax.",
            inputSchema={
                "type": "object",
                "properties": {
                    "session_id": {
                        "type": "string",
                        "description": "Checkout session ID from create_checkout"
                    },
                    "address": {
                        "type": "object",
                        "description": "Shipping address",
                        "properties": {
                            "name": {"type": "string"},
                            "address_line_1": {"type": "string"},
                            "address_line_2": {"type": "string"},
                            "city": {"type": "string"},
                            "state": {"type": "string"},
                            "postal_code": {"type": "string"},
                            "country": {"type": "string", "default": "US"}
                        },
                        "required": ["address_line_1", "city", "state", "postal_code"]
                    }
                },
                "required": ["session_id", "address"]
            }
        ),
        
        ToolSchema(
            name="complete_purchase",
            description="Complete the purchase by processing payment and creating the order. Returns order confirmation.",
            inputSchema={
                "type": "object",
                "properties": {
                    "session_id": {
                        "type": "string",
                        "description": "Checkout session ID"
                    },
                    "payment_method": {
                        "type": "object",
                        "description": "Payment method details (will be tokenized)",
                        "properties": {
                            "card_number": {"type": "string"},
                            "exp_month": {"type": "number"},
                            "exp_year": {"type": "number"},
                            "cvc": {"type": "string"}
                        },
                        "required": ["card_number", "exp_month", "exp_year", "cvc"]
                    }
                },
                "required": ["session_id", "payment_method"]
            }
        ),
        
        ToolSchema(
            name="get_order_status",
            description="Check the status of an order by order ID.",
            inputSchema={
                "type": "object",
                "properties": {
                    "order_id": {
                        "type": "string",
                        "description": "Order ID from order confirmation"
                    }
                },
                "required": ["order_id"]
            }
        ),
    ]

