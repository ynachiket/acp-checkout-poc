"""
Tests for Product Service

Following TDD: Write tests FIRST, then implement service.

Test Coverage:
1. search_products() - full text search with filters
2. get_by_id() - retrieve by internal ID
3. get_by_gtin() - retrieve by GTIN
4. check_buyability() - validate product can be purchased
5. get_variants() - retrieve product variants
6. Error handling for all methods
"""

import pytest
from decimal import Decimal
from app.services.product_service import ProductService, ProductNotFoundError, InvalidGTINError
from app.models.product import Product


@pytest.mark.unit
@pytest.mark.services
class TestProductService:
    """Test suite for ProductService."""
    
    @pytest.fixture
    def product_service(self, db_session):
        """Create ProductService instance."""
        return ProductService(db_session)
    
    @pytest.fixture
    def multiple_products(self, db_session):
        """Create multiple products for search testing."""
        products = [
            Product(
                id="nike-air-max-90",
                gtin="00883419552502",
                title="Nike Air Max 90",
                description="Classic running shoe with visible Air cushioning",
                brand="Nike",
                category="Shoes > Running > Sneakers",
                price=Decimal("120.00"),
                availability="in_stock"
            ),
            Product(
                id="nike-air-max-270",
                gtin="00883419552503",
                title="Nike Air Max 270",
                description="Modern Air Max with 270 degrees of visibility",
                brand="Nike",
                category="Shoes > Lifestyle > Sneakers",
                price=Decimal("150.00"),
                availability="in_stock"
            ),
            Product(
                id="nike-pegasus-40",
                gtin="00883419552504",
                title="Nike Pegasus 40",
                description="Versatile running shoe for everyday training",
                brand="Nike",
                category="Shoes > Running > Road Running",
                price=Decimal("140.00"),
                availability="out_of_stock"
            ),
            Product(
                id="nike-dri-fit-shirt",
                gtin="00883419552505",
                title="Nike Dri-FIT Training Shirt",
                description="Moisture-wicking training shirt",
                brand="Nike",
                category="Apparel > Training > Shirts",
                price=Decimal("45.00"),
                availability="in_stock"
            ),
        ]
        for product in products:
            db_session.add(product)
        db_session.commit()
        return products
    
    # ============================================================================
    # search_products() Tests
    # ============================================================================
    
    def test_search_products_by_title(self, product_service, multiple_products):
        """Test searching products by title keyword."""
        # When: Searching for "Air Max"
        results = product_service.search_products(query="Air Max")
        
        # Then: Returns matching products
        assert len(results) == 2
        titles = [p.title for p in results]
        assert "Nike Air Max 90" in titles
        assert "Nike Air Max 270" in titles
    
    def test_search_products_case_insensitive(self, product_service, multiple_products):
        """Test that search is case insensitive."""
        # When: Searching with different cases
        results_lower = product_service.search_products(query="air max")
        results_upper = product_service.search_products(query="AIR MAX")
        results_mixed = product_service.search_products(query="Air Max")
        
        # Then: All return same results
        assert len(results_lower) == len(results_upper) == len(results_mixed)
    
    def test_search_products_by_description(self, product_service, multiple_products):
        """Test searching in product descriptions."""
        # When: Searching for description keyword
        results = product_service.search_products(query="cushioning")
        
        # Then: Returns products with matching description
        assert len(results) == 1
        assert results[0].title == "Nike Air Max 90"
    
    def test_search_products_with_category_filter(self, product_service, multiple_products):
        """Test filtering by category."""
        # When: Searching with category filter
        results = product_service.search_products(
            query="Nike",
            category="Shoes > Running"
        )
        
        # Then: Returns only running shoes
        assert len(results) == 2
        for product in results:
            assert "Running" in product.category
    
    def test_search_products_with_price_filter(self, product_service, multiple_products):
        """Test filtering by price range."""
        # When: Searching with price filter
        results = product_service.search_products(
            query="Nike",
            price_min=Decimal("100.00"),
            price_max=Decimal("130.00")
        )
        
        # Then: Returns products in price range
        assert len(results) == 1
        assert results[0].title == "Nike Air Max 90"
        assert results[0].price == Decimal("120.00")
    
    def test_search_products_with_availability_filter(self, product_service, multiple_products):
        """Test filtering by availability."""
        # When: Searching for in-stock products only
        results = product_service.search_products(
            query="Nike",
            availability="in_stock"
        )
        
        # Then: Returns only in-stock products
        assert len(results) == 3
        for product in results:
            assert product.availability == "in_stock"
    
    def test_search_products_empty_query_returns_all(self, product_service, multiple_products):
        """Test that empty query returns all products."""
        # When: Searching with empty query
        results = product_service.search_products(query="")
        
        # Then: Returns all products
        assert len(results) == 4
    
    def test_search_products_no_matches(self, product_service, multiple_products):
        """Test searching with no matching results."""
        # When: Searching for non-existent product
        results = product_service.search_products(query="Adidas")
        
        # Then: Returns empty list
        assert len(results) == 0
    
    def test_search_products_with_limit(self, product_service, multiple_products):
        """Test limiting search results."""
        # When: Searching with limit
        results = product_service.search_products(query="Nike", limit=2)
        
        # Then: Returns limited results
        assert len(results) == 2
    
    # ============================================================================
    # get_by_id() Tests
    # ============================================================================
    
    def test_get_by_id_success(self, product_service, sample_product):
        """Test retrieving product by ID."""
        # When: Getting product by ID
        product = product_service.get_by_id(sample_product.id)
        
        # Then: Returns correct product
        assert product is not None
        assert product.id == sample_product.id
        assert product.title == sample_product.title
    
    def test_get_by_id_not_found(self, product_service):
        """Test retrieving non-existent product by ID."""
        # When: Getting non-existent product
        # Then: Raises ProductNotFoundError
        with pytest.raises(ProductNotFoundError) as exc_info:
            product_service.get_by_id("non-existent-id")
        
        assert "not found" in str(exc_info.value).lower()
        assert "non-existent-id" in str(exc_info.value)
    
    def test_get_by_id_none_raises_error(self, product_service):
        """Test that None ID raises error."""
        # When: Getting product with None ID
        # Then: Raises ValueError
        with pytest.raises(ValueError):
            product_service.get_by_id(None)
    
    def test_get_by_id_empty_string_raises_error(self, product_service):
        """Test that empty string ID raises error."""
        # When: Getting product with empty ID
        # Then: Raises ValueError
        with pytest.raises(ValueError):
            product_service.get_by_id("")
    
    # ============================================================================
    # get_by_gtin() Tests
    # ============================================================================
    
    def test_get_by_gtin_success(self, product_service, sample_product):
        """Test retrieving product by GTIN."""
        # When: Getting product by GTIN
        product = product_service.get_by_gtin(sample_product.gtin)
        
        # Then: Returns correct product
        assert product is not None
        assert product.gtin == sample_product.gtin
        assert product.id == sample_product.id
    
    def test_get_by_gtin_not_found(self, product_service):
        """Test retrieving non-existent product by GTIN."""
        # When: Getting non-existent product
        # Then: Raises ProductNotFoundError
        with pytest.raises(ProductNotFoundError) as exc_info:
            product_service.get_by_gtin("99999999999999")
        
        assert "not found" in str(exc_info.value).lower()
    
    def test_get_by_gtin_invalid_format(self, product_service):
        """Test that invalid GTIN format raises error."""
        # When: Getting product with invalid GTIN
        # Then: Raises InvalidGTINError
        with pytest.raises(InvalidGTINError):
            product_service.get_by_gtin("invalid-gtin")
    
    def test_get_by_gtin_too_short(self, product_service):
        """Test that GTIN too short raises error."""
        # When: GTIN with less than 8 digits
        # Then: Raises InvalidGTINError
        with pytest.raises(InvalidGTINError):
            product_service.get_by_gtin("1234567")
    
    def test_get_by_gtin_too_long(self, product_service):
        """Test that GTIN too long raises error."""
        # When: GTIN with more than 14 digits
        # Then: Raises InvalidGTINError
        with pytest.raises(InvalidGTINError):
            product_service.get_by_gtin("123456789012345")
    
    # ============================================================================
    # check_buyability() Tests
    # ============================================================================
    
    def test_check_buyability_available_product(self, product_service, sample_product):
        """Test that in-stock product is buyable."""
        # Given: In-stock product
        sample_product.availability = "in_stock"
        
        # When: Checking buyability
        is_buyable, reason = product_service.check_buyability(sample_product.id)
        
        # Then: Product is buyable
        assert is_buyable is True
        assert reason is None
    
    def test_check_buyability_out_of_stock(self, product_service, sample_product):
        """Test that out-of-stock product is not buyable."""
        # Given: Out-of-stock product
        sample_product.availability = "out_of_stock"
        product_service.db.commit()
        
        # When: Checking buyability
        is_buyable, reason = product_service.check_buyability(sample_product.id)
        
        # Then: Product is not buyable
        assert is_buyable is False
        assert "out of stock" in reason.lower()
    
    def test_check_buyability_gift_card_not_allowed(self, product_service, db_session):
        """Test that gift cards are not buyable via ACP."""
        # Given: Gift card product
        gift_card = Product(
            id="nike-gift-card",
            gtin="12345678901234",
            title="Nike Gift Card",
            category="Gift Cards",
            price=Decimal("50.00"),
            availability="in_stock"
        )
        db_session.add(gift_card)
        db_session.commit()
        
        # When: Checking buyability
        is_buyable, reason = product_service.check_buyability(gift_card.id)
        
        # Then: Product is not buyable
        assert is_buyable is False
        assert "gift card" in reason.lower()
    
    def test_check_buyability_nike_by_you_not_allowed(self, product_service, db_session):
        """Test that Nike By You customizable products are not buyable via ACP."""
        # Given: Nike By You product
        custom_product = Product(
            id="nike-by-you-custom",
            gtin="12345678901235",
            title="Nike By You Custom Shoe",
            category="Shoes > Customizable",
            price=Decimal("180.00"),
            availability="in_stock",
            product_metadata={"customizable": True}
        )
        db_session.add(custom_product)
        db_session.commit()
        
        # When: Checking buyability
        is_buyable, reason = product_service.check_buyability(custom_product.id)
        
        # Then: Product is not buyable
        assert is_buyable is False
        assert "customizable" in reason.lower() or "nike by you" in reason.lower()
    
    def test_check_buyability_product_not_found(self, product_service):
        """Test buyability check for non-existent product."""
        # When: Checking buyability of non-existent product
        # Then: Raises ProductNotFoundError
        with pytest.raises(ProductNotFoundError):
            product_service.check_buyability("non-existent-id")
    
    # ============================================================================
    # get_variants() Tests
    # ============================================================================
    
    def test_get_variants_returns_all_variants(self, product_service, sample_product):
        """Test retrieving product variants."""
        # When: Getting variants
        variants = product_service.get_variants(sample_product.id)
        
        # Then: Returns all variants
        assert len(variants) == 3
        sizes = [v["size"] for v in variants]
        assert "8" in sizes
        assert "9" in sizes
        assert "10" in sizes
    
    def test_get_variants_no_variants(self, product_service, db_session):
        """Test product with no variants."""
        # Given: Product without variants
        product = Product(
            id="simple-product",
            gtin="12345678901236",
            title="Simple Product",
            price=Decimal("99.99"),
            variants=None
        )
        db_session.add(product)
        db_session.commit()
        
        # When: Getting variants
        variants = product_service.get_variants(product.id)
        
        # Then: Returns empty list
        assert len(variants) == 0
    
    def test_get_variants_product_not_found(self, product_service):
        """Test getting variants for non-existent product."""
        # When: Getting variants of non-existent product
        # Then: Raises ProductNotFoundError
        with pytest.raises(ProductNotFoundError):
            product_service.get_variants("non-existent-id")
    
    # ============================================================================
    # Edge Cases and Error Handling
    # ============================================================================
    
    def test_service_requires_db_session(self):
        """Test that service requires database session."""
        # When: Creating service without db session
        # Then: Raises TypeError
        with pytest.raises(TypeError):
            ProductService()
    
    def test_search_with_all_filters(self, product_service, multiple_products):
        """Test search with all filters combined."""
        # When: Searching with all filters
        results = product_service.search_products(
            query="Nike",
            category="Shoes",
            price_min=Decimal("100.00"),
            price_max=Decimal("150.00"),
            availability="in_stock",
            limit=5
        )
        
        # Then: Returns filtered results
        assert len(results) >= 1
        for product in results:
            assert "Nike" in product.title or "Nike" in product.description
            assert "Shoes" in product.category
            assert Decimal("100.00") <= product.price <= Decimal("150.00")
            assert product.availability == "in_stock"

