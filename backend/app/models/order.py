"""
Order Model

Represents a completed order.
"""

from sqlalchemy import Column, String, JSON, DateTime, Text
from sqlalchemy.sql import func
from app.database import Base


class Order(Base):
    """
    Order model representing completed purchases.
    
    Attributes:
        id: Unique order identifier
        checkout_session_id: Reference to checkout session
        status: Order status (created, confirmed, processing, shipped, delivered, canceled)
        line_items: Ordered items (JSON)
        shipping_address: Delivery address (JSON)
        shipping_option: Selected shipping method (JSON)
        totals: Price breakdown (JSON)
        buyer_info: Customer information (JSON)
        payment_id: Payment identifier from Stripe
        tracking_number: Shipping tracking number
        permalink: URL to view order details
        order_metadata: Additional order data (JSON)
    """
    
    __tablename__ = "orders"
    
    # Primary identifier
    id = Column(String(50), primary_key=True, index=True)
    
    # Reference to checkout session
    checkout_session_id = Column(String(50), nullable=False, index=True)
    
    # Status
    status = Column(
        String(30),
        nullable=False,
        default="created",
        index=True
    )  # created, confirmed, processing, shipped, delivered, canceled
    
    # Order contents
    line_items = Column(JSON, nullable=False)  # List of {gtin, quantity, unit_price, total, title}
    
    # Fulfillment
    shipping_address = Column(JSON, nullable=False)  # {name, address, city, state, zip, country}
    shipping_option = Column(JSON, nullable=False)  # {id, title, cost, delivery_estimate}
    tracking_number = Column(String(100), nullable=True, index=True)
    
    # Pricing
    totals = Column(JSON, nullable=False)  # {items_total, fulfillment, taxes, total}
    
    # Buyer information
    buyer_info = Column(JSON, nullable=False)  # {first_name, last_name, email, phone}
    
    # Payment
    payment_id = Column(String(100), nullable=False)  # Stripe payment intent ID
    
    # Permalink
    permalink = Column(Text, nullable=True)  # URL to view order
    
    # Additional data
    order_metadata = Column(JSON, nullable=True)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    
    def __repr__(self):
        return f"<Order(id='{self.id}', status='{self.status}')>"
    
    def to_dict(self):
        """Convert model to dictionary."""
        return {
            "id": self.id,
            "checkout_session_id": self.checkout_session_id,
            "status": self.status,
            "line_items": self.line_items,
            "shipping_address": self.shipping_address,
            "shipping_option": self.shipping_option,
            "tracking_number": self.tracking_number,
            "totals": self.totals,
            "buyer_info": self.buyer_info,
            "payment_id": self.payment_id,
            "permalink": self.permalink,
            "metadata": self.order_metadata,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
        }

