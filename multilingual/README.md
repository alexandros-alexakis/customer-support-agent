# Multilingual Support

## Overview

The assistant detects the player's language from their message and responds in kind. No translation service is required. Claude handles language detection and multilingual response generation natively.

---

## How It Works

1. Player message arrives
2. `detect_language()` sends the message to Claude with a minimal detection prompt
3. If the language is not English, a language instruction is prepended to the system prompt
4. The assistant responds in the detected language
5. All support policies, escalation rules, and prohibited actions remain identical regardless of language

---

## What This Solves

The original system was explicitly English-only. This created two problems:

- Players who write in other languages receive lower quality classification (keyword signals are English)
- Players may receive English responses they cannot understand

With language detection and multilingual response, a Spanish-speaking player who writes in Spanish receives a Spanish response. The underlying decision logic is unchanged.

---

## Supported Languages

Claude has strong support for major European and Asian languages. Quality degrades for less common languages. The implementation returns English as a fallback when detection is uncertain.

Languages with strong support: English, Spanish, French, German, Portuguese, Italian, Russian, Turkish, Polish, Dutch, Japanese, Korean, Chinese.

---

## Limitations

**Classification is still English-biased.** The keyword classifier in `engine/classifier.py` uses English signals. A Spanish player writing "me cobraron" will not match the "charged" signal. The RAG retriever using semantic embeddings handles this better, but the keyword classifier remains a gap until multilingual signals are added.

**KB content is English.** Retrieved KB chunks are in English. Claude will translate the content when responding in another language, but the translation quality depends on the model and the complexity of the policy text.

**Detection adds latency.** Language detection requires an additional API call. In production, this would be parallelised or replaced with a local language detection library (e.g. `langdetect`) for speed.

**Quality varies by language.** Claude's multilingual performance is uneven. European languages are generally strong. Less common languages may produce responses that are technically in the right language but awkward.

---

## What Production Would Add

- Local language detection (e.g. `langdetect`) to remove the API call overhead
- Multilingual KB content for the most common non-English player languages
- Multilingual keyword signals in the classifier
- Per-language CSAT tracking to identify languages where quality drops
- Human review of multilingual interactions as a priority QA category
