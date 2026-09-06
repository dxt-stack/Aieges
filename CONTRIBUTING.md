# Contributing to AEGIS

AEGIS welcomes focused contributions that improve correctness, safety, observability, accessibility, or documentation. Please open an issue before large architectural changes.

## Local setup

Create a virtual environment, install `requirements.txt`, copy `.env.example` to `.env`, and run `python -m uvicorn aegis.api:app --reload`. The default data files are intentionally local and should not contain real customer or payment data.

## Validation

Run `python -m compileall aegis aegis-cli.py`, then `python -m pytest -q`. Add regression coverage for every bug fix. Changes to API behavior should update the README and the relevant generated-service tests.

## Pull requests

Explain the problem, the behavior change, the test evidence, and any deployment or migration implications. Do not include credentials, private URLs, customer data, or generated runtime state in commits.
