from django.contrib.postgres.search import SearchVector, SearchQuery, SearchRank
from django.db.models import F
from .models import DocumentChunk


def keyword_search(question, limit=5):
    search_vector = SearchVector("content")
    search_query = SearchQuery(question)

    results = (
        DocumentChunk.objects
        .annotate(
            search_document=search_vector,
            rank=SearchRank(search_vector, search_query),
        )
        .filter(search_document=search_query)
        .order_by("-rank")[:limit]
    )

    return results
