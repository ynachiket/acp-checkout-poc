# ChatGPT Simulator - Nike ACP Demo

Beautiful React-based simulator that demonstrates the complete Nike Agentic Commerce purchase flow.

---

## 🚀 Quick Start

### 1. Install Dependencies

```bash
cd frontend/simulator
npm install
```

### 2. Start Development Server

```bash
npm run dev
```

### 3. Open Browser

```
http://localhost:5173
```

**Make sure the backend is running on port 8000!**

---

## 🎬 Demo Flow

### Conversation Flow

```
User: "I want to buy Nike Air Max shoes"
  ↓
ChatGPT: Shows Nike Air Max 90 product card
  ↓
User: "Add to cart"
  ↓
ChatGPT: "Added! Where should I ship it?"
  ↓
User: "Ship to 123 Main St, New York, NY"
  ↓
ChatGPT: Shows checkout summary with totals
  ↓
User: "Complete purchase"
  ↓
ChatGPT: 🎉 Order confirmation with order ID
```

---

## ✨ Features

### ChatGPT-Like Interface
- Dark mode UI matching ChatGPT aesthetic
- Conversational flow
- Typing indicators
- Smooth scrolling

### Product Display
- Product cards with images
- Add to cart functionality
- Price display
- Stock status

### Checkout Summary
- Line items breakdown
- Shipping options (3 choices)
- Tax calculation (8%)
- Total calculation
- Complete purchase button

### Order Confirmation
- Success animation
- Order ID display
- Order link
- Confirmation message

### Debug Panel (Toggle)
- API call log
- Request/response tracking
- Session state
- Performance metrics

---

## 🎨 UI Components

```
src/
├── App.jsx                    # Main app
├── components/
│   ├── Header.jsx             # Top bar with debug toggle
│   ├── ChatInterface.jsx      # Main chat UI
│   ├── Message.jsx            # Individual messages
│   ├── ProductCard.jsx        # Product display
│   ├── CheckoutSummary.jsx    # Cart & totals
│   ├── OrderConfirmation.jsx  # Success screen
│   └── DebugPanel.jsx         # API call inspector
└── store.js                   # Zustand state management
```

---

## 🔧 Tech Stack

- **React 18** - UI library
- **Vite** - Build tool (fast HMR)
- **TailwindCSS** - Styling
- **Zustand** - State management
- **Axios** - API client

---

## 🎯 Demo Scenarios

### Scenario 1: Quick Purchase (30 seconds)

1. Type: "I want to buy Nike Air Max shoes"
2. Click "Add to Cart"
3. Type: "Ship to New York"
4. Click "Complete Purchase"
5. See order confirmation!

### Scenario 2: With Debug Panel (Visual)

1. Click "🔍 Show Debug" in header
2. Watch API calls in real-time
3. See session state
4. Track performance

---

## 🐛 Troubleshooting

### Backend Not Responding

```bash
# Make sure backend is running
cd backend
uvicorn app.main:app --reload --port 8000
```

### CORS Errors

Backend has CORS enabled for `localhost:5173` by default.

### Port 5173 Already in Use

```bash
# Kill process on port 5173
lsof -ti:5173 | xargs kill -9

# Or use different port
npm run dev -- --port 5174
```

---

## 📸 Screenshots

### Chat Interface
- ChatGPT-style dark theme
- Product cards with Nike styling
- Smooth animations

### Checkout Summary
- Line items
- Shipping options
- Price breakdown
- Complete purchase button

### Order Confirmation
- Success animation
- Order details
- Confirmation message

---

## 🎨 Customization

### Colors

Edit `tailwind.config.js`:
```js
theme: {
  extend: {
    colors: {
      'nike-orange': '#FF6B35',  // Nike brand color
      'chatgpt': { ... }          // ChatGPT theme
    }
  }
}
```

### API Endpoint

Edit `src/store.js`:
```js
const API_BASE = 'http://localhost:8000'  // Change if needed
```

---

## 🚀 Production Build

```bash
npm run build
```

Outputs to `dist/` directory.

---

## 📦 What's Next

**Enhancements:**
- [ ] Multiple product search
- [ ] Quantity selector
- [ ] Address autocomplete
- [ ] Payment method UI
- [ ] Order history
- [ ] Real ChatGPT model integration

---

**Status:** ✅ Working demo UI  
**Demo-Ready:** Yes!  
**Integration:** Backend ACP API

