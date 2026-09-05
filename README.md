# AEGIS — Autonomous Economic Growth & Intelligent Survival System

[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.115+-009688.svg?logo=fastapi)](https://fastapi.tiangolo.com)
[![Pydantic v2](https://img.shields.io/badge/Pydantic-v2-e92063.svg)](https://docs.pydantic.dev/)
[![Tests](https://img.shields.io/badge/tests-7%20passed-brightgreen.svg)]()
[![License](https://img.shields.io/badge/license-MIT-green.svg)]()

> **"Money is survival. Cash reserves are life support. Revenue is oxygen. Profitability is health. Financial collapse is existential failure."**

AEGIS is a self-directed economic organism designed to autonomously discover, evaluate, scaffold, document, and manage legal recurring value-producing systems and software ventures with zero unnecessary human labor.

---

## 🛡️ Core Architecture

```
+========================================================================================+
|                                    AEGIS ORGANISM                                      |
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
|  [ KNOWLEDGE BASE (Compounding) ] <-------------------> [ HUMAN GOVERNANCE QUEUE ]    |
|                                                          (Banking, KYC, Legal, Equity) |
+========================================================================================+
```

---

## ⚡ Key Features

1. **Survival State Machine**: Dynamic tactical posture shifts (`CRITICAL`, `WARNING`, `STABLE`, `STRONG`, `FORTRESS`) based on treasury runway calculations.
2. **Algorithmic Opportunity Scorer**: Multi-factor Expected Value (EV) & Risk-Adjusted Return on Effort (RAROE, 0–100) adhering strictly to the Revenue Priority Hierarchy (SaaS > Subscriptions > Licensing > B2B Services ...).
3. **6 Specialized Autonomous Divisions**:
   - 🔬 **Research Division**: Market TAM/SAM/SOM, competitor weaknesses, intent clusters.
   - 📐 **Product Division**: MVP scoping, pricing matrices, lean roadmaps.
   - ⚙️ **Engineering Division**: Headless microservices, security & resilience audits.
   - 📣 **Marketing Division**: Programmatic SEO matrices, automated cold B2B sequences.
   - 🔄 **Operations Division**: Standard Operating Procedures (SOPs), churn mitigation.
   - 📈 **Finance Division**: Treasury stress tests, LTV/CAC payback calculations.
4. **Mandatory 16-Artifact Documentation Suite**: Auto-generates the canonical 16 markdown artifacts for every venture.
5. **Human Governance Protocol**: Segregates human intervention strictly to *Ownership, Legal Signatures, KYC, and Banking authorizations*.
6. **Live Web Cockpit UI & REST API**: Real-time HUD, interactive division workbench, treasury simulator, and telemetry logs.

---

## 🚀 Quickstart

### 1. Installation
```bash
git clone <repo-url>
cd aegis
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

# Initialize a new venture with all 16 docs generated
./aegis-cli.py venture new --name "AgentPulse" --category "SaaS" --mrr 25000

# Dispatch task to an autonomous division
./aegis-cli.py division --name RESEARCH --task discover_niche_opportunities
./aegis-cli.py division --name FINANCE --task run_treasury_stress_test
```

### 4. Running Tests
```bash
PYTHONPATH=. pytest tests/ -v
```

---

## 📄 License
MIT License. Built for long-term sustainable value creation.
