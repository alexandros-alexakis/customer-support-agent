"""
Example: run a player message through the RAG pipeline.

This demonstrates how the retriever finds relevant KB content
and how it would be injected into a Claude prompt.

Run: python rag/example_rag.py
Requires: python rag/kb_sync.py to have been run first
"""
from rag.retriever import retrieve_and_format


example_queries = [
    # Standard phrasing - keyword matching would also catch this
    "I was charged but didn't receive my coins",

    # Non-standard phrasing - keyword matching would miss this
    "they took money from my account but nothing arrived",

    # Translation-style phrasing
    "my purchase it not arrive in game",

    # Churn signal in unusual phrasing
    "I think I am done playing this game, too many problems",

    # Legal signal in formal language
    "I intend to pursue this matter through the appropriate consumer channels",
]

for query in example_queries:
    print(f"\n{'='*60}")
    print(f"Query: {query}")
    print("-"*60)

    context, results = retrieve_and_format(query, top_k=2)

    if not results:
        print("No relevant KB content found (KB may not be synced)")
        print("Run: python rag/kb_sync.py")
    else:
        for r in results:
            print(f"  [{r['score']:.3f}] {r['source']} - {r['section']}")
        print(f"\nContext block (first 300 chars):")
        print(context[:300] + "..." if len(context) > 300 else context)
