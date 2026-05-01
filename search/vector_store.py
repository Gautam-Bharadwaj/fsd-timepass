import os
import json
import numpy as np
import faiss

from config import get_faiss_index_path, get_metadata_path

# FAISS dimension must match the embedding model output (all-MiniLM-L6-v2 = 384)
EMBEDDING_DIM = 384


def _load_metadata() -> dict:
    """Load chunk metadata from JSON file."""
    if not os.path.exists(get_metadata_path()):
        return {}
    with open(get_metadata_path(), "r") as f:
        return json.load(f)


def _save_metadata(metadata: dict):
    """Save chunk metadata to JSON file."""
    with open(get_metadata_path(), "w") as f:
        json.dump(metadata, f, indent=2)


from typing import Optional, Union, List

def _load_index() -> Optional[faiss.Index]:
    """Load FAISS index from disk. Returns None if not found."""
    if not os.path.exists(get_faiss_index_path()):
        return None
    return faiss.read_index(get_faiss_index_path())


def _save_index(index: faiss.Index):
    """Save FAISS index to disk."""
    faiss.write_index(index, get_faiss_index_path())


def add_chunks(chunks: list[dict], embeddings: np.ndarray):
    """
    Add new chunks and their embeddings to the FAISS index.

    Args:
        chunks: List of chunk dicts (chunk_text, doc_id, file_name, source, chunk_index)
        embeddings: numpy array of shape (len(chunks), 384)
    """
    if len(chunks) == 0:
        return

    # Load or create FAISS index
    index = _load_index()
    if index is None:
        index = faiss.IndexFlatIP(EMBEDDING_DIM)  # Inner Product (cosine after normalization)

    # Load existing metadata
    metadata = _load_metadata()

    # Current offset = number of existing vectors
    offset = index.ntotal

    # Add embeddings to FAISS index
    index.add(embeddings)

    # Add metadata at corresponding positions
    for i, chunk in enumerate(chunks):
        metadata[str(offset + i)] = chunk

    # Persist
    _save_index(index)
    _save_metadata(metadata)
    print(f"[VectorStore] Added {len(chunks)} chunks. Total: {index.ntotal}")


def search(query_embedding: np.ndarray, top_k: int = 5, filters: dict = None, query_text: str = "") -> list[dict]:
    """
    Hybrid Search: Semantic (FAISS) + Basic Keyword Matching.
    """
    index = _load_index()
    if index is None or index.ntotal == 0:
        return []

    metadata = _load_metadata()
    search_k = min(index.ntotal, top_k * 10) # Search a larger pool for hybrid ranking

    scores, indices = index.search(query_embedding, search_k)
    results = []
    
    query_words = set(query_text.lower().split()) if query_text else set()

    for score, idx in zip(scores[0], indices[0]):
        if idx == -1:
            continue
        
        chunk = metadata.get(str(idx), {})
        
        # Metadata Filtering
        if filters:
            if not all(chunk.get(k) == v for k, v in filters.items()):
                continue

        # Hybrid Scoring: Boost if keywords match (Exceptional Tier Feature)
        final_score = float(score)
        if query_words:
            text_lower = chunk.get("chunk_text", "").lower()
            match_count = sum(1 for word in query_words if word in text_lower)
            if match_count > 0:
                final_score += 0.2 * match_count # Simple boost for keyword matches

        chunk["relevance_score"] = final_score
        results.append(chunk)

    # Re-sort by boosted score
    results = sorted(results, key=lambda x: x["relevance_score"], reverse=True)
    return results[:top_k]


def list_indexed_files() -> list[dict]:
    """Returns a list of unique files currently in the vector index."""
    metadata = _load_metadata()
    files = {}
    for entry in metadata.values():
        fid = entry.get("doc_id")
        if fid not in files:
            files[fid] = {
                "id": fid,
                "name": entry.get("file_name"),
                "source": entry.get("source"),
                "chunks": 0
            }
        files[fid]["chunks"] += 1
    return list(files.values())


def delete_file_from_index(doc_id: str):
    """
    Removes a file and its chunks from the metadata. 
    Note: FAISS IndexFlatIP doesn't support easy deletion by ID, 
    so we filter the metadata. For a full cleanup, a re-sync is better.
    """
    metadata = _load_metadata()
    new_metadata = {k: v for k, v in metadata.items() if v.get("doc_id") != doc_id}
    _save_metadata(new_metadata)
    # The FAISS index still has the vectors, but they won't match any metadata keys.
    print(f"[VectorStore] Removed metadata for file: {doc_id}")


def get_index_stats() -> dict:
    """Return stats about the current FAISS index."""
    index = _load_index()
    metadata = _load_metadata()
    return {
        "faiss_index_exists": index is not None,
        "total_chunks_indexed": index.ntotal if index else 0,
        "unique_documents": len(set(v.get("doc_id") for v in metadata.values())),
        "files": list_indexed_files()
    }


def get_sample_chunks(n: int = 5) -> list[str]:
    """Retrieve up to n random chunks for AI recommendations."""
    import random
    metadata = _load_metadata()
    if not metadata:
        return []
    keys = list(metadata.keys())
    if len(keys) > n:
        keys = random.sample(keys, n)
    return [metadata[k].get("chunk_text", "") for k in keys]


def clear_index():
    """Delete the FAISS index and metadata."""
    if os.path.exists(get_faiss_index_path()):
        os.remove(get_faiss_index_path())
    if os.path.exists(get_metadata_path()):
        os.remove(get_metadata_path())
    print("[VectorStore] Index cleared.")

