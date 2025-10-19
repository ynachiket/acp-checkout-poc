# Architectural Decision Log

**Project:** Nike Agentic Commerce POC  
**Date Started:** October 19, 2025  
**Status:** Active Development

---

## Overview

This document records all significant architectural decisions made during the design and implementation of Nike's Agentic Commerce POC. Each decision includes context, options considered, rationale, and consequences.

---

## Decision Index

1. [POC Scope and Approach](#decision-1-poc-scope-and-approach)
2. [Technology Stack Selection](#decision-2-technology-stack-selection)
3. [Architectural Pattern: Gateway vs. Monolithic](#decision-3-architectural-pattern-gateway-vs-monolithic)
4. [MCP Server Integration](#decision-4-mcp-server-integration)
5. [Payment Integration Strategy](#decision-5-payment-integration-strategy)
6. [Product Data Source](#decision-6-product-data-source)
7. [Deployment Strategy](#decision-7-deployment-strategy)
8. [Database Selection](#decision-8-database-selection)

---

## Decision 1: POC Scope and Approach

**Date:** October 19, 2025  
**Status:** ✅ Accepted  
**Deciders:** Architecture Team, Stakeholders

### Context

Need to demonstrate Nike's integration with OpenAI's Agentic Commerce Protocol (ACP) for Instant Checkout in ChatGPT. Must balance speed of POC delivery with architectural quality that can inform production decisions.

### Options Considered

#### Option A: Quick Prototype
- Single Python script
- Hardcoded data
- Mock all external services
- 2-3 days delivery

**Pros:**
- Fastest to deliver
- Minimal complexity

**Cons:**
- Throwaway code
- No production insights
- Doesn't demonstrate scalability

#### Option B: Production-Ready Implementation
- Full Nike service integration (CPA, Digital Rollup, etc.)
- Kubernetes deployment
- Multi-region support
- 3-4 months delivery

**Pros:**
- Production-ready immediately
- No refactoring needed

**Cons:**
- Too slow for POC
- High complexity
- Requires extensive Nike integration work

#### Option C: Simplified Production-Like Architecture ✅ SELECTED
- Clean architectural layers
- Real integrations (Stripe) in test mode
- Local deployment
- Production patterns, POC scope
- 1-2 weeks delivery

**Pros:**
- Demonstrates best practices
- Informs production decisions
- Real payment flow
- Extensible architecture

**Cons:**
- Slightly longer than quick prototype
- More upfront design needed

### Decision

**Selected Option C** - Build simplified POC with production-ready architecture patterns.

### Rationale

- POC should demonstrate **how** Nike would integrate, not just **if** it works
- Architecture patterns (gateway, layering) will be needed in production
- Stakeholders need confidence in scalability path
- 1-2 week timeline still acceptable for POC
- Real Stripe integration provides concrete learning

### Consequences

**Positive:**
- POC code can evolve to production (not throwaway)
- Clear path to add Nike's internal services
- Easy to extend with new protocols
- Demonstrates technical sophistication

**Negative:**
- Requires more upfront design
- Slightly longer delivery timeline
- May be over-engineered for pure POC

### Related Decisions
- Decision 3: Gateway Pattern
- Decision 4: MCP Integration

---

## Decision 2: Technology Stack Selection

**Date:** October 19, 2025  
**Status:** ✅ Accepted  
**Deciders:** Engineering Team

### Context

Need to select backend and frontend technologies that enable rapid POC development while aligning with potential production requirements.

### Options Considered

#### Backend Options

**Option A: Node.js + Express**
- Pros: Fast development, large ecosystem, good for REST APIs
- Cons: Less structured than Python, not team preference

**Option B: Python + FastAPI** ✅ SELECTED
- Pros: Team preference, excellent API docs (OpenAPI), Pydantic validation, async support
- Cons: None significant for POC

**Option C: Go**
- Pros: High performance, strong typing
- Cons: Longer development time, unfamiliar to team

#### Frontend Options

**Option A: React + Vite** ✅ SELECTED
- Pros: Fast development, modern tooling, component reusability
- Cons: None significant

**Option B: Vue.js**
- Pros: Simpler learning curve
- Cons: Less team familiarity

**Option C: Plain HTML/JS**
- Pros: Simplest
- Cons: Poor development experience, limited reusability

### Decision

**Backend:** Python 3.11+ with FastAPI  
**Frontend:** React 18 with Vite  
**Database:** SQLite (POC simplicity)  
**External Services:** Stripe (test mode)

### Rationale

- **Python/FastAPI:** Team expertise, excellent API documentation, strong typing with Pydantic
- **React/Vite:** Modern, fast dev server, component-based for simulator UI
- **SQLite:** Zero setup, file-based, sufficient for POC, easy migration to PostgreSQL
- **Stripe:** Industry-leading, excellent docs, test mode support

### Consequences

**Positive:**
- Rapid development with familiar tools
- Strong typing and validation (Pydantic)
- Auto-generated API documentation
- Easy to containerize for future deployment

**Negative:**
- SQLite has limitations (no concurrent writes, but acceptable for POC)
- Python GIL may limit concurrency (not a concern for POC scale)

---

## Decision 3: Architectural Pattern: Gateway vs. Monolithic

**Date:** October 19, 2025  
**Status:** ✅ Accepted  
**Deciders:** Architecture Team

### Context

Must decide whether to build ACP integration directly into a monolithic service or create a gateway layer that translates between protocols and internal services.

This is a **critical decision** that impacts extensibility, maintainability, and future protocol support.

### Options Considered

#### Option A: Direct/Monolithic FastAPI Backend

```
ChatGPT → [FastAPI with ACP endpoints] → SQLite + Stripe
```

**Pros:**
- Simpler to build initially
- Fewer abstractions
- Single codebase
- Faster POC delivery (by ~1 day)

**Cons:**
- ACP protocol tightly coupled to business logic
- Hard to add new protocols (Google Shopping, Meta Commerce)
- Protocol changes require touching business logic
- Not reflective of enterprise architecture
- When ACP spec changes, must update business logic
- Cannot reuse services for web/mobile/other channels

#### Option B: Gateway Pattern with Protocol Translation ✅ SELECTED

```
ChatGPT → [ACP Gateway] → [Internal Services] → SQLite + Stripe
              ↓                    ↓
        Protocol Layer     Business Logic Layer
```

**Pros:**
- Protocol-agnostic core business logic
- Easy to add new protocols (new gateway handler)
- Protocol changes only affect translator
- Clean separation of concerns
- Services reusable across channels
- Aligns with Nike enterprise architecture
- Production-ready pattern

**Cons:**
- More complex (but manageable)
- Additional abstraction layer
- Slightly longer POC development (~1 extra day)

#### Option C: Microservices Architecture

```
ChatGPT → [API Gateway] → [Product Service]
                       → [Checkout Service]
                       → [Payment Service]
```

**Pros:**
- Maximum decoupling
- Independent scaling
- Technology diversity

**Cons:**
- Over-engineered for POC
- Deployment complexity
- Network latency between services
- 2-3 weeks additional effort

### Decision

**Selected Option B** - Gateway pattern with protocol translation layer.

### Rationale

**Why NOT Monolithic (Option A):**
1. **Multiple Protocols Coming:** Google Shopping Actions, Meta Commerce, Amazon Buy with Prime all emerging
2. **Nike's Guidance:** Enterprise architecture document explicitly recommends gateway pattern
3. **When (not if) ACP changes:** Will need to modify everywhere in monolithic approach
4. **Future requirement:** Same services need to support web, mobile, native apps

**Why Gateway Pattern (Option B):**
1. **Extensibility:** Adding Google Shopping = 1-2 days (new gateway), not 5-7 days (rewrite)
2. **Maintainability:** Protocol changes contained to translator layer
3. **Testing:** Can test services without protocol knowledge
4. **Production-ready:** This is how enterprise systems are built
5. **Cost:** Only +1 day for POC, saves weeks/months later

**Why NOT Microservices (Option C):**
- Over-engineered for POC scale
- Adds deployment complexity without benefit at POC scale
- Can evolve gateway pattern to microservices later if needed

### Consequences

**Positive:**
- Can add Google Shopping protocol in 1-2 days vs. weeks
- Services reusable for Nike.com, Nike app, etc.
- Protocol spec changes don't ripple through codebase
- Better POC demo (shows architectural maturity)
- Clear evolution path to production

**Negative:**
- ~1 extra day for POC development
- More folders/files to manage
- Need to maintain protocol translators

**Mitigation:**
- Keep both layers in single FastAPI app (not separate deployments)
- Clear folder structure makes navigation easy
- Translator logic is straightforward mapping code

### Validation

This decision aligns with:
- Nike's internal architecture guidance
- Industry best practices (API Gateway pattern)
- Upcoming multi-protocol commerce landscape
- Production scalability requirements

### Related Decisions
- Decision 1: POC Scope (informed this decision)
- Decision 4: MCP Integration (builds on this decision)

---

## Decision 4: MCP Server Integration

**Date:** October 19, 2025  
**Status:** ✅ Accepted  
**Deciders:** Architecture Team

### Context

The gateway pattern (Decision 3) is accepted. Now must decide whether to add an MCP (Model Context Protocol) server layer on top of the ACP gateway, or expose ACP directly via REST API.

### Background: What is MCP?

Model Context Protocol (MCP) is a standard for AI agents to discover and invoke tools dynamically. Instead of hardcoding API endpoints, AI agents can:
1. **Discover** available tools
2. **Understand** tool schemas and descriptions
3. **Invoke** tools with type-safe parameters

### Options Considered

#### Option A: ACP Gateway Only (REST API)

```
ChatGPT → [REST API: ACP endpoints] → Gateway → Services
```

**Pros:**
- Simpler implementation
- One less abstraction layer
- Follows OpenAI's ACP spec exactly
- Faster POC delivery (~1 day faster)

**Cons:**
- AI agents need hardcoded knowledge of your API
- No dynamic tool discovery
- Less aligned with modern AI agent architecture
- ChatGPT/Claude need different integration approaches

#### Option B: MCP Server + ACP Gateway ✅ SELECTED

```
ChatGPT → [MCP Protocol] → MCP Server → ACP Gateway → Services
              ↓                ↓              ↓
      Tool Discovery    Tool Invocation   Protocol Translation
```

**Pros:**
- Dynamic tool discovery for AI agents
- Industry standard for AI integration
- Better AI agent experience (natural tool use)
- Multi-agent support (ChatGPT, Claude, custom agents)
- Future-proof as MCP adoption grows
- Aligns with how modern AI systems work

**Cons:**
- Additional layer of abstraction
- ~1-2 days extra POC development
- MCP implementation learning curve

#### Option C: Direct MCP (Skip ACP Gateway)

```
ChatGPT → [MCP Protocol] → MCP Server → Services (no ACP layer)
```

**Pros:**
- One less layer
- Simpler architecture

**Cons:**
- Loses protocol translation benefits
- Can't add other commerce protocols easily
- MCP and business logic mixed

### Decision

**Selected Option B** - Implement MCP Server layer on top of ACP Gateway.

### Rationale

**Industry Trends:**
- MCP is becoming standard for AI tool integration
- Anthropic (Claude) uses MCP natively
- OpenAI moving toward tool-based interactions
- Agent ecosystems standardizing on MCP

**Technical Benefits:**
1. **Dynamic Discovery:**
   ```python
   # Without MCP: ChatGPT must know
   POST /checkout_sessions with this exact JSON...
   
   # With MCP: ChatGPT discovers
   tools = discover_tools()
   # Returns: ["search_products", "create_checkout", ...]
   ```

2. **Better AI Experience:**
   - AI doesn't need API documentation
   - Natural tool invocation
   - Type-safe parameters
   - Clear tool descriptions

3. **Multi-Agent Support:**
   - ChatGPT, Claude, Gemini can all use same interface
   - Custom AI agents integrate easily
   - No per-agent customization needed

4. **Future-Proof:**
   ```
   Today:    MCP → ACP Gateway → Services
   Q2 2026:  MCP → [ACP, Google, Meta] Gateways → Services
   
   AI agents use same MCP interface regardless of protocols underneath
   ```

**Cost-Benefit:**
- Additional effort: ~1-2 days
- Benefit: Industry-standard AI integration
- Better demo: Shows understanding of modern AI architecture
- Production value: This is how AI agents will integrate

### Consequences

**Positive:**
- AI agents discover tools dynamically
- Same interface works for ChatGPT, Claude, custom agents
- Clear separation: MCP (AI interface) vs. ACP (commerce protocol)
- Demonstrates deep understanding of AI integration
- Production-ready approach

**Negative:**
- One more abstraction layer
- MCP spec to learn and implement
- Slightly more complex POC

**Mitigation:**
- MCP layer is thin wrapper over gateway
- Clear separation of concerns
- Well-documented protocol

### Implementation Details

**MCP Tools to Expose:**
```python
1. search_products(query, category, filters)
2. get_product_details(gtin)
3. create_checkout(items, address?)
4. update_checkout(session_id, updates)
5. complete_purchase(session_id, payment)
6. check_order_status(order_id)
```

**Architecture:**
```python
backend/
├── app/
│   ├── mcp/              # MCP Server Layer
│   │   ├── server.py     # MCP protocol handler
│   │   ├── tools.py      # Tool definitions
│   │   └── handlers.py   # Tool invocation handlers
│   ├── gateway/          # Protocol Gateway Layer
│   │   └── acp/          # ACP protocol handler
│   └── services/         # Business Logic Layer
```

### Related Decisions
- Decision 3: Gateway Pattern (foundation for this decision)
- Decision 1: POC Scope (informed by production readiness)

### References
- MCP Specification: https://modelcontextprotocol.io
- OpenAI Tool Use: https://platform.openai.com/docs/guides/function-calling
- Industry article: https://agenticcommerce.com

---

## Decision 5: Payment Integration Strategy

**Date:** October 19, 2025  
**Status:** ✅ Accepted  
**Deciders:** Engineering Team

### Context

Need to implement payment processing for the POC. Must decide between real payment integration (test mode) vs. mocked payment flow.

### Options Considered

#### Option A: Mock Payment Flow
```python
def process_payment(card_details):
    return {"success": True, "payment_id": "mock_123"}
```

**Pros:**
- Zero setup required
- No external dependencies
- Fastest implementation

**Cons:**
- Doesn't demonstrate real integration complexity
- No learning about payment flows
- Can't validate delegate payment spec
- Not representative of production challenges

#### Option B: Stripe Test Mode ✅ SELECTED

**Pros:**
- Real payment API integration
- Validates Delegated Payment Spec
- Learn actual payment flows
- Test mode = safe, no real charges
- Stripe has excellent ACP support
- Representative of production integration

**Cons:**
- Requires Stripe account setup
- API key management
- Slightly more complex

#### Option C: Multiple Payment Providers
- Stripe + Adyen + others

**Pros:**
- Demonstrates multi-PSP support

**Cons:**
- Over-engineered for POC
- Multiple integrations to maintain

### Decision

**Selected Option B** - Integrate with Stripe in test mode using Shared Payment Token API.

### Rationale

- **Real Integration:** Validates delegate payment flow end-to-end
- **Learning Value:** Understand actual payment complexities
- **ACP Support:** Stripe has first-class ACP support with Shared Payment Token
- **Test Mode:** Safe, no real money, unlimited test transactions
- **Documentation:** Stripe has excellent docs for agentic commerce
- **Production Path:** Same code works in production with key change

### Implementation

**Payment Flow:**
```
1. ChatGPT collects payment info from user
2. Delegate Payment Endpoint receives card details
3. Payment Service → Stripe: Create PaymentMethod
4. Stripe → Payment Service: Returns payment_token_id
5. Complete Checkout uses token to charge customer
6. Payment Service → Stripe: Create and confirm PaymentIntent
7. Stripe → Payment Service: Payment confirmed
8. Order Service creates order
```

**Test Cards:**
- Success: 4242 4242 4242 4242
- Decline: 4000 0000 0000 0002
- 3DS required: 4000 0025 0000 3155

### Consequences

**Positive:**
- Real payment integration validates POC
- Learn Stripe Shared Payment Token API
- Demonstrate end-to-end flow
- Confidence in production implementation

**Negative:**
- Requires Stripe account setup (~15 minutes)
- Need to manage API keys (use .env file)
- Webhook handling for async events

---

## Decision 6: Product Data Source

**Date:** October 19, 2025  
**Status:** ✅ Accepted  
**Deciders:** Engineering Team

### Context

Need 25 Nike products for the POC product feed. Must decide between scraping real data vs. creating mock data.

### Options Considered

#### Option A: Mock Data
```python
products = [
    {"title": "Nike Air Max 1", "price": 120, ...},
    {"title": "Nike Air Max 2", "price": 130, ...},
]
```

**Pros:**
- Fastest implementation
- Full control over data

**Cons:**
- Unrealistic data
- Missing real-world edge cases
- Less impressive demo

#### Option B: Scrape Nike.com ✅ SELECTED

**Pros:**
- Real product data
- Real images, descriptions, pricing
- Realistic variant data (sizes, colors)
- Better demo with actual products
- Test real-world data quality issues

**Cons:**
- Scraping complexity
- Potential data inconsistencies
- Nike.com structure changes

### Decision

**Selected Option B** - Scrape 25 actual Nike products from nike.com.

### Rationale

- **Realism:** Real products make demo more compelling
- **Data Quality:** Learn about real-world data challenges
- **Variants:** Test actual size/color variant handling
- **Images:** High-quality Nike product images
- **POC Scope:** 25 products is manageable to scrape

### Implementation

**Products to Scrape:**
- 10 shoes (running, basketball, lifestyle)
- 10 apparel (shirts, pants, jackets)
- 5 equipment (bags, accessories)

**Data to Extract:**
- Product title, description
- Price, currency
- Images (multiple angles)
- Sizes, colors (variants)
- Availability
- Product codes (for GTIN/MPN)

### Consequences

**Positive:**
- Realistic product feed
- Better demo experience
- Real product images
- Learn data quality challenges

**Negative:**
- Scraper maintenance if Nike.com changes
- May need to handle incomplete data

---

## Decision 7: Deployment Strategy

**Date:** October 19, 2025  
**Status:** ✅ Accepted  
**Deciders:** Engineering Team

### Context

POC deployment approach.

### Options Considered

1. **Kubernetes/Cloud** - Over-engineered for POC
2. **Docker Compose** - Good for multi-service, but overkill
3. **Local Development** ✅ SELECTED - Simplest for POC

### Decision

**Run everything locally** with uvicorn (backend) and vite (frontend).

### Rationale

- POC scale doesn't require orchestration
- Faster development iteration
- No cloud costs
- Easy to demo on laptop

### Future Evolution

Production deployment:
```
Local (POC) → Docker Compose (Integration) → Kubernetes (Production)
```

---

## Decision 8: Database Selection

**Date:** October 19, 2025  
**Status:** ✅ Accepted  
**Deciders:** Engineering Team

### Context

Database for POC.

### Options Considered

1. **PostgreSQL** - Production-grade, but setup overhead
2. **MongoDB** - NoSQL flexibility, but overkill
3. **SQLite** ✅ SELECTED - Zero setup, file-based

### Decision

**SQLite** for POC, with schema designed for easy migration to PostgreSQL.

### Rationale

- Zero setup required
- File-based (no separate process)
- Sufficient for POC scale
- Easy migration path to PostgreSQL (same SQL)
- SQLAlchemy abstracts database specifics

### Migration Path

```python
# POC
DATABASE_URL = "sqlite:///./checkout.db"

# Production
DATABASE_URL = "postgresql://user:pass@host/dbname"

# Same SQLAlchemy code works for both
```

---

## Summary of Key Decisions

| Decision | Selected Approach | Rationale |
|----------|-------------------|-----------|
| POC Scope | Production-like architecture, POC complexity | Balance speed with quality |
| Backend | Python + FastAPI | Team expertise, great docs |
| Frontend | React + Vite | Modern, fast development |
| Architecture | Gateway Pattern | Protocol-agnostic, extensible |
| MCP Integration | Yes, add MCP server layer | Future-proof, industry standard |
| Payment | Stripe test mode | Real integration, safe testing |
| Product Data | Scrape Nike.com | Realistic demo data |
| Deployment | Local development | Simplest for POC |
| Database | SQLite → PostgreSQL | Zero setup, easy migration |

---

## Lessons Learned (To be updated)

_This section will be updated during and after POC implementation._

### What Worked Well
- TBD

### What Could Be Improved
- TBD

### Unexpected Challenges
- TBD

---

## Change History

| Date | Change | Reason |
|------|--------|--------|
| Oct 19, 2025 | Initial decisions documented | Architecture planning complete |
| TBD | | |

---

## References

1. OpenAI ACP Specification: https://developers.openai.com/commerce
2. Nike Implementation Guidance Document (internal)
3. Model Context Protocol: https://modelcontextprotocol.io
4. Stripe Agentic Commerce: https://docs.stripe.com/agentic-commerce
5. ACP GitHub: https://github.com/agentic-commerce-protocol/agentic-commerce-protocol

