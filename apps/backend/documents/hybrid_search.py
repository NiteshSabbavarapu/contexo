
from .search import semantic_search
from .keyword_search import keyword_search


def hybrid_search(question, limit=5, k=60):
    semantic_results = semantic_search(question)
    keyword_results = keyword_search(question)

    scores = {}
    chunks = {}

    for rank, chunk in enumerate(semantic_results, start=1):
        chunk_id = str(chunk.id)
        scores[chunk_id] = scores.get(chunk_id, 0) + 1 / (k + rank)
        chunks[chunk_id] = chunk

    for rank, chunk in enumerate(keyword_results, start=1):
        chunk_id = str(chunk.id)
        scores[chunk_id] = scores.get(chunk_id, 0) + 1 / (k + rank)
        chunks[chunk_id] = chunk

    ranked_ids = sorted(
        scores,
        key=lambda chunk_id: scores[chunk_id],
        reverse=True,
    )

    results = []

    for chunk_id in ranked_ids[:limit]:
        chunk = chunks[chunk_id]
        chunk.rrf_score = scores[chunk_id]
        results.append(chunk)

    return results
