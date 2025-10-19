# Testing Guide - Path to 90% Coverage

**Current Coverage:** 56% (47 tests)  
**Target Coverage:** 90% (165 tests)  
**Gap:** ~70-80 tests to add

---

## 🎯 Current State

### ✅ What's Fully Tested (Product Service)

```
Product Model:     100% coverage (22 tests)
Product Service:    97% coverage (44 tests)
Product Integration: 9 tests

Total: 75 tests, Pattern established ✅
```

### ⚠️ What Needs Tests

```
Checkout Service:   17% coverage → Need ~30 tests
Payment Service:    57% coverage → Need ~20 tests
Shipping Service:   44% coverage → Need ~15 tests
Order Service:      35% coverage → Need ~15 tests
ACP Gateway:        22% coverage → Need ~25 tests

Total: ~105 tests needed
```

---

## 📚 Testing Pattern (Follow This)

### Template: tests/test_services/test_product_service.py

**This file shows the complete pattern:**

```python
import pytest
from app.services.your_service import YourService

@pytest.mark.unit
@pytest.mark.services
class TestYourService:
    """Test suite for YourService."""
    
    @pytest.fixture
    def service(self, db_session):
        """Create service instance."""
        return YourService(db_session)
    
    # Test each method with:
    # - Success case
    # - Error cases
    # - Edge cases
    # - Validation
    
    def test_method_name_success(self, service):
        """Test happy path."""
        # GIVEN: Setup
        # WHEN: Call method
        result = service.method_name(args)
        # THEN: Assert expected result
        assert result == expected
    
    def test_method_name_error_case(self, service):
        """Test error handling."""
        with pytest.raises(ExpectedError):
            service.method_name(invalid_args)
```

---

## 🔨 Step-by-Step: Add Tests for Checkout Service

### 1. Create Test File

```bash
touch tests/test_services/test_checkout_service.py
```

### 2. Write Tests (Copy Pattern)

```python
"""
Tests for Checkout Service

Test coverage:
1. create_session() - with/without address, multiple items, validation
2. get_session() - success, not found, expired
3. update_session() - address, shipping option, calculations
4. Status transitions
5. Price calculations (tax, shipping, totals)
"""

import pytest
from decimal import Decimal
from app.services.checkout_service import CheckoutService
from app.models.product import Product

@pytest.mark.unit
@pytest.mark.services
class TestCheckoutService:
    
    @pytest.fixture
    def checkout_service(self, db_session):
        return CheckoutService(db_session)
    
    @pytest.fixture
    def sample_product(self, db_session):
        product = Product(
            id="test-product",
            gtin="12345678901234",
            title="Test Product",
            price=Decimal("100.00"),
            availability="in_stock"
        )
        db_session.add(product)
        db_session.commit()
        return product
    
    # Test 1: Create session without address
    def test_create_session_without_address(self, checkout_service, sample_product):
        """Test creating session without shipping address."""
        # GIVEN: Product and items
        items = [{"product_id": sample_product.id, "quantity": 1}]
        
        # WHEN: Creating session without address
        session = checkout_service.create_session(items=items)
        
        # THEN: Session created with not_ready_for_payment status
        assert session.id is not None
        assert session.status == "not_ready_for_payment"
        assert len(session.line_items) == 1
        assert session.fulfillment_address is None
        assert session.fulfillment_options is None
    
    # Test 2: Create session with address
    def test_create_session_with_address(self, checkout_service, sample_product):
        """Test creating session with shipping address."""
        # GIVEN: Product, items, and address
        items = [{"product_id": sample_product.id, "quantity": 1}]
        address = {
            "name": "John Doe",
            "address_line_1": "123 Main St",
            "city": "New York",
            "state": "NY",
            "postal_code": "10001",
            "country": "US"
        }
        
        # WHEN: Creating session with address
        session = checkout_service.create_session(items=items, address=address)
        
        # THEN: Session is ready for payment
        assert session.status == "ready_for_payment"
        assert session.fulfillment_address == address
        assert session.fulfillment_options is not None
        assert len(session.fulfillment_options) == 3  # Standard, Express, Overnight
        assert session.selected_fulfillment_option_id == "standard"
    
    # Test 3: Calculate totals correctly
    def test_calculate_totals_correctly(self, checkout_service, sample_product):
        """Test that totals are calculated correctly."""
        # GIVEN: Product at $100, quantity 2, with address
        items = [{"product_id": sample_product.id, "quantity": 2}]
        address = {
            "address_line_1": "123 Main St",
            "city": "New York",
            "state": "NY",
            "postal_code": "10001",
            "country": "US"
        }
        
        # WHEN: Creating session
        session = checkout_service.create_session(items=items, address=address)
        
        # THEN: Totals are correct
        # Items: $100 * 2 = $200
        # Shipping: $5 (standard)
        # Tax: ($200) * 8% = $16
        # Total: $200 + $5 + $16 = $221
        assert session.totals["items_total"]["value"] == "200.00"
        assert session.totals["fulfillment"]["value"] == "5.00"
        assert session.totals["taxes"]["value"] == "16.00"
        assert session.totals["total"]["value"] == "221.00"
    
    # ... Add 25+ more tests
    
    # Test 4: Out of stock product
    def test_create_session_out_of_stock_product(self, checkout_service, db_session):
        """Test that out of stock products raise error."""
        # GIVEN: Out of stock product
        product = Product(
            id="out-of-stock",
            gtin="99999999999999",
            title="Out of Stock",
            price=Decimal("100.00"),
            availability="out_of_stock"
        )
        db_session.add(product)
        db_session.commit()
        
        # WHEN: Creating session
        # THEN: Raises ValueError
        with pytest.raises(ValueError) as exc:
            checkout_service.create_session(
                items=[{"product_id": product.id, "quantity": 1}]
            )
        
        assert "not available" in str(exc.value).lower()
```

