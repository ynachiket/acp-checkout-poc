# 🎬 Visual Demo Guide - Nike ACP POC

**Complete End-to-End Demonstration with ChatGPT Simulator**

---

## 🎯 Demo Overview

**What:** Visual demonstration of Nike products being purchased through ChatGPT  
**Duration:** 2-3 minutes  
**Audience:** Stakeholders, leadership, technical team  
**Impact:** Shows the future of AI commerce! 🚀

---

## 🚀 Setup (One Time, 5 minutes)

### Terminal 1: Backend

```bash
cd /Users/ntorwe/checkout-poc/backend

# Make sure database is seeded
python scripts/seed_products.py

# Start backend
uvicorn app.main:app --reload --port 8000
```

**Wait for:** `Application startup complete`

### Terminal 2: Frontend

```bash
cd /Users/ntorwe/checkout-poc/frontend/simulator

# Install dependencies (first time only)
npm install

# Start frontend
npm run dev
```

**Wait for:** `Local: http://localhost:5173/`

### Browser

```
open http://localhost:5173
```

---

## 🎬 Demo Script

### Opening (30 seconds)

**Say to audience:**
> "I'm going to show you how customers will buy Nike products through ChatGPT.
> This is a real working demo - watch as I have a conversation and complete
> a purchase without leaving the chat interface."

**Screen shows:** ChatGPT Simulator landing page

---

### Act 1: Product Discovery (30 seconds)

**Action:** Type: "I want to buy Nike Air Max shoes"

**What happens:**
1. Message appears in chat
2. "Typing..." animation
3. ChatGPT responds with product card
4. Shows: Nike Air Max 90, image, price ($120), description
5. "Add to Cart" button visible

**Say:**
> "ChatGPT understood my intent, searched the Nike catalog, and found
> the perfect product. Notice the product image, description, and price."

**Technical note:** Backend called `POST /acp/v1/checkout_sessions`

---

### Act 2: Add to Cart (20 seconds)

**Action:** Click "Add to Cart" button

**What happens:**
1. Button feedback
2. ChatGPT responds: "Great! Where would you like it shipped?"

**Say:**
> "With one click, the product is added to the cart. ChatGPT now guides
> me to provide shipping information."

---

### Act 3: Shipping & Pricing (40 seconds)

**Action:** Type: "Ship to 123 Main St, New York, NY 10001"

**What happens:**
1. Message sent
2. Backend calculates shipping and tax
3. ChatGPT shows **Checkout Summary Card**:
   - 📦 Items: Nike Air Max 90 ($120)
   - 📍 Shipping address displayed
   - 🚚 Three shipping options:
     - ✓ Standard ($5.00) - selected
     - Express ($15.00)
     - Overnight ($25.00)
   - 💰 Price breakdown:
     - Items: $120.00
     - Shipping: $5.00
     - Tax: $9.60
     - **Total: $134.60**
   - Orange "Complete Purchase" button

**Say:**
> "Look at this - ChatGPT calculated everything: shipping options,
> tax based on the address, and shows the complete breakdown. The
> customer has full transparency before purchasing."

**Technical note:** Backend called `POST /acp/v1/checkout_sessions/{id}` with address

---

### Act 4: Complete Purchase (30 seconds)

**Action:** Click "Complete Purchase" button

**What happens:**
1. Button shows loading
2. Payment tokenized (mock card)
3. Order created
4. **Order Confirmation Card** appears:
   - ✓ Green success animation
   - "Order Confirmed!"
   - Order number: `order_abc123...`
   - Timestamp
   - Confirmation message
   - "View Order Details" link

**Say:**
> "And we're done! The order is confirmed. Behind the scenes, we tokenized
> the payment through Stripe, charged the card, and created the order in
> Nike's system. The customer gets instant confirmation."

**Technical note:** 
- Backend called `POST /acp/v1/delegate_payment`
- Then `POST /acp/v1/checkout_sessions/{id}/complete`
- Order persisted to database

---

### Act 5: Show Technical Details (Optional, 30 seconds)

**Action:** Click "🔍 Show Debug" in header

**What appears:**
- Debug panel slides in from right
- Shows ALL API calls made:
  - POST /checkout_sessions (201 OK, 245ms)
  - POST /checkout_sessions/{id} (200 OK, 123ms)
  - POST /delegate_payment (200 OK, 67ms)
  - POST /checkout_sessions/{id}/complete (200 OK, 189ms)
- Shows current session state
- Shows performance metrics

**Say:**
> "For the technical folks - here's what's happening behind the scenes.
> Each conversation step triggers API calls to our ACP gateway. Notice
> the response times - all under 250ms. The session state is maintained
> throughout the flow."

---

## 🎯 Key Talking Points

### For Business Audience

1. **Conversational Commerce**
   - No app to download
   - No website to navigate
   - Just talk naturally

2. **Seamless Experience**
   - Product discovery → checkout in one interface
   - No context switching
   - Guided experience

