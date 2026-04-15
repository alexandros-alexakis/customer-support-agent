# Customer Support Agent - Claude AI (Gaming Support)

## Overview

This project documents the design and implementation of an AI-powered 
customer support agent built using Claude AI (Anthropic). The agent is 
designed for Tier 1 gaming customer support operations, specifically 
targeting common player issues in mobile/PC strategy games.

The goal is to reduce agent handling time on repetitive tickets, 
improve response consistency across multilingual teams, and create a 
scalable onboarding resource for new support agents.

---

## Problem Statement

Customer support teams in gaming handle high volumes of repetitive 
Tier 1 tickets: payment issues, account access, in-game bugs, and 
general game mechanic questions. New agents require significant ramp-up 
time, and response quality varies across team members and languages.

An AI agent that handles or assists with Tier 1 queries can:
- Reduce average handling time (AHT)
- Improve first contact resolution (FCR)
- Free senior agents for complex escalations
- Standardize tone and policy adherence

---

## Agent Design

### Scope
The agent is scoped to Tier 1 customer support queries including:
- Payment and purchase issues
- Account access and login problems
- In-game item or currency discrepancies
- Basic game mechanic questions
- Escalation routing for issues outside Tier 1 scope

### Architecture
- **Model:** Claude (Anthropic)
- **Interface:** Claude.ai Projects (prototype stage)
- **Knowledge base:** Structured FAQ documents uploaded as context
- **Escalation logic:** Defined in system prompt rules

---

## Repository Structure

/customer-support-agent
├── README.md                        ← Project overview (this file)
├── system-prompt.md                 ← Core agent instructions and behavior rules
├── knowledge-base/
│   ├── faq-payments.md              ← Payment and purchase FAQ
│   ├── faq-account-access.md        ← Login and account recovery FAQ
│   └── escalation-rules.md         ← When and how to escalate
├── sample-conversations/
│   ├── payment-issue-example.md     ← Sample handled ticket
│   └── escalation-example.md       ← Sample escalated ticket
└── evaluation-criteria.md          ← KPIs used to measure agent performance

---

## Key Design Decisions

**Tone:** The agent maintains a professional, empathetic tone at all 
times. It does not speculate on issues outside its knowledge base.

**Escalation-first on ambiguity:** When the agent cannot resolve an 
issue with confidence, it escalates rather than guessing. This protects 
player trust and reduces incorrect resolutions.

**Multilingual consideration:** The agent is designed to handle queries 
in English, with notes on how prompt design can be adapted for 
multilingual team use.

**Policy adherence:** The agent references only documented policies. 
It does not make exceptions or promises outside defined parameters.

---

## Evaluation Criteria

Success for this agent would be measured against:

| Metric | Target |
|---|---|
| First Contact Resolution (FCR) | >75% on Tier 1 scope |
| Average Handling Time (AHT) | Reduction vs. baseline |
| Escalation Accuracy | <10% incorrect escalations |
| Player Satisfaction (CSAT) | Maintained or improved vs. human Tier 1 |

---

## Author

**Alexandros Alexakis**  
Vendor Manager & L&D Lead | Player Care  
Scorewarrior, Limassol, Cyprus  
[LinkedIn](https://www.linkedin.com/in/YOUR-LINKEDIN-URL)

---

## Status

Work in progress. System prompt and knowledge base files being added 
iteratively.
