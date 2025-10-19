# Nike Agentic Commerce POC

**OpenAI Instant Checkout Integration - Complete Working Demo**

[![Status](https://img.shields.io/badge/status-demo--ready-green)](.)
[![Coverage](https://img.shields.io/badge/coverage-56%25-yellow)](./docs/TESTING_GUIDE.md)
[![Backend](https://img.shields.io/badge/backend-FastAPI-009688)](./backend)
[![Frontend](https://img.shields.io/badge/frontend-React-61DAFB)](./frontend/simulator)

---

## 🎯 Quick Start (5 Minutes)

### 1. Start Backend

```bash
cd backend
pip install -r requirements.txt
python scripts/seed_products.py
uvicorn app.main:app --reload
```

### 2. Start Frontend

```bash
# Ensure Node.js 18+
cd frontend/simulator
npm install
npm run dev
```

### 3. Open Demo

```
http://localhost:5173
```

**Demo Flow:**
1. Type: "I want to buy Nike Air Max shoes"
2. Click: "Add to Cart"
3. Type: "3775 SW Morrison, Portland, OR 97220"
4. Click: "Complete Purchase"
5. See: Order confirmed! ✅

---

## 📊 What's Included

### ✅ Complete Backend API
- **MCP Server** - 6 discoverable tools for AI agents (NEW!)
- **6 ACP Endpoints** - Full Agentic Checkout implementation
- **6 Internal Services** - Product, Inventory, Checkout, Shipping, Payment, Order
- **4 Database Models** - SQLAlchemy ORM with SQLite
- **47 Tests** - 56% coverage (Product Service: 97%)
- **10 Nike Products** - Ready for demo

### ✅ ChatGPT Simulator UI
- **React 18** - Modern frontend
- **ChatGPT-style Interface** - Dark theme, conversational UX
- **MCP Integration** - Uses Model Context Protocol for all operations (NEW!)
- **Complete Purchase Flow** - Search → Cart → Checkout → Order
- **Debug Panel** - Shows MCP tool calls in real-time
- **Order Confirmation** - Beautiful success screen

### ✅ Comprehensive Documentation
- **Architecture Specs** - Complete technical documentation
- **Business Case** - ROI analysis and recommendations
- **Demo Guides** - Multiple ways to demonstrate
- **Decision Log** - All architectural decisions documented

---

## 🏗️ Architecture

```
AI Agents (ChatGPT, Claude, Gemini...)
         ↓
   MCP Server (Tool Discovery) ✨ NEW!
         ↓
Protocol Gateway Layer (ACP + Future: Google, Meta)
         ↓
Internal Services Layer (Protocol-Agnostic)
         ↓
Data Layer (SQLite + Stripe)
```

**Key Pattern:** MCP + Gateway architecture = true agentic commerce

---

## 📚 Documentation

### Essential Reading
- **[ARCHITECTURE.md](./ARCHITECTURE.md)** - Complete technical architecture
- **[EXECUTIVE_SUMMARY.md](./EXECUTIVE_SUMMARY.md)** - Business case and ROI
- **[START_HERE.md](./START_HERE.md)** - Quick navigation guide

### Guides
- **[docs/guides/](./docs/guides/)** - Demo guides and tutorials
- **[docs/status/](./docs/status/)** - Project status and progress
- **[docs/TESTING_GUIDE.md](./docs/TESTING_GUIDE.md)** - Path to 90% coverage

---

## 🎬 Demo Options

### Option 1: Visual UI (Recommended)
```bash
# Start servers (see Quick Start above)
open http://localhost:5173
```

ChatGPT-style interface with complete purchase flow

### Option 2: Python Script (ACP)
```bash
cd backend
python scripts/test_purchase_flow.py
```

Shows complete flow using ACP REST endpoints

### Option 3: Python Script (MCP) ✨ NEW!
```bash
cd backend
python scripts/test_mcp_flow.py
```

Shows complete flow using MCP tool discovery and invocation

### Option 3: API Documentation
```bash
open http://localhost:8000/docs
```

Interactive Swagger UI for API testing

---

## 🧪 Testing

```bash
cd backend

# Run all tests
pytest

# Run with coverage
pytest --cov=app --cov-report=html

# View coverage report
open htmlcov/index.html
```

**Current Coverage:** 56% overall, Product Service: 97%

---

## 🎯 Project Status

| Component | Status | Coverage |
|-----------|--------|----------|
| Backend API | ✅ Complete | 56% |
| Frontend UI | ✅ Complete | N/A |
| Purchase Flow | ✅ Working | E2E Validated |
| Documentation | ✅ Complete | 20+ docs |
| Demo Scripts | ✅ Ready | 3 options |

**Overall:** ✅ Demo-Ready POC

---

## 🚀 Tech Stack

**Backend:**
- Python 3.11+ / FastAPI
- SQLAlchemy (ORM)
- SQLite (database)
- Stripe SDK (payment)
- pytest (testing)

**Frontend:**
- React 18 / Vite
- TailwindCSS
- Zustand (state)
- Axios (API client)

---

## 📋 Next Steps

### To Reach 90% Test Coverage
- Add ~70 tests for remaining services
- Follow pattern in `tests/test_services/test_product_service.py`
- Estimated: 8-10 hours

### For Production
- Integrate real Stripe API
- Add MCP server layer
- Nike CPA/Digital Rollup integration
- Kubernetes deployment
- OpenAI certification

See [EXECUTIVE_SUMMARY.md](./EXECUTIVE_SUMMARY.md) for complete production roadmap.

---

## 🤝 Contributing

Internal Nike project. See documentation for development guidelines.

---

## 📝 License

Internal Nike project - All rights reserved

---

## 📧 Support

- **Architecture Questions:** See [ARCHITECTURE.md](./ARCHITECTURE.md)
- **Demo Issues:** See [docs/guides/](./docs/guides/)
- **Business Case:** See [EXECUTIVE_SUMMARY.md](./EXECUTIVE_SUMMARY.md)

---

**Built:** October 19, 2025  
**Status:** ✅ Complete Working Demo  
**Timeline:** 1 day (90% ahead of schedule)  
**Coverage:** 56% (Product Service: 97%)
