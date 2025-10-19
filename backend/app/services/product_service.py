"""
Product Service

Protocol-agnostic service for product catalog operations.
This service has NO knowledge of ACP, MCP, or any external protocols.
"""

from typing import List, Optional, Tuple
from decimal import Decimal
from sqlalchemy.orm import Session
from sqlalchemy import or_, and_

from app.models.product import Product


# ============================================================================
# Custom Exceptions
# ============================================================================

class ProductNotFoundError(Exception):
    """Raised when a product is not found."""
    pass


class InvalidGTINError(Exception):
    """Raised when GTIN format is invalid."""
    pass


# ============================================================================
# Product Service
# ============================================================================

class ProductService:
    """
    Service for managing product catalog operations.
    
    This service is protocol-agnostic and contains pure business logic.
    It has no knowledge of ACP, MCP, or any external protocols.
    """
    
    def __init__(self, db: Session):
        """
        Initialize Product Service.
        
        Args:
            db: Database session
        """
        self.db = db
    
    def search_products(
        self,
        query: str = "",
        category: Optional[str] = None,
        price_min: Optional[Decimal] = None,
        price_max: Optional[Decimal] = None,
        availability: Optional[str] = None,
        limit: int = 100
    ) -> List[Product]:
        """
        Search products with filters.
        
        Args:
            query: Search query (searches title and description)
            category: Filter by category (partial match)
            price_min: Minimum price filter
            price_max: Maximum price filter
            availability: Filter by availability status
            limit: Maximum number of results
            
        Returns:
            List of matching products
            
        Example:
            >>> products = service.search_products(
            ...     query="Air Max",
            ...     category="Running",
            ...     price_max=Decimal("150.00"),
            ...     availability="in_stock"
            ... )
        """
        # Start with base query
        query_obj = self.db.query(Product)
        
        # Apply search query (case-insensitive)
        if query:
            search_term = f"%{query.lower()}%"
            query_obj = query_obj.filter(
                or_(
                    Product.title.ilike(search_term),
                    Product.description.ilike(search_term)
                )
            )
        
        # Apply filters
        if category:
            query_obj = query_obj.filter(Product.category.ilike(f"%{category}%"))
        
        if price_min is not None:
            query_obj = query_obj.filter(Product.price >= price_min)
        
        if price_max is not None:
            query_obj = query_obj.filter(Product.price <= price_max)
        
        if availability:
            query_obj = query_obj.filter(Product.availability == availability)
        
        # Apply limit and execute
        return query_obj.limit(limit).all()
    
    def get_by_id(self, product_id: str) -> Product:
        """
        Get product by internal ID.
        
        Args:
            product_id: Internal product identifier
            
        Returns:
            Product instance
            
        Raises:
            ValueError: If product_id is None or empty
            ProductNotFoundError: If product not found
            
        Example:
            >>> product = service.get_by_id("nike-air-max-90")
        """
        if not product_id:
            raise ValueError("Product ID cannot be None or empty")
        
        product = self.db.query(Product).filter(Product.id == product_id).first()
        
        if not product:
            raise ProductNotFoundError(f"Product with ID '{product_id}' not found")
        
        return product
    
    def get_by_gtin(self, gtin: str) -> Product:
        """
        Get product by GTIN (Global Trade Item Number).
        
        Args:
            gtin: GTIN identifier (8-14 digits)
            
        Returns:
            Product instance
            
        Raises:
            InvalidGTINError: If GTIN format is invalid
            ProductNotFoundError: If product not found
            
        Example:
            >>> product = service.get_by_gtin("00883419552502")
        """
        # Validate GTIN format
        if not gtin or not gtin.isdigit():
            raise InvalidGTINError(f"GTIN must be numeric, got: {gtin}")
        
        if len(gtin) < 8 or len(gtin) > 14:
            raise InvalidGTINError(f"GTIN must be 8-14 digits, got {len(gtin)} digits")
        
        # Query by GTIN
        product = self.db.query(Product).filter(Product.gtin == gtin).first()
        
        if not product:
            raise ProductNotFoundError(f"Product with GTIN '{gtin}' not found")
        
        return product
    
    def check_buyability(self, product_id: str) -> Tuple[bool, Optional[str]]:
        """
        Check if a product can be purchased through ACP.
        
        Implements buyability constraints:
        - Product must be in stock
        - No gift cards
        - No Nike By You (customizable products)
        - No other restricted product types
        
        Args:
            product_id: Internal product identifier
            
        Returns:
            Tuple of (is_buyable, reason_if_not_buyable)
            
        Raises:
            ProductNotFoundError: If product not found
            
        Example:
            >>> is_buyable, reason = service.check_buyability("nike-air-max-90")
            >>> if not is_buyable:
            ...     print(f"Cannot buy: {reason}")
        """
        # Get product
        product = self.get_by_id(product_id)
        
        # Check availability
        if product.availability != "in_stock":
            return False, "Product is out of stock"
        
        # Check for gift cards
        if product.category and "gift card" in product.category.lower():
            return False, "Gift cards cannot be purchased through this channel"
        
        if product.title and "gift card" in product.title.lower():
            return False, "Gift cards cannot be purchased through this channel"
        
        # Check for customizable products (Nike By You)
        if product.category and "customizable" in product.category.lower():
            return False, "Customizable products (Nike By You) cannot be purchased through this channel"
        
        if product.product_metadata and product.product_metadata.get("customizable"):
            return False, "Customizable products (Nike By You) cannot be purchased through this channel"
        
        # Product is buyable
        return True, None
    
    def get_variants(self, product_id: str) -> List[dict]:
        """
        Get product variants (sizes, colors, etc.).
        
        Args:
            product_id: Internal product identifier
            
        Returns:
            List of variant dictionaries
            
        Raises:
            ProductNotFoundError: If product not found
            
        Example:
            >>> variants = service.get_variants("nike-air-max-90")
            >>> for variant in variants:
            ...     print(f"Size: {variant['size']}")
        """
        product = self.get_by_id(product_id)
        
        if not product.variants:
            return []
        
        return product.variants

