"""
Pytest Configuration and Fixtures

This file contains shared fixtures and configuration for all tests.
"""

import os
from typing import AsyncGenerator, Generator
from decimal import Decimal

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.pool import StaticPool

# Set testing environment
os.environ["TESTING"] = "true"
os.environ["DATABASE_URL"] = "sqlite:///:memory:"

from app.database import Base, get_db
from app.main import app
from app.models.product import Product
from app.models.checkout_session import CheckoutSession
from app.models.order import Order


# ============================================================================
# Database Fixtures
# ============================================================================

@pytest.fixture(scope="function")
def db_engine():
    """Create a test database engine."""
    engine = create_engine(
        "sqlite:///:memory:",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    Base.metadata.create_all(bind=engine)
    yield engine
    Base.metadata.drop_all(bind=engine)
    engine.dispose()


@pytest.fixture(scope="function")
def db_session(db_engine) -> Generator[Session, None, None]:
    """Create a test database session."""
    TestingSessionLocal = sessionmaker(
        autocommit=False,
        autoflush=False,
        bind=db_engine
    )
    session = TestingSessionLocal()
    try:
        yield session
    finally:
        session.rollback()
        session.close()


@pytest.fixture(scope="function")
def test_client(db_session) -> Generator[TestClient, None, None]:
    """Create a test client with overridden database dependency."""
    def override_get_db():
        try:
            yield db_session
        finally:
            pass

    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as client:
        yield client
    app.dependency_overrides.clear()


# ============================================================================
# Sample Data Fixtures
# ============================================================================

@pytest.fixture
def sample_product_data():
    """Sample product data for testing."""
    return {
        "id": "nike-air-max-90-white",
        "gtin": "00883419552502",
        "mpn": "CW2288-111",
        "title": "Nike Air Max 90",
        "description": "Nothing as fly, nothing as comfortable, nothing as proven. The Nike Air Max 90 stays true to its OG running roots.",
        "brand": "Nike",
        "category": "Shoes > Running > Sneakers",
        "price": Decimal("120.00"),
        "currency": "USD",
        "images": [
            "https://static.nike.com/a/images/c_limit,w_592,f_auto/t_product_v1/abc123.jpg",
            "https://static.nike.com/a/images/c_limit,w_592,f_auto/t_product_v1/abc124.jpg"
        ],
        "availability": "in_stock",
            "variants": [
                {"size": "8", "size_system": "US", "gtin": "00883419552502"},
                {"size": "9", "size_system": "US", "gtin": "00883419552503"},
                {"size": "10", "size_system": "US", "gtin": "00883419552504"}
            ],
            "product_metadata": {
                "gender": "unisex",
                "color": "White",
                "popularity_score": 85
            }
    }


@pytest.fixture
def sample_product(db_session, sample_product_data):
    """Create a sample product in the database."""
    product = Product(**sample_product_data)
    db_session.add(product)
    db_session.commit()
    db_session.refresh(product)
    return product


@pytest.fixture
def sample_checkout_session_data(sample_product):
    """Sample checkout session data."""
    return {
        "currency": "USD",
        "line_items": [
            {
                "gtin": sample_product.gtin,
                "quantity": 1,
                "unit_price": float(sample_product.price),
                "total": float(sample_product.price)
            }
        ],
        "fulfillment_address": {
            "name": "John Doe",
            "address_line_1": "123 Main St",
            "address_line_2": "Apt 4B",
            "city": "New York",
            "state": "NY",
            "postal_code": "10001",
            "country": "US"
        },
        "buyer_info": {
            "first_name": "John",
            "last_name": "Doe",
            "email": "john.doe@example.com",
            "phone": "+12125551234"
        }
    }


@pytest.fixture
def sample_shipping_address():
    """Sample shipping address."""
    return {
        "name": "John Doe",
        "address_line_1": "123 Main St",
        "address_line_2": "Apt 4B",
        "city": "New York",
        "state": "NY",
        "postal_code": "10001",
        "country": "US"
    }


# ============================================================================
# Mock Service Fixtures
# ============================================================================

@pytest.fixture
def mock_stripe_payment_method():
    """Mock Stripe payment method response."""
    return {
        "id": "pm_1234567890abcdef",
        "object": "payment_method",
        "type": "card",
        "card": {
            "brand": "visa",
            "last4": "4242",
            "exp_month": 12,
            "exp_year": 2025
        }
    }


@pytest.fixture
def mock_stripe_payment_intent():
    """Mock Stripe payment intent response."""
    return {
        "id": "pi_1234567890abcdef",
        "object": "payment_intent",
        "amount": 13500,  # $135.00
        "currency": "usd",
        "status": "succeeded",
        "payment_method": "pm_1234567890abcdef"
    }


# ============================================================================
# Helper Fixtures
# ============================================================================

@pytest.fixture
def stripe_test_cards():
    """Stripe test card numbers."""
    return {
        "success": "4242424242424242",
        "decline": "4000000000000002",
        "requires_3ds": "4000002500003155",
        "insufficient_funds": "4000000000009995"
    }


@pytest.fixture
def auth_headers():
    """Authentication headers for API requests."""
    return {
        "X-API-Key": os.getenv("API_KEY", "test-api-key")
    }


# ============================================================================
# Pytest Hooks
# ============================================================================

def pytest_configure(config):
    """Configure pytest with custom markers."""
    config.addinivalue_line(
        "markers", "unit: Unit tests (fast, isolated)"
    )
    config.addinivalue_line(
        "markers", "integration: Integration tests (slower)"
    )
    config.addinivalue_line(
        "markers", "slow: Slow tests (> 1 second)"
    )


def pytest_collection_modifyitems(config, items):
    """Modify test items during collection."""
    # Add 'unit' marker to tests without markers
    for item in items:
        if not any(item.iter_markers()):
            item.add_marker(pytest.mark.unit)

