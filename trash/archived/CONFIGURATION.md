# Configuration Guide

> Archived. Moved to docs/setup/configuration.md

All environment variables, their purpose, whether they are required, and safe defaults.

## Variables

| Variable | Required | Purpose |
|---|---|---|
| `ANTHROPIC_API_KEY` | Yes (for LLM) | Authenticates requests to Claude API |
| `ZENDESK_SUBDOMAIN` | Zendesk only | Your Zendesk URL prefix |
| `ZENDESK_EMAIL` | Zendesk only | Admin email registered in Zendesk |
| `ZENDESK_API_TOKEN` | Zendesk only | Zendesk API token |
| `WEBHOOK_SECRET` | Zendesk only | HMAC signing secret for webhook verification |
| `PORT` | No | Port the webhook server listens on (default 8000) |
