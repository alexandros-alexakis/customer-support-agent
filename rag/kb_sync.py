import os
import glob
import re
from pathlib import Path
import chromadb
from chromadb.utils import embedding_functions

# ChromaDB persistent store - survives process restarts
# Data is stored in ./rag/chroma_store relative to project root
CHROMA_PATH = str(Path(__file__).parent / "chroma_store")
COLLECTION_NAME = "player_care_kb"
KB_PATH = str(Path(__file__).parent.parent / "knowledge-base")

# Using sentence-transformers locally - no external API needed
# Model is small (~80MB) and fast enough for real-time use
EMBEDDING_MODEL = "all-MiniLM-L6-v2"


def get_collection():
    """
    Return the ChromaDB collection.
    Creates the client and collection if they do not exist.
    """
    client = chromadb.PersistentClient(path=CHROMA_PATH)
    ef = embedding_functions.SentenceTransformerEmbeddingFunction(
        model_name=EMBEDDING_MODEL
    )
    collection = client.get_or_create_collection(
        name=COLLECTION_NAME,
        embedding_function=ef,
        metadata={"hnsw:space": "cosine"},
    )
    return collection


def chunk_markdown(content: str, source_file: str) -> list[dict]:
    """
    Split a markdown file into chunks by ## section headers.

    Why chunk by section rather than by fixed token count:
    Each section covers a distinct topic. A chunk that starts mid-section
    loses context about what the section is about. Section-based chunking
    keeps each chunk semantically coherent.
    """
    chunks = []
    # Split on ## headers (not ###)
    sections = re.split(r"(?=^## )", content, flags=re.MULTILINE)

    for i, section in enumerate(sections):
        section = section.strip()
        if not section or len(section) < 50:  # Skip empty or trivially short sections
            continue

        # Extract section title for metadata
        first_line = section.split("\n")[0].strip("# ").strip()

        chunks.append({
            "text": section,
            "metadata": {
                "source": source_file,
                "section": first_line,
                "chunk_index": i,
            },
            "id": f"{source_file}::section_{i}",
        })

    return chunks


def sync_kb(kb_path: str = KB_PATH, verbose: bool = True) -> dict:
    """
    Load all markdown files from the knowledge base directory into ChromaDB.

    This replaces the entire collection on each sync to avoid stale content.
    For large KBs, an incremental sync based on file modification time
    would be more efficient - this is appropriate for prototype scale.

    Returns a summary of what was synced.
    """
    client = chromadb.PersistentClient(path=CHROMA_PATH)
    ef = embedding_functions.SentenceTransformerEmbeddingFunction(
        model_name=EMBEDDING_MODEL
    )

    # Delete and recreate collection to ensure clean sync
    try:
        client.delete_collection(COLLECTION_NAME)
        if verbose:
            print(f"Cleared existing collection: {COLLECTION_NAME}")
    except Exception:
        pass  # Collection didn't exist yet

    collection = client.create_collection(
        name=COLLECTION_NAME,
        embedding_function=ef,
        metadata={"hnsw:space": "cosine"},
    )

    md_files = glob.glob(os.path.join(kb_path, "**/*.md"), recursive=True)
    md_files += glob.glob(os.path.join(kb_path, "*.md"))
    md_files = list(set(md_files))  # Deduplicate

    total_chunks = 0
    files_processed = 0

    for filepath in md_files:
        filename = os.path.relpath(filepath, kb_path)
        try:
            with open(filepath, "r", encoding="utf-8") as f:
                content = f.read()

            chunks = chunk_markdown(content, filename)
            if not chunks:
                continue

            collection.add(
                documents=[c["text"] for c in chunks],
                metadatas=[c["metadata"] for c in chunks],
                ids=[c["id"] for c in chunks],
            )

            total_chunks += len(chunks)
            files_processed += 1

            if verbose:
                print(f"  Synced {filename}: {len(chunks)} chunks")

        except Exception as e:
            print(f"  ERROR syncing {filename}: {e}")

    summary = {
        "files_processed": files_processed,
        "total_chunks": total_chunks,
        "collection": COLLECTION_NAME,
        "store_path": CHROMA_PATH,
    }

    if verbose:
        print(f"\nSync complete: {files_processed} files, {total_chunks} chunks")

    return summary


if __name__ == "__main__":
    print(f"Syncing knowledge base from: {KB_PATH}")
    result = sync_kb(verbose=True)
    print(result)
