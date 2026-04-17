# Helpshift Integration Guide

> **Example file** — replace with your actual Helpshift configuration and instructions.

## Overview

This guide covers how to connect the AI customer support agent to Helpshift.

## Prerequisites

- Helpshift account with API access
- API key and domain from your Helpshift dashboard
- Python `requests` library (already in `requirements.txt`)

## Configuration

Add the following to your `.env` file:

```env
HELPSHIFT_API_KEY=your_api_key_here
HELPSHIFT_DOMAIN=your_domain.helpshift.com
HELPSHIFT_APP_ID=your_app_id_here
```

## Example: Fetching Open Issues

```python
import requests
import os

HELPSHIFT_API_KEY = os.getenv("HELPSHIFT_API_KEY")
HELPSHIFT_DOMAIN = os.getenv("HELPSHIFT_DOMAIN")

def get_open_issues():
    url = f"https://api.helpshift.com/v1/{HELPSHIFT_DOMAIN}/issues"
    params = {"state": "open"}
    response = requests.get(url, auth=(HELPSHIFT_API_KEY, ""), params=params)
    response.raise_for_status()
    return response.json()
```

## Example: Sending a Reply

```python
def send_reply(issue_id: str, message: str):
    url = f"https://api.helpshift.com/v1/{HELPSHIFT_DOMAIN}/issues/{issue_id}/messages"
    payload = {"body": message}
    response = requests.post(url, auth=(HELPSHIFT_API_KEY, ""), json=payload)
    response.raise_for_status()
    return response.json()
```

## Webhook Setup (Optional)

1. Go to **Settings → Integrations → Webhooks** in your Helpshift dashboard.
2. Set the endpoint URL to your server (e.g. `https://your-server.com/helpshift/webhook`).
3. Select events to subscribe to (e.g. `new_issue`, `message_added`).

## Further Reading

- [Helpshift REST API docs](https://developers.helpshift.com/api/)
- See `zendesk_client.py` in this folder for a reference integration pattern.
