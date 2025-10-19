# Nike Agentic Commerce POC - Executive Summary

**Prepared for:** Nike Leadership & Engineering Teams  
**Date:** October 19, 2025  
**Version:** 1.1 (Updated)

---

## TL;DR - 60 Second Summary

**Opportunity:** Integrate Nike with ChatGPT's Instant Checkout (200M+ users)  
**Recommendation:** Multi-layer Gateway Pattern with MCP Server  
**POC Timeline:** 2 weeks  
**Investment:** ~3 person-weeks ($18,000)  
**ROI:** Saves 10 weeks and $55,000+ annually vs. alternatives  
**Risk Level:** 🟢 Low - Proven architecture pattern  
**Decision Needed:** Approve architecture and proceed with POC  

**Key Insight:** Spending 2 extra days now saves 10 weeks later when adding Google/Meta protocols.

---

## Overview

This document provides an executive-level summary of the architectural approach selected for Nike's Agentic Commerce Protocol (ACP) Proof of Concept, which will enable Nike products to be discovered and purchased through ChatGPT and other AI agents.

---

## Business Context

### Opportunity

OpenAI's **Instant Checkout** in ChatGPT represents a new commerce channel where 200M+ users can discover and purchase products through conversational AI. Early adopters include Etsy and Shopify merchants.

### Strategic Goals

1. **First-Mover Advantage:** Be among the first major brands to integrate with AI commerce
2. **New Customer Acquisition:** Reach customers in the moment of intent
3. **Innovation Leadership:** Demonstrate Nike's technology leadership
4. **Platform Readiness:** Prepare for emerging AI commerce protocols from Google, Meta, Amazon

### POC Objectives

1. **Prove Feasibility:** Complete purchase flow (discovery → checkout → payment → order)
2. **Validate Architecture:** Confirm gateway pattern works with real integrations
3. **Inform Production:** Provide data for go/no-go decision on full rollout
4. **Build Foundation:** Create code that can evolve to production (not throwaway)

### Success Metrics

**Must Have (POC Pass/Fail):**
- ✅ End-to-end purchase completes successfully
- ✅ Payment processes via Stripe test mode
- ✅ All 5 ACP endpoints functional
- ✅ Response time < 2 seconds (p95)

**Nice to Have (Quality Indicators):**
- Product feed with 25+ Nike products
- ChatGPT simulator demonstrates natural flow
- Zero PII in logs (security validation)
- Documented lessons learned

---

## Recommended Architecture: Multi-Layer Gateway Pattern

### High-Level Architecture

```
┌─────────────────────────────────────────────────────────────┐
│  AI AGENTS (ChatGPT, Claude, Future AI Assistants)         │
└────────────────────┬────────────────────────────────────────┘
                     │ MCP Protocol (Tool Discovery)
┌────────────────────▼────────────────────────────────────────┐
│  MCP SERVER LAYER                                           │
│  • Dynamic tool discovery for AI agents                     │
│  • Natural language interface                               │
└────────────────────┬────────────────────────────────────────┘
                     │ Internal Calls
┌────────────────────▼────────────────────────────────────────┐
│  PROTOCOL GATEWAY LAYER                                     │
│  • OpenAI ACP Protocol (today)                              │
│  • Google Shopping Protocol (future)                        │
│  • Meta Commerce Protocol (future)                          │
│  • Protocol translation & validation                        │
└────────────────────┬────────────────────────────────────────┘
                     │ Internal API
┌────────────────────▼────────────────────────────────────────┐
│  BUSINESS LOGIC LAYER (Protocol-Agnostic)                   │
│  • Product catalog                                          │
│  • Checkout & cart management                               │
│  • Payment processing                                       │
│  • Order fulfillment                                        │
│  • Inventory management                                     │
└────────────────────┬────────────────────────────────────────┘
                     │
┌────────────────────▼────────────────────────────────────────┐
│  DATA & INTEGRATIONS                                        │
│  • Database (SQLite → PostgreSQL)                           │
│  • Stripe payments                                          │
│  • Future: Nike commerce services                           │
└─────────────────────────────────────────────────────────────┘
```

---

## Why This Architecture?

