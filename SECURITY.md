# Security Policy

## Scope

AEGIS is an experimental operational and financial-planning system. Do not connect it to production banking, billing, or customer data without an independent security review.

## Reporting a vulnerability

Please do not open a public issue for a security vulnerability. Contact the repository owner privately with a description, reproduction steps, affected version, and suggested mitigation. Remove credentials, personal data, and customer information from reports.

## Deployment requirements

Set `AEGIS_API_KEY` for every non-local deployment. Set `STRIPE_WEBHOOK_SECRET` before accepting Stripe events. Restrict `AEGIS_CORS_ORIGINS` to known origins. Run the application behind TLS, a reverse proxy, rate limiting, and a process supervisor. The live research endpoint intentionally rejects private and loopback targets to reduce SSRF risk.

## Data handling

The default JSON files are local development storage, not a multi-user database. Treat them as sensitive operational records and do not commit customer, payment, or personally identifying information.
