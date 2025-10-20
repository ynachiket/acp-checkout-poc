# Agentic Commerce POC - System Architecture

**Version:** 1.1 (Updated)  
**Date:** October 19, 2025  
**Status:** Approved for POC Implementation

---

## Table of Contents
1. [Overview](#overview)
2. [Architecture Diagrams](#architecture-diagrams)
3. [Component Details](#component-details)
4. [Data Flow](#data-flow)
5. [API Examples](#api-examples) ⭐ NEW
6. [Security & Privacy](#security--privacy) ⭐ NEW
7. [Technology Stack](#technology-stack)
8. [Design Principles](#design-principles)
9. [Troubleshooting](#troubleshooting) ⭐ NEW
10. [Glossary](#glossary) ⭐ NEW

---

## Overview

This document describes the architecture for an Agentic Commerce Protocol (ACP) Proof of Concept, demonstrating integration with AI agents' checkout capabilities through a multi-layered gateway pattern.

### Goals
- Demonstrate end-to-end ACP integration with simulated ChatGPT client
- Build protocol-agnostic commerce services for future extensibility
- Integrate with Stripe for real payment processing (test mode)
- Provide foundation for production implementation

### Non-Goals (POC Scope)
- Production-scale deployment (Kubernetes, multi-region)
- Internal service integrations (CRM, ERP systems)
- Advanced security features (mTLS, HSM integration)
- Multi-marketplace support (US-only for POC)

---

## Architecture Diagrams

### High-Level System Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                   AI Agents / Clients                           │
│          (ChatGPT, Claude, Custom UIs, Scripts)                 │
└────────┬─────────────────────────────────────────┬──────────────┘
         │                                         │
         │ PATH 1: MCP Protocol                    │ PATH 2: Direct ACP REST
         │ (Simplified Tool Invocation)            │ (OpenAI Standard Protocol)
         │                                         │
         ▼                                         ▼
┌─────────────────────────┐             ┌─────────────────────────┐
│   MCP ENDPOINT LAYER    │             │   ACP REST ENDPOINTS    │
│   POST /mcp             │             │   /acp/v1/*             │
│                         │             │                         │
│  • Tool dispatch        │             │  • GET /products        │
│  • JSON-RPC style       │             │  • POST /checkout_      │
│  • 6 available tools    │             │    sessions             │
│                         │             │  • PATCH /checkout_     │
│  Tools:                 │             │    sessions/{id}        │
│  - search_products      │             │  • POST /payment_       │
│  - get_product_details  │             │    tokens               │
│  - create_checkout      │             │  • POST /orders         │
│  - add_shipping_address │             │                         │
│  - complete_purchase    │             │                         │
│  - get_order_status     │             │                         │
└────────┬────────────────┘             └────────┬────────────────┘
         │                                       │
         │          Both paths converge          │
         │                  ▼                    │
         └──────────────────┬────────────────────┘
                            │
┌───────────────────────────▼─────────────────────────────────────┐
│                  AGENTIC COMMERCE GATEWAY                       │
│              (Protocol Translation & Orchestration)             │
│                                                                 │
│  ┌──────────────────────────────────────────────────────────┐ │
│  │  Protocol Translation Layer                              │ │
│  │  ├── MCP Tool Handler (dispatches to services)          │ │
│  │  ├── ACP Protocol Translator (ACP ↔ Internal)           │ │
│  │  ├── Error Code Mapper                                  │ │
│  │  ├── Response Enrichment                                │ │
│  │  └── Validation & Guardrails                            │ │
│  └──────────────────────────────────────────────────────────┘ │
│                                                                 │
│  ┌──────────────────────────────────────────────────────────┐ │
│  │  Future Protocol Handlers                                │ │
│  │  • Google Shopping Protocol (planned)                    │ │
│  │  • Meta Commerce Protocol (planned)                      │ │
│  │  • Custom protocols                                      │ │
│  └──────────────────────────────────────────────────────────┘ │
│                                                                 │
│  ┌──────────────────────────────────────────────────────────┐ │
│  │  Gateway Shared Services                                 │ │
│  │  • Authentication & Authorization                        │ │
│  │  • Rate Limiting                                         │ │
│  │  • Request/Response Logging                              │ │
│  │  • Cost Attribution                                      │ │
│  └──────────────────────────────────────────────────────────┘ │
└────────────────────────┬────────────────────────────────────────┘
                         │
                         │ Internal API (Protocol-Agnostic)
                         │
┌────────────────────────▼────────────────────────────────────────┐
│                   INTERNAL COMMERCE SERVICES                    │
│                  (Business Logic - No Protocol Knowledge)       │
│                                                                 │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐           │
│  │   Product   │  │  Checkout   │  │   Payment   │           │
│  │   Service   │  │   Service   │  │   Service   │           │
│  │             │  │             │  │             │           │
│  │ • Search    │  │ • Session   │  │ • Stripe    │           │
│  │ • Get by ID │  │   Mgmt      │  │   Token     │           │
│  │ • Feed Gen  │  │ • Pricing   │  │   Exchange  │           │
│  │ • Variants  │  │ • Validation│  │ • Charge    │           │
│  └─────────────┘  └─────────────┘  └─────────────┘           │
│                                                                 │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐           │
│  │  Shipping   │  │    Order    │  │  Inventory  │           │
│  │   Service   │  │   Service   │  │   Service   │           │
│  │             │  │             │  │             │           │
│  │ • Calculate │  │ • Create    │  │ • Check     │           │
│  │   Options   │  │ • Retrieve  │  │   Stock     │           │
│  │ • Estimates │  │ • Update    │  │ • Reserve   │           │
│  │ • Carriers  │  │ • Events    │  │ • Release   │           │
│  └─────────────┘  └─────────────┘  └─────────────┘           │
│                                                                 │
└────────────────────────┬────────────────────────────────────────┘
                         │
                         │ Data Access Layer
                         │
┌────────────────────────▼────────────────────────────────────────┐
│                      DATA & EXTERNAL SYSTEMS                    │
│                                                                 │
│  ┌────────────────────┐      ┌────────────────────────────┐   │
│  │   SQLite Database  │      │   Stripe API (Test Mode)   │   │
│  │                    │      │                            │   │
│  │  • products        │      │  • Payment Intents         │   │
│  │  • checkout_       │      │  • Shared Payment Token    │   │
│  │    sessions        │      │  • Payment Methods         │   │
│  │  • orders          │      │                            │   │
│  │  • order_events    │      │                            │   │
│  └────────────────────┘      └────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────┘
```

### Layered Architecture View

```
┌─────────────────────────────────────────────────────────────────┐
│  LAYER 1: AI INTERFACE LAYER (MCP Server)                       │
│  Purpose: Tool discovery and AI-native interaction              │
│  Protocols: MCP (Model Context Protocol)                        │
└─────────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────────┐
│  LAYER 2: PROTOCOL GATEWAY LAYER (Multi-Protocol Support)       │
│  Purpose: Protocol translation, validation, orchestration       │
│  Protocols: ACP, Google Shopping, Meta Commerce (future)        │
└─────────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────────┐
│  LAYER 3: BUSINESS LOGIC LAYER (Internal Services)              │
│  Purpose: Protocol-agnostic commerce operations                 │
│  Technology: Python services, business rules, orchestration     │
└─────────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────────┐
│  LAYER 4: DATA & INTEGRATION LAYER                              │
│  Purpose: Data persistence and external integrations            │
│  Technology: SQLite, Stripe API, future payment processors      │
└─────────────────────────────────────────────────────────────────┘
```

### Integration Paths: MCP vs. Direct ACP REST

This POC implements **two integration paths** to demonstrate flexibility:

| Aspect | PATH 1: MCP Endpoint | PATH 2: Direct ACP REST |
|--------|---------------------|------------------------|
| **Use Case** | Simplified tool-based API | Standard OpenAI ACP protocol |
| **Endpoint** | `POST /mcp` | `/acp/v1/*` (5 endpoints) |
| **Protocol** | JSON-RPC style tool dispatch | OpenAI ACP v1.0 spec |
| **Complexity** | Low - single endpoint | Medium - multiple REST endpoints |
| **Tools/APIs** | 6 tools | 5 REST endpoints + product feed |
| **Best For** | Custom UIs, scripts, demos | ChatGPT integration, production |
| **POC Use** | ✅ Frontend simulator uses this | Test scripts available |

#### When to Use MCP Path
- Building custom AI-powered UIs
- Rapid prototyping and demos  
- Internal tools that need simplified API
- Tool-based interaction model

#### When to Use Direct ACP REST Path
- Integrating with ChatGPT Instant Checkout
- Production AI agents following OpenAI standards
- Full ACP protocol compliance required
- Multi-protocol gateway architectures

**Important:** Both paths use the same internal services layer - they're just different "front doors" to the same commerce logic.

---

## Component Details

### Layer 1: MCP Endpoint & ACP REST (External Interfaces)

#### 1a. MCP Endpoint (Simplified Tool-Based API)

**Purpose:** Provide simplified, tool-based interface for AI agents and custom UIs.

**Endpoint:**
```
POST /mcp          # Single endpoint for all operations
```

**Available Tools:**
```python
Tools:
  - search_products(query, category, filters)
  - get_product_details(gtin)
  - create_checkout(items, address?)
  - add_shipping_address(checkout_id, address)
  - complete_purchase(checkout_id, payment)
  - check_order_status(order_id)
```

**Request Format:**
```json
{
  "tool": "search_products",
  "arguments": {
    "query": "running shoes",
    "limit": 5
  }
}
```

**Technology:**
- Python FastAPI
- Simplified MCP-inspired protocol
- Tool dispatch pattern

**Benefits:**
- Single endpoint - easier to integrate
- Tool-based interaction familiar to AI developers
- Perfect for custom UIs and demos
- Lower learning curve

#### 1b. ACP REST Endpoints (OpenAI Standard Protocol)

**Purpose:** Full OpenAI Agentic Commerce Protocol (ACP) v1.0 compliance.

**Endpoints:**
```
POST   /acp/v1/checkout_sessions              # Create session
PATCH  /acp/v1/checkout_sessions/{id}         # Update session
POST   /acp/v1/checkout_sessions/{id}/complete # Complete checkout
POST   /acp/v1/checkout_sessions/{id}/cancel  # Cancel session
GET    /acp/v1/checkout_sessions/{id}         # Retrieve session
GET    /acp/v1/product-feed.json              # Product catalog
POST   /acp/v1/payment_tokens                 # Payment tokenization
POST   /acp/v1/orders                         # Create order
```

**Technology:**
- Python FastAPI
- OpenAI ACP v1.0 specification
- RESTful architecture

**Benefits:**
- Standard protocol for ChatGPT integration
- Production-ready for AI agent ecosystem
- Well-documented specification
- Multi-agent compatibility

---

### Layer 2: Agentic Commerce Gateway

**Purpose:** Translate between external commerce protocols and internal services.

#### 2.1 ACP Protocol Handler

**REST Endpoints:**
```
POST   /acp/v1/checkout_sessions              # Create session
POST   /acp/v1/checkout_sessions/{id}         # Update session
POST   /acp/v1/checkout_sessions/{id}/complete # Complete checkout
POST   /acp/v1/checkout_sessions/{id}/cancel  # Cancel session
GET    /acp/v1/checkout_sessions/{id}         # Retrieve session
GET    /acp/v1/product-feed.json              # Product feed
POST   /acp/v1/delegate_payment               # Payment tokenization
```

**Protocol Translation:**
```python
ACP Format                    →    Internal Format
─────────────────────────────────────────────────────
line_items[].gtin             →    items[].product_id
line_items[].quantity         →    items[].quantity
fulfillment_address           →    shipping_address
fulfillment_options           →    shipping_options
totals.items_total            →    pricing.subtotal
totals.fulfillment            →    pricing.shipping_cost
totals.taxes                  →    pricing.tax
```

**Error Code Mapping:**
```python
Internal Error                →    ACP Error Code
─────────────────────────────────────────────────
ProductNotFoundError          →    "missing"
InvalidGTINError              →    "invalid"
OutOfStockError               →    "out_of_stock"
PaymentDeclinedError          →    "payment_declined"
InvalidAddressError           →    "invalid"
SessionExpiredError           →    "missing"
AuthenticationError           →    "requires_sign_in"
```

**Validation Rules:**
- GTIN format validation (8-14 digits)
- Quantity limits (1-10 per item)
- Product buyability rules (no gift cards, customization)
- Address completeness
- Payment token validity

#### 2.2 Shared Gateway Services

**Authentication:**
- API key validation (POC: simple key)
- Request signature verification
- Rate limit enforcement

**Logging:**
- Request/response logging
- Error tracking
- Performance metrics
- Cost attribution

**Orchestration:**
- Multi-service coordination
- Timeout handling
- Retry logic with exponential backoff

---

### Layer 3: Internal Commerce Services

**Design Principle:** These services know NOTHING about ACP, MCP, or any external protocol. They implement pure business logic.

#### 3.1 Product Service

**Responsibilities:**
- Product catalog management
- Product search and filtering
- GTIN → Internal ID mapping
- Product feed generation

**API:**
```python
class ProductService:
    async def search(query: str, filters: dict) -> list[Product]
    async def get_by_id(product_id: str) -> Product
    async def get_by_gtin(gtin: str) -> Product
    async def check_buyability(product_id: str) -> bool
    async def get_variants(product_id: str) -> list[Variant]
    async def generate_feed() -> ProductFeed
```

**Data Model:**
```python
Product:
  - id: str (internal ID)
  - gtin: str (Global Trade Item Number)
  - mpn: str (Manufacturer Part Number)
  - title: str
  - description: str
  - brand: str
  - category: str
  - price: Decimal
  - currency: str
  - images: list[str]
  - availability: str (in_stock, out_of_stock)
  - variants: list[Variant] (size, color options)
  - metadata: dict
```

#### 3.2 Checkout Service

**Responsibilities:**
- Session lifecycle management
- Cart operations
- Pricing calculations
- Checkout orchestration

**API:**
```python
class CheckoutService:
    async def create_session(request: CreateSessionRequest) -> Session
    async def update_session(session_id: str, updates: dict) -> Session
    async def get_session(session_id: str) -> Session
    async def calculate_totals(session: Session) -> Totals
    async def validate_session(session: Session) -> ValidationResult
    async def cancel_session(session_id: str) -> Session
```

**Session State Machine:**
```
pending → address_provided → payment_ready → completed
   ↓            ↓                 ↓              ↓
   └────────────┴─────────────────┴────────→ canceled
```

#### 3.3 Payment Service

**Responsibilities:**
- Stripe integration
- Payment tokenization
- Payment processing
- Payment status tracking

**API:**
```python
class PaymentService:
    async def tokenize_payment(card_details: dict) -> str
    async def create_payment_intent(amount: Decimal, token: str) -> PaymentIntent
    async def capture_payment(intent_id: str) -> PaymentResult
    async def refund_payment(charge_id: str, amount: Decimal) -> Refund
```

**Stripe Integration:**
- Test mode only for POC
- Shared Payment Token API
- Payment Intents API
- Webhook handling for async updates

#### 3.4 Shipping Service

**Responsibilities:**
- Calculate shipping options
- Delivery estimates
- Carrier selection

**API:**
```python
class ShippingService:
    async def calculate_options(address: Address, cart: Cart) -> list[ShippingOption]
    async def estimate_delivery(option: ShippingOption) -> DateRange
    async def validate_address(address: Address) -> AddressValidation
```

**Shipping Options (POC - Simplified):**
```python
STANDARD:  $5.00  (5-7 business days)
EXPRESS:   $15.00 (2-3 business days)
OVERNIGHT: $25.00 (1 business day)
```

#### 3.5 Order Service

**Responsibilities:**
- Order creation
- Order status tracking
- Order history
- Event publishing

**API:**
```python
class OrderService:
    async def create_order(session: Session, payment: Payment) -> Order
    async def get_order(order_id: str) -> Order
    async def update_order_status(order_id: str, status: str) -> Order
    async def publish_event(event: OrderEvent) -> None
```

**Order Lifecycle:**
```
created → confirmed → processing → shipped → delivered
    ↓          ↓            ↓          ↓         
    └──────────┴────────────┴──────────┴────→ canceled
```

#### 3.6 Inventory Service

**Responsibilities:**
- Stock checking
- Inventory reservation
- Availability tracking

**API:**
```python
class InventoryService:
    async def check_availability(product_id: str, quantity: int) -> bool
    async def reserve_inventory(items: list[CartItem]) -> Reservation
    async def release_reservation(reservation_id: str) -> None
    async def commit_reservation(reservation_id: str) -> None
```

---

### Layer 4: Data & Integration

#### 4.1 SQLite Database

**Schema:**

```sql
-- Products Table
CREATE TABLE products (
    id TEXT PRIMARY KEY,
    gtin TEXT UNIQUE NOT NULL,
    mpn TEXT,
    title TEXT NOT NULL,
    description TEXT,
    brand TEXT,
    category TEXT,
    price DECIMAL(10,2) NOT NULL,
    currency TEXT DEFAULT 'USD',
    images JSON,
    availability TEXT,
    variants JSON,
    metadata JSON,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Checkout Sessions Table
CREATE TABLE checkout_sessions (
    id TEXT PRIMARY KEY,
    status TEXT NOT NULL,
    currency TEXT DEFAULT 'USD',
    line_items JSON NOT NULL,
    fulfillment_address JSON,
    fulfillment_options JSON,
    selected_fulfillment_option_id TEXT,
    totals JSON,
    buyer_info JSON,
    payment_token_id TEXT,
    order_id TEXT,
    metadata JSON,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    expires_at TIMESTAMP
);

-- Orders Table
CREATE TABLE orders (
    id TEXT PRIMARY KEY,
    checkout_session_id TEXT REFERENCES checkout_sessions(id),
    status TEXT NOT NULL,
    line_items JSON NOT NULL,
    shipping_address JSON NOT NULL,
    shipping_option JSON NOT NULL,
    totals JSON NOT NULL,
    buyer_info JSON NOT NULL,
    payment_id TEXT NOT NULL,
    tracking_number TEXT,
    permalink TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Order Events Table
CREATE TABLE order_events (
    id TEXT PRIMARY KEY,
    order_id TEXT REFERENCES orders(id),
    event_type TEXT NOT NULL,
    event_data JSON,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Indexes
CREATE INDEX idx_sessions_status ON checkout_sessions(status);
CREATE INDEX idx_orders_checkout_session ON orders(checkout_session_id);
CREATE INDEX idx_order_events_order_id ON order_events(order_id);
CREATE INDEX idx_products_gtin ON products(gtin);
```

#### 4.2 Stripe Integration

**Configuration:**
- Test Mode API Keys
- Shared Payment Token enabled
- Webhook endpoint configured

**Payment Flow:**
```
1. ChatGPT → Delegate Payment → Payment Service
2. Payment Service → Stripe: Create PaymentMethod from card details
3. Stripe → Payment Service: Returns payment_token_id
4. ChatGPT → Complete Checkout with payment_token_id
5. Gateway → Payment Service: Create PaymentIntent
6. Payment Service → Stripe: Confirm PaymentIntent
7. Stripe → Payment Service: Payment successful
8. Gateway → Order Service: Create order
```

---

## Data Flow

### End-to-End Purchase Flow

```
1. Product Discovery
   User: "I want Nike Air Max shoes"
   ↓
   ChatGPT Simulator → MCP Tool: search_products(query="Nike Air Max")
   ↓
   MCP Server → Gateway → Product Service
   ↓
   Product Service → Database: Query products
   ↓
   Return: List of matching products

2. Add to Cart
   User: "Add size 10 to cart"
   ↓
   ChatGPT Simulator → MCP Tool: create_checkout(items=[{gtin, qty}])
   ↓
   MCP Server → Gateway (ACP Handler) → Checkout Service
   ↓
   Checkout Service:
     - Validate product exists (Product Service)
     - Check inventory (Inventory Service)
     - Calculate pricing
     - Create session
   ↓
   Return: Session with status="pending"

3. Add Shipping Address
   User: "Ship to 123 Main St, New York, NY"
   ↓
   ChatGPT Simulator → MCP Tool: update_checkout(session_id, address={...})
   ↓
   Gateway → Checkout Service
   ↓
   Checkout Service:
     - Validate address (Shipping Service)
     - Calculate shipping options (Shipping Service)
     - Calculate tax (8% flat rate for POC)
     - Update session status to "ready"
   ↓
   Return: Session with shipping options and totals

4. Select Shipping & Payment
   User: "Use standard shipping, pay with card 4242..."
   ↓
   ChatGPT Simulator → MCP Tool: complete_purchase(payment={...})
   ↓
   Gateway → Payment Service: tokenize_payment()
   ↓
   Payment Service → Stripe: Create PaymentMethod
   ↓
   Stripe → Payment Service: Returns payment_token_id
   ↓
   Gateway → Checkout Service: Update session with payment token
   ↓
   Gateway → Payment Service: Create and confirm PaymentIntent
   ↓
   Payment Service → Stripe: Charge card
   ↓
   Stripe → Payment Service: Payment successful
   ↓
   Gateway → Order Service: Create order
   ↓
   Order Service:
     - Create order record
     - Publish order.created event
     - Reserve inventory (Inventory Service)
   ↓
   Return: Order confirmation with order_id

5. Order Tracking
   User: "Check my order status"
   ↓
   ChatGPT Simulator → MCP Tool: check_order_status(order_id)
   ↓
   Gateway → Order Service: get_order()
   ↓
   Return: Order details with current status
```

---

## API Examples

### Complete Request/Response Examples

#### 1. Create Checkout Session

**Request:**
```http
POST /acp/v1/checkout_sessions
Content-Type: application/json

{
  "line_items": [
    {
      "gtin": "00883419552502",
      "quantity": 1
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
```

**Response:**
```http
HTTP/1.1 200 OK
Content-Type: application/json

{
  "id": "cs_1234567890abcdef",
  "status": "ready_for_payment",
  "currency": "USD",
  "line_items": [
    {
      "gtin": "00883419552502",
      "quantity": 1,
      "title": "Nike Air Max 90",
      "unit_amount": {
        "value": "120.00",
        "currency": "USD"
      },
      "total_amount": {
        "value": "120.00",
        "currency": "USD"
      },
      "image_url": "https://static.nike.com/a/images/c_limit,w_592,f_auto/t_product_v1/abc123.jpg"
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
  "fulfillment_options": [
    {
      "id": "standard",
      "title": "Standard Shipping",
      "subtitle": "5-7 business days",
      "cost": {
        "value": "5.00",
        "currency": "USD"
      }
    },
    {
      "id": "express",
      "title": "Express Shipping",
      "subtitle": "2-3 business days",
      "cost": {
        "value": "15.00",
        "currency": "USD"
      }
    }
  ],
  "selected_fulfillment_option_id": "standard",
  "totals": {
    "items_total": {
      "value": "120.00",
      "currency": "USD"
    },
    "discounts": {
      "value": "0.00",
      "currency": "USD"
    },
    "subtotal": {
      "value": "120.00",
      "currency": "USD"
    },
    "fulfillment": {
      "value": "5.00",
      "currency": "USD"
    },
    "taxes": {
      "value": "10.00",
      "currency": "USD"
    },
    "fees": {
      "value": "0.00",
      "currency": "USD"
    },
    "total": {
      "value": "135.00",
      "currency": "USD"
    }
  },
  "buyer_info": {
    "first_name": "John",
    "last_name": "Doe",
    "email": "john.doe@example.com",
    "phone": "+12125551234"
  },
  "links": {
    "terms_of_service": "https://www.nike.com/us/terms",
    "privacy_policy": "https://www.nike.com/us/privacy"
  },
  "created_at": "2025-10-19T10:30:00Z",
  "updated_at": "2025-10-19T10:30:00Z"
}
```

#### 2. Complete Checkout (After Payment)

**Request:**
```http
POST /acp/v1/checkout_sessions/cs_1234567890abcdef/complete
Content-Type: application/json

{
  "payment_token_id": "pm_1234567890abcdef"
}
```

**Response:**
```http
HTTP/1.1 200 OK
Content-Type: application/json

{
  "id": "cs_1234567890abcdef",
  "status": "completed",
  "order": {
    "id": "order_9876543210fedcba",
    "checkout_session_id": "cs_1234567890abcdef",
    "permalink": "https://nike.com/orders/9876543210fedcba",
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

#### 3. Error Response Example

**Response (Out of Stock):**
```http
HTTP/1.1 400 Bad Request
Content-Type: application/json

{
  "error": {
    "code": "out_of_stock",
    "message": "The requested item is currently out of stock",
    "details": {
      "gtin": "00883419552502",
      "available_quantity": 0
    }
  }
}
```

### MCP Tool Invocation Example

**Tool Discovery Request:**
```json
{
  "jsonrpc": "2.0",
  "id": 1,
  "method": "tools/list"
}
```

**Tool Discovery Response:**
```json
{
  "jsonrpc": "2.0",
  "id": 1,
  "result": {
    "tools": [
      {
        "name": "search_products",
        "description": "Search Nike products by keywords, category, or filters",
        "inputSchema": {
          "type": "object",
          "properties": {
            "query": {
              "type": "string",
              "description": "Search keywords (e.g., 'Air Max', 'running shoes')"
            },
            "category": {
              "type": "string",
              "enum": ["shoes", "apparel", "equipment"],
              "description": "Product category filter"
            },
            "price_max": {
              "type": "number",
              "description": "Maximum price filter"
            }
          },
          "required": ["query"]
        }
      },
      {
        "name": "create_checkout",
        "description": "Create a checkout session with products in the cart",
        "inputSchema": {
          "type": "object",
          "properties": {
            "items": {
              "type": "array",
              "items": {
                "type": "object",
                "properties": {
                  "gtin": {"type": "string"},
                  "quantity": {"type": "number"}
                }
              }
            },
            "address": {
              "type": "object",
              "properties": {
                "street": {"type": "string"},
                "city": {"type": "string"},
                "state": {"type": "string"},
                "zip": {"type": "string"}
              }
            }
          },
          "required": ["items"]
        }
      }
    ]
  }
}
```

**Tool Invocation Request:**
```json
{
  "jsonrpc": "2.0",
  "id": 2,
  "method": "tools/call",
  "params": {
    "name": "search_products",
    "arguments": {
      "query": "Nike Air Max",
      "category": "shoes",
      "price_max": 200
    }
  }
}
```

**Tool Invocation Response:**
```json
{
  "jsonrpc": "2.0",
  "id": 2,
  "result": {
    "content": [
      {
        "type": "text",
        "text": "Found 5 Nike Air Max shoes:\n\n1. Nike Air Max 90 - $120\n2. Nike Air Max 270 - $150\n3. Nike Air Max 97 - $175\n..."
      },
      {
        "type": "resource",
        "resource": {
          "uri": "nike://products",
          "mimeType": "application/json",
          "text": "{\"products\": [{\"gtin\": \"00883419552502\", \"title\": \"Nike Air Max 90\", ...}]}"
        }
      }
    ]
  }
}
```

---

## Security & Privacy

### Data Privacy Considerations

#### PII Handling

**Personal Identifiable Information (PII) in System:**
- Customer name
- Email address
- Phone number
- Shipping address
- Payment information (handled by Stripe, not stored)

**POC Security Measures:**
```python
# PII Logging Prevention
class PIIFilter(logging.Filter):
    """Filter to prevent PII from being logged"""
    PII_PATTERNS = [
        r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b',  # Email
        r'\b\d{3}[-.]?\d{3}[-.]?\d{4}\b',  # Phone
        r'\b\d{4}[- ]?\d{4}[- ]?\d{4}[- ]?\d{4}\b',  # Credit card
    ]
    
    def filter(self, record):
        for pattern in self.PII_PATTERNS:
            record.msg = re.sub(pattern, '[REDACTED]', str(record.msg))
        return True
```

**Production Requirements:**
- Encrypt PII at rest (AES-256)
- Encrypt PII in transit (TLS 1.3)
- PII access logging and auditing
- Data retention policies (delete after 90 days)
- GDPR/CCPA compliance for EU/CA customers

#### Payment Security

**POC Approach:**
```
Customer Card Details
         ↓
   Delegate Payment Endpoint
         ↓
   Stripe Tokenization (PCI-compliant)
         ↓
   Return Token ID (not card details)
         ↓
   Use Token for Payment
```

**Security Measures:**
- Never log card details
- Never store card details (even tokenized)
- Stripe handles PCI compliance
- Token expires after successful charge

**Production Requirements (Nike Specific):**
- PCI DSS Level 1 compliance
- Network segmentation (PCI zone isolated)
- HSM for key management
- Quarterly security audits
- Penetration testing

### Authentication & Authorization

**POC Implementation:**
```python
# Simple API Key Authentication
@app.middleware("http")
async def verify_api_key(request: Request, call_next):
    api_key = request.headers.get("X-API-Key")
    if api_key != settings.EXPECTED_API_KEY:
        return JSONResponse(
            status_code=401,
            content={"error": "Invalid API key"}
        )
    return await call_next(request)
```

**Production Requirements:**
- OAuth 2.0 with JWT tokens
- mTLS for service-to-service auth
- API key rotation every 90 days
- Rate limiting per client (1000 req/hour)
- IP allowlisting for known agents

### Data Retention

**POC:**
- Checkout sessions: 24 hours (TTL in database)
- Orders: Retained indefinitely (for demo purposes)
- Logs: 7 days

**Production:**
- Checkout sessions: 24 hours (auto-deleted)
- Orders: 7 years (compliance requirement)
- Order events: 2 years
- Logs: 90 days (PII scrubbed after 7 days)

### Vulnerability Prevention

**SQL Injection Prevention:**
```python
# Use parameterized queries (SQLAlchemy ORM)
# BAD: f"SELECT * FROM products WHERE id = '{product_id}'"
# GOOD:
session.query(Product).filter(Product.id == product_id).first()
```

**XSS Prevention:**
```python
# Sanitize all user inputs
from bleach import clean

def sanitize_input(text: str) -> str:
    return clean(text, tags=[], strip=True)
```

**Rate Limiting:**
```python
from slowapi import Limiter

limiter = Limiter(key_func=get_remote_address)

@app.post("/checkout_sessions")
@limiter.limit("10/minute")
async def create_checkout_session():
    ...
```

---

## Technology Stack

### Backend
- **Language:** Python 3.11+
- **Framework:** FastAPI 0.104+
- **Database:** SQLite 3
- **ORM:** SQLAlchemy 2.0
- **Validation:** Pydantic 2.0
- **HTTP Client:** httpx
- **Testing:** pytest

### Frontend (Simulator)
- **Framework:** React 18
- **Build Tool:** Vite
- **Styling:** TailwindCSS
- **State Management:** Zustand
- **API Client:** Axios
- **UI Components:** shadcn/ui

### External Services
- **Payment Processing:** Stripe (Test Mode)
- **Product Data:** Scraped from nike.com

### Development Tools
- **API Server:** Uvicorn
- **Code Quality:** Black, isort, pylint
- **API Documentation:** Swagger/OpenAPI
- **Version Control:** Git

---

## Design Principles

### 1. Separation of Concerns
- **MCP Layer:** AI interface (tool discovery)
- **Gateway Layer:** Protocol translation
- **Service Layer:** Business logic
- **Data Layer:** Persistence

### 2. Protocol Agnostic Core
Internal services have zero knowledge of external protocols (ACP, MCP, etc.).

### 3. Single Responsibility
Each service owns one domain:
- Product Service → Product catalog
- Checkout Service → Cart and sessions
- Payment Service → Payments
- Shipping Service → Shipping
- Order Service → Orders

### 4. Fail Fast
Validate at gateway boundary, propagate errors clearly.

### 5. Explicit Over Implicit
- Explicit error codes
- Explicit data transformations
- Explicit state transitions

### 6. Testability
- Each layer independently testable
- Mock boundaries between layers
- Integration tests at gateway level

### 7. Extensibility
- Easy to add new protocols (new gateway handler)
- Easy to add new tools (MCP tool registration)
- Easy to swap implementations (Stripe → Adyen)

---

## Future Evolution

### Phase 1: POC (Current)
- Single protocol (ACP)
- Local deployment
- Simplified business logic

### Phase 2: Multi-Protocol
- Add Google Shopping handler
- Add Meta Commerce handler
- Protocol version management

### Phase 3: Production Hardening
- Kubernetes deployment
- Multi-region support
- Advanced security (mTLS, HSM)
- Observability (OpenTelemetry)

### Phase 4: Nike Integration
- CPA integration for products
- Digital Rollup for GTIN mapping
- Nike commerce services
- PCI-compliant payment handling

---

## Appendix

### Key OpenAI ACP Specifications
- Agentic Checkout Spec: https://developers.openai.com/commerce/specs/checkout
- Product Feed Spec: https://developers.openai.com/commerce/specs/feed
- Delegated Payment Spec: https://developers.openai.com/commerce/specs/payment

### Reference Documentation
- MCP Protocol: https://modelcontextprotocol.io
- Stripe Agentic Commerce: https://docs.stripe.com/agentic-commerce
- ACP GitHub: https://github.com/agentic-commerce-protocol/agentic-commerce-protocol

---

## Troubleshooting

### Common Issues & Solutions

#### Issue: "Product not found" errors

**Symptoms:**
- API returns 404 for valid GTINs
- Product search returns empty results

**Causes:**
1. Product scraper didn't complete
2. GTIN mismatch in database
3. Database not initialized

**Solutions:**
```bash
# 1. Check if products table has data
sqlite3 data/checkout.db "SELECT COUNT(*) FROM products;"

# 2. Re-run product scraper
python scripts/scrape_nike_products.py

# 3. Verify GTIN format (should be 8-14 digits)
sqlite3 data/checkout.db "SELECT id, gtin, title FROM products LIMIT 5;"
```

---

#### Issue: Stripe payment failures

**Symptoms:**
- Payment returns "payment_declined" error
- "Invalid API key" errors

**Causes:**
1. Wrong Stripe API keys
2. Test mode not enabled
3. Invalid card number format

**Solutions:**
```bash
# 1. Verify Stripe keys in .env
cat .env | grep STRIPE

# 2. Test with Stripe test cards
# Success: 4242 4242 4242 4242
# Decline: 4000 0000 0000 0002

# 3. Check Stripe dashboard
# https://dashboard.stripe.com/test/payments
```

---

#### Issue: Session expires before completion

**Symptoms:**
- "Session not found" errors during checkout
- Session status stuck at "pending"

**Causes:**
1. Session TTL expired (24 hours)
2. Session not properly saved to database
3. Session ID mismatch

**Solutions:**
```python
# 1. Check session expiration
from datetime import datetime, timedelta

session = db.query(CheckoutSession).filter_by(id=session_id).first()
if session.expires_at < datetime.utcnow():
    print("Session expired!")

# 2. Increase TTL for testing
session.expires_at = datetime.utcnow() + timedelta(hours=48)
db.commit()
```

---

#### Issue: CORS errors in ChatGPT simulator

**Symptoms:**
- Browser console shows CORS errors
- API calls fail from frontend

**Causes:**
1. CORS middleware not configured
2. Wrong origin in CORS config

**Solutions:**
```python
# Add CORS middleware to FastAPI
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # Vite default port
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

---

#### Issue: MCP tools not discoverable

**Symptoms:**
- ChatGPT simulator can't find tools
- Tool list returns empty array

**Causes:**
1. MCP server not running
2. Tools not registered properly
3. JSON-RPC format incorrect

**Solutions:**
```python
# 1. Verify MCP server is running
curl -X POST http://localhost:8000/mcp \
  -H "Content-Type: application/json" \
  -d '{"jsonrpc": "2.0", "id": 1, "method": "tools/list"}'

# 2. Check tool registration
from app.mcp.server import mcp_server
print(mcp_server.list_tools())

# 3. Verify JSON-RPC response format
# Must have: jsonrpc, id, result fields
```

---

### Performance Troubleshooting

#### Slow API response times

**Diagnostic:**
```python
# Add timing middleware
import time
from fastapi import Request

@app.middleware("http")
async def log_requests(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    response.headers["X-Process-Time"] = str(process_time)
    print(f"{request.method} {request.url.path} - {process_time:.2f}s")
    return response
```

**Common Slow Points:**
1. Product search (add database index on `title`, `gtin`)
2. Stripe API calls (use async, add timeout)
3. Large product feed (paginate results)

---

### Debugging Tips

**Enable verbose logging:**
```python
# In config.py
import logging

logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
```

**Test individual services:**
```python
# Test product service directly
from app.services.product_service import ProductService

service = ProductService()
products = await service.search("Air Max")
print(f"Found {len(products)} products")
```

**Database inspection:**
```bash
# Connect to SQLite
sqlite3 data/checkout.db

# Useful queries
.tables
.schema checkout_sessions
SELECT * FROM checkout_sessions ORDER BY created_at DESC LIMIT 5;
```

---

## Glossary

### Acronyms

| Term | Full Name | Description |
|------|-----------|-------------|
| **ACP** | Agentic Commerce Protocol | OpenAI's open standard for AI agent commerce |
| **MCP** | Model Context Protocol | Standard for AI agents to discover and invoke tools |
| **GTIN** | Global Trade Item Number | Universal product identifier (8-14 digits) |
| **SKU** | Stock Keeping Unit | Nike's internal product identifier |
| **MPN** | Manufacturer Part Number | Nike's product code (styleCode + colorCode) |
| **PSP** | Payment Service Provider | Company that processes payments (e.g., Stripe) |
| **PII** | Personal Identifiable Information | Data that can identify individuals |
| **PCI DSS** | Payment Card Industry Data Security Standard | Security standard for card processing |
| **TTL** | Time To Live | Duration before data expires |
| **REST** | Representational State Transfer | Web API architectural style |
| **JSON** | JavaScript Object Notation | Data interchange format |
| **HTTP** | Hypertext Transfer Protocol | Web communication protocol |
| **TLS** | Transport Layer Security | Encryption protocol for secure connections |
| **OAuth** | Open Authorization | Authorization framework |
| **JWT** | JSON Web Token | Authentication token format |
| **CORS** | Cross-Origin Resource Sharing | Browser security mechanism |
| **SQL** | Structured Query Language | Database query language |
| **ORM** | Object-Relational Mapping | Database abstraction (e.g., SQLAlchemy) |
| **API** | Application Programming Interface | Interface for software communication |
| **SDK** | Software Development Kit | Pre-built library for integration |
| **POC** | Proof of Concept | Prototype to validate feasibility |

### Key Terms

**Agentic Commerce**
Commerce transactions initiated and managed by AI agents (like ChatGPT) on behalf of users.

**Checkout Session**
A temporary state object that holds cart items, shipping address, and pricing calculations during the purchase process. Expires after 24 hours.

**Delegate Payment**
Process where the merchant receives payment credentials from the AI agent (not the user directly), tokenizes them via a PSP, and returns a token for later charging.

**Gateway Pattern**
Architectural pattern that translates between external protocols (ACP, Google Shopping) and internal business logic, enabling protocol-agnostic core services.

**Product Feed**
Structured file (JSON/CSV) containing merchant's product catalog with all required attributes (GTIN, title, price, availability, etc.) for AI agent discovery.

**Protocol Translation**
Converting data and operations from one protocol format (e.g., ACP) to another (internal format), handling schema differences and error code mapping.

**Shared Payment Token**
Stripe's implementation of delegated payment where payment credentials are tokenized and can be used across multiple parties (OpenAI, merchant).

**Tool Discovery**
MCP feature where AI agents can dynamically query what tools/operations are available, removing need for hardcoded API knowledge.

### OpenAI ACP Specific Terms

**enable_search**
Product feed attribute (boolean) indicating if product should be searchable by AI agents.

**enable_checkout**
Product feed attribute (boolean) indicating if product can be purchased through AI agents.

**fulfillment_address**
ACP term for shipping/delivery address (not "shipping_address").

**fulfillment_options**
ACP term for available shipping methods with costs and delivery estimates.

**line_items**
ACP term for products in cart (not "cart_items" or "products").

**ready_for_payment** / **not_ready_for_payment**
ACP checkout session statuses indicating if all required info is collected.

### Nike Specific Terms

**CPA** (Consumer Product API)
Nike's internal API for product catalog data.

**Digital Rollup**
Nike service that maps between GTINs and internal Nike product identifiers (Merch ID, SKU ID).

**styleCode** / **colorCode**
Components of Nike's product identification system. Combined they form the MPN.

**A-Grade** / **B-Grade**
Nike inventory classifications. A-Grade is first quality, B-Grade is factory seconds (excluded from ACP feed).

### Stripe Terms

**PaymentIntent**
Stripe object representing an intent to collect payment, tracking the payment through its lifecycle.

**PaymentMethod**
Stripe object representing payment credentials (card, bank account, etc.).

**Test Mode**
Stripe environment where no real money is charged, used for development and testing.

**Webhook**
HTTP callback from Stripe to merchant when payment events occur (success, failure, etc.).

---

## Quick Reference Cards

### POC vs. Production Comparison

| Feature | POC | Production |
|---------|-----|------------|
| **Database** | SQLite (local file) | PostgreSQL (managed) |
| **Deployment** | Local (laptop) | Kubernetes (multi-region) |
| **Authentication** | Simple API key | OAuth 2.0 + mTLS |
| **Products** | 25 (scraped) | Full catalog via CPA |
| **Payment** | Stripe test mode | Stripe production + fraud detection |
| **Monitoring** | Console logs | OpenTelemetry + dashboards |
| **Security** | Basic PII filtering | Full PCI DSS compliance |
| **Scale** | 10 req/sec | 1000+ req/sec |
| **Availability** | Best effort | 99.9% SLA |

### API Quick Reference

```
# Product Operations
GET /api/v1/products              # Search products
GET /api/v1/products/{id}         # Get product details
GET /acp/v1/product-feed.json     # ACP product feed

# Checkout Operations (ACP)
POST /acp/v1/checkout_sessions                 # Create session
POST /acp/v1/checkout_sessions/{id}            # Update session
POST /acp/v1/checkout_sessions/{id}/complete   # Complete purchase
POST /acp/v1/checkout_sessions/{id}/cancel     # Cancel session
GET  /acp/v1/checkout_sessions/{id}            # Get session

# Payment Operations
POST /acp/v1/delegate_payment     # Tokenize payment

# MCP Operations
POST /mcp                         # JSON-RPC endpoint
  - methods: tools/list, tools/call
```

### HTTP Status Codes

```
200 OK                    # Success
201 Created               # Resource created (order)
400 Bad Request           # Invalid input
401 Unauthorized          # Invalid API key
404 Not Found             # Resource doesn't exist
409 Conflict              # State conflict (e.g., session already completed)
429 Too Many Requests     # Rate limit exceeded
500 Internal Server Error # Server error
```

### ACP Error Codes

```
missing          # Required field not provided
invalid          # Malformed data or invalid value
out_of_stock     # Product unavailable
payment_declined # Payment processing failed
requires_sign_in # Authentication required
requires_3ds     # 3D Secure verification needed
```

---

**End of Architecture Document**