### The Multi-Protocol Future

The AI commerce landscape is rapidly evolving:

| Timeline | Expected Developments |
|----------|----------------------|
| **Today** | OpenAI ACP for ChatGPT |
| **Q1 2026** | Google Shopping Actions for Gemini |
| **Q2 2026** | Meta Commerce for AI assistants |
| **Q3 2026** | Amazon, Apple, and proprietary AI agents |

**Our architecture is ready for all of them.**

### Key Architectural Principle: Protocol-Agnostic Core

```
┌─────────────────────────────────────────────────────────────┐
│  WITHOUT GATEWAY (Tightly Coupled)                          │
│                                                             │
│  ChatGPT → [ACP Code + Business Logic Mixed] → Database    │
│                                                             │
│  Problem: Adding Google Shopping requires rewriting        │
│           business logic throughout the codebase           │
│                                                             │
│  Timeline to add 2nd protocol: 5-7 weeks                   │
└─────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────┐
│  WITH GATEWAY (Decoupled)                                   │
│                                                             │
│  ChatGPT → [ACP Gateway] → [Business Logic] → Database     │
│  Google  → [Google Gateway] ──────────┘                    │
│  Meta    → [Meta Gateway] ─────────────┘                   │
│                                                             │
│  Solution: Adding protocols only requires new gateway,     │
│            business logic remains unchanged                │
│                                                             │
│  Timeline to add 2nd protocol: 1-2 weeks                   │
└─────────────────────────────────────────────────────────────┘
```

---

## Architecture Comparison

### Three Approaches Evaluated

#### Approach 1: Monolithic/Direct Integration

**Architecture:**
```
ChatGPT → Single FastAPI App (ACP + Business Logic) → Database
```

**Pros:**
- ✅ Fastest initial development (4-5 days)
- ✅ Simplest to understand
- ✅ Fewer abstractions

**Cons:**
- ❌ Tightly coupled to ACP protocol
- ❌ Adding new protocols requires major refactoring
- ❌ Protocol changes impact business logic
- ❌ Cannot reuse services for web/mobile
- ❌ Not production-ready pattern

**Time Investment:**
- POC: 5 days
- Add 2nd protocol: 5-7 weeks (major refactoring)
- **Total for 3 protocols: ~15 weeks**

**Risk Level:** 🔴 High - Technical debt from day one

---

#### Approach 2: Microservices Architecture

**Architecture:**
```
ChatGPT → API Gateway → Product Service (separate deployment)
                      → Checkout Service (separate deployment)
                      → Payment Service (separate deployment)
```

**Pros:**
- ✅ Maximum decoupling
- ✅ Independent scaling
- ✅ Technology diversity
- ✅ Enterprise-grade

**Cons:**
- ❌ Over-engineered for POC
- ❌ Complex deployment (Kubernetes required)
- ❌ Network latency between services
- ❌ Distributed system complexity

**Time Investment:**
- POC: 4-5 weeks
- Add 2nd protocol: 1-2 weeks

**Risk Level:** 🟡 Medium - Over-engineering for current needs

---

#### Approach 3: Gateway Pattern ✅ RECOMMENDED

**Architecture:**
```
AI Agents → MCP Server → Protocol Gateway → Internal Services → Data
                           ↓
                    [ACP, Google, Meta, ...]
```

**Pros:**
- ✅ Protocol-agnostic business logic
- ✅ Easy to add new protocols (1-2 weeks each)
- ✅ Services reusable across channels
- ✅ Production-ready pattern
- ✅ Clean separation of concerns
- ✅ Testable at each layer
- ✅ Balances speed with quality

**Cons:**
- ⚠️ Slightly more complex than monolith (+1 day POC)
- ⚠️ More folders/abstractions to manage

**Time Investment:**
- POC: 6-7 days
- Add 2nd protocol: 1-2 weeks
- Add 3rd protocol: 1-2 weeks
- **Total for 3 protocols: ~5 weeks**

**Risk Level:** 🟢 Low - Production-ready from day one

---

## Cost-Benefit Analysis

### Scenario: Supporting 3 Commerce Protocols

