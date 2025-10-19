# 🎬 Nike ACP POC - Demo Guide

**Complete demonstration of the working purchase flow**

---

## 🚀 Quick Demo

### Option 1: Python Test Script (Recommended)

**Best for:** Visual, step-by-step demonstration with colored output

```bash
cd backend

# Make sure server is running in another terminal
# uvicorn app.main:app --reload

# Run the test script
python scripts/test_purchase_flow.py
```

**Output:**
```
======================================================================
        NIKE AGENTIC COMMERCE POC - PURCHASE FLOW TEST
======================================================================

Step 0: Health Check
✅ API is healthy: healthy
ℹ️  App: Nike Agentic Commerce POC
ℹ️  Version: 1.0.0

Step 1: Create Checkout Session
ℹ️  Creating checkout session with Nike Air Max 90...
✅ Session created: cs_a1b2c3d4e5f6g7h8
ℹ️  Status: ready_for_payment
ℹ️  Total: $135.60

📦 Items in cart:
   - Nike Air Max 90 (qty: 1) - $120.00

🚚 Shipping options:
   [✓] Standard Shipping - $5.00 (5-7 business days)
   [ ] Express Shipping - $15.00 (2-3 business days)
   [ ] Overnight Shipping - $25.00 (1 business day)

💰 Price breakdown:
   Items:    $120.00
   Shipping: $5.00
   Tax:      $10.60
   ─────────────────────
   Total:    $135.60

...

🎉 ALL TESTS PASSED! The purchase flow is working correctly.
```

### Option 2: Shell Script Demo

**Best for:** Quick command-line demo using curl

```bash
cd backend

# Run the demo script
./scripts/demo_api.sh
```

### Option 3: Manual curl Commands

**Best for:** Understanding each API call

See detailed commands below ↓

---

## 📝 Manual API Testing

### Prerequisites

```bash
# Terminal 1: Start server
cd backend
uvicorn app.main:app --reload --port 8000

# Terminal 2: Run tests
```

### Step 0: Health Check

```bash
curl http://localhost:8000/health | jq
```

**Expected Response:**
```json
{
  "status": "healthy",
  "app": "Nike Agentic Commerce POC",
  "version": "1.0.0"
}
```

---

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
  }' | jq
```

**Save the `session_id` from the response!**

**Expected Response:**
```json
{
  "id": "cs_a1b2c3d4e5f6g7h8",
  "status": "ready_for_payment",
  "currency": "USD",
  "line_items": [...],
  "totals": {
    "items_total": {"value": "120.00", "currency": "USD"},
    "fulfillment": {"value": "5.00", "currency": "USD"},
    "taxes": {"value": "10.00", "currency": "USD"},
    "total": {"value": "135.00", "currency": "USD"}
  }
}
```

---

### Step 2: Retrieve Session (Optional)

```bash
curl http://localhost:8000/acp/v1/checkout_sessions/{SESSION_ID} | jq
```

Replace `{SESSION_ID}` with actual ID from Step 1.

---

### Step 3: Update Shipping (Optional)

```bash
curl -X POST http://localhost:8000/acp/v1/checkout_sessions/{SESSION_ID} \
  -H "Content-Type: application/json" \
  -d '{
    "selected_fulfillment_option_id": "express"
  }' | jq
```

**Note:** Total will increase by $10 (Express shipping)

---

### Step 4: Tokenize Payment

```bash
curl -X POST http://localhost:8000/acp/v1/delegate_payment \
  -H "Content-Type: application/json" \
  -d '{
    "card_number": "4242424242424242",
    "exp_month": 12,
    "exp_year": 2025,
    "cvc": "123"
  }' | jq
```

**Save the `payment_token_id` from the response!**

**Expected Response:**
```json
{
  "payment_token_id": "pm_x9y8z7w6v5u4t3s2"
}
```

---

### Step 5: Complete Purchase

```bash
curl -X POST http://localhost:8000/acp/v1/checkout_sessions/{SESSION_ID}/complete \
  -H "Content-Type: application/json" \
  -d '{
    "payment_token_id": "{PAYMENT_TOKEN}"
  }' | jq
```

Replace `{SESSION_ID}` and `{PAYMENT_TOKEN}` with actual values.

**Expected Response:**
```json
{
  "id": "cs_a1b2c3d4e5f6g7h8",
  "status": "completed",
  "order": {
    "id": "order_123abc456def",
    "checkout_session_id": "cs_a1b2c3d4e5f6g7h8",
    "permalink": "https://nike.com/orders/order_123abc456def",
    "created_at": "2025-10-19T10:35:00Z"
  },
  "messages": [
    {
      "type": "success",
      "text": "Your order has been confirmed! You'll receive a confirmation email at john.doe@example.com"
    }
  ]
}
```

---

## 🔍 Verify Database

```bash
# Check products
sqlite3 data/checkout.db "SELECT id, title, price FROM products LIMIT 5;"

# Check sessions
sqlite3 data/checkout.db "SELECT id, status, created_at FROM checkout_sessions ORDER BY created_at DESC LIMIT 5;"

