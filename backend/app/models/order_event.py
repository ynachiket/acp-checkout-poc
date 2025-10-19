"""
Order Event Model

Tracks lifecycle events for orders.
"""

from sqlalchemy import Column, String, JSON, DateTime
from sqlalchemy.sql import func
from app.database import Base


class OrderEvent(Base):
    """
    Order event model for tracking order lifecycle.
    
    Attributes:
        id: Unique event identifier
        order_id: Reference to order
        event_type: Type of event (created, confirmed, shipped, delivered, canceled)
        event_data: Additional event data (JSON)
        created_at: Event timestamp
    """
    
    __tablename__ = "order_events"
    
    # Primary identifier
    id = Column(String(50), primary_key=True, index=True)
    
    # Order reference
    order_id = Column(String(50), nullable=False, index=True)
    
    # Event information
    event_type = Column(
        String(30),
        nullable=False,
        index=True
    )  # order.created, order.updated, order.shipped, order.delivered, order.canceled
    
    event_data = Column(JSON, nullable=True)  # Additional event details
    
    # Timestamp
    created_at = Column(DateTime(timezone=True), server_default=func.now(), index=True)
    
    def __repr__(self):
        return f"<OrderEvent(id='{self.id}', order_id='{self.order_id}', event_type='{self.event_type}')>"
    
    def to_dict(self):
        """Convert model to dictionary."""
        return {
            "id": self.id,
            "order_id": self.order_id,
            "event_type": self.event_type,
            "event_data": self.event_data,
            "created_at": self.created_at.isoformat() if self.created_at else None,
        }

