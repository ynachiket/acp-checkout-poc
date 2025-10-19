"""
MCP Tool Handlers (Hybrid Strategy)

Implements the logic for each MCP tool.

HYBRID STRATEGY:
- MCP provides tool discovery and AI-friendly interface
- Handlers delegate to ACP REST endpoints for scalable execution
- Best of both worlds: MCP UX + ACP scalability
"""

from typing import Dict, Any, List
from decimal import Decimal
from sqlalchemy.orm import Session

from app.services.product_service import ProductService, ProductNotFoundError
from app.services.order_service import OrderService
from app.mcp.acp_client import ACPClient


class MCPHandlers:
    """
    Handlers for MCP tool invocations.
    
    Uses hybrid strategy: Delegates to ACP endpoints for scalability.
    """
    
    def __init__(self, db: Session):
        self.db = db
        # For product search (read-only, can use service directly)
        self.product_service = ProductService(db)
        self.order_service = OrderService(db)
        # For write operations, use ACP client (hybrid strategy)
        self.acp_client = ACPClient()
    
    async def search_products(self, query: str, category: str = None, price_max: float = None, limit: int = 10) -> List[Dict]:
        """
        Search products tool handler.
        
        Returns list of products matching search criteria.
        """
        price_max_decimal = Decimal(str(price_max)) if price_max else None
        
        products = self.product_service.search_products(
            query=query,
            category=category,
            price_max=price_max_decimal,
            limit=limit
        )
        
        return [
            {
                "gtin": p.gtin,
                "title": p.title,
                "description": p.description,
                "price": float(p.price),
                "currency": p.currency,
                "category": p.category,
                "availability": p.availability,
                "images": p.images if p.images else []
            }
            for p in products
        ]
    
    async def get_product_details(self, gtin: str) -> Dict:
        """
        Get product details tool handler.
        
        Returns detailed product information.
        """
        try:
            product = self.product_service.get_by_gtin(gtin)
            
            return {
                "gtin": product.gtin,
                "id": product.id,
                "title": product.title,
                "description": product.description,
                "price": float(product.price),
                "currency": product.currency,
                "brand": product.brand,
                "category": product.category,
                "availability": product.availability,
                "images": product.images if product.images else [],
                "variants": product.variants if product.variants else []
            }
        except ProductNotFoundError as e:
            return {"error": str(e), "gtin": gtin}
    
    async def create_checkout(self, items: List[Dict], buyer_email: str = None) -> Dict:
        """
        Create checkout tool handler (HYBRID).
        
        Delegates to ACP REST endpoint for scalability.
        """
        # Build buyer_info if email provided
        buyer_info = None
        if buyer_email:
            buyer_info = {
                "email": buyer_email,
                "first_name": "Customer",
                "last_name": "User"
            }
        
        # HYBRID: Call ACP endpoint instead of service directly
        acp_response = await self.acp_client.create_checkout_session(
            line_items=items,
            buyer_info=buyer_info
        )
        
        # Transform ACP response to MCP-friendly format
        return {
            "session_id": acp_response["id"],
            "status": acp_response["status"],
            "items": acp_response["line_items"],
            "subtotal": acp_response["totals"]["subtotal"]["value"],
            "currency": acp_response["currency"],
            "message": "Checkout session created. Add shipping address to continue.",
            "_acp_call": "✅ Used ACP REST for scalability"
        }
    
    async def add_shipping_address(self, session_id: str, address: Dict) -> Dict:
        """
        Add shipping address tool handler (HYBRID).
        
        Delegates to ACP REST endpoint for scalability.
        """
        # Ensure address has required name field
        if "name" not in address:
            address["name"] = "Customer"
        
        # HYBRID: Call ACP endpoint
        acp_response = await self.acp_client.update_checkout_session(
            session_id=session_id,
            fulfillment_address=address
        )
        
        # Transform to MCP-friendly format
        return {
            "session_id": acp_response["id"],
            "status": acp_response["status"],
            "shipping_address": acp_response["fulfillment_address"],
            "shipping_options": acp_response["fulfillment_options"],
            "selected_shipping": acp_response["selected_fulfillment_option_id"],
            "totals": {
                "items": acp_response["totals"]["items_total"]["value"],
                "shipping": acp_response["totals"]["fulfillment"]["value"],
                "tax": acp_response["totals"]["taxes"]["value"],
                "total": acp_response["totals"]["total"]["value"]
            },
            "message": "Shipping calculated. Ready for payment.",
            "_acp_call": "✅ Used ACP REST for scalability"
        }
    
    async def complete_purchase(self, session_id: str, payment_method: Dict) -> Dict:
        """
        Complete purchase tool handler (HYBRID).
        
        Delegates to ACP REST endpoints for scalability.
        """
        try:
            # HYBRID: Step 1 - Tokenize via ACP endpoint
            payment_token = await self.acp_client.delegate_payment(payment_method)
            
            # HYBRID: Step 2 - Complete via ACP endpoint
            acp_response = await self.acp_client.complete_checkout_session(
                session_id=session_id,
                payment_token_id=payment_token
            )
            
            # Transform to MCP-friendly format
            return {
                "success": True,
                "order_id": acp_response["order"]["id"],
                "order_status": "created",
                "total": "0.00",  # Would get from ACP response if needed
                "currency": "USD",
                "permalink": acp_response["order"]["permalink"],
                "message": acp_response["messages"][0]["text"] if acp_response.get("messages") else f"Order {acp_response['order']['id']} confirmed!",
                "_acp_calls": "✅ Used ACP REST (2 calls: tokenize + complete)"
            }
        
        except Exception as e:
            return {
                "error": str(e),
                "message": "Failed to complete purchase. Please try again."
            }
    
    async def get_order_status(self, order_id: str) -> Dict:
        """
        Get order status tool handler.
        
        Returns current order information.
        """
        try:
            order = self.order_service.get_order(order_id)
            
            return {
                "order_id": order.id,
                "status": order.status,
                "items": order.line_items,
                "shipping_address": order.shipping_address,
                "total": order.totals["total"]["value"],
                "tracking_number": order.tracking_number,
                "permalink": order.permalink,
                "created_at": order.created_at.isoformat() if order.created_at else None
            }
        except ValueError as e:
            return {
                "error": str(e),
                "order_id": order_id
            }