# Check orders
sqlite3 data/checkout.db "SELECT id, status, created_at FROM orders ORDER BY created_at DESC LIMIT 5;"
```

---

## 📊 What's Being Tested

### ✅ Complete Purchase Flow
1. **Product Lookup** - GTIN → Product Service
2. **Session Creation** - Checkout Service with items + address
3. **Shipping Calculation** - Shipping Service calculates 3 options
4. **Tax Calculation** - Checkout Service applies 8% tax
5. **Payment Tokenization** - Payment Service (mock Stripe)
6. **Payment Processing** - Payment Service processes payment
7. **Order Creation** - Order Service creates order record
8. **Event Logging** - OrderEvent created

### ✅ Services Tested
- Product Service (search by GTIN)
- Inventory Service (availability check)
- Checkout Service (session management, totals calculation)
- Shipping Service (options, validation)
- Payment Service (tokenization, processing)
- Order Service (order creation, events)

### ✅ Data Flow
```
Request → ACP Gateway → Internal Services → Database
   ↑                           ↓
   └──────── Response ─────────┘
```

---

## 🎯 Expected Behavior

### Successful Flow
1. ✅ Health check returns 200
2. ✅ Session created with status `ready_for_payment`
3. ✅ Total calculated correctly (items + shipping + tax)
4. ✅ Payment tokenized
5. ✅ Purchase completed
6. ✅ Order created with unique ID
7. ✅ Order event logged

### Error Scenarios (For Testing)

#### Invalid GTIN
```bash
curl -X POST http://localhost:8000/acp/v1/checkout_sessions \
  -H "Content-Type: application/json" \
  -d '{
    "line_items": [{"gtin": "99999999999999", "quantity": 1}]
  }'
```
**Expected:** 400 error with "Product not found"

#### Invalid Address
```bash
curl -X POST http://localhost:8000/acp/v1/checkout_sessions \
  -H "Content-Type: application/json" \
  -d '{
    "line_items": [{"gtin": "00883419552502", "quantity": 1}],
    "fulfillment_address": {
      "country": "UK"
    }
  }'
```
**Expected:** 400 error with "Only shipping to US"

---

## 📈 Performance Metrics

**Expected Response Times:**
- Health check: < 10ms
- Create session: < 200ms
- Get session: < 50ms
- Complete checkout: < 300ms

**Total Flow Time:** ~1 second

---

## 🐛 Troubleshooting

### Server Not Responding
```bash
# Check if server is running
curl http://localhost:8000/health

# If not, start it:
uvicorn app.main:app --reload --port 8000
```

### Database Errors
```bash
# Reseed database
rm data/checkout.db
python scripts/seed_products.py
```

### Import Errors in Test Script
```bash
# Install requests library
pip install requests
```

---

## 📱 Swagger UI Demo

**Interactive API testing:**

1. Open browser: http://localhost:8000/docs
2. Click on "POST /acp/v1/checkout_sessions"
3. Click "Try it out"
4. Use example payload
5. Click "Execute"
6. View response

**Advantage:** Visual, no command line needed!

---

## 🎓 What This Demonstrates

### Architecture
✅ **Gateway Pattern** - ACP endpoints translate to internal services  
✅ **Service Separation** - Each service has single responsibility  
✅ **Protocol Agnostic** - Services know nothing about ACP  

### Flow
✅ **Complete Purchase** - From cart to order confirmation  
✅ **Price Calculation** - Items + Shipping + Tax  
✅ **Payment Processing** - Tokenization and charging  
✅ **Order Creation** - Persistent order records  

### Quality
✅ **Error Handling** - Graceful error responses  
✅ **Data Validation** - Address, GTIN, payment validation  
✅ **State Management** - Session status transitions  

---

## 📊 Demo Results Summary

After running the test script, you'll see:

```
TEST SUMMARY

Results:
  ✅ PASS - Health Check
  ✅ PASS - Create Checkout Session
  ✅ PASS - Retrieve Session
  ✅ PASS - Update Shipping
  ✅ PASS - Tokenize Payment
  ✅ PASS - Complete Purchase

Summary:
  Total tests: 6
  Passed: 6
  Failed: 0

🎉 ALL TESTS PASSED! The purchase flow is working correctly.

Order Details:
  Order ID: order_abc123def456
  Session ID: cs_xyz789uvw012
  Status: Completed ✅
```

---

## 🚀 Next Steps After Demo

1. **Add More Products** - Run scraper for real Nike products
2. **Add Tests** - Comprehensive test suite (90% coverage target)
3. **Integrate Real Stripe** - Replace mock payment with real Stripe API
4. **Build MCP Server** - Add tool discovery layer
5. **Build Frontend** - ChatGPT simulator UI

---

## 📞 Support

**Issues?**
- Check server is running: `curl http://localhost:8000/health`
- Check database: `ls -lh data/checkout.db`
- Check logs: Server terminal output
- View API docs: http://localhost:8000/docs

**Working?** 🎉 Congratulations! Your Nike ACP POC is ready for demo!

