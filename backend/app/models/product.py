"""
Product Model

Represents a Nike product in the catalog.
"""

from sqlalchemy import Column, String, Numeric, JSON, DateTime, Text
from sqlalchemy.sql import func
from app.database import Base


class Product(Base):
    """
    Product model representing items in the catalog.
    
    Attributes:
        id: Internal product ID
        gtin: Global Trade Item Number (8-14 digits)
        mpn: Manufacturer Part Number (Nike product code)
        title: Product title (max 150 chars)
        description: Product description (max 5000 chars)
        brand: Brand name (e.g., "Nike", "Nike Sportswear")
        category: Hierarchical category (e.g., "Shoes > Running > Sneakers")
        price: Product price (Decimal for precision)
        currency: Currency code (ISO 4217, e.g., "USD")
        images: List of image URLs (JSON)
        availability: Stock status ("in_stock", "out_of_stock")
        variants: Product variants (JSON list of size/color options)
        product_metadata: Additional product metadata (JSON)
    """
    
    __tablename__ = "products"
    
    # Primary identifiers
    id = Column(String(100), primary_key=True, index=True)
    gtin = Column(String(14), unique=True, nullable=False, index=True)
    mpn = Column(String(50), nullable=True, index=True)
    
    # Product information
    title = Column(String(150), nullable=False)
    description = Column(Text, nullable=True)
    brand = Column(String(70), nullable=False, default="Nike")
    category = Column(String(200), nullable=True, index=True)
    
    # Pricing
    price = Column(Numeric(10, 2), nullable=False)
    currency = Column(String(3), nullable=False, default="USD")
    
    # Media
    images = Column(JSON, nullable=True)  # List of image URLs
    
    # Availability
    availability = Column(String(20), nullable=False, default="in_stock", index=True)
    
    # Variants (sizes, colors)
    variants = Column(JSON, nullable=True)
    
    # Additional metadata (renamed from 'metadata' to avoid SQLAlchemy reserved name)
    product_metadata = Column(JSON, nullable=True)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    
    def __repr__(self):
        return f"<Product(id='{self.id}', gtin='{self.gtin}', title='{self.title}')>"
    
    def to_dict(self):
        """Convert model to dictionary."""
        return {
            "id": self.id,
            "gtin": self.gtin,
            "mpn": self.mpn,
            "title": self.title,
            "description": self.description,
            "brand": self.brand,
            "category": self.category,
            "price": float(self.price) if self.price else None,
            "currency": self.currency,
            "images": self.images,
            "availability": self.availability,
            "variants": self.variants,
            "metadata": self.product_metadata,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
        }