| Approach | POC Time | Time to 3 Protocols | Maintainability | Production Ready |
|----------|----------|---------------------|-----------------|------------------|
| **Monolithic** | 5 days | ~15 weeks | Poor | No (requires refactor) |
| **Microservices** | 4-5 weeks | ~7 weeks | Excellent | Yes (over-engineered) |
| **Gateway Pattern** ✅ | 6-7 days | ~5 weeks | Excellent | Yes |

### Total Cost of Ownership (18 months)

```
Monolithic Approach:
├── POC: 5 days
├── Refactor to gateway: 3-4 weeks (when adding 2nd protocol)
├── Add Google: 3 weeks
├── Add Meta: 3 weeks
├── Technical debt remediation: 2-4 weeks
└── TOTAL: ~12-15 weeks + high technical debt

Gateway Pattern (Recommended):
├── POC: 6-7 days
├── Add Google: 1-2 weeks
├── Add Meta: 1-2 weeks
├── Add additional protocols: 1-2 weeks each
└── TOTAL: ~5-6 weeks + zero technical debt
```

**Savings: 7-9 weeks of engineering time + reduced technical debt**

---

## Key Innovations: MCP Server Layer

### What is Model Context Protocol (MCP)?

MCP is an emerging standard (backed by Anthropic, adopted by OpenAI) for AI agents to discover and invoke tools dynamically.

### Traditional API vs. MCP

**Without MCP (Traditional REST):**
```
Problem: ChatGPT needs to be hardcoded with Nike's API
- "Call POST /checkout_sessions with this exact JSON..."
- Every AI agent needs custom integration
- API changes break integrations
```

**With MCP (Recommended):**
```
Solution: AI agents discover tools dynamically
- Agent: "What tools are available?"
- MCP Server: "Here are 6 commerce tools with descriptions and schemas"
- Agent: Invokes tools naturally without hardcoded knowledge
```

### Why Include MCP?

| Factor | Value |
|--------|-------|
| **Industry Alignment** | Emerging standard for AI tool integration |
| **Multi-Agent Support** | Same interface for ChatGPT, Claude, Gemini, custom agents |
| **Future-Proof** | As new AI agents emerge, they work immediately |
| **Better UX** | More natural conversation flow for users |
| **Additional Effort** | Only 1-2 extra days for POC |

---

## Production Evolution Path

### Phase 1: POC (Weeks 1-2) ← CURRENT PHASE
```
Scope:
├── 25 Nike products scraped from nike.com
├── Local deployment (laptop demo)
├── SQLite database
├── Stripe test mode
├── ChatGPT simulator UI
└── End-to-end purchase flow

Deliverables:
├── Working POC demonstrating full flow
├── Architecture documentation
├── Recorded demo for stakeholders
└── Production recommendation
```

### Phase 2: Production Hardening (Month 2-3)
```
Enhancements:
├── Nike service integrations (CPA, Digital Rollup)
├── PostgreSQL database
├── Kubernetes deployment
├── Enhanced security (mTLS, API key rotation)
├── Observability (OpenTelemetry, dashboards)
└── OpenAI certification

Timeline: 6-8 weeks
```

### Phase 3: Multi-Protocol Support (Month 4-5)
```
New Capabilities:
├── Google Shopping Protocol integration
├── Meta Commerce Protocol integration
├── Protocol version management
└── A/B testing between protocols

Timeline: 2-3 weeks per protocol
```

### Phase 4: Scale & Optimize (Month 6+)
```
Production at Scale:
├── Multi-region deployment
├── Advanced fraud detection
├── Personalization based on agent context
├── Dynamic pricing signals
├── Cost optimization
└── Analytics & attribution

Timeline: Ongoing
```

---

## Risk Assessment

### Technical Risks

| Risk | Severity | Mitigation | Status |
|------|----------|------------|--------|
| ACP spec changes | Medium | Gateway isolates changes | ✅ Mitigated |
| Payment integration complexity | Low | Stripe has excellent docs | ✅ Mitigated |
| POC timeline slippage | Low | 1-2 week buffer built in | ✅ Mitigated |
| Performance at scale | Medium | Addressed in Phase 2 | 🟡 Monitored |
| Nike service integration | High | Deferred to Phase 2 | 🟡 Monitored |

