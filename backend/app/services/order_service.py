"""
Order Service

Simplified implementation for POC.
TODO: Add comprehensive tests (90% coverage target)
"""

import uuid
from typing import Dict
from datetime import datetime
from sqlalchemy.orm import Session

from app.models.order import Order
from app.models.order_event import OrderEvent
from app.models.checkout_session import CheckoutSession


class OrderService:
    """Service for order management."""
    
    def __init__(self, db: Session):
        self.db = db
    
    def create_order(
        self,
        session: CheckoutSession,
        payment_id: str
    ) -> Order:
        """
        Create order from completed checkout session.
        
        Args:
            session: Completed checkout session
            payment_id: Payment intent ID from Stripe
            
        Returns:
            Created order
        """
        order_id = f"order_{uuid.uuid4().hex[:12]}"
        
        # Extract shipping option details
        selected_option = next(
            (opt for opt in session.fulfillment_options 
             if opt["id"] == session.selected_fulfillment_option_id),
            session.fulfillment_options[0]
        )
        
        # Create order
        order = Order(
            id=order_id,
            checkout_session_id=session.id,
            status="created",
            line_items=session.line_items,
            shipping_address=session.fulfillment_address,
            shipping_option=selected_option,
            totals=session.totals,
            buyer_info=session.buyer_info,
            payment_id=payment_id,
            permalink=f"https://nike.com/orders/{order_id}"
        )
        
        self.db.add(order)
        
        # Create order event
        event = OrderEvent(
            id=f"evt_{uuid.uuid4().hex[:12]}",
            order_id=order_id,
            event_type="order.created",
            event_data={
                "total": session.totals["total"]["value"],
                "items_count": len(session.line_items)
            }
        )
        
        self.db.add(event)
        self.db.commit()
        self.db.refresh(order)
        
        return order
    
    def get_order(self, order_id: str) -> Order:
        """Get order by ID."""
        order = self.db.query(Order).filter(Order.id == order_id).first()
        
        if not order:
            raise ValueError(f"Order {order_id} not found")
        
        return order
    
    def update_order_status(self, order_id: str, status: str) -> Order:
        """
        Update order status.
        
        POC: Simple status update.
        Production: Would validate status transitions, update fulfillment systems.
        """
        order = self.get_order(order_id)
        order.status = status
        order.updated_at = datetime.utcnow()
        
        # Create event
        event = OrderEvent(
            id=f"evt_{uuid.uuid4().hex[:12]}",
            order_id=order_id,
            event_type=f"order.{status}",
            event_data={"status": status}
        )
        
        self.db.add(event)
        self.db.commit()
        self.db.refresh(order)
        
        return order

