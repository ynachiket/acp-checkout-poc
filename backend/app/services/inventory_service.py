"""
Inventory Service

Simplified implementation for POC.
TODO: Add comprehensive tests (90% coverage target)
"""

from typing import Dict
from sqlalchemy.orm import Session
from app.models.product import Product


class InventoryService:
    """Service for inventory management operations."""
    
    def __init__(self, db: Session):
        self.db = db
    
    def check_availability(self, product_id: str, quantity: int) -> bool:
        """
        Check if requested quantity is available.
        
        POC: Simple check based on product availability status.
        Production: Would check actual inventory levels.
        """
        product = self.db.query(Product).filter(Product.id == product_id).first()
        if not product:
            return False
        
        # For POC: in_stock = available for any reasonable quantity
        return product.availability == "in_stock" and quantity <= 10
    
    def get_inventory_level(self, product_id: str) -> Dict[str, any]:
        """
        Get inventory level for a product.
        
        Returns:
            Dict with availability info
        """
        product = self.db.query(Product).filter(Product.id == product_id).first()
        if not product:
            return {"available": False, "quantity": 0}
        
        # POC: Simplified inventory levels
        inventory_map = {
            "in_stock": 100,
            "out_of_stock": 0
        }
        
        return {
            "available": product.availability == "in_stock",
            "quantity": inventory_map.get(product.availability, 0)
        }