### 3. Run Tests

```bash
pytest tests/test_services/test_checkout_service.py -v
```

### 4. Check Coverage

```bash
pytest --cov=app/services/checkout_service --cov-report=term-missing
```

**Target:** 90%+ coverage

---

## 📋 Test Checklist

Use this to track progress to 90%:

### Checkout Service (~30 tests)
- [ ] test_create_session_without_address
- [ ] test_create_session_with_address
- [ ] test_create_session_multiple_items
- [ ] test_create_session_invalid_product
- [ ] test_create_session_out_of_stock
- [ ] test_get_session_success
- [ ] test_get_session_not_found
- [ ] test_get_session_expired
- [ ] test_update_session_add_address
- [ ] test_update_session_change_shipping
- [ ] test_calculate_totals_correctly
- [ ] test_calculate_tax_correctly
- [ ] test_status_transitions
- [ ] ... (~17 more tests)

### Payment Service (~20 tests)
- [ ] test_tokenize_payment_success
- [ ] test_tokenize_payment_invalid_card
- [ ] test_create_payment_intent_success
- [ ] test_create_payment_intent_declined
- [ ] test_capture_payment_success
- [ ] ... (~15 more tests)

### Shipping Service (~15 tests)
- [ ] test_calculate_options_returns_three
- [ ] test_validate_address_success
- [ ] test_validate_address_missing_field
- [ ] test_validate_address_non_us
- [ ] ... (~11 more tests)

### Order Service (~15 tests)
- [ ] test_create_order_from_session
- [ ] test_create_order_event
- [ ] test_get_order_success
- [ ] test_get_order_not_found
- [ ] test_update_order_status
- [ ] ... (~10 more tests)

### ACP Gateway (~25 tests)
- [ ] test_create_checkout_endpoint
- [ ] test_create_checkout_invalid_gtin
- [ ] test_update_checkout_endpoint
- [ ] test_get_checkout_endpoint
- [ ] test_complete_checkout_endpoint
- [ ] test_cancel_checkout_endpoint
- [ ] test_delegate_payment_endpoint
- [ ] test_error_code_mapping
- [ ] ... (~17 more tests)

**Total:** ~105 tests to add  
**Time:** 8-10 hours  
**Result:** 90%+ coverage

---

## 🎓 TDD Tips

### Good Test Structure

```python
def test_specific_behavior():
    """Clear description of what's being tested."""
    # GIVEN: Setup and preconditions
    product = create_product(...)
    
    # WHEN: Action being tested
    result = service.method(product)
    
    # THEN: Assertions
    assert result.status == "expected"
    assert result.total == 100.00
```

### Test Names

✅ **GOOD:**
- `test_create_session_with_address_calculates_shipping`
- `test_get_session_expired_raises_error`
- `test_calculate_totals_includes_tax`

❌ **BAD:**
- `test_session`
- `test_works`
- `test_1`

### Coverage Targets

```
Critical Services:    95%+ (Checkout, Payment, Order)
Supporting Services:  85%+ (Shipping, Inventory)
Models:              95%+
Gateway:             85%+
```

---

## 🚀 Quick Commands

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=app --cov-report=html

# Run specific file
pytest tests/test_services/test_checkout_service.py -v

# Run by marker
pytest -m unit
pytest -m integration

# View coverage
open htmlcov/index.html

# Watch coverage increase
pytest --cov=app --cov-report=term | grep TOTAL
```

---

## 📊 Coverage Progress Tracker

Track your progress to 90%:

```
Day 1 (Today):     56% ███████████░░░░░░░░░
+ Checkout tests:  68% ██████████████░░░░░░
+ Payment tests:   76% ███████████████░░░░░
+ Shipping tests:  82% ████████████████░░░░
+ Order tests:     87% █████████████████░░░
+ Gateway tests:   91% ██████████████████░░
```

**Target:** 90%+ ████████████████████

---

## 🎯 When to Stop Adding Tests

**Stop when:**
- ✅ Overall coverage ≥ 90%
- ✅ All critical paths tested
- ✅ All error cases covered
- ✅ Edge cases handled

**Don't need 100%:**
- Some __repr__ methods
- Some logging statements
- Some defensive code that's hard to trigger

**90% is excellent for production!**

---

**Current Status:** 56% → Need 34% more → ~80 tests  
**Time Required:** 8-10 hours  
**Priority:** Medium (POC works, tests for production confidence)

---

**Ready to add tests? Follow the Product Service pattern! 🚀**

