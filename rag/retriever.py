from pathlib import Path
import chromadb
from chromadb.utils import embedding_functions
from rag.kb_sync import CHROMA_PATH, COLLECTION_NAME, EMBEDDING_MODEL


DEFAULT_TOP_K = 3
MIN_RELEVANCE_SCORE = 0.4  # Cosine similarity threshold below which results are discarded


def retrieve(query: str, top_k: int = DEFAULT_TOP_K) -> list[dict]:
    """
    Retrieve the most semantically relevant KB chunks for a player message.

    Returns a list of dicts with:
    - text: the chunk content
    - source: which KB file it came from
    - section: which section within that file
    - score: cosine similarity score (higher = more relevant)

    Returns empty list if the KB has not been synced or no relevant results found.
    """
    try:
        client = chromadb.PersistentClient(path=CHROMA_PATH)
        ef = embedding_functions.SentenceTransformerEmbeddingFunction(
            model_name=EMBEDDING_MODEL
        )
        collection = client.get_collection(
            name=COLLECTION_NAME,
            embedding_function=ef,
        )
    except Exception:
        # KB not synced yet - fail gracefully
        # In production this should alert, not silently return empty
        return []

    results = collection.query(
        query_texts=[query],
        n_results=min(top_k, collection.count()),
        include=["documents", "metadatas", "distances"],
    )

    if not results["documents"] or not results["documents"][0]:
        return []

    retrieved = []
    for doc, meta, distance in zip(
        results["documents"][0],
        results["metadatas"][0],
        results["distances"][0],
    ):
        # ChromaDB returns cosine distance (0=identical, 2=opposite)
        # Convert to similarity score (1=identical, 0=no similarity)
        similarity = 1 - (distance / 2)

        if similarity < MIN_RELEVANCE_SCORE:
            continue  # Discard low-relevance results

        retrieved.append({
            "text": doc,
            "source": meta.get("source", "unknown"),
            "section": meta.get("section", ""),
            "score": round(similarity, 3),
        })

    # Sort by score descending
    retrieved.sort(key=lambda x: x["score"], reverse=True)
    return retrieved


def format_context(retrieved: list[dict]) -> str:
    """
    Format retrieved chunks into a context block for injection into the Claude prompt.

    The format makes the source visible so Claude can reference it accurately
    rather than presenting retrieved content as its own knowledge.
    """
    if not retrieved:
        return ""

    parts = ["RELEVANT KNOWLEDGE BASE CONTENT:\n"]
    for i, result in enumerate(retrieved, 1):
        parts.append(
            f"[Source {i}: {result['source']} - {result['section']}]\n"
            f"{result['text']}\n"
        )

    return "\n".join(parts)


def retrieve_and_format(query: str, top_k: int = DEFAULT_TOP_K) -> tuple[str, list[dict]]:
    """
    Convenience function: retrieve and format in one call.
    Returns (formatted_context_string, raw_results_list)
    """
    results = retrieve(query, top_k=top_k)
    context = format_context(results)
    return context, results
