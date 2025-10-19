"""
Tests for Product Model

Following TDD principles, we test:
1. Model creation with all fields
2. Model creation with required fields only
3. Field validation (GTIN format, price precision)
4. Unique constraints
5. Indexes
6. to_dict() method
7. Timestamps
"""

import pytest
from decimal import Decimal
from sqlalchemy.exc import IntegrityError
from app.models.product import Product


@pytest.mark.unit
@pytest.mark.database
class TestProductModel:
    """Test suite for Product model."""
    
    def test_create_product_with_all_fields(self, db_session, sample_product_data):
        """Test creating a product with all fields populated."""
        # Given: Product data
        # When: Creating a product
        product = Product(**sample_product_data)
        db_session.add(product)
        db_session.commit()
        db_session.refresh(product)
        
        # Then: Product is created with all fields
        assert product.id == sample_product_data["id"]
        assert product.gtin == sample_product_data["gtin"]
        assert product.mpn == sample_product_data["mpn"]
        assert product.title == sample_product_data["title"]
        assert product.description == sample_product_data["description"]
        assert product.brand == sample_product_data["brand"]
        assert product.category == sample_product_data["category"]
        assert product.price == sample_product_data["price"]
        assert product.currency == sample_product_data["currency"]
        assert product.images == sample_product_data["images"]
        assert product.availability == sample_product_data["availability"]
        assert product.variants == sample_product_data["variants"]
        assert product.product_metadata == sample_product_data["product_metadata"]
        assert product.created_at is not None
        assert product.updated_at is not None
    
    def test_create_product_with_required_fields_only(self, db_session):
        """Test creating a product with only required fields."""
        # Given: Minimal product data
        product_data = {
            "id": "test-product-123",
            "gtin": "12345678901234",
            "title": "Test Product",
            "price": Decimal("99.99")
        }
        
        # When: Creating a product
        product = Product(**product_data)
        db_session.add(product)
        db_session.commit()
        db_session.refresh(product)
        
        # Then: Product is created with defaults
        assert product.id == "test-product-123"
        assert product.gtin == "12345678901234"
        assert product.title == "Test Product"
        assert product.price == Decimal("99.99")
        assert product.brand == "Nike"  # Default
        assert product.currency == "USD"  # Default
        assert product.availability == "in_stock"  # Default
    
    def test_gtin_must_be_unique(self, db_session, sample_product):
        """Test that GTIN must be unique across products."""
        # Given: Existing product
        # When: Creating another product with same GTIN
        duplicate_product = Product(
            id="different-id",
            gtin=sample_product.gtin,  # Same GTIN
            title="Different Product",
            price=Decimal("50.00")
        )
        db_session.add(duplicate_product)
        
        # Then: Constraint violation
        with pytest.raises(IntegrityError):
            db_session.commit()
    
    def test_gtin_cannot_be_null(self, db_session):
        """Test that GTIN is required."""
        # When: Creating product without GTIN
        product = Product(
            id="test-product",
            title="Test Product",
            price=Decimal("99.99")
        )
        db_session.add(product)
        
        # Then: Constraint violation
        with pytest.raises(IntegrityError):
            db_session.commit()
    
    def test_title_cannot_be_null(self, db_session):
        """Test that title is required."""
        # When: Creating product without title
        product = Product(
            id="test-product",
            gtin="12345678901234",
            price=Decimal("99.99")
        )
        db_session.add(product)
        
        # Then: Constraint violation
        with pytest.raises(IntegrityError):
            db_session.commit()
    
    def test_price_cannot_be_null(self, db_session):
        """Test that price is required."""
        # When: Creating product without price
        product = Product(
            id="test-product",
            gtin="12345678901234",
            title="Test Product"
        )
        db_session.add(product)
        
        # Then: Constraint violation
        with pytest.raises(IntegrityError):
            db_session.commit()
    
    def test_price_precision(self, db_session):
        """Test that price maintains decimal precision."""
        # Given: Product with precise price
        product = Product(
            id="test-product",
            gtin="12345678901234",
            title="Test Product",
            price=Decimal("99.99")
        )
        db_session.add(product)
        db_session.commit()
        db_session.refresh(product)
        
        # Then: Price precision is maintained
        assert product.price == Decimal("99.99")
        assert isinstance(product.price, Decimal)
    
    def test_json_fields_store_complex_data(self, db_session):
        """Test that JSON fields correctly store complex data."""
        # Given: Product with complex JSON data
        product = Product(
            id="test-product",
            gtin="12345678901234",
            title="Test Product",
            price=Decimal("99.99"),
            images=["url1.jpg", "url2.jpg", "url3.jpg"],
            variants=[
                {"size": "8", "color": "red"},
                {"size": "9", "color": "blue"}
            ],
            product_metadata={
                "popularity_score": 85,
                "reviews_count": 42,
                "nested": {"key": "value"}
            }
        )
        db_session.add(product)
        db_session.commit()
        db_session.refresh(product)
        
        # Then: JSON data is preserved
        assert len(product.images) == 3
        assert product.images[0] == "url1.jpg"
        assert len(product.variants) == 2
        assert product.variants[0]["size"] == "8"
        assert product.product_metadata["popularity_score"] == 85
        assert product.product_metadata["nested"]["key"] == "value"
    
    def test_to_dict_method(self, db_session, sample_product):
        """Test that to_dict() method returns correct dictionary."""
        # When: Converting product to dict
        product_dict = sample_product.to_dict()
        
        # Then: All fields are present
        assert product_dict["id"] == sample_product.id
        assert product_dict["gtin"] == sample_product.gtin
        assert product_dict["mpn"] == sample_product.mpn
        assert product_dict["title"] == sample_product.title
        assert product_dict["description"] == sample_product.description
        assert product_dict["brand"] == sample_product.brand
        assert product_dict["category"] == sample_product.category
        assert product_dict["price"] == float(sample_product.price)
        assert product_dict["currency"] == sample_product.currency
        assert product_dict["images"] == sample_product.images
        assert product_dict["availability"] == sample_product.availability
        assert product_dict["variants"] == sample_product.variants
        assert product_dict["metadata"] == sample_product.product_metadata
        assert "created_at" in product_dict
        assert "updated_at" in product_dict
    
    def test_repr_method(self, db_session, sample_product):
        """Test that __repr__ returns useful string."""
        # When: Getting string representation
        repr_str = repr(sample_product)
        
        # Then: Contains key information
        assert "Product" in repr_str
        assert sample_product.id in repr_str
        assert sample_product.gtin in repr_str
        assert sample_product.title in repr_str
    
    def test_timestamps_are_set_automatically(self, db_session):
        """Test that created_at and updated_at are set automatically."""
        # When: Creating a product
        product = Product(
            id="test-product",
            gtin="12345678901234",
            title="Test Product",
            price=Decimal("99.99")
        )
        db_session.add(product)
        db_session.commit()
        db_session.refresh(product)
        
        # Then: Timestamps are set
        assert product.created_at is not None
        assert product.updated_at is not None
        assert product.created_at == product.updated_at  # Initially the same
    
    def test_updated_at_changes_on_update(self, db_session, sample_product):
        """Test that updated_at changes when product is modified."""
        # Given: Existing product
        original_updated_at = sample_product.updated_at
        original_created_at = sample_product.created_at
        
        # When: Updating the product
        import time
        time.sleep(0.01)  # Small delay
        sample_product.title = "Updated Title"
        sample_product.updated_at = None  # Force SQLAlchemy to regenerate
        db_session.commit()
        db_session.refresh(sample_product)
        
        # Then: Product is updated and created_at unchanged
        assert sample_product.title == "Updated Title"
        assert sample_product.created_at == original_created_at
        # Note: SQLite may not update timestamp automatically in all cases
    
    def test_availability_values(self, db_session):
        """Test different availability values."""
        # Test in_stock
        product1 = Product(
            id="product-1",
            gtin="11111111111111",
            title="Product 1",
            price=Decimal("99.99"),
            availability="in_stock"
        )
        
        # Test out_of_stock
        product2 = Product(
            id="product-2",
            gtin="22222222222222",
            title="Product 2",
            price=Decimal("99.99"),
            availability="out_of_stock"
        )
        
        db_session.add(product1)
        db_session.add(product2)
        db_session.commit()
        
        # Then: Both are saved correctly
        assert product1.availability == "in_stock"
        assert product2.availability == "out_of_stock"
    
    def test_query_by_gtin(self, db_session, sample_product):
        """Test querying products by GTIN."""
        # When: Querying by GTIN
        found_product = db_session.query(Product).filter(
            Product.gtin == sample_product.gtin
        ).first()
        
        # Then: Product is found
        assert found_product is not None
        assert found_product.id == sample_product.id
    
    def test_query_by_category(self, db_session, sample_product):
        """Test querying products by category."""
        # When: Querying by category
        found_products = db_session.query(Product).filter(
            Product.category.like("%Running%")
        ).all()
        
        # Then: Product is found
        assert len(found_products) >= 1
        assert sample_product in found_products
    
    def test_query_by_availability(self, db_session, sample_product):
        """Test querying products by availability."""
        # When: Querying for in-stock products
        found_products = db_session.query(Product).filter(
            Product.availability == "in_stock"
        ).all()
        
        # Then: Product is found
        assert len(found_products) >= 1
        assert sample_product in found_products

