# 🎬 Complete Demo Guide - Nike ACP POC

**End-to-End Visual Demonstration**

---

## 🎯 What This Demo Shows

A complete purchase flow through a **ChatGPT-like interface**:

```
User has conversation → ChatGPT finds products → Add to cart
→ Enter shipping → Calculate totals → Complete purchase → Order created
```

**All happening through natural conversation!** 🤖💬

---

## 🚀 Running the Complete Demo

### Prerequisites

✅ Backend server running  
✅ Database seeded with products  
✅ Node.js installed  

### Setup (5 minutes)

```bash
# Terminal 1: Start Backend
cd backend
uvicorn app.main:app --reload --port 8000

# Terminal 2: Start Frontend
cd frontend/simulator
npm install
npm run dev

# Terminal 3 (Optional): Watch logs
cd backend
tail -f logs/app.log
```

### Open Browser

```
http://localhost:5173
```

---

## 🎬 Demo Script (2 minutes)

### Step 1: Welcome Screen

**You'll see:**
- ChatGPT-style interface
- Nike Shopping Assistant greeting
- Quick action buttons

**Do:** Click "I want to buy Nike Air Max shoes" or type it

---

### Step 2: Product Discovery

**ChatGPT responds with:**
- Product card for Nike Air Max 90
- Product image, title, description
- Price: $120.00
- "Add to Cart" button

**Backend call:** `POST /acp/v1/checkout_sessions`

**Do:** Click "Add to Cart"

---

### Step 3: Shipping Request

**ChatGPT responds:**
- "Great! Where would you like it shipped?"

**Do:** Type: "Ship to 123 Main St, New York, NY 10001"

---

### Step 4: Checkout Summary

**ChatGPT shows:**
- 🛒 Checkout Summary card
- Line items: Nike Air Max 90 ($120.00)
- Shipping address: New York
- Shipping options:
  - ✓ Standard ($5.00) - selected
  - Express ($15.00)
  - Overnight ($25.00)
- Price breakdown:
  - Items: $120.00
  - Shipping: $5.00
  - Tax: $9.60
  - **Total: $134.60**
- "Complete Purchase" button

**Backend call:** `POST /acp/v1/checkout_sessions/{id}` (update with address)

**Do:** Click "Complete Purchase"

---

### Step 5: Order Confirmation

**ChatGPT shows:**
- ✓ Green success card
- "Order Confirmed!"
- Order number: `order_abc123...`
- Order date
- Confirmation message
- "View Order Details" link

**Backend calls:**
1. `POST /acp/v1/delegate_payment` (tokenize card)
2. `POST /acp/v1/checkout_sessions/{id}/complete` (create order)

**Result:** Order created in database! ✅

---

## 🔍 Debug Panel Features

### Enable Debug Mode

Click "🔍 Show Debug" in header

**You'll see:**
- **Current Session:**
  - Session ID
  - Status (not_ready_for_payment → ready_for_payment → completed)
  - Current total

- **API Call Log:**
  - HTTP method (POST/GET)
  - Endpoint path
  - Status code (200, 400, etc.)
  - Response time (ms)
  - Timestamp

**Perfect for demos to show technical implementation!**

---

## 🎨 Visual Features

