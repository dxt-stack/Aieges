# AEGIS — Autonomous Economic Growth & Intelligent Survival System

[![Python 3.10+](https://img.shields.io/badge/python-3.10+-white.svg)](https://www.python.org/downloads/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.115+-black.svg?logo=fastapi)](https://fastapi.tiangolo.com)
[![Pydantic v2](https://img.shields.io/badge/Pydantic-v2-d4af37.svg)](https://docs.pydantic.dev/)
[![Tests](https://img.shields.io/badge/tests-passing-white.svg)]()
[![Design](https://img.shields.io/badge/Theme-Monochrome%20%2B%20NAB%20Gold-d4af37.svg)]()

> **"Money is survival. Cash reserves are life support. Revenue is oxygen. Profitability is health. Financial collapse is existential failure."**

AEGIS is a self-directed economic organism designed to autonomously discover, evaluate, scaffold, document, and manage legal recurring value-producing systems and software ventures with zero unnecessary human labor.

---

## 🛡️ Core Architecture

```
+========================================================================================+
|                                      AEGIS v1.0                                        |
+========================================================================================+
|                                                                                        |
|  [ TREASURY (Life Support) ] <---------> [ SURVIVAL STATE MACHINE (Posture Gauge) ]    |
|   - Liquid Cash Reserves                  - CRITICAL (<30d)                            |
|   - Burn Rate & MRR                       - WARNING (30-90d)                           |
|   - Net Runway Telemetry                  - STABLE (3-12mo) / STRONG / FORTRESS        |
|                                                                                        |
|  +----------------------------------------------------------------------------------+  |
|  |                        VALUE CREATION AUTONOMOUS LOOP                            |  |
|  |  Observe -> Analyze -> Discover -> Prioritize -> Plan -> Build -> Deploy -> ... |  |
|  +----------------------------------------------------------------------------------+  |
|                                                                                        |
|  +----------------------------------------------------------------------------------+  |
|  |                           6 AUTONOMOUS DIVISIONS                                 |  |
|  |  [ Research ] [ Product ] [ Engineering ] [ Marketing ] [ Operations ] [ Finance ] |  |
|  +----------------------------------------------------------------------------------+  |
|                                                                                        |
|  [ OPPORTUNITY SCORER (EV/RAROE) ]  [ DECISION FILTER (5 Qs) ]  [ 16-DOC GENERATOR ]   |
|                                                                                        |
|  [ STRIPE REVENUE BRIDGE ] <-------------> [ KNOWLEDGE BASE ] <-> [ GOVERNANCE QUEUE ]|
+========================================================================================+
```

---

## ⚡ Real & Active Capabilities

1. **Survival State Machine**: Dynamic tactical posture shifts (`CRITICAL`, `WARNING`, `STABLE`, `STRONG`, `FORTRESS`) based on treasury runway calculations.
2. **Real Web Research Scraper**: Live URL competitor audits, extracting headings, meta tags, pricing signals, and competitive weaknesses.
3. **Stripe Revenue Bridge**: Real webhook handler for `invoice.payment_succeeded`, `customer.subscription.deleted`, and `charge.refunded` that updates Treasury cash reserves and MRR in real time.
4. **Runnable Micro-SaaS Code Generator**: Automatically generates working FastAPI microservices (`app.py`), Dockerfiles, and test suites alongside the 16 markdown documents.
5. **Background Autonomous Daemon**: Continuous background loop checking telemetry, evaluating opportunities, and maintaining resilience.
6. **Compounding Knowledge Ledger**: Persistent memory for decisions, experiments, and lessons learned.
7. **Minimalist Black/White & NAB Beige Theme**: Executive fintech aesthetic with high-contrast monochrome design and warm beige/yellow accents.

---

## 🚀 Quickstart

### 1. Installation
```bash
git clone https://github.com/dxt-stack/Aieges.git
cd Aieges
pip install -r requirements.txt
```

### 2. Run the Web Cockpit Dashboard
```bash
python3 -m uvicorn aegis.api:app --host 0.0.0.0 --port 8000
```
Open `http://localhost:8000` in your browser.

### 3. CLI Automation
```bash
# Check organism status
./aegis-cli.py status

# Run autonomous value creation cycles
./aegis-cli.py loop --cycles 3

# List all ventures in portfolio
./aegis-cli.py venture list

# Initialize a new venture with software bundle and 16 docs
./aegis-cli.py venture new --name "AgentPulse" --category "SaaS" --mrr 25000
```

### 4. Running Test Suites
```bash
PYTHONPATH=. pytest tests/ -v
PYTHONPATH=aegis/ventures/docuflow pytest aegis/ventures/docuflow/test_app.py -v
```

---

## 📄 License
MIT License. Built for long-term sustainable value creation.
