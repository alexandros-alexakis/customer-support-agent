# RAG Architecture - Retrieval Augmented Generation

## Overview

This document explains why keyword matching is insufficient for player support classification, how RAG addresses the gap, and what design decisions were made in this implementation.

---

## The Problem with Keyword Matching

The current classifier in `engine/classifier.py` matches keywords against predefined signal lists. This works when players use expected vocabulary:

- "charged" -> payment intent
- "banned" -> ban appeal
- "refund" -> refund request

It breaks in three real scenarios:

**Non-standard phrasing:**
"They took money from my account" does not match "charged". "I can't get in" does not match "cannot login".

**Translations and non-native English:**
A player writing "my purchase it not arrive" will not match clean English signal patterns reliably.

**Novel issue types:**
New game features generate new ticket types that the signal dictionary does not cover until someone manually adds them.

---

## How RAG Fixes This

Instead of matching keywords, RAG converts both the player's message and the knowledge base documents into vector embeddings - numerical representations of meaning. Similar meaning produces similar vectors, regardless of the exact words used.

"They took money from my account" and "I was charged but received nothing" will have similar embeddings and retrieve the same knowledge base content.

The retrieved content is then passed to Claude as context, grounding the response in actual documented policy rather than model inference.

---

## Implementation

**Vector store:** ChromaDB - lightweight, runs locally, no external service or API key required beyond Anthropic.

**Embeddings:** Generated via the `sentence-transformers` library using the `all-MiniLM-L6-v2` model. This runs locally and is fast enough for real-time ticket processing.

**Knowledge base source:** Markdown files in the `knowledge-base/` directory. Each file is chunked by section and stored as a separate document in ChromaDB.

**Query flow:**
1. Player message arrives
2. Message is embedded
3. ChromaDB returns the top-k most semantically similar KB chunks
4. Retrieved chunks are injected into the Claude prompt as context
5. Claude responds grounded in retrieved policy

---

## Design Decisions

**Why ChromaDB over Pinecone or Weaviate?**
ChromaDB runs entirely locally with no account, no API key, and no cost. For a prototype this is the correct choice. Production would evaluate managed vector stores based on scale and latency requirements.

**Why sentence-transformers over OpenAI embeddings?**
Local embeddings remove an external dependency and associated cost. The `all-MiniLM-L6-v2` model is small, fast, and produces good results for support text. It is not state-of-the-art but it is appropriate for this use case.

**Why chunk by section rather than by file?**
A single knowledge base file can cover multiple distinct topics. Chunking by section (split on `##` headers) means retrieved context is relevant to the specific question, not the entire document.

**Tradeoff: embedding quality vs. speed**
Larger embedding models produce better semantic matches but are slower. For ticket triage where response time matters, the smaller model is the right tradeoff at prototype stage.

---

## Limitations

- Embeddings are generated at sync time. New or updated KB files require a re-sync.
- The model handles English well. Non-English embedding quality depends on the model's multilingual coverage.
- ChromaDB is not designed for high-concurrency production workloads. Production would require a managed vector store.
- Retrieval quality depends on KB content quality. A poorly written KB produces poor retrievals.

---

## What Production Would Add

- Managed vector store (Pinecone, Weaviate, or pgvector)
- Embedding model fine-tuned on support domain text
- Hybrid search (semantic + keyword) for best of both approaches
- Retrieval evaluation pipeline to measure chunk relevance
- Automatic re-sync when KB files change
