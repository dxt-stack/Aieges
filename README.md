# AEGIS

### Autonomous Economic Growth & Intelligent Survival System

AEGIS is a self-hosted command center for turning business ideas into measurable, documented, and governable software ventures.

It brings treasury awareness, opportunity evaluation, venture scaffolding, operational memory, and human approval boundaries into one focused system.

> **Build durable value. Protect the downside. Keep humans in control of consequential decisions.**

## Why AEGIS exists

Most early ventures lose context between spreadsheets, product notes, dashboards, and deployment scripts. AEGIS keeps those decisions connected. It shows the current financial posture, ranks opportunities against explicit criteria, creates a documented starting point for the next venture, and records what the system learned.

The operating loop is simple:

```text
Observe → Analyze → Discover → Prioritize → Plan → Build → Measure → Improve
```

AEGIS is intentionally not a black-box money machine. It is a transparent operating system for disciplined experimentation and automation. It does not sign contracts, move money, change ownership, or make regulatory decisions without a human governor.

## Does AEGIS create or handle real money?

**No. AEGIS does not create money, hold funds, execute trades, or transfer money.** The dashboard’s initial treasury values are local demo data stored in JSON so that the interface and scoring workflow are immediately usable. They are not proof of revenue, a bank balance, or financial performance.

The optional Stripe bridge can receive verified Stripe webhook events and mirror payment, subscription, and refund information into AEGIS’s internal telemetry. It does not replace Stripe, an accounting system, a bank, or payment reconciliation. Do not connect production billing until the security, privacy, accounting, and operational controls have been independently reviewed.

## The cockpit

The dashboard is designed as a high-contrast fintech command center: monochrome surfaces, warm gold telemetry, cyan signal highlights, animated grid and scanline layers, live posture indicators, and reduced-motion support for accessibility.

The main views answer practical questions:

- **How much runway is left?** Treasury data is translated into a survival posture.
- **What deserves attention next?** Opportunities are ranked using expected value, capital efficiency, timing, risk, and defensibility.
- **What has already been tried?** Decisions, assumptions, outcomes, failures, and lessons remain in a searchable knowledge ledger.
- **What needs a human?** Banking, legal, regulatory, ownership, and other high-impact actions appear in a governance queue.

## Current capabilities

| Capability | Purpose |
| --- | --- |
| Treasury posture | Monitor reserves, burn, revenue, net burn, and runway. |
| Opportunity engine | Compare possible products and rank them against explicit economic criteria. |
| Venture factory | Generate a documented venture workspace with a starter FastAPI service, Dockerfile, tests, and operating artifacts. |
| Public-market research | Inspect allowed public webpages for metadata, headings, pricing signals, and keyword clues. |
| Revenue bridge | Process supported Stripe event payloads and update internal telemetry after signature verification is configured. |
| Governance queue | Keep consequential actions visible for human review. |
| Knowledge ledger | Preserve the reasoning and lessons that make future cycles better. |

## Set up and use AEGIS locally

```bash
git clone https://github.com/dxt-stack/Aieges.git
cd Aieges
python3 -m venv .venv
. .venv/bin/activate
python -m pip install -r requirements.txt
cp .env.example .env
python -m uvicorn aegis.api:app --host 127.0.0.1 --port 8000
```

Open [http://127.0.0.1:8000](http://127.0.0.1:8000) to enter the cockpit. The interactive API reference is available at `/docs`.

The local dashboard starts in **demo mode**. Use the tabs to inspect the seeded treasury, opportunity rankings, venture documents, knowledge ledger, and governance queue. The **Run Loop** action executes one local orchestration cycle. The **Treasury Stress Lab** and **Stripe Simulator** are local demonstrations; they do not contact a bank or charge a customer.

To start with your own values, use the treasury controls in the dashboard or run:

```bash
python aegis-cli.py treasury --reserves 50000 --burn 8000 --revenue 4500
```

To scaffold a venture locally:

```bash
python aegis-cli.py venture new \
  --name "AgentPulse" \
  --category "SaaS" \
  --tagline "Automated operational intelligence for small teams"
```

This creates documentation, a starter FastAPI service, tests, and a Dockerfile under the configured workspace. It does not deploy the service or claim that the venture has customers.

For a quick command-line view:

```bash
python aegis-cli.py status
python aegis-cli.py venture list
```

## Safety before deployment

AEGIS is ready for public collaboration as an honest prototype. It is not yet production financial infrastructure. Before exposing it beyond a private machine:

- Set `AEGIS_API_KEY` so state-changing requests require `X-Aegis-Key`.
- Restrict `AEGIS_CORS_ORIGINS` to trusted origins.
- Set `STRIPE_WEBHOOK_SECRET` before accepting payment events.
- Run behind TLS, rate limiting, edge authentication, logging, and a process supervisor.
- Treat the JSON data files as local development storage, not a multi-user database.
- Review every generated venture for security, privacy, legal, and operational readiness.

Read [SECURITY.md](SECURITY.md) for the deployment boundary and responsible disclosure process.

## Project map

The code is organized around a small number of responsibilities rather than a large framework:

```text
aegis/
├── api.py                 FastAPI application and cockpit routes
├── orchestrator.py        Value-creation loop coordinator
├── core/                  Models, state, scoring, decisions, and memory
├── divisions/             Research, product, engineering, marketing, operations, finance
├── integrations/          Research, Stripe handling, and venture generation
├── data/                  Local example state
├── templates/             Animated cockpit interface
└── ventures/              Generated venture workspaces
```

## Quality checks

```bash
python -m compileall -q aegis aegis-cli.py
python -m pytest -q
```

Continuous integration runs the same checks on supported Python versions. Contributions should include regression coverage and should never include credentials, customer data, or runtime state.

See [CONTRIBUTING.md](CONTRIBUTING.md) to get involved.

## Status

AEGIS is an actively evolving prototype for transparent venture operations, economic experimentation, and human-governed automation. The project favors explicit assumptions, observable state, reversible actions, and durable documentation over claims of full autonomy.

## License

AEGIS is released under the [MIT License](LICENSE).
