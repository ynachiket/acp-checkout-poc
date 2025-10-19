"""
Integration Test: Product Service Vertical Slice

This test demonstrates the COMPLETE vertical slice:
1. Database → Model → Service → Integration

Tests the full flow without mocking to ensure all layers work together.
"""

import pytest
from decimal import Decimal
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.database import Base
from app.models.product import Product
from app.services.product_service import ProductService, ProductNotFoundError


@pytest.mark.integration
class TestProductServiceIntegration:
    """Integration tests for Product Service."""
    
    @pytest.fixture(scope="class")
    def integration_db(self):
        """Create a fresh database for integration testing."""
        engine = create_engine(
            "sqlite:///:memory:",
            connect_args={"check_same_thread": False},
            poolclass=StaticPool,
        )
        Base.metadata.create_all(bind=engine)
        
        SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
        return SessionLocal
    
    @pytest.fixture
    def integration_session(self, integration_db):
        """Create a session for each test."""
        session = integration_db()
        yield session
        session.rollback()
        session.close()
    
    @pytest.fixture
    def product_service(self, integration_session):
        """Create ProductService with integration session."""
        return ProductService(integration_session)
    
    @pytest.fixture
    def seed_products(self, integration_session):
        """Seed database with test products."""
        products = [
            Product(
                id="nike-air-max-90-white",
                gtin="00883419552502",
                mpn="CW2288-111",
                title="Nike Air Max 90",
                description="Nothing as fly, nothing as comfortable. The Nike Air Max 90 stays true to its OG running roots.",
                brand="Nike",
                category="Shoes > Running > Sneakers",
                price=Decimal("120.00"),
                currency="USD",
                images=[
                    "https://static.nike.com/a/images/t_PDP_1728_v1/f_auto,q_auto:eco/abc123.jpg"
                ],
                availability="in_stock",
                variants=[
                    {"size": "8", "size_system": "US", "gtin": "00883419552502"},
                    {"size": "9", "size_system": "US", "gtin": "00883419552503"},
                    {"size": "10", "size_system": "US", "gtin": "00883419552504"}
                ],
                product_metadata={
                    "gender": "unisex",
                    "color": "White",
                    "popularity_score": 85
                }
            ),
            Product(
                id="nike-air-max-270-black",
                gtin="00883419552510",
                mpn="AH8050-002",
                title="Nike Air Max 270",
                description="The Nike Air Max 270 features Nike's biggest heel Air unit yet for cushioning.",
                brand="Nike",
                category="Shoes > Lifestyle > Sneakers",
                price=Decimal("150.00"),
                currency="USD",
                availability="in_stock"
            ),
            Product(
                id="nike-pegasus-40",
                gtin="00883419552520",
                title="Nike Pegasus 40",
                description="Responsive cushioning and support for your daily run.",
                brand="Nike",
                category="Shoes > Running > Road Running",
                price=Decimal("140.00"),
                availability="out_of_stock"
            ),
        ]
        
        for product in products:
            integration_session.add(product)
        integration_session.commit()
        
        return products
    
    def test_complete_product_search_flow(self, product_service, seed_products):
        """
        Integration test: Complete product search flow.
        
        Tests: Database → Model → Service
        """
        # GIVEN: Products in database
        # WHEN: Searching for products
        results = product_service.search_products(query="Air Max")
        
        # THEN: Returns correct products from database
        assert len(results) == 2
        titles = [p.title for p in results]
        assert "Nike Air Max 90" in titles
        assert "Nike Air Max 270" in titles
        
        # AND: Products have all expected fields
        for product in results:
            assert product.id is not None
            assert product.gtin is not None
            assert product.title is not None
            assert product.price > 0
            assert product.availability is not None
    
    def test_complete_product_retrieval_by_id(self, product_service, seed_products):
        """
        Integration test: Retrieve product by ID.
        
        Tests: Database → Model → Service
        """
        # GIVEN: Known product ID
        product_id = "nike-air-max-90-white"
        
        # WHEN: Getting product by ID
        product = product_service.get_by_id(product_id)
        
        # THEN: Returns complete product with all data
        assert product.id == product_id
        assert product.gtin == "00883419552502"
        assert product.mpn == "CW2288-111"
        assert product.title == "Nike Air Max 90"
        assert product.price == Decimal("120.00")
        assert product.currency == "USD"
        assert product.availability == "in_stock"
        assert len(product.images) == 1
        assert len(product.variants) == 3
        assert product.product_metadata["popularity_score"] == 85
    
    def test_complete_product_retrieval_by_gtin(self, product_service, seed_products):
        """
        Integration test: Retrieve product by GTIN.
        
        Tests: Database → Model → Service with GTIN lookup
        """
        # GIVEN: Known GTIN
        gtin = "00883419552502"
        
        # WHEN: Getting product by GTIN
        product = product_service.get_by_gtin(gtin)
        
        # THEN: Returns correct product
        assert product.gtin == gtin
        assert product.id == "nike-air-max-90-white"
        assert product.title == "Nike Air Max 90"
    
    def test_complete_buyability_check_flow(self, product_service, seed_products):
        """
        Integration test: Check product buyability.
        
        Tests: Database → Model → Service → Business Logic
        """
        # GIVEN: In-stock product
        product_id = "nike-air-max-90-white"
        
        # WHEN: Checking buyability
        is_buyable, reason = product_service.check_buyability(product_id)
        
        # THEN: Product is buyable
        assert is_buyable is True
        assert reason is None
        
        # GIVEN: Out-of-stock product
        out_of_stock_id = "nike-pegasus-40"
        
        # WHEN: Checking buyability
        is_buyable, reason = product_service.check_buyability(out_of_stock_id)
        
        # THEN: Product is not buyable with reason
        assert is_buyable is False
        assert "out of stock" in reason.lower()
    
    def test_complete_search_with_filters_flow(self, product_service, seed_products):
        """
        Integration test: Search with multiple filters.
        
        Tests: Complex database queries through service layer
        """
        # WHEN: Searching with multiple filters
        results = product_service.search_products(
            query="Nike",
            category="Running",
            price_min=Decimal("100.00"),
            price_max=Decimal("130.00"),
            availability="in_stock"
        )
        
        # THEN: Returns filtered results
        assert len(results) == 1
        product = results[0]
        assert product.title == "Nike Air Max 90"
        assert "Running" in product.category
        assert Decimal("100.00") <= product.price <= Decimal("130.00")
        assert product.availability == "in_stock"
    
    def test_complete_variants_retrieval_flow(self, product_service, seed_products):
        """
        Integration test: Retrieve product variants.
        
        Tests: JSON field handling through all layers
        """
        # GIVEN: Product with variants
        product_id = "nike-air-max-90-white"
        
        # WHEN: Getting variants
        variants = product_service.get_variants(product_id)
        
        # THEN: Returns all variants from database
        assert len(variants) == 3
        sizes = [v["size"] for v in variants]
        assert "8" in sizes
        assert "9" in sizes
        assert "10" in sizes
        
        # AND: Variants have complete data
        for variant in variants:
            assert "size" in variant
            assert "size_system" in variant
            assert "gtin" in variant
    
    def test_error_handling_across_layers(self, product_service):
        """
        Integration test: Error handling through all layers.
        
        Tests: Exception propagation from database through service
        """
        # WHEN: Getting non-existent product
        # THEN: Raises ProductNotFoundError
        with pytest.raises(ProductNotFoundError) as exc_info:
            product_service.get_by_id("non-existent-product")
        
        assert "not found" in str(exc_info.value).lower()
        assert "non-existent-product" in str(exc_info.value)
    
    def test_database_constraints_enforced(self, integration_session):
        """
        Integration test: Database constraints are enforced.
        
        Tests: Database layer integrity constraints
        """
        from sqlalchemy.exc import IntegrityError
        
        # GIVEN: Product with specific GTIN
        product1 = Product(
            id="product-1",
            gtin="12345678901234",
            title="Product 1",
            price=Decimal("99.99")
        )
        integration_session.add(product1)
        integration_session.commit()
        
        # WHEN: Creating another product with same GTIN
        product2 = Product(
            id="product-2",
            gtin="12345678901234",  # Duplicate GTIN
            title="Product 2",
            price=Decimal("99.99")
        )
        integration_session.add(product2)
        
        # THEN: Database constraint violation
        with pytest.raises(IntegrityError):
            integration_session.commit()

