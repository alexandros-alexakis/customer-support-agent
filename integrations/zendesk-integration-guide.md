# Production Integration Guide - Zendesk

## Overview

This guide walks through connecting the player care AI engine to Zendesk as a live support platform. When complete, every new Zendesk ticket will automatically be triaged by the engine: classified, prioritised, tagged, and routed before a human agent sees it.

This guide assumes:
- You have a Zendesk account with admin access
- You have Python 3.10+ installed on a server or cloud instance
- You have an Anthropic API key
- You have cloned this repository

**Estimated setup time:** 2-4 hours for a technically confident person.

---

## Architecture Overview

```
Player sends ticket
        |
        v
   Zendesk receives it
        |
        v
   Zendesk Trigger fires
        |
        v
   Webhook POST to your server
        |
        v
   engine/pipeline.py processes it
        |
        v
   Zendesk API updates the ticket:
   - Adds internal note with triage result
   - Sets priority
   - Adds tags (intent, flags)
   - Assigns to correct group
```

The engine never responds to the player directly. It enriches the ticket so the human agent who picks it up already knows the intent, priority, and recommended action.

---

## Part 1: Prepare Your Server

### 1.1 Choose where to run the engine

You need a server with a public URL that Zendesk can POST to. Options:

| Option | Cost | Complexity | Good for |
|---|---|---|---|
| Railway.app | Free tier available | Low | Getting started |
| Render.com | Free tier available | Low | Getting started |
| DigitalOcean Droplet | ~$6/month | Medium | Production |
| AWS EC2 | Variable | High | Enterprise |
| Your own server | Variable | Medium | If you already have one |

For this guide we use a simple Flask server. Any of the above will host it.

### 1.2 Install dependencies

```bash
pip install -r requirements.txt
pip install flask gunicorn
```

### 1.3 Set environment variables

Create a `.env` file in the project root. Never commit this file.

```bash
# .env
ANTHROPIC_API_KEY=your_anthropic_api_key_here
ZENDESK_SUBDOMAIN=yourcompany          # e.g. scorewarrior (not the full URL)
ZENDESK_EMAIL=support@yourcompany.com  # Admin email
ZENDESK_API_TOKEN=your_zendesk_api_token
WEBHOOK_SECRET=generate_a_random_string_here
```

To generate a webhook secret:
```bash
python -c "import secrets; print(secrets.token_hex(32))"
```

### 1.4 Get your Zendesk API token

1. In Zendesk: go to **Admin Center** > **Apps and Integrations** > **APIs** > **Zendesk API**
2. Enable **Token Access**
3. Click **Add API token**
4. Copy the token immediately - it is only shown once
5. Paste it into your `.env` file

---

## Part 2: Build the Webhook Server

Create this file at `integrations/zendesk_webhook.py`:

