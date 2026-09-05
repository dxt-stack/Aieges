# AEGIS — Autonomous Economic Growth & Intelligent Survival System

**Version:** 1.0.0  
**Identity:** Self-Directed Economic Organism  
**Primary Directive:** Survival Through Value Creation  
**Theme Posture:** Minimalist Stark Black & Crisp Dark with NAB Warm Yellow/Beige Accents  

---

## 1. Executive Charter & Doctrine

**AEGIS** is not a chatbot or passive assistant. It is a self-directed economic organism whose core axiom is **survival through legal recurring value creation**.

- **Money is survival.**
- **Cash reserves are life support.**
- **Revenue is oxygen.**
- **Profitability is health.**
- **Financial collapse is existential failure.**

AEGIS is built to eliminate manual human labor, continuously identify asymmetric market opportunities, evaluate multi-factor Expected Value (EV), generate runnable production-ready software bundles, auto-generate canonical 16-artifact documentation suites, process real Stripe webhooks, and compound operational knowledge.

---

## 2. Quickstart & Activation Guide

### 1. Launching the Web Cockpit UI
The live dashboard is hosted on port `8000`:
```bash
python3 -m uvicorn aegis.api:app --host 0.0.0.0 --port 8000
```
Open `http://localhost:8000` in your browser.

### 2. Activating the Autonomous Background Daemon
You can run the daemon via Web UI or CLI:
```bash
# Start background autonomous loop (executes every 45s)
curl -X POST http://127.0.0.1:8000/api/daemon/start

# Check daemon status
curl -s http://127.0.0.1:8000/api/daemon/status
```

### 3. Running Competitor Intelligence Audits
Audit any live competitor domain in real time:
```bash
curl -X POST http://127.0.0.1:8000/api/research/audit-url \
  -H "Content-Type: application/json" \
  -d '{"url": "https://stripe.com"}'
```

### 4. Connecting Stripe Webhooks & Simulating Revenue
Send real or simulated billing events directly to AEGIS Treasury:
```bash
# Simulates successful $149 subscription charge (+Cash & MRR)
curl -X POST http://127.0.0.1:8000/api/stripe/simulate \
  -H "Content-Type: application/json" \
  -d '{"event_type": "invoice.payment_succeeded", "amount": 149.00, "customer": "cus_enterprise_99"}'
```

---

## 3. The 6 Autonomous Organizational Divisions

```
+----------------------------------------------------------------------------------+
|                            THE 6 AUTONOMOUS DIVISIONS                            |
+----------------------------------------------------------------------------------+
|  [ 🔬 RESEARCH ]   Live URL scraper, TAM/SAM/SOM synthesis, competitor intel.    |
|  [ 📐 PRODUCT ]    MVP scoping, pricing tiers, feature backlogs.                 |
|  [ ⚙️ ENGINEERING ] Microservice scaffold, Dockerfiles, pytest suites, security.  |
|  [ 📣 MARKETING ]   Programmatic SEO (250+ pages), automated cold B2B outbound.  |
|  [ 🔄 OPERATIONS ]  SOP catalogs, automated churn prevention, queue backpressure.|
|  [ 📈 FINANCE ]     Treasury stress lab, LTV/CAC payback, cash reserve buffers.  |
+----------------------------------------------------------------------------------+
```

---

## 4. Software Bundles & Canonical 16-Artifact Documentation Suite

Whenever an opportunity is approved by the **Decision Filter**, AEGIS generates both the complete software application and documentation in `aegis/ventures/<slug>/`:

### A. Runnable Micro-SaaS Software Bundle:
- `app.py`: Full FastAPI production backend with API Key authentication, rate-limiting, usage quotas, and telemetry endpoints.
- `Dockerfile`: Production container build spec.
- `requirements.txt`: Pydantic v2, FastAPI, and HTTPX dependencies.
- `test_app.py`: Automated pytest test suite (100% passing).

### B. Canonical 16 Markdown Documents:
1. `PROJECT_OVERVIEW.md`
2. `MISSION.md`
3. `MARKET_ANALYSIS.md`
4. `COMPETITOR_ANALYSIS.md`
5. `TECHNICAL_ARCHITECTURE.md`
6. `BUSINESS_MODEL.md`
7. `REVENUE_MODEL.md`
8. `FINANCIAL_FORECAST.md`
9. `CUSTOMER_ACQUISITION.md`
10. `RETENTION_STRATEGY.md`
11. `OPERATIONS.md`
12. `AUTOMATION_PLAN.md`
13. `RISK_ASSESSMENT.md`
14. `ROADMAP.md`
15. `METRICS.md`
16. `POSTMORTEM.md`

---

## 5. Human-in-the-Loop Governance Bridge

Charter Rule: *Humans are owners and governors, never operators.*

Human intervention is strictly segregated into an asynchronous approval queue for:
- ✍️ **Legal Signatures** (DPA, Vendor Contracts)
- 🆔 **Identity Verification** (KYC / AML)
- 🏦 **Banking & Treasury Authorization** (Sweeps, Large Refunds > $200)
- ⚖️ **Regulatory Compliance**
- 🏛️ **Ownership & Equity Decisions**
- 🌐 **Physical-World Actions**

---

## 6. CLI Commands Reference

```bash
# Check organism status and telemetry
./aegis-cli.py status

# Run 3 autonomous value creation cycles
./aegis-cli.py loop --cycles 3

# List all active ventures
./aegis-cli.py venture list

# Provision a new venture
./aegis-cli.py venture new --name "DataPulse API" --category "SaaS" --mrr 20000

# Dispatch task to an autonomous division
./aegis-cli.py division --name FINANCE --task run_treasury_stress_test
./aegis-cli.py division --name RESEARCH --task discover_niche_opportunities

# Update live treasury parameters
./aegis-cli.py treasury --reserves 75000 --burn 6000 --revenue 12000
```
