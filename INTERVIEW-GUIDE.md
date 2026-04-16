# Interview & Conversation Guide

How to talk about this project confidently. Written for someone with no technical background.

The pattern for any tough question: acknowledge the limitation, explain the design decision behind it, explain the mitigation, explain what production would do differently. That's the answer that shows real understanding.

---

# Common Questions

These are the first things anyone will ask when they see your repo.

---

## "What is this project?"

You built an AI-powered support ticket system for gaming companies. When a player sends a support message - like "I was charged but never got my coins" - the system automatically figures out what the problem is, how urgent it is, whether a human needs to get involved, and what information the agent should collect. It's like having a smart assistant that reads every ticket before a human touches it and tells the agent exactly what to do.

---

## "Did you build all of this yourself?"

You designed it and built it with the help of Claude AI. That's a completely honest and accurate answer. Using AI to build things is a real skill in 2025. The decisions about what to build, how to structure it, what the escalation logic should be, how to handle edge cases - those came from your operational experience. The AI helped you implement it.

---

## "What problem does it solve?"

Two main problems. First, inconsistency - in a support team, different agents handle the same issue differently. One agent escalates a legal threat, another doesn't. One collects the transaction ID, another forgets. This system makes those decisions consistent every time. Second, efficiency - by the time an agent sees a ticket, the system has already figured out what it is, how urgent it is, and what to collect. The agent doesn't have to start from scratch.

---

## "Is this actually working or just a document?"

Both. The triage engine is real Python code that runs and produces real results. You can clone it, install it, and run it in minutes. The part that is still a prototype is the connection to a live support platform - it's not plugged into a real Zendesk with real players yet, but the code for doing that is there and documented step by step.

---

## "What technology did you use?"

Three main things. Claude AI from Anthropic, which is the intelligence layer. Python, which is the programming language. And ChromaDB, which is a database that stores the knowledge base in a way that allows intelligent searching. You don't need to go deeper than this in most conversations.

---

## "Can I use this for my company?"

Yes. The repo has a full guide called CONTRIBUTING.md that explains exactly what to replace and keep. You swap out the knowledge base with your own policies, update the decision rules for your ticket types, and follow the Zendesk integration guide to connect it to your platform. The core engine, the RAG system, the feedback loop - all of that stays the same.

---

# Tricky Questions

These are designed to catch you out. Have a clear answer ready.

---

## "So the AI is making decisions on its own?"

No, and this is an important distinction. The triage engine is entirely rules-based - it's deterministic code, not an AI making judgment calls. When it sees the word "lawyer" it triggers a legal threat flag. That's a rule, not a decision. The AI part is Claude, which generates the actual response to the player. But even Claude is constrained by a system prompt that defines exactly what it can and cannot say. The system is designed so humans remain in control of the important decisions.

---

## "What if it gets something wrong?"

Good question and we designed for it. First, there's a confidence threshold - if the system isn't sure what type of ticket it's looking at, it automatically routes to a human instead of guessing. Second, there's a feedback loop where QA reviewers can record corrections when something goes wrong. Third, we documented 10 specific failure modes and their mitigations in the repo. No AI system is perfect but this one fails predictably rather than catastrophically.

---

## "How is this different from ChatGPT?"

ChatGPT is a general purpose AI. It knows about everything but is specialized in nothing. What we built is domain-specific - it only handles gaming customer support, it knows our specific policies, our specific escalation rules, our specific ticket types. It can't be asked to write a poem or explain history. It does one thing and it does it consistently because it's constrained by rules, not just prompted to be helpful.

---

## "Doesn't this replace support agents?"

No, and the repo says this explicitly. It handles Tier 1 - simple, repetitive queries with clear answers. Anything complex, anything with legal implications, anything involving a VIP player, anything a repeat contact - all of that goes to a human. The idea is that agents spend less time on "what's a refund policy" and more time on the cases that actually need human judgment.

---

## "What's the CSAT bias thing you wrote about?"

