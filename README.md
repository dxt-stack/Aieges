# AEGIS

## Autonomous Economic Growth & Intelligent Survival System

AEGIS is a self-hosted Python/FastAPI control plane for evaluating business opportunities, monitoring treasury runway, scaffolding small software ventures, and recording operational decisions. It is an **experimental decision-support and automation platform**, not an autonomous financial adviser, payment processor, or guarantee of revenue.

> Money is survival. Cash reserves are life support. Revenue is oxygen. Profitability is health.

The project is designed around a value-creation loop:

```text
Observe → Analyze → Discover → Prioritize → Plan → Build → Measure → Improve
```

## What works today

| Area | Current behavior |
| --- | --- |
| Treasury | Calculates net burn, runway, and survival posture from persisted JSON state. |
| Opportunity scoring | Scores opportunities using revenue potential, capital, timing, risk, scalability, and defensibility. |
| Venture scaffolding | Generates a documentation suite, FastAPI service, Dockerfile, and tests for a venture. |
| Dashboard | Provides a dark fintech command center with animated grid, scanline, glow, telemetry, and accessible reduced-motion support. |
| Research | Audits public HTTP(S) pages for metadata, headings, pricing clues, and keyword signals. Private, loopback, link-local, and credential-bearing targets are rejected. |
| Stripe bridge | Handles supported event payloads and verifies the Stripe signature when `STRIPE_WEBHOOK_SECRET` is configured. |
| Governance | Records actions that require human approval, including banking, legal, regulatory, and ownership decisions. |
| Knowledge ledger | Persists decisions, assumptions, experiments, outcomes, failures, and lessons. |

AEGIS deliberately keeps consequential actions inside a human governance boundary. It does not autonomously sign contracts, move money, change ownership, or make regulatory attestations.

## Quick start

```bash
git clone https://github.com/dxt-stack/Aieges.git
cd Aieges
python3 -m venv .venv
. .venv/bin/activate
python -m pip install -r requirements.txt
cp .env.example .env
python -m uvicorn aegis.api:app --host 127.0.0.1 --port 8000
```

Open [http://127.0.0.1:8000](http://127.0.0.1:8000). API documentation is available at `/docs`.

For a CLI status check:

```bash
python aegis-cli.py status
python aegis-cli.py venture list
python aegis-cli.py loop --cycles 1
```

## Configuration and deployment safety

The application uses repository-local JSON files by default. Set `AEGIS_WORKSPACE` and `AEGIS_DATA_DIR` for another location. Never place real customer, payment, or personally identifying data in the tracked example files.

For any deployment beyond a private local machine:

1. Set `AEGIS_API_KEY`; state-changing API requests then require the `X-Aegis-Key` header.
2. Set `AEGIS_CORS_ORIGINS` to an explicit comma-separated origin allowlist.
3. Set `STRIPE_WEBHOOK_SECRET` before accepting Stripe webhooks.
4. Put the service behind TLS, authentication at the edge, rate limiting, logging, and a process supervisor.
5. Review the JSON persistence model before using multiple workers or multiple users.

See [SECURITY.md](SECURITY.md) for the threat model and disclosure process.

## API surface

The dashboard uses the following main routes:

- `GET /api/status` — current treasury, posture, loop, venture, and governance telemetry.
- `POST /api/loop/execute-step` — run one value-creation cycle.
- `GET /api/opportunities` and `POST /api/opportunities/evaluate` — list and score opportunities.
- `POST /api/ventures/create` — generate a venture bundle.
- `POST /api/research/audit-url` — audit an allowed public URL.
- `POST /api/stripe/webhook` — receive verified Stripe events when a webhook secret is configured.
- `POST /api/stripe/simulate` — local development simulator.

## Testing

```bash
python -m compileall -q aegis aegis-cli.py
python -m pytest -q
```

The repository includes core orchestration tests and tests for both checked-in generated venture services.

## Architecture

| Module | Responsibility |
| --- | --- |
| `aegis/api.py` | FastAPI application and dashboard endpoints. |
| `aegis/orchestrator.py` | Coordinates the value-creation loop. |
| `aegis/core/` | Models, state, scoring, decision filters, documents, and knowledge. |
| `aegis/divisions/` | Research, product, engineering, marketing, operations, and finance directives. |
| `aegis/integrations/` | Research, Stripe event handling, and venture code generation. |
| `aegis/data/` | Local example state and seeded demo records. |
| `aegis/templates/index.html` | The animated AEGIS cockpit dashboard. |

## Project status and limitations

AEGIS is ready for public collaboration as a transparent prototype, not as production financial infrastructure. JSON files are not a multi-user database. The daemon is process-local. The Stripe bridge updates internal telemetry but does not replace Stripe SDK signature verification, idempotency storage, accounting reconciliation, or payment-provider controls. Generated ventures are starter services and require an independent security, privacy, legal, and operational review before deployment.

## License

MIT. See [LICENSE](LICENSE) if present in the repository.

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md). Please report security vulnerabilities privately as described in [SECURITY.md](SECURITY.md).
