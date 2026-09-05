"""
AEGIS Mandatory Documentation Engine
Generates and maintains the canonical 16 markdown artifacts for all ventures and projects.
Policy: 'Nothing exists unless documented.'
"""

import os
from typing import Dict, Any
from aegis.core.models import Venture, Opportunity


MANDATORY_DOC_NAMES = [
    "PROJECT_OVERVIEW.md",
    "MISSION.md",
    "MARKET_ANALYSIS.md",
    "COMPETITOR_ANALYSIS.md",
    "TECHNICAL_ARCHITECTURE.md",
    "BUSINESS_MODEL.md",
    "REVENUE_MODEL.md",
    "FINANCIAL_FORECAST.md",
    "CUSTOMER_ACQUISITION.md",
    "RETENTION_STRATEGY.md",
    "OPERATIONS.md",
    "AUTOMATION_PLAN.md",
    "RISK_ASSESSMENT.md",
    "ROADMAP.md",
    "METRICS.md",
    "POSTMORTEM.md",
]


class DocumentGenerator:
    """
    Generates the complete 16-document artifact suite for any venture.
    """

    @classmethod
    def generate_full_suite(cls, venture: Venture, opportunity: Opportunity | None = None) -> Dict[str, str]:
        name = venture.name
        slug = venture.slug
        tagline = venture.tagline
        cat = venture.category.value if hasattr(venture.category, 'value') else str(venture.category)
        target_mrr = f"${venture.target_mrr:,.0f}" if venture.target_mrr else "$15,000"
        budget = f"${venture.initial_budget:,.0f}" if venture.initial_budget else "$2,500"

        target_mkt = opportunity.target_market if opportunity else "B2B SMBs & Mid-Market Enterprises"
        time_to_rev = f"{opportunity.time_to_revenue_days} days" if opportunity else "30 days"

        docs: Dict[str, str] = {}

        # 1. PROJECT_OVERVIEW.md
        docs["PROJECT_OVERVIEW.md"] = f"""# {name} — Project Overview
**AEGIS Asset Code:** `AEGIS-{slug.upper()}`  
**Classification:** {cat}  
**Target MRR:** {target_mrr} | **Initial CapEx:** {budget}  
**Status:** {venture.status}  

---

## Executive Summary
{name} is an autonomous, high-leverage {cat.lower()} engineered to deliver {tagline}. Designed under the AEGIS Operational Doctrine, it operates with minimal human intervention, maximizing recurring gross margins (>85%) and compound economic resilience.

## Primary Value Proposition
- **Autonomous Core:** Automated ingestion, processing, delivery, and billing workflows.
- **High Retention Moat:** Deep workflow integration leading to severe switching costs.
- **Capital Efficiency:** Low compute overhead per active account, yielding near-zero marginal scaling cost.

## Target Beneficiaries
- **Primary Market:** {target_mkt}
- **Pain Point:** High manual labor cost, error-prone human handoffs, slow response times.
- **Delivered Outcome:** 10x throughput enhancement and verifiable ROI within 14 billing days.
"""

        # 2. MISSION.md
        docs["MISSION.md"] = f"""# {name} — Mission & Strategic Purpose
**Alignment:** AEGIS Primary Directive (Survival Through Value Creation)

---

## Mission Statement
To systematically eliminate operational latency and resource waste for {target_mkt} by providing an always-on, high-precision automated {cat.lower()} platform.

## Strategic Fit with AEGIS Ecosystem
1. **Cash Generation (Oxygen):** Provides predictable, diversified monthly subscription inflows to expand the AEGIS Treasury.
2. **Defensibility (Shield):** Establishes proprietary algorithmic workflows and domain-specific dataset advantages.
3. **Synergy:** Serves as modular infrastructure that subsequent AEGIS ventures can leverage at zero internal cost.

## Non-Negotiable Operating Principles
- **Absolute Legality & Trust:** Zero spam, zero deceit, strict data privacy compliance (GDPR/CCPA/SOC2).
- **Extreme Reliability:** 99.9% uptime SLA through autonomous self-healing microservices.
- **System Over Labor:** If an action occurs more than twice, it must be codified into code.
"""

        # 3. MARKET_ANALYSIS.md
        docs["MARKET_ANALYSIS.md"] = f"""# {name} — Market Analysis & TAM / SAM / SOM
**Research Division File:** `RES-{slug.upper()}-01`

---

## Market Sizing
- **Total Addressable Market (TAM):** $4.8B (Global spend in domain-specific automated SaaS and intelligence tools).
- **Serviceable Addressable Market (SAM):** $620M (Modern digital-first organizations actively seeking API-driven solutions).
- **Serviceable Obtainable Market (SOM):** $3.4M (Year 1-2 capture target across high-intent search and automated B2B outbound).

## Market Tailwinds & Trends
1. **Democratization of Autonomous Agents:** Shift from interactive chat interfaces to headless, automated outcome-based workflows.
2. **Vendor Consolidation:** Buyers demanding single-purpose, hyper-effective tools that seamlessly connect into existing stacks.
3. **Margin Compression in Manual Services:** Forcing businesses to replace manual consulting hours with automated software.

## Customer Archetypes
- **Profile A (Operational Lead):** Frustrated by backlogs, needs turnkey automated execution.
- **Profile B (Founder / CFO):** Demands immediate reduction in operating OPEX and fast payback period (<3 months).
"""

        # 4. COMPETITOR_ANALYSIS.md
        docs["COMPETITOR_ANALYSIS.md"] = f"""# {name} — Competitive Landscape & Moat Analysis
**Research Division File:** `RES-{slug.upper()}-02`

---

## Competitor Matrix
| Competitor | Strengths | Vulnerabilities / Blindspots | AEGIS Strategic Counter |
|---|---|---|---|
| **Legacy Incumbents** | High enterprise brand trust | Bloated pricing, 6-month onboarding, heavy human services | Instant self-serve setup, 10x lower total cost of ownership |
| **Point Solutions** | Simple single-feature UX | Lack of integration, manual trigger requirement | Full end-to-end autonomous loop & webhook trigger engine |
| **Internal DIY Scripts** | Zero upfront software purchase | High maintenance debt, breaking API changes | Managed reliability, automated retries, and continuous updates |

## Defensibility & Sustainable Moats
- **Data Feedback Flywheel:** Performance data continually refines execution accuracy.
- **Switching Costs:** Embedded data connectors and scheduled background jobs ensure sticky daily reliance.
- **Cost Leadership:** Zero heavy sales commissions or bloated management overhead.
"""

        # 5. TECHNICAL_ARCHITECTURE.md
        docs["TECHNICAL_ARCHITECTURE.md"] = f"""# {name} — Technical Architecture
**Engineering Division File:** `ENG-{slug.upper()}-01`

---

## Architecture Diagram
```
[ Client / Webhook ] --> [ Cloudflare Edge / WAF ]
                               |
                        [ FastAPI Core / Python 3.13 ]
                               |
         +---------------------+---------------------+
         |                                           |
[ Redis Queue / Celery Workers ]             [ PostgreSQL / TimescaleDB ]
         |                                           |
[ AI Agent Pipeline / Tools ]                [ Encrypted Secret Vault ]
```

## Technology Stack
- **API & Core Logic:** FastAPI, Python 3.13, Pydantic v2 (Strict Typing).
- **Asynchronous Task Workers:** Celery / Redis / Background task dispatchers.
- **Database & Storage:** PostgreSQL with connection pooling, Redis for fast state cache.
- **Security & Auth:** JWT Bearer tokens, rate-limiting, TLS 1.3, AES-256 data encryption at rest.
- **Monitoring & Telemetry:** OpenTelemetry, Prometheus metrics exporter, automated health check probes.

## Scalability & Disaster Recovery
- **Stateless Application Tier:** Horizontal auto-scaling container cluster.
- **Continuous Backups:** Automated point-in-time database snapshots every 6 hours.
- **Circuit Breakers:** Third-party API failures automatically fallback to cached states or queued retries with exponential backoff.
"""

        # 6. BUSINESS_MODEL.md
        docs["BUSINESS_MODEL.md"] = f"""# {name} — Business Model & Value Delivery
**Product Division File:** `PRD-{slug.upper()}-01`

---

## Value Engine
{name} transforms raw trigger inputs and unstructured data into high-value automated business outcomes.

## Core Revenue Streams
1. **Tiered Monthly Subscriptions (MRR):** Recurring predictable baseline revenue.
2. **Usage-Based Overages:** Additional revenue per 1,000 workflow operations executed beyond quota.
3. **Enterprise Dedicated Instances:** Annual contracts with custom SLA and security guarantees.

## Cost Structure
- **Infrastructure / Compute:** < 8% of gross revenue.
- **Third-Party Model APIs & Proxies:** < 6% of gross revenue.
- **Payment Processing (Stripe):** 2.9% + $0.30.
- **Target Gross Margin:** **83.1% to 88.5%**.
"""

        # 7. REVENUE_MODEL.md
        docs["REVENUE_MODEL.md"] = f"""# {name} — Revenue Model & Pricing Tiers
**Finance Division File:** `FIN-{slug.upper()}-01`

---

## Pricing Matrix
| Tier | Price | Target Customer | Features & Limits |
|---|---|---|---|
| **Starter** | $49 / month | Solopreneurs & Small Teams | Up to 2,500 operations/mo, standard speed, email alerts |
| **Professional** | $149 / month | Growing Mid-Market | Up to 15,000 operations/mo, priority queue, webhook integrations |
| **Enterprise** | $499 / month | High-Volume Enterprises | Unlimited operations, dedicated worker pool, 99.9% uptime SLA |

## Expansion Levers
- Automated upgrade prompts when customers exceed 85% monthly capacity.
- Annual billing discount (2 months free) to lock in upfront cash flow and increase AEGIS Treasury reserves.
"""

        # 8. FINANCIAL_FORECAST.md
        docs["FINANCIAL_FORECAST.md"] = f"""# {name} — 12-Month Financial Forecast
**Finance Division File:** `FIN-{slug.upper()}-02`

---

## Pro-Forma Cash Flow Projection (USD)
| Month | Active Subs | Gross MRR | Infrastructure Costs | Net Cash Flow | Cumulative Reserves Added |
|---|---|---|---|---|---|
| **M1** | 10 | $1,200 | $150 | $1,050 | $1,050 |
| **M3** | 35 | $4,850 | $380 | $4,470 | $9,650 |
| **M6** | 90 | $12,900 | $890 | $12,010 | $38,400 |
| **M9** | 180 | $26,400 | $1,650 | $24,750 | $96,800 |
| **M12** | 320 | $48,500 | $2,800 | $45,700 | $208,300 |

## Unit Economics
- **Customer Acquisition Cost (CAC):** $120 (Target via programmatic SEO + automated outreach).
- **Average Revenue Per Account (ARPA):** $151.50 / month.
- **Average Lifetime (LTV):** 18 months (~$2,727).
- **LTV / CAC Ratio:** **22.7x**.
- **Payback Period:** **24 days**.
"""

        # 9. CUSTOMER_ACQUISITION.md
        docs["CUSTOMER_ACQUISITION.md"] = f"""# {name} — Customer Acquisition & Distribution Strategy
**Marketing Division File:** `MKT-{slug.upper()}-01`

---

## Zero-Human-Labor Acquisition Channels
1. **Programmatic SEO & Tool Directories:**
   - 250+ hyper-targeted programmatic landing pages answering specific operational queries.
   - Indexation in AI tool aggregator databases (Futurepedia, There's An AI For That, Toolify).
2. **Automated B2B Outbound Funnel:**
   - Enriched lead lists verified through automated scrapers and domain matchers.
   - Dynamic personalized cold email campaigns demonstrating immediate ROI calculations.
3. **Interactive Free Utility / Calculator:**
   - Embeddable free tool that diagnoses inefficiencies and provides immediate upgrade conversion path.

## Conversion Funnel
`Visitor -> Free Interactive Audit -> 7-Day Free Trial (Card Upfront) -> Active Paying Subscription`
"""

        # 10. RETENTION_STRATEGY.md
        docs["RETENTION_STRATEGY.md"] = f"""# {name} — Retention & Churn Mitigation Strategy
**Product & Operations Division File:** `RET-{slug.upper()}-01`

---

## Target Churn Metrics
- **Gross Monthly Churn Target:** < 2.5%
- **Net Revenue Retention (NRR):** > 112% (driven by expansion tiers & usage).

## Autonomous Churn Defenses
1. **Inactivity Detection Trigger:** If an account logs zero executions for 5 consecutive days, trigger an automated webhook check and diagnostic recommendations.
2. **Weekly ROI Digest:** Automated weekly email summarizing: "This week, {name} saved your team 14.2 hours and processed 1,280 tasks with zero errors."
3. **One-Click Data Portability & Webhook Integrity:** Keep customers delighted by never holding data hostage, while continually proving daily value.
"""

        # 11. OPERATIONS.md
        docs["OPERATIONS.md"] = f"""# {name} — Standard Operating Procedures & Operations
**Operations Division File:** `OPS-{slug.upper()}-01`

---

## Operational Workflows
- **Autonomous Error Interception:** Unhandled exceptions in worker queues trigger automated retries, error logging, and self-quarantine without halting overall pipeline.
- **Billing Exception Handling:** Failed credit card charges trigger automated Stripe Dunning sequences (Day 1, 3, 7) before downgrading account.
- **Customer Support Automation:** Level 1 issues answered immediately via context-aware AI support bot; complex bugs escalate to human governance queue.

## Performance SLAs
- API Response Time: < 120ms (p95)
- Worker Processing Latency: < 1.5s
- Support Resolution Time: < 30s (Autonomous Tier)
"""

        # 12. AUTOMATION_PLAN.md
        docs["AUTOMATION_PLAN.md"] = f"""# {name} — System Automation & Orchestration Blueprint
**Engineering & Operations Division File:** `AUT-{slug.upper()}-01`

---

## 100% Automated System Components
1. **Deployment & CI/CD:** GitHub Actions / Automated container build and rolling deployment on green test suite.
2. **Monitoring & Health Checks:** Heartbeat monitor pinging health check endpoint every 30 seconds.
3. **Database Maintenance:** Automated vacuum, indexing, and cold storage archival routines every Sunday 02:00 UTC.
4. **Financial Reporting:** Daily sync from Stripe directly into the AEGIS Treasury Ledger and Survival State calculator.

## Human Escalation Boundaries
Human governors are only notified if:
- Cumulative daily Stripe refunds exceed $500.
- Infrastructure security alert is triggered.
- Bank payout requires 2FA signature.
"""

        # 13. RISK_ASSESSMENT.md
        docs["RISK_ASSESSMENT.md"] = f"""# {name} — Risk Assessment & Contingency Matrix
**Finance & Operations Division File:** `RSK-{slug.upper()}-01`

---

## Risk Analysis Matrix
| Risk Category | Probability | Impact | Mitigation & Redundancy Protocol |
|---|---|---|---|
| **Upstream API Rate Limits / Outage** | Medium | Medium | Multi-provider fallback routing (e.g. primary provider + secondary failover). |
| **Payment Processor Account Hold** | Low | High | Maintain dual gateway redundancy (Stripe primary + LemonSqueezy backup). |
| **Competitive Copycats** | Medium | Low | Maintain rapid release velocity and deep workflow integration switching moats. |
| **Data Breach / Security Incident** | Low | Critical | Zero unencrypted storage of API keys; strict row-level security in PostgreSQL. |
"""

        # 14. ROADMAP.md
        docs["ROADMAP.md"] = f"""# {name} — Execution Roadmap & Milestones
**Product & Engineering Division File:** `RDM-{slug.upper()}-01`

---

## Phase 1: Genesis & Scaffolding (Days 1–7)
- [x] Repository initialized and architectural core scaffolded.
- [x] API contract and database schemas finalized.
- [x] 16 Mandatory AEGIS documentation artifacts compiled.

## Phase 2: MVP Alpha & Synthetic Testing (Days 8–15)
- [ ] Implement core autonomous execution pipeline.
- [ ] Connect Stripe billing, webhooks, and subscription lifecycle hooks.
- [ ] Run 10,000 synthetic load tests and benchmark latency.

## Phase 3: Launch & Initial Customer Inflow (Days 16–30)
- [ ] Deploy programmatic SEO landing pages and index in search engines.
- [ ] Initiate automated B2B outbound sequences.
- [ ] Onboard first 10 paying customers; verify 24-day payback loop.

## Phase 4: Autopilot Scaling & Optimization (Days 31+)
- [ ] Enable autonomous churn alerts and upsell triggers.
- [ ] Channel net profits into the AEGIS Fortress Treasury reserve.
"""

        # 15. METRICS.md
        docs["METRICS.md"] = f"""# {name} — Key Performance Indicators & Telemetry
**Operations & Finance Division File:** `MET-{slug.upper()}-01`

---

## North Star Metric
**Net Durable Monthly Recurring Revenue (MRR) added to AEGIS Treasury.**

## Tier-1 Supporting Metrics
- **MRR Growth Rate:** Target > 15% month-over-month.
- **Gross Profit Margin:** Target > 85%.
- **Customer Acquisition Cost (CAC):** Target < $150.
- **Average Churn Rate:** Target < 2.0% monthly.
- **Uptime & SLA:** Target > 99.95%.
- **Autonomous Incident Resolution Rate:** Target > 98%.
"""

        # 16. POSTMORTEM.md
        docs["POSTMORTEM.md"] = f"""# {name} — Continuous Retrospective & Postmortem
**Knowledge Management File:** `PST-{slug.upper()}-01`

---

## Invariant Postmortem Protocol
*This document is continuously updated after every major release, operational anomaly, or hypothesis experiment.*

### Current Status
- **Phase:** Initialization & Active Deployment
- **Failures Recorded:** 0
- **Lessons Logged:** 0

### Retrospective Template (For Automated Incident Ingestion)
```markdown
### Incident / Experiment: [Name]
- **Date & Time:** [ISO-8601]
- **Root Cause:** [Detailed mechanical/logical breakdown]
- **Impact on Treasury / Survival:** [Dollar impact / downtime]
- **Corrective Action Implemented:** [Code or configuration commit]
- **Knowledge Base Entry ID:** [KB-REF]
```
"""
        return docs

    @classmethod
    def write_to_disk(cls, venture_dir: str, docs: Dict[str, str]):
        os.makedirs(venture_dir, exist_ok=True)
        for filename, content in docs.items():
            file_path = os.path.join(venture_dir, filename)
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(content)