### ChatGPT-Style Interface
- ✅ Dark theme (#343541)
- ✅ Message bubbles (user vs assistant)
- ✅ Typing animation (...)
- ✅ Smooth scrolling
- ✅ Avatar icons

### Nike Branding
- ✅ Nike orange accent color (#FF6B35)
- ✅ Product cards with Nike styling
- ✅ Professional color scheme

### Interactive Elements
- ✅ Hover effects
- ✅ Button states
- ✅ Loading indicators
- ✅ Success animations

---

## 📊 What's Happening Behind the Scenes

### Conversation Flow → API Calls

```
User: "I want to buy Nike shoes"
  ↓
Frontend: Detects purchase intent
  ↓
API Call: POST /acp/v1/checkout_sessions
  ├── line_items: [{ gtin: "00883419552502", quantity: 1 }]
  └── Response: Session created
  ↓
ChatGPT: Shows product card

User: "Ship to [address]"
  ↓
API Call: POST /acp/v1/checkout_sessions/{id}
  ├── fulfillment_address: { ... }
  └── Response: Shipping calculated
  ↓
ChatGPT: Shows checkout summary

User: "Complete purchase"
  ↓
API Call 1: POST /acp/v1/delegate_payment
  ├── card_number: "4242..."
  └── Response: payment_token_id
  ↓
API Call 2: POST /acp/v1/checkout_sessions/{id}/complete
  ├── payment_token_id: "pm_..."
  └── Response: Order created
  ↓
ChatGPT: Shows order confirmation
```

---

## 🎯 Stakeholder Demo Tips

### For Business Audience

**Focus on:**
1. **Natural conversation** - "Just talk to ChatGPT"
2. **Seamless experience** - No app switching
3. **Trust signals** - Price breakdown, shipping options
4. **Order confirmation** - Real order created

**Script:**
> "Watch how a customer can buy Nike products just by talking to ChatGPT. 
> No apps to download, no websites to navigate - just conversation."

### For Technical Audience

**Enable debug panel and show:**
1. **API calls in real-time**
2. **Session state management**
3. **Response times** (< 500ms)
4. **Error handling**

**Script:**
> "Behind the scenes, this is calling our ACP gateway, which orchestrates
> calls to our protocol-agnostic services. Notice the clean separation."

---

## 🎨 UI Customization

### Quick Actions (Edit in ChatInterface.jsx)

```javascript
const quickActions = [
  "I want to buy Nike Air Max shoes",
  "Show me running shoes under $150",
  "Add size 10 to my cart",
  "Ship to 123 Main St, New York, NY 10001",
]
```

Add more quick actions for different demo scenarios!

### Product Search (Edit in store.js)

```javascript
// Currently hardcoded to Nike Air Max 90
// Can be extended to search multiple products
searchProducts: async (query) => {
  // Add product search logic
}
```

---

## 📸 Screenshot Guide

### Landing Screen
- Empty chat with welcome message
- Quick action buttons
- Clean, modern interface

### Product Display
- Product card within chat
- Image, title, description
- Price and "Add to Cart" button
- In-stock indicator

### Checkout Summary
- Detailed price breakdown
- Shipping options with selection
- Address display
- Prominent "Complete Purchase" button

### Order Confirmation
- Green success card
- Order number prominently displayed
- Confirmation message
- Action button

---

## 🎯 Demo Variations

### Variation 1: Speed Demo (30 seconds)

Use quick action buttons:
1. Click "I want to buy Nike Air Max shoes"
2. Click "Add to cart"
3. Click "Ship to..."
4. Click "Complete Purchase"
5. Done!

### Variation 2: Natural Conversation (2 minutes)

Type naturally:
1. "I need new running shoes"
2. "What about Air Max?"
3. "Add those to my cart"
4. "Ship to my address in New York"
5. "Complete the order"

### Variation 3: Technical Demo (with debug panel)

1. Enable debug panel
2. Go through purchase flow
3. Point out each API call
4. Show response times
5. Explain session state

---

## 🔧 Troubleshooting

### "Network Error" in Chat

**Check:**
1. Backend server is running (`http://localhost:8000/health`)
2. CORS is configured (should be automatic)
3. No firewall blocking

### Products Not Showing

**Check:**
1. Database is seeded (`sqlite3 backend/data/checkout.db "SELECT COUNT(*) FROM products;"`)
2. GTIN is correct in store.js

### Styling Issues

```bash
# Rebuild Tailwind
npm run dev
```

---

## 📦 What's Included

**15 Frontend Files:**
- 1 main app
- 6 React components
- 1 state management store
- 7 config files (package.json, vite, tailwind, etc.)

**Features:**
- ChatGPT-style interface
- Product cards
- Checkout summary
- Order confirmation
- Debug panel
- API integration

---

## 🎉 Demo Ready!

**Status:** ✅ Complete visual demo  
**Integration:** Backend ACP API  
**Experience:** ChatGPT-like shopping  

**Open http://localhost:5173 and start shopping! 🛍️**