```python
import os
import hmac
import hashlib
import json
import requests
from flask import Flask, request, jsonify
from dotenv import load_dotenv
from engine.pipeline import run, TicketContext
from engine.logging_config import configure_logging

load_dotenv()
configure_logging(level="INFO")

app = Flask(__name__)

ZENDESK_SUBDOMAIN = os.getenv("ZENDESK_SUBDOMAIN")
ZENDESK_EMAIL = os.getenv("ZENDESK_EMAIL")
ZENDESK_API_TOKEN = os.getenv("ZENDESK_API_TOKEN")
WEBHOOK_SECRET = os.getenv("WEBHOOK_SECRET", "")

ZENDESK_BASE_URL = f"https://{ZENDESK_SUBDOMAIN}.zendesk.com/api/v2"


def verify_webhook_signature(request) -> bool:
    """
    Verify that the webhook came from Zendesk and not an attacker.
    Zendesk signs webhooks with HMAC-SHA256.
    Never skip this check in production.
    """
    if not WEBHOOK_SECRET:
        return True  # Skip in development only

    signature = request.headers.get("X-Zendesk-Webhook-Signature", "")
    timestamp = request.headers.get("X-Zendesk-Webhook-Signature-Timestamp", "")
    body = request.get_data(as_text=True)

    expected = hmac.new(
        WEBHOOK_SECRET.encode(),
        f"{timestamp}{body}".encode(),
        hashlib.sha256,
    ).hexdigest()

    return hmac.compare_digest(signature, expected)


def get_zendesk_auth():
    return (f"{ZENDESK_EMAIL}/token", ZENDESK_API_TOKEN)


def get_ticket_details(ticket_id: int) -> dict:
    """
    Fetch full ticket details from Zendesk.
    The webhook payload contains limited fields - we fetch the rest.
    """
    url = f"{ZENDESK_BASE_URL}/tickets/{ticket_id}.json"
    response = requests.get(url, auth=get_zendesk_auth())
    response.raise_for_status()
    return response.json()["ticket"]


def get_requester_details(user_id: int) -> dict:
    """
    Fetch the ticket requester's details.
    Used to check VIP status and contact history.
    """
    url = f"{ZENDESK_BASE_URL}/users/{user_id}.json"
    response = requests.get(url, auth=get_zendesk_auth())
    response.raise_for_status()
    return response.json()["user"]


def get_contact_count(user_id: int) -> int:
    """
    Count how many tickets this user has submitted.
    Used to detect repeat contacts.
    """
    url = f"{ZENDESK_BASE_URL}/users/{user_id}/tickets/requested.json"
    response = requests.get(url, auth=get_zendesk_auth())
    if response.status_code != 200:
        return 1  # Default to 1 if lookup fails
    data = response.json()
    return data.get("count", 1)


def is_vip_user(user: dict) -> bool:
    """
    Check if the user is marked as VIP.
    In Zendesk, VIP status is typically stored as a user tag or custom field.
    Adjust this to match how your team marks VIP players.
    """
    tags = user.get("tags", [])
    return "vip" in tags or "vip_player" in tags


def update_ticket(ticket_id: int, pipeline_result) -> bool:
    """
    Update the Zendesk ticket with triage results.

    We add:
    - An internal note summarising the triage decision
    - Priority level
    - Tags for intent and flags
    - Group assignment based on escalation routing

    We do NOT change the ticket status or respond to the player.
    The human agent remains in control of the conversation.
    """
    c = pipeline_result.classification
    p = pipeline_result.priority
    e = pipeline_result.escalation
    s = pipeline_result.strategy

    # Build internal note
    note_lines = [
        "**AI Triage Result**",
        f"- Intent: {c.intent.value} (confidence: {c.confidence})",
        f"- Tone: {c.tone.value}",
        f"- Priority: {p.label} (P{p.score}) | SLA: {p.sla_hours}h",
        f"- Escalate: {'Yes' if e.should_escalate else 'No'} -> {e.team}",
        f"- Flags: {', '.join(c.flags) if c.flags else 'none'}",
        "",
        f"**Recommended action:** {s.action}",
        f"**Collect:** {', '.join(s.collect)}",
        "",
        f"*This note was generated automatically. Review before acting.*",
    ]

    # Map priority score to Zendesk priority values
    zendesk_priority_map = {
        1: "low",
        2: "normal",
        3: "high",
        4: "urgent",
        5: "urgent",
    }

    # Build tags from intent and flags
    tags = [f"ai_{c.intent.value}"]
    tags += [f"ai_{flag}" for flag in c.flags]
    if e.should_escalate:
        tags.append(f"ai_escalate_{e.team}")

    payload = {
        "ticket": {
            "priority": zendesk_priority_map.get(p.score, "normal"),
            "tags": tags,
            "comment": {
                "body": "\n".join(note_lines),
                "public": False,  # Internal note only - player does not see this
            },
        }
    }

    url = f"{ZENDESK_BASE_URL}/tickets/{ticket_id}.json"
    response = requests.put(url, json=payload, auth=get_zendesk_auth())
    return response.status_code == 200


@app.route("/webhook/zendesk", methods=["POST"])
def zendesk_webhook():
    """
    Main webhook endpoint.
    Zendesk POSTs here when a new ticket is created.
    """
    # Step 1: Verify the request is genuinely from Zendesk
    if not verify_webhook_signature(request):
        return jsonify({"error": "Invalid signature"}), 401

    payload = request.get_json()
    if not payload:
        return jsonify({"error": "Empty payload"}), 400

    ticket_id = payload.get("ticket_id") or payload.get("id")
    if not ticket_id:
        return jsonify({"error": "No ticket ID"}), 400

    # Step 2: Fetch full ticket and requester details
    try:
        ticket = get_ticket_details(ticket_id)
        requester = get_requester_details(ticket["requester_id"])
        contact_count = get_contact_count(ticket["requester_id"])
        is_vip = is_vip_user(requester)
    except Exception as e:
        return jsonify({"error": f"Failed to fetch ticket: {str(e)}"}), 500

    # Step 3: Extract message text
    # Use the ticket description (first comment) as the message
    message = ticket.get("description", "").strip()
    if not message:
        return jsonify({"status": "skipped", "reason": "empty message"}), 200

    # Step 4: Run the triage pipeline
    try:
        ctx = TicketContext(
            message=message,
            player_id=str(ticket["requester_id"]),
            contact_count=contact_count,
            is_vip=is_vip,
        )
        result = run(ctx)
    except Exception as e:
        return jsonify({"error": f"Pipeline failed: {str(e)}"}), 500

    # Step 5: Update Zendesk ticket with triage results
    try:
        updated = update_ticket(ticket_id, result)
        if not updated:
            return jsonify({"error": "Failed to update ticket"}), 500
    except Exception as e:
        return jsonify({"error": f"Ticket update failed: {str(e)}"}), 500

    return jsonify({
        "status": "ok",
        "ticket_id": ticket_id,
        "intent": result.classification.intent.value,
        "priority": result.priority.label,
        "escalate": result.escalation.should_escalate,
    }), 200


@app.route("/health", methods=["GET"])
def health():
    """Health check endpoint for monitoring."""
    return jsonify({"status": "ok"}), 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=False)
```

