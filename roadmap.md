# Roadmap

## Overview

This document outlines planned improvements to the customer support agent. Items are organized by priority and estimated effort.

---

## Short Term (Next 1-3 Months)

### 1. Live account data integration
**Goal:** Connect the agent to live player account data so it can verify purchases and account status in real time without requiring human lookup.
**Effort:** High - requires API integration
**Impact:** High - eliminates the biggest current limitation

### 2. Multilingual support
**Goal:** Extend the agent to handle queries in the top 3 languages of the player base.
**Effort:** Medium - requires prompt adaptation and testing
**Impact:** High - significant portion of player base contacts in non-English languages

### 3. CSAT survey integration
**Goal:** Automatically trigger a CSAT survey after ticket closure.
**Effort:** Low - configuration change
**Impact:** Medium - enables proper CSAT measurement

---

## Medium Term (3-6 Months)

### 4. Proactive outreach for known issues
**Goal:** When a widespread bug or outage is confirmed, automatically notify affected players before they contact support.
**Effort:** High - requires incident detection and player notification system
**Impact:** High - reduces inbound volume during incidents

### 5. Agent assist mode
**Goal:** Run the AI agent as a real-time assistant to human agents, suggesting responses rather than sending them autonomously.
**Effort:** Medium - requires platform integration
**Impact:** Medium - improves human agent quality and speed

### 6. Knowledge base automation
**Goal:** Automatically flag knowledge base gaps based on tickets the agent escalated due to missing information.
**Effort:** Medium - requires logging and review workflow
**Impact:** Medium - reduces knowledge base maintenance overhead

---

## Long Term (6-12 Months)

### 7. Full Tier 1 autonomy
**Goal:** Agent handles Tier 1 tickets end-to-end without human review, with human oversight only for escalations and QA sampling.
**Effort:** High - requires proven performance baseline and stakeholder approval
**Impact:** Very high - significant cost and efficiency impact

### 8. Predictive volume forecasting
**Goal:** Use historical ticket data to predict volume spikes before they occur and automatically adjust staffing recommendations.
**Effort:** High - requires data pipeline and forecasting model
**Impact:** High - improves capacity planning accuracy
