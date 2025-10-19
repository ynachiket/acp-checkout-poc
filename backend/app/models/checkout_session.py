"""
Checkout Session Model

Represents a checkout session for the Agentic Commerce Protocol.
"""

from sqlalchemy import Column, String, JSON, DateTime, Text
from sqlalchemy.sql import func
from datetime import datetime, timedelta
from app.database import Base


class CheckoutSession(Base):
    """
    Checkout session model for managing purchase flow.
    
    Attributes:
        id: Unique session identifier
        status: Session status (not_ready_for_payment, ready_for_payment, completed, canceled)
        currency: Currency code (ISO 4217)
        line_items: List of items in cart (JSON)
        fulfillment_address: Shipping address (JSON)
        fulfillment_options: Available shipping options (JSON)
        selected_fulfillment_option_id: Selected shipping option
        totals: Price breakdown (JSON)
        buyer_info: Customer information (JSON)
        payment_token_id: Payment token from delegate payment
        order_id: Reference to created order
        session_metadata: Additional session data (JSON)
        expires_at: Session expiration timestamp (24 hours)
    """
    
    __tablename__ = "checkout_sessions"
    
    # Primary identifier
    id = Column(String(50), primary_key=True, index=True)
    
    # Status
    status = Column(
        String(30),
        nullable=False,
        default="not_ready_for_payment",
        index=True
    )  # not_ready_for_payment, ready_for_payment, completed, canceled
    
    # Currency
    currency = Column(String(3), nullable=False, default="USD")
    
    # Cart items
    line_items = Column(JSON, nullable=False)  # List of {gtin, quantity, unit_price, total}
    
    # Fulfillment information
    fulfillment_address = Column(JSON, nullable=True)  # {name, address_line_1, city, state, zip, country}
    fulfillment_options = Column(JSON, nullable=True)  # List of shipping options
    selected_fulfillment_option_id = Column(String(50), nullable=True)
    
    # Pricing
    totals = Column(JSON, nullable=True)  # {items_total, discounts, subtotal, fulfillment, taxes, fees, total}
    
    # Buyer information
    buyer_info = Column(JSON, nullable=True)  # {first_name, last_name, email, phone}
    
    # Payment
    payment_token_id = Column(String(100), nullable=True)  # From Stripe
    
    # Order reference
    order_id = Column(String(50), nullable=True, index=True)
    
    # Additional data
    session_metadata = Column(JSON, nullable=True)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    expires_at = Column(DateTime(timezone=True), nullable=True)
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        if not self.expires_at:
            # Default expiration: 24 hours from creation
            self.expires_at = datetime.utcnow() + timedelta(hours=24)
    
    def __repr__(self):
        return f"<CheckoutSession(id='{self.id}', status='{self.status}')>"
    
    def is_expired(self) -> bool:
        """Check if session has expired."""
        return datetime.utcnow() > self.expires_at if self.expires_at else False
    
    def to_dict(self):
        """Convert model to dictionary."""
        return {
            "id": self.id,
            "status": self.status,
            "currency": self.currency,
            "line_items": self.line_items,
            "fulfillment_address": self.fulfillment_address,
            "fulfillment_options": self.fulfillment_options,
            "selected_fulfillment_option_id": self.selected_fulfillment_option_id,
            "totals": self.totals,
            "buyer_info": self.buyer_info,
            "payment_token_id": self.payment_token_id,
            "order_id": self.order_id,
            "metadata": self.session_metadata,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
            "expires_at": self.expires_at.isoformat() if self.expires_at else None,
        }