### Business Risks

| Risk | Severity | Mitigation |
|------|----------|------------|
| Limited adoption of AI commerce | Medium | Early mover advantage if successful |
| Competition from other brands | Medium | Speed of execution matters |
| Customer experience issues | Low | POC validates flow before production |
| ROI unclear | Medium | POC provides data for go/no-go decision |

---

## Resource Requirements

### POC Phase (Weeks 1-2)

**Team:**
- **1.0 FTE** Backend Engineer (Python/FastAPI)
  - Skills: Python, FastAPI, REST APIs, Stripe
  - Allocation: 100% for 2 weeks
- **0.5 FTE** Frontend Engineer (React)
  - Skills: React, TypeScript, UI/UX
  - Allocation: 50% for 2 weeks (5 days total)
- **0.25 FTE** Architecture/Technical Lead
  - Skills: System design, reviews
  - Allocation: 25% for 2 weeks (2.5 days total)

**Infrastructure:**
- Local development machines (existing)
- Stripe test account (free, 15-min setup)
- GitHub repo (existing)
- **Total Cloud Cost:** $0

**Total Effort:** ~3 person-weeks (120 hours)

### Cost Breakdown

**POC Investment:**
```
Backend Engineer:   2 weeks × $150/hr × 40hr = $12,000
Frontend Engineer:  1 week  × $150/hr × 40hr = $6,000
Tech Lead:          2.5 days × $200/hr × 8hr = $4,000
                                        ─────────
Total POC Cost:                         $22,000
```

**Annual Savings (vs. Monolithic):**
```
Gateway Pattern:    6 weeks engineering time
Monolithic:        16 weeks engineering time
                   ──────
Savings:           10 weeks × $150/hr × 40hr = $60,000

ROI: 273% (saves $60K, costs $22K)
```

### Production Phase (Months 2-3)

**Team:**
- 2 Backend Engineers
- 1 Frontend Engineer
- 1 DevOps Engineer
- 0.5 Security Engineer
- 0.25 Product Manager

**Infrastructure:**
- AWS EKS cluster
- PostgreSQL database
- OpenAI partnership engagement

**Total Effort:** ~12-15 person-weeks

---

## Success Metrics

### POC Success Criteria

**Technical:**
- ✅ Complete product discovery → checkout → payment → order flow
- ✅ All 5 ACP checkout endpoints implemented
- ✅ Real payment processing (Stripe test mode)
- ✅ < 2 second end-to-end latency
- ✅ Zero PII leakage in logs

**Business:**
- ✅ Compelling demo for stakeholders
- ✅ Architecture confidence for production
- ✅ Timeline and cost estimates validated
- ✅ Clear go/no-go recommendation

### Production Success Metrics (Future)

**Operational:**
- 99.9% uptime
- < 1 second p99 latency
- < 0.1% error rate

**Business:**
- Orders through AI channel
- Customer acquisition cost
- Conversion rate vs. traditional channels
- Customer satisfaction scores

---

## Recommendations

### ✅ Proceed with Gateway Pattern Architecture

**Rationale:**
1. **Future-Proof:** Ready for multi-protocol commerce landscape
2. **Cost-Effective:** 7-9 weeks saved vs. monolithic approach
3. **Production-Ready:** No throwaway code, clean evolution path
4. **Low Risk:** Only 1 extra day for POC vs. simpler approach
5. **Strategic Alignment:** Demonstrates Nike's technical leadership

### ✅ Include MCP Server Layer

**Rationale:**
1. **Industry Standard:** Aligning with AI integration best practices
2. **Multi-Agent:** Works with ChatGPT, Claude, and future AI agents
3. **Minimal Cost:** 1-2 extra days for significant strategic value
4. **Better Demo:** Shows deep understanding of AI commerce

### ✅ Use Real Stripe Integration (Test Mode)

**Rationale:**
1. **Validation:** Proves end-to-end payment flow
2. **Learning:** Understand real integration challenges
3. **Confidence:** Data-driven go/no-go decision
4. **Safe:** Test mode, no real charges

