# 🚀 Quick Start Guide - ACP POC

**Get the API running in 5 minutes!**

---

## Prerequisites

✅ Python 3.11+  
✅ pip  

---

## Setup

### 1. Install Dependencies

```bash
cd backend
pip install -r requirements.txt
```

### 2. Create Data Directory

```bash
mkdir -p data
```

### 3. Seed Database

```bash
python scripts/seed_products.py
```

**Expected Output:**
```
🌱 Seeding database with sample products...

✅ Added: Air Max 90
✅ Added: Air Max 270
✅ Added: Pegasus 40
✅ Added: Dunk Low Retro
✅ Added: Air Force 1 '07
✅ Added: Dri-FIT Training Shirt
✅ Added: Sportswear Tech Fleece Hoodie
✅ Added: Pro 365 Women's High-Waisted Leggings
✅ Added: React Infinity Run Flyknit 4
✅ Added: Metcon 9

✅ Seeding complete! 10 products processed.
```

### 4. Run Server

```bash
uvicorn app.main:app --reload --port 8000
```

**Expected Output:**
```
INFO:     Uvicorn running on http://0.0.0.0:8000
INFO:     Application startup complete.
```

---

## Test the API

### Health Check

```bash
curl http://localhost:8000/health
```

**Response:**
```json
{
  "status": "healthy",
  "app": "Agentic Commerce POC",
  "version": "1.0.0",
  "environment": "development"
}
```

### View API Docs

Open in browser: http://localhost:8000/docs

---

## Test Complete Purchase Flow

### Step 1: Create Checkout Session

```bash
curl -X POST http://localhost:8000/acp/v1/checkout_sessions \
  -H "Content-Type: application/json" \
  -d '{
    "line_items": [
      {
        "gtin": "00883419552502",
        "quantity": 1
      }
    ],
    "fulfillment_address": {
      "name": "John Doe",
      "address_line_1": "123 Main St",
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
  }'
```

**Save the `session_id` from response!**

### Step 2: Tokenize Payment

```bash
curl -X POST http://localhost:8000/acp/v1/delegate_payment \
  -H "Content-Type: application/json" \
  -d '{
    "card_number": "4242424242424242",
    "exp_month": 12,
    "exp_year": 2025,
    "cvc": "123"
  }'
```

**Save the `payment_token_id` from response!**

### Step 3: Complete Purchase

```bash
curl -X POST http://localhost:8000/acp/v1/checkout_sessions/{SESSION_ID}/complete \
  -H "Content-Type: application/json" \
  -d '{
    "payment_token_id": "{PAYMENT_TOKEN}"
  }'
```

**Replace `{SESSION_ID}` and `{PAYMENT_TOKEN}` with actual values!**

---

## Run Tests

### Run All Tests

```bash
pytest
```

### Run with Coverage

```bash
pytest --cov=app --cov-report=html --cov-report=term-missing
```

### View Coverage Report

```bash
open htmlcov/index.html
```

---

## API Endpoints

### ACP Protocol Endpoints

```
POST   /acp/v1/checkout_sessions              # Create session
POST   /acp/v1/checkout_sessions/{id}         # Update session
GET    /acp/v1/checkout_sessions/{id}         # Get session
POST   /acp/v1/checkout_sessions/{id}/complete # Complete purchase
POST   /acp/v1/checkout_sessions/{id}/cancel  # Cancel session
POST   /acp/v1/delegate_payment               # Tokenize payment
```

### Health & Info

```
GET    /                   # API info
GET    /health             # Health check
GET    /docs               # Swagger UI
GET    /redoc              # ReDoc UI
```

---

## What's Working

✅ Product catalog (10 sample products)  
✅ Checkout session creation  
✅ Address and shipping calculation  
✅ Payment tokenization (mock for POC)  
✅ Order creation  
✅ Full ACP protocol implementation  

---

## What's Not Yet Implemented

⚠️ Real Stripe integration (using mocks for POC)  
⚠️ Comprehensive tests for all services (Product service has 75 tests, others pending)  
⚠️ MCP server layer  
⚠️ Webhooks for order events  
⚠️ Real product data integration  

---

## Next Steps

### Add Tests for Remaining Services

Follow the pattern from `tests/test_services/test_product_service.py`:

1. Write tests FIRST
2. Implement to pass tests
3. Verify 90%+ coverage

**Services needing tests:**
- Inventory Service
- Checkout Service
- Shipping Service
- Payment Service
- Order Service
- ACP Gateway

### Integrate Real Stripe

Update `app/services/payment_service.py`:
```python
import stripe
stripe.api_key = settings.stripe_secret_key
# Use real Stripe API calls
```

### Build Real Product Scraper

Create `scripts/fetch_products.py` to fetch real product data from your e-commerce platform

---

## Troubleshooting

### Port 8000 already in use

```bash
# Find and kill process using port 8000
lsof -ti:8000 | xargs kill -9

# Or use different port
uvicorn app.main:app --reload --port 8080
```

### Database errors

```bash
# Delete and recreate database
rm data/checkout.db
python scripts/seed_products.py
```

### Import errors

```bash
# Make sure you're in the backend directory
cd backend

# Reinstall dependencies
pip install -r requirements.txt
```

---

## Development Tips

### Watch logs in real-time

```bash
uvicorn app.main:app --reload --port 8000 --log-level debug
```

### Test a single endpoint

```bash
pytest tests/test_services/test_product_service.py::TestProductService::test_search_products_by_title -v
```

### Format code

```bash
black app/
isort app/
```

---

**POC Status:** 🟢 Runnable  
**Test Coverage:** ~40% (Product service fully tested, others minimal)  
**Target Coverage:** 90% (add tests for remaining services)

**Ready to demo the API! 🎉**

