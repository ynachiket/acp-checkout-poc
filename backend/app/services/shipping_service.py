"""
Shipping Service

Simplified implementation for POC.
TODO: Add comprehensive tests (90% coverage target)
"""

from typing import List, Dict
from decimal import Decimal


class ShippingService:
    """Service for shipping calculations."""
    
    # POC: Fixed shipping options
    SHIPPING_OPTIONS = [
        {
            "id": "standard",
            "title": "Standard Shipping",
            "subtitle": "5-7 business days",
            "cost": "5.00",  # String for JSON serialization
            "delivery_min_days": 5,
            "delivery_max_days": 7
        },
        {
            "id": "express",
            "title": "Express Shipping",
            "subtitle": "2-3 business days",
            "cost": "15.00",  # String for JSON serialization
            "delivery_min_days": 2,
            "delivery_max_days": 3
        },
        {
            "id": "overnight",
            "title": "Overnight Shipping",
            "subtitle": "1 business day",
            "cost": "25.00",  # String for JSON serialization
            "delivery_min_days": 1,
            "delivery_max_days": 1
        }
    ]
    
    def __init__(self):
        pass
    
    def calculate_options(self, address: Dict, cart_total: Decimal) -> List[Dict]:
        """
        Calculate available shipping options.
        
        POC: Returns fixed options.
        Production: Would calculate based on address, weight, carrier rates.
        """
        # POC: Return all options for any address
        return [option.copy() for option in self.SHIPPING_OPTIONS]
    
    def validate_address(self, address: Dict) -> tuple[bool, str]:
        """
        Validate shipping address.
        
        Returns:
            (is_valid, error_message)
        """
        required_fields = ["address_line_1", "city", "state", "postal_code", "country"]
        
        for field in required_fields:
            if not address.get(field):
                return False, f"Missing required field: {field}"
        
        # POC: Basic validation only
        if address["country"] != "US":
            return False, "Currently only shipping to US addresses"
        
        return True, ""