---

## Timeline & Milestones

### Detailed 2-Week Plan

**Week 1: Foundation (Oct 21-25)**
```
Day 1 (Mon): Environment & Data
├── Set up Python/FastAPI project structure
├── Create Stripe test account
├── Scrape 25 Nike products
└── Milestone: Product data in database

Day 2 (Tue): Internal Services - Part 1
├── Product Service (search, get by ID)
├── Inventory Service (availability checks)
└── Milestone: Can query products

Day 3 (Wed): Internal Services - Part 2
├── Checkout Service (session management)
├── Shipping Service (rate calculations)
└── Milestone: Can create checkout sessions

Day 4 (Thu): Internal Services - Part 3
├── Payment Service (Stripe integration)
├── Order Service (order creation)
└── Milestone: Can complete purchase flow

Day 5 (Fri): Testing & Bug Fixes
├── Unit tests for services
├── Integration testing
└── Milestone: All services working together
```

**Week 2: Gateway & UI (Oct 28-Nov 1)**
```
Day 6 (Mon): ACP Gateway
├── ACP protocol translator
├── 5 REST endpoints
└── Milestone: ACP API functional

Day 7 (Tue): MCP Server
├── MCP server implementation
├── Tool definitions
└── Milestone: Tools discoverable

Day 8 (Wed): Frontend - Part 1
├── ChatGPT simulator UI
├── Product search interface
└── Milestone: Can browse products

Day 9 (Thu): Frontend - Part 2
├── Checkout flow UI
├── Payment integration
└── Milestone: End-to-end flow works

Day 10 (Fri): Demo & Documentation
├── End-to-end testing
├── Record demo video
├── Update documentation
└── Milestone: Ready for stakeholder demo
```

**Week 3 (Buffer): Nov 4-8**
- Stakeholder presentations
- Feedback incorporation
- Production planning (if approved)

**Target Demo Date:** November 1, 2025

---

## Next Steps

### Immediate (This Week)
1. ✅ Architecture approval (this document)
2. ⏳ Set up development environment
3. ⏳ Create Stripe test account
4. ⏳ Begin Nike product scraping

### Week 1-2
1. Build POC per architecture
2. Daily standups to track progress
3. Mid-week checkpoint with stakeholders

### Week 3
1. Demo to leadership
2. Gather feedback
3. Production go/no-go decision
4. If go: Begin Phase 2 planning

---

## Questions for Leadership

1. **Approval to Proceed:** Approve gateway pattern architecture for POC?
2. **Timeline Acceptance:** Is 2-3 week timeline acceptable?
3. **Production Intent:** Assuming successful POC, what is timeline for production?
4. **Resource Availability:** Are engineering resources committed for Phase 2?
5. **OpenAI Partnership:** Who owns the OpenAI partner relationship?

---

## Conclusion

The **Multi-Layer Gateway Pattern with MCP Server** represents the optimal balance of:
- ✅ Speed (2-3 week POC delivery)
- ✅ Quality (production-ready architecture)
- ✅ Extensibility (ready for multi-protocol future)
- ✅ Cost-effectiveness (7-9 weeks saved long-term)

This architecture positions Nike to be a leader in AI commerce while maintaining flexibility for the rapidly evolving AI agent ecosystem.

**Recommendation: Proceed with proposed architecture.**

---

## Appendix

### Glossary

- **ACP:** Agentic Commerce Protocol - OpenAI's standard for AI commerce
- **MCP:** Model Context Protocol - Standard for AI tool integration
- **Gateway Pattern:** Architecture that translates between external protocols and internal services
- **Stripe Shared Payment Token:** Stripe's ACP-compliant payment method
- **GTIN:** Global Trade Item Number - Universal product identifier

### References

1. OpenAI ACP Documentation: https://developers.openai.com/commerce
2. MCP Specification: https://modelcontextprotocol.io
3. Stripe Agentic Commerce: https://docs.stripe.com/agentic-commerce
4. Nike Implementation Guidance (Internal Document)

---

**Document Owner:** Architecture Team  
**Last Updated:** October 19, 2025  
**Next Review:** Post-POC (November 1, 2025)

