from pgvector.django import CosineDistance

from .models import DocumentChunk
from .embeddings import generate_embedding


def semantic_search(question, limit=5):
    question_embedding = generate_embedding(question)

    results = (
        DocumentChunk.objects
        .filter(embedding__isnull=False)
        .annotate(
            distance=CosineDistance("embedding", question_embedding)
        )
        .order_by("distance")[:limit]
    )

    return results