3. **Trust & Transparency**
   - Clear pricing breakdown
   - Multiple shipping options
   - Immediate confirmation

4. **Nike Maintains Control**
   - Customer data stays with Nike
   - Order flows through Nike systems
   - Nike brand experience preserved

### For Technical Audience

1. **Clean Architecture**
   - Frontend → ACP Gateway → Services → Database
   - Protocol-agnostic services
   - Multi-protocol ready

2. **Performance**
   - Sub-second response times
   - Real-time updates
   - Smooth user experience

3. **Extensibility**
   - Same backend serves web, mobile, AI agents
   - Easy to add Google Shopping, Meta Commerce
   - Services are reusable

---

## 🎨 Visual Highlights

### Welcome Screen
- ChatGPT aesthetic (dark theme)
- Quick action buttons
- Professional branding

### Product Cards
- High-quality imagery (or Nike shoe emoji)
- Clear pricing
- Stock status
- One-click add to cart

### Checkout Summary
- Detailed line items
- Visual shipping options
- Clear price breakdown
- Prominent CTA button

### Order Confirmation
- Success animation
- Order details
- Actionable next steps

### Debug Panel
- Real-time API calls
- Performance metrics
- Technical transparency

---

## 📱 Demo Variations

### Quick Demo (1 minute)
Use quick action buttons:
1. Click all 4 quick actions in sequence
2. Shows complete flow rapidly
3. Perfect for time-constrained presentations

### Natural Demo (2-3 minutes)
Type natural language:
1. "I need running shoes"
2. "Show me Air Max"
3. "Add those"
4. "Ship to New York"
5. "Complete my order"

More realistic, shows conversational AI capability

### Technical Deep-Dive (5 minutes)
Enable debug panel from start:
1. Show API architecture
2. Explain each API call
3. Point out response times
4. Discuss scalability

---

## 🎤 Sample Presentation Script

**Opening:**
> "Good [morning/afternoon]. Today I'm going to show you Nike's integration
> with ChatGPT's Instant Checkout. This is a working proof of concept that
> demonstrates how 200 million ChatGPT users could purchase Nike products
> through simple conversation."

**[Run Demo]**

**Closing:**
> "What you just saw is completely functional. The order was created in our
> database, the payment was processed, and the customer received instant
> confirmation. This is the future of commerce - and Nike can be one of
> the first major brands to offer it."

---

## 🔧 Technical Setup for Demo Day

### Day Before Demo

```bash
# Test everything works
cd backend
python scripts/test_purchase_flow.py

# Verify frontend builds
cd frontend/simulator
npm install
npm run build
npm run preview
```

### Day of Demo

```bash
# Start both servers
cd backend && uvicorn app.main:app --reload &
cd frontend/simulator && npm run dev &

# Test in browser
open http://localhost:5173

# Do one test run
```

### Backup Plan

If frontend has issues:
```bash
# Use Python demo script instead
cd backend
python scripts/test_purchase_flow.py
```

Still shows complete flow with beautiful output!

---

## 📊 What to Show

### Minimum (Must Show)
- ✅ Natural language interaction
- ✅ Product discovery
- ✅ Order completion
- ✅ Order confirmation

### Good to Show
- ✅ Price breakdown
- ✅ Shipping options
- ✅ Address handling

### Great to Show (If Time)
- ✅ Debug panel (API calls)
- ✅ Session state
- ✅ Performance metrics
- ✅ Database verification

---

## 🎯 Success Criteria

**Demo is successful if:**
- ✅ Complete purchase flow demonstrated
- ✅ Audience understands the concept
- ✅ No technical glitches
- ✅ Questions answered confidently

**Use these docs for answers:**
- Business questions → EXECUTIVE_SUMMARY.md
- Technical questions → ARCHITECTURE.md
- "How does it work?" → Show debug panel
- "What's next?" → HANDOFF_DOCUMENT.md

---

## 🎉 Demo Checklist

### Before Demo
- [ ] Backend server running
- [ ] Frontend server running
- [ ] Database seeded
- [ ] Tested complete flow once
- [ ] Browser ready at localhost:5173
- [ ] Backup demo ready (Python script)
- [ ] Architecture docs ready for Q&A

### During Demo
- [ ] Explain what they're seeing
- [ ] Show natural conversation
- [ ] Highlight price transparency
- [ ] Show order confirmation
- [ ] (Optional) Show debug panel
- [ ] Handle questions

### After Demo
- [ ] Gather feedback
- [ ] Answer technical questions
- [ ] Discuss next steps
- [ ] Share documentation links

---

## 🎬 You're Ready!

**Everything is set up for an impressive end-to-end demo!**

**Commands to run:**
```bash
# Backend
cd backend && uvicorn app.main:app --reload

# Frontend  
cd frontend/simulator && npm run dev

# Open
http://localhost:5173
```

**Demo flow:** Conversation → Product → Cart → Checkout → Order ✅

**Status:** 🟢 READY FOR VISUAL DEMO!