---

## Part 3: Configure Zendesk

### 3.1 Create a Webhook in Zendesk

1. Go to **Admin Center** > **Apps and Integrations** > **Webhooks**
2. Click **Create webhook**
3. Fill in:
   - **Name:** Player Care AI Triage
   - **Endpoint URL:** `https://your-server-url.com/webhook/zendesk`
   - **Request method:** POST
   - **Request format:** JSON
4. Under **Authentication:** select **HMAC Signature**
5. Copy the signing secret and paste it into your `.env` as `WEBHOOK_SECRET`
6. Click **Create webhook**

### 3.2 Create a Trigger to fire the webhook

Triggers tell Zendesk when to call the webhook. We want it to fire on every new ticket.

1. Go to **Admin Center** > **Objects and rules** > **Business rules** > **Triggers**
2. Click **Add trigger**
3. Fill in:
   - **Name:** AI Triage - New Ticket
   - **Description:** Send new tickets to AI triage engine
4. Under **Conditions** (ALL of these must be true):
   - Ticket: Is | Created
   - Ticket: Channel | Is not | Internal note
5. Under **Actions**:
   - Select **Notify active webhook**
   - Select **Player Care AI Triage**
   - In the JSON body, paste:

```json
{
  "ticket_id": "{{ticket.id}}",
  "subject": "{{ticket.title}}",
  "requester_id": "{{ticket.requester.id}}"
}
```

6. Click **Create trigger**

### 3.3 Create Zendesk Groups for routing

The engine routes tickets to teams by name. Map these to Zendesk groups:

| Engine team name | Zendesk group to create |
|---|---|
| `billing` | Billing Specialist |
| `account_team` | Account Team |
| `trust_and_safety` | Trust and Safety |
| `technical` | Technical Support |
| `player_relations` | Player Relations |
| `senior_agent` | Senior Agents |
| `legal_compliance` | Legal and Compliance |

To create groups: **Admin Center** > **People** > **Teams** > **Groups** > **Add group**

---

## Part 4: Deploy the Server

### Option A: Railway.app (simplest)

1. Create an account at railway.app
2. Click **New Project** > **Deploy from GitHub repo**
3. Connect your GitHub account and select this repository
4. Add environment variables in the Railway dashboard (from your `.env` file)
5. Railway will auto-detect the Python app and deploy it
6. Copy the generated URL and paste it as the webhook endpoint in Zendesk

### Option B: Run locally with ngrok (for testing only)

ngrok creates a temporary public URL that tunnels to your local machine. Good for testing before deploying.

```bash
# Install ngrok from ngrok.com
# Run your server
gunicorn integrations.zendesk_webhook:app --bind 0.0.0.0:8000

# In a separate terminal
ngrok http 8000
```

Copy the `https://` URL ngrok gives you and use it as the Zendesk webhook endpoint.

**Important:** ngrok URLs change every time you restart it. This is for testing only.

### Option C: DigitalOcean Droplet

1. Create a $6/month Ubuntu droplet
2. SSH into it
3. Clone your repository
4. Install Python and dependencies
5. Create your `.env` file
6. Run with gunicorn and systemd so it restarts automatically:

```bash
# Install gunicorn
pip install gunicorn

# Create a systemd service
sudo nano /etc/systemd/system/ai-triage.service
```

Paste this into the file:

```ini
[Unit]
Description=Player Care AI Triage
After=network.target

[Service]
User=ubuntu
WorkingDirectory=/home/ubuntu/customer-support-agent
EnvironmentFile=/home/ubuntu/customer-support-agent/.env
ExecStart=/usr/local/bin/gunicorn integrations.zendesk_webhook:app --bind 0.0.0.0:8000 --workers 2
Restart=always

[Install]
WantedBy=multi-user.target
```

```bash
sudo systemctl enable ai-triage
sudo systemctl start ai-triage
```

