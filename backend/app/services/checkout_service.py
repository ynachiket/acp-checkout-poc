"""
Checkout Service

Simplified implementation for POC.
TODO: Add comprehensive tests (90% coverage target)
"""

import uuid
from typing import List, Dict, Optional
from decimal import Decimal
from datetime import datetime, timedelta
from sqlalchemy.orm import Session

from app.models.checkout_session import CheckoutSession
from app.services.product_service import ProductService
from app.services.inventory_service import InventoryService
from app.services.shipping_service import ShippingService


class CheckoutService:
    """Service for checkout session management."""
    
    # POC: Flat tax rate
    TAX_RATE = Decimal("0.08")  # 8%
    
    def __init__(self, db: Session):
        self.db = db
        self.product_service = ProductService(db)
        self.inventory_service = InventoryService(db)
        self.shipping_service = ShippingService()
    
    def create_session(
        self,
        items: List[Dict],
        address: Optional[Dict] = None,
        buyer_info: Optional[Dict] = None
    ) -> CheckoutSession:
        """
        Create a new checkout session.
        
        Args:
            items: List of {product_id, quantity}
            address: Optional shipping address
            buyer_info: Optional buyer information
        """
        session_id = f"cs_{uuid.uuid4().hex[:16]}"
        
        # Build line items with pricing
        line_items = []
        items_total = Decimal("0.00")
        
        for item in items:
            product = self.product_service.get_by_id(item["product_id"])
            
            # Check availability
            if not self.inventory_service.check_availability(product.id, item["quantity"]):
                raise ValueError(f"Product {product.id} not available in requested quantity")
            
            unit_price = product.price
            quantity = item["quantity"]
            item_total = unit_price * quantity
            
            line_items.append({
                "gtin": product.gtin,
                "product_id": product.id,
                "title": product.title,
                "quantity": quantity,
                "unit_price": float(unit_price),
                "total": float(item_total)
            })
            
            items_total += item_total
        
        # Calculate shipping if address provided
        fulfillment_options = None
        shipping_cost = Decimal("0.00")
        selected_option_id = None
        
        if address:
            is_valid, error = self.shipping_service.validate_address(address)
            if not is_valid:
                raise ValueError(f"Invalid address: {error}")
            
            fulfillment_options = self.shipping_service.calculate_options(address, items_total)
            # Default to standard shipping
            shipping_cost = Decimal(fulfillment_options[0]["cost"])
            selected_option_id = fulfillment_options[0]["id"]
        
        # Calculate totals
        subtotal = items_total
        tax = subtotal * self.TAX_RATE
        total = subtotal + shipping_cost + tax
        
        totals = {
            "items_total": {"value": str(items_total), "currency": "USD"},
            "discounts": {"value": "0.00", "currency": "USD"},
            "subtotal": {"value": str(subtotal), "currency": "USD"},
            "fulfillment": {"value": str(shipping_cost), "currency": "USD"},
            "taxes": {"value": str(tax), "currency": "USD"},
            "fees": {"value": "0.00", "currency": "USD"},
            "total": {"value": str(total), "currency": "USD"}
        }
        
        # Determine status
        status = "ready_for_payment" if address else "not_ready_for_payment"
        
        # Create session
        session = CheckoutSession(
            id=session_id,
            status=status,
            currency="USD",
            line_items=line_items,
            fulfillment_address=address,
            fulfillment_options=fulfillment_options,
            selected_fulfillment_option_id=selected_option_id,
            totals=totals,
            buyer_info=buyer_info,
            expires_at=datetime.utcnow() + timedelta(hours=24)
        )
        
        self.db.add(session)
        self.db.commit()
        self.db.refresh(session)
        
        return session
    
    def get_session(self, session_id: str) -> CheckoutSession:
        """Get checkout session by ID."""
        session = self.db.query(CheckoutSession).filter(
            CheckoutSession.id == session_id
        ).first()
        
        if not session:
            raise ValueError(f"Session {session_id} not found")
        
        if session.is_expired():
            raise ValueError(f"Session {session_id} has expired")
        
        return session
    
    def update_session(
        self,
        session_id: str,
        address: Optional[Dict] = None,
        fulfillment_option_id: Optional[str] = None
    ) -> CheckoutSession:
        """Update checkout session with new information."""
        session = self.get_session(session_id)
        
        # Update address if provided
        if address:
            is_valid, error = self.shipping_service.validate_address(address)
            if not is_valid:
                raise ValueError(f"Invalid address: {error}")
            
            session.fulfillment_address = address
            
            # Recalculate shipping
            items_total = Decimal(session.totals["items_total"]["value"])
            fulfillment_options = self.shipping_service.calculate_options(address, items_total)
            session.fulfillment_options = fulfillment_options
            
            # Use provided option or default to first
            if fulfillment_option_id:
                session.selected_fulfillment_option_id = fulfillment_option_id
            else:
                session.selected_fulfillment_option_id = fulfillment_options[0]["id"]
            
            # Recalculate totals
            selected_option = next(
                (opt for opt in fulfillment_options if opt["id"] == session.selected_fulfillment_option_id),
                fulfillment_options[0]
            )
            shipping_cost = Decimal(selected_option["cost"])
            tax = items_total * self.TAX_RATE
            total = items_total + shipping_cost + tax
            
            session.totals["fulfillment"] = {"value": str(shipping_cost), "currency": "USD"}
            session.totals["taxes"] = {"value": str(tax), "currency": "USD"}
            session.totals["total"] = {"value": str(total), "currency": "USD"}
            
            # Update status
            session.status = "ready_for_payment"
        
        # Update fulfillment option if provided
        elif fulfillment_option_id and session.fulfillment_options:
            session.selected_fulfillment_option_id = fulfillment_option_id
            
            # Recalculate totals
            selected_option = next(
                opt for opt in session.fulfillment_options 
                if opt["id"] == fulfillment_option_id
            )
            items_total = Decimal(session.totals["items_total"]["value"])
            shipping_cost = Decimal(selected_option["cost"])
            tax = items_total * self.TAX_RATE
            total = items_total + shipping_cost + tax
            
            session.totals["fulfillment"] = {"value": str(shipping_cost), "currency": "USD"}
            session.totals["total"] = {"value": str(total), "currency": "USD"}
        
        session.updated_at = datetime.utcnow()
        self.db.commit()
        self.db.refresh(session)
        
        return session

