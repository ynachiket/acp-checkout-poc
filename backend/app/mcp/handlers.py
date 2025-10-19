"""
MCP Tool Handlers

Implements the logic for each MCP tool.
These handlers call the ACP gateway, which in turn calls internal services.
"""

from typing import Dict, Any, List
from decimal import Decimal
from sqlalchemy.orm import Session

from app.services.product_service import ProductService, ProductNotFoundError
from app.services.checkout_service import CheckoutService
from app.services.payment_service import PaymentService
from app.services.order_service import OrderService


class MCPHandlers:
    """Handlers for MCP tool invocations."""
    
    def __init__(self, db: Session):
        self.db = db
        self.product_service = ProductService(db)
        self.checkout_service = CheckoutService(db)
        self.payment_service = PaymentService()
        self.order_service = OrderService(db)
    
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
        Create checkout tool handler.
        
        Creates a checkout session and returns session details.
        """
        # Convert items to internal format
        internal_items = []
        for item in items:
            product = self.product_service.get_by_gtin(item["gtin"])
            internal_items.append({
                "product_id": product.id,
                "quantity": item["quantity"]
            })
        
        buyer_info = None
        if buyer_email:
            buyer_info = {
                "email": buyer_email,
                "first_name": "Customer",
                "last_name": "User"
            }
        
        # Create session
        session = self.checkout_service.create_session(
            items=internal_items,
            buyer_info=buyer_info
        )
        
        return {
            "session_id": session.id,
            "status": session.status,
            "items": session.line_items,
            "subtotal": session.totals["subtotal"]["value"],
            "currency": session.currency,
            "message": "Checkout session created. Add shipping address to continue."
        }
    
    async def add_shipping_address(self, session_id: str, address: Dict) -> Dict:
        """
        Add shipping address tool handler.
        
        Updates session with address and calculates shipping/tax.
        """
        # Ensure address has required name field
        if "name" not in address:
            address["name"] = "Customer"
        
        session = self.checkout_service.update_session(
            session_id=session_id,
            address=address
        )
        
        return {
            "session_id": session.id,
            "status": session.status,
            "shipping_address": session.fulfillment_address,
            "shipping_options": session.fulfillment_options,
            "selected_shipping": session.selected_fulfillment_option_id,
            "totals": {
                "items": session.totals["items_total"]["value"],
                "shipping": session.totals["fulfillment"]["value"],
                "tax": session.totals["taxes"]["value"],
                "total": session.totals["total"]["value"]
            },
            "message": "Shipping calculated. Ready for payment."
        }
    
    async def complete_purchase(self, session_id: str, payment_method: Dict) -> Dict:
        """
        Complete purchase tool handler.
        
        Processes payment and creates order.
        """
        # Tokenize payment
        payment_token = self.payment_service.tokenize_payment(payment_method)
        
        # Get session and verify
        session = self.checkout_service.get_session(session_id)
        
        if session.status != "ready_for_payment":
            return {
                "error": "Session is not ready for payment",
                "status": session.status,
                "message": "Please add shipping address first."
            }
        
        # Process payment
        total_amount = Decimal(session.totals["total"]["value"])
        payment_intent = self.payment_service.create_payment_intent(total_amount, payment_token)
        
        if payment_intent["status"] != "succeeded":
            return {
                "error": "Payment failed",
                "message": "Payment was declined. Please check payment details."
            }
        
        # Create order
        order = self.order_service.create_order(session, payment_intent["id"])
        
        # Update session
        session.status = "completed"
        session.payment_token_id = payment_token
        session.order_id = order.id
        self.db.commit()
        
        return {
            "success": True,
            "order_id": order.id,
            "order_status": order.status,
            "total": session.totals["total"]["value"],
            "currency": session.currency,
            "permalink": order.permalink,
            "message": f"Order {order.id} confirmed! Confirmation email sent."
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