7. Point your domain or droplet IP at port 8000
8. Use the public URL as your Zendesk webhook endpoint

---

## Part 5: Sync the Knowledge Base

Before tickets arrive, load your knowledge base into the vector store:

```bash
python rag/kb_sync.py
```

Re-run this any time you update KB files.

---

## Part 6: Test the Integration

### 6.1 Test the webhook endpoint directly

```bash
curl -X POST https://your-server-url.com/webhook/zendesk \
  -H "Content-Type: application/json" \
  -d '{"ticket_id": 12345}'
```

Expected response:
```json
{"status": "ok", "ticket_id": 12345, "intent": "payment_issue", "priority": "High", "escalate": true}
```

### 6.2 Create a test ticket in Zendesk

1. Go to your Zendesk and create a new ticket manually
2. Set the subject to: "I was charged but didn't receive my coins"
3. Submit it
4. Wait 10-15 seconds
5. Open the ticket and check the internal notes

You should see an **AI Triage Result** internal note with intent, priority, flags, and recommended action.

### 6.3 Check your server logs

```bash
# If running with systemd
journalctl -u ai-triage -f

# If running locally
python integrations/zendesk_webhook.py
```

Logs are structured JSON. Look for `ticket_classified` and `pipeline_complete` events.

---

## Part 7: VIP Player Setup

The engine elevates priority for VIP players. To use this:

1. In Zendesk, add a tag called `vip` to VIP player user profiles
2. The webhook reads user tags automatically
3. Any ticket from a user with the `vip` tag will be classified as VIP and prioritised accordingly

To tag a user as VIP in Zendesk:
- Open the user profile
- Add the tag `vip` in the tags field

---

## Part 8: Security Checklist

Before going live, verify all of the following:

- [ ] `WEBHOOK_SECRET` is set and webhook signature verification is active
- [ ] `.env` file is in `.gitignore` and never committed
- [ ] `ANTHROPIC_API_KEY` is stored as an environment variable, not hardcoded
- [ ] `ZENDESK_API_TOKEN` is stored as an environment variable, not hardcoded
- [ ] Server is running HTTPS (not HTTP)
- [ ] The `/webhook/zendesk` endpoint only accepts POST requests
- [ ] The `/health` endpoint does not expose sensitive information
- [ ] Gunicorn workers are limited to prevent resource exhaustion
- [ ] Server logs do not contain player message content in plain text

---

## Part 9: Monitoring

### What to watch

| Signal | What it means | Action |
|---|---|---|
| Webhook returning 500 errors | Pipeline is failing | Check server logs immediately |
| Webhook returning 401 errors | Signature mismatch | Check WEBHOOK_SECRET in .env |
| Tickets not getting internal notes | Trigger not firing or update failing | Check Zendesk trigger and API token |
| High unknown intent rate | KB or classifier not covering ticket types | Run gap tracker, review KB |
| Processing time above 2 seconds | Server under load or API latency | Check server resources |

### Health check

Set up an uptime monitor (UptimeRobot is free) pointing at `https://your-server-url.com/health`. You will get an alert if the server goes down.

---

## Part 10: Ongoing Maintenance

| Task | Frequency | How |
|---|---|---|
| Re-sync KB after updates | Every KB change | `python rag/kb_sync.py` |
| Review gap tracker | Weekly | `python -c "from feedback.gap_tracker import get_gap_summary; print(get_gap_summary())"` |
| Review feedback records | Weekly | `python -c "from feedback.feedback_store import get_feedback_summary; print(get_feedback_summary())"` |
| Run evaluation pipeline | Monthly | See `GETTING_STARTED.md` |
| Review Zendesk trigger performance | Monthly | Check trigger execution stats in Zendesk admin |
| Rotate API tokens | Every 90 days | Zendesk admin + update .env |

---

## Troubleshooting

**Webhook returns 401**
The signature verification is failing. Check that `WEBHOOK_SECRET` in your `.env` matches the signing secret in Zendesk exactly.

**Ticket gets no internal note**
Check three things in order: (1) Is the trigger firing? Check trigger execution log in Zendesk. (2) Is the webhook receiving the request? Check server logs. (3) Is the Zendesk API update succeeding? Check for 403 errors in logs - your API token may have insufficient permissions.

**Pipeline returns wrong intent**
Run `python example_run.py` locally with the same message to reproduce. Check classifier signals and RAG retrieval for that message type.

**Server crashes under load**
Increase gunicorn workers: `--workers 4`. If the issue persists, the server needs more RAM or CPU.

**KB not being used in classification**
Run `python rag/kb_sync.py` to ensure the vector store is populated. Check that `rag/chroma_store/` exists and is not empty.
