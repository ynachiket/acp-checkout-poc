# 🎬 Run Complete End-to-End Demo

**Nike ACP POC - Full Visual Demonstration**

---

## 🚀 Start Everything (2 commands)

### Terminal 1: Backend

```bash
cd /Users/ntorwe/checkout-poc/backend
uvicorn app.main:app --reload --port 8000
```

**Wait for:** `Application startup complete.`

### Terminal 2: Frontend

```bash
cd /Users/ntorwe/checkout-poc/frontend/simulator
npm run dev
```

**Wait for:** `Local: http://localhost:5173/`

---

## 🌐 Open Browser

```
http://localhost:5173
```

**You'll see:** ChatGPT-style interface with Nike branding! 🎨

---

## 🎬 Demo the Complete Flow

### Step 1: Start Conversation

**Type or click:** "I want to buy Nike Air Max shoes"

**Watch:**
- Message appears in chat (blue bubble)
- Typing indicator (...)
- ChatGPT responds with product card
- Product shows: Nike Air Max 90, image, price, description
- "Add to Cart" button

**Time:** 2 seconds

---

### Step 2: Add to Cart

**Click:** "Add to Cart" button on product card

**Watch:**
- Button feedback
- ChatGPT asks: "Where would you like it shipped?"

**Time:** 1 second

---

### Step 3: Add Shipping Address

**Type:** "Ship to 123 Main St, New York, NY 10001"

**Watch:**
- Message sent
- Typing indicator
- **Checkout Summary Card appears:**
  - 📦 Items in cart
  - 📍 Shipping address
  - 🚚 3 shipping options (Standard selected)
  - 💰 Price breakdown:
    - Items: $120.00
    - Shipping: $5.00
    - Tax: $9.60
    - **Total: $134.60**
  - Orange "Complete Purchase" button

**Time:** 2 seconds

---

### Step 4: Complete Purchase

**Click:** "Complete Purchase" button

**Watch:**
- Button loading state
- Processing...
- **Order Confirmation Card appears:**
  - ✓ Green success animation
  - "Order Confirmed!"
  - Order number: `order_xyz123...`
  - Timestamp
  - Confirmation message
  - "View Order Details" link

**Time:** 1 second

---

### 🎉 DONE!

**Total demo time:** < 30 seconds  
**Order created:** ✅ Check database!  
**Experience:** Conversational commerce in action!

---

## 🔍 Show Technical Details

### Enable Debug Panel

**Click:** "🔍 Show Debug" in top-right header

**Debug panel shows:**
- **Current Session:**
  - Session ID: `cs_abc123...`
  - Status: `completed`
  - Total: `$134.60`

- **API Call Log:**
  ```
  POST /acp/v1/checkout_sessions          (200 OK, 245ms)
  POST /acp/v1/checkout_sessions/{id}     (200 OK, 123ms)
  POST /acp/v1/delegate_payment           (200 OK, 67ms)
  POST /acp/v1/checkout_sessions/{id}/complete  (200 OK, 189ms)
  ```

**Perfect for technical audiences!**

---

## ✨ Demo Features to Highlight

### 1. Natural Language Interface
> "Notice how the customer just talks naturally - no forms to fill out,
> no navigation menus. ChatGPT guides them through the purchase."

### 2. Visual Product Cards
> "Products are displayed beautifully within the conversation,
> making it easy to browse and decide."

### 3. Transparent Pricing
> "Every cost is broken down clearly - shipping options, tax calculation,
> final total. No surprises at checkout."

### 4. Instant Confirmation
> "Order is created immediately with a unique order ID that can be tracked."

### 5. Technical Excellence (Debug Panel)
> "Behind the scenes, this is calling our ACP gateway with sub-second
> response times. The architecture is production-ready."

---

## 🎯 Demo Scenarios

### Scenario A: Executive Demo (1 minute)

**Focus:** Business value

1. Show conversation flow
2. Complete purchase
3. Explain: "200M ChatGPT users can now buy Nike this way"

**Skip:** Debug panel, technical details

---

### Scenario B: Technical Demo (3 minutes)

**Focus:** Implementation

1. Enable debug panel from start
2. Show each API call
3. Explain gateway pattern
4. Discuss architecture

**Include:** Code walkthrough if needed

---

### Scenario C: Full Stakeholder Demo (5 minutes)

**Focus:** Complete story

1. Business context (why this matters)
2. Run demo (complete flow)
3. Show debug panel (how it works)
4. Discuss production path
5. Q&A

---

## 📊 Verification

### Check Order Was Created

```bash
# In Terminal 3
cd /Users/ntorwe/checkout-poc/backend
sqlite3 data/checkout.db "SELECT id, status, created_at FROM orders ORDER BY created_at DESC LIMIT 1;"
```

**You'll see:** The order that was just created! ✅

### Check Session State

```bash
sqlite3 data/checkout.db "SELECT id, status FROM checkout_sessions WHERE status='completed' ORDER BY created_at DESC LIMIT 1;"
```

**Status:** `completed` ✅

---

## 🎨 Visual Highlights

### ChatGPT Aesthetic
- Dark theme (#343541)
- Smooth animations
- Professional polish
- Familiar interface

### Nike Branding
- Orange accent color (#FF6B35)
- Product cards
- Brand-appropriate styling

### Interactive Elements
- Hover effects on buttons
- Typing indicators
- Smooth scrolling
- Loading states

---

## 🐛 Troubleshooting

### Frontend Not Loading

```bash
# Check if server is running
curl http://localhost:5173

# Restart if needed
cd frontend/simulator
npm run dev
```

### Backend Connection Issues

```bash
# Check backend
curl http://localhost:8000/health

# Check CORS (should see localhost:5173 in allowed origins)
```

### Products Not Appearing

```bash
# Reseed database
cd backend
python scripts/seed_products.py
```

---

## 🎯 Demo Success Checklist

Before demo:
- [ ] Backend running (`http://localhost:8000/health` returns OK)
- [ ] Frontend running (`http://localhost:5173` loads)
- [ ] Database seeded (10 products)
- [ ] Tested flow once (do a test purchase)
- [ ] Browser ready and maximized
- [ ] Architecture docs ready for Q&A

During demo:
- [ ] Explain what they're seeing
- [ ] Show natural conversation
- [ ] Highlight price transparency
- [ ] Show order confirmation
- [ ] (Optional) Show debug panel
- [ ] Handle questions confidently

After demo:
- [ ] Verify order in database
- [ ] Show architecture diagram
- [ ] Discuss ROI and timeline
- [ ] Get feedback

---

## 🎬 You're Ready!

**Run these commands:**

```bash
# Backend (Terminal 1)
cd backend && uvicorn app.main:app --reload

# Frontend (Terminal 2)  
cd frontend/simulator && npm run dev

# Open Browser
open http://localhost:5173
```

**Then:** Follow the demo script above!

---

## 🎉 What You'll Demonstrate

✅ **Conversational AI Commerce** - Natural language shopping  
✅ **Complete Purchase Flow** - Cart to order in seconds  
✅ **Nike Integration** - Real Nike products  
✅ **Price Transparency** - Clear breakdown  
✅ **Instant Confirmation** - Order created  
✅ **Technical Excellence** - Fast, reliable, scalable  

**Status:** 🟢 READY FOR END-TO-END VISUAL DEMO!

---

**The complete Nike ACP POC experience is now ready to demonstrate! 🚀**