This is one of the most interesting parts. Companies that deploy AI for easy tickets and keep humans for hard tickets then compare their CSAT scores and declare "AI is amazing, humans are terrible." But it's a flawed comparison - easy tickets always get better ratings. We wrote an analysis in the repo showing how to measure fairly by comparing like-for-like: AI on simple tickets vs humans on simple tickets, not AI on simple vs humans on complex. Most companies haven't even thought about this.

---

## "Could someone misuse this or get wrong information?"

The system prompt has explicit prohibitions against the agent making up policies, promising refunds, or stating outcomes it can't guarantee. If a player asks something the system doesn't know, it escalates rather than guessing. We also documented the hallucination risk as a known failure mode and the mitigation for it. Is it bulletproof? No. Is it significantly safer than a less constrained AI? Yes.

---

# In-Depth Questions

These come from technical people or senior stakeholders who actually understand what they're looking at.

---

## "Why keyword matching instead of a pure LLM classifier?"

Deliberate choice. Keyword matching is fast, deterministic, and auditable. If a ticket is classified as a payment issue, you can look at exactly which words triggered it. With an LLM classifier you get better accuracy on unusual phrasing but you lose explainability - you can't tell a compliance team exactly why a ticket was escalated. We use RAG with semantic search to compensate for the phrasing weakness of keywords, so you get the best of both: auditable classification and semantic retrieval.

---

## "What's the confidence threshold and why 0.65?"

The confidence score measures how clearly one intent type dominated over others. If a message matches payment signals strongly and everything else weakly, confidence is high. If it matches three intent types equally, confidence is low. We set 0.65 as the threshold below which we route to a human instead of acting. It's conservative by design - we'd rather a human review an ambiguous ticket than the system make a wrong call on it. 0.65 can be adjusted based on real-world performance data.

---

## "How does the RAG work?"

RAG stands for Retrieval Augmented Generation. The knowledge base documents are broken into sections and converted into numbers - vectors - that represent their meaning. When a player message comes in, it's also converted into a number. The system then finds the knowledge base sections whose numbers are closest to the message's number. Closest here means most similar in meaning, not in exact words. So "they took money from my account" finds the same KB section as "I was charged" even though the words are completely different. Those sections are then given to Claude as context so its response is grounded in actual policy.

---

## "What would it take to actually deploy this?"

We documented this in a five-phase roadmap. The two biggest gaps are: one, account data access - right now the system only knows what the player tells it, it can't verify purchases or account history. Two, a live response loop - the triage engine is wired up but the piece that sends Claude's response back to the player through Zendesk is the integration step. Beyond that you need rate limiting, authentication, persistent logging, a human review workflow, and compliance review for AI-generated customer communication. Realistically six to twelve months of engineering work for a small team.

---

## "How do you evaluate if it's working?"

We have three layers. Unit tests that test specific classification rules - does "lawyer" trigger a legal threat flag, does a VIP player always get escalated. An evaluation pipeline that runs 200 synthetic tickets through the engine and produces a report showing escalation accuracy, false negatives, and false positives. And a QA framework with a 100-point scoring system that human reviewers use to assess real interactions. The key metric we care most about is escalation accuracy - routing the right tickets to the right teams.

---

## "What's the biggest weakness?"

Honest answer: the keyword classifier breaks on non-standard phrasing, especially from non-native English speakers. Someone who writes "my purchase it not arrive" won't match the payment signals cleanly. The RAG layer compensates partially because semantic search finds the right KB content anyway, but the classification itself may still return low confidence and route to a human. In production you'd replace keyword classification with an LLM-based classifier that understands intent regardless of phrasing. We documented this explicitly in LIMITATIONS.md rather than hiding it.

---

# Key phrases to remember

If you forget everything else, these four sentences cover almost any question:

- "The triage engine is rules-based and deterministic. The AI layer is constrained by a system prompt."
- "When the system isn't confident, it routes to a human instead of guessing."
- "It handles Tier 1. Everything complex, sensitive, or ambiguous goes to a human."
- "We documented the limitations honestly. No AI system is perfect but this one fails predictably."